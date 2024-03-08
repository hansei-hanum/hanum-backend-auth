import traceback
from sqlalchemy import select, delete, insert
from database import FCMToken, Notification
from rpc.declaration.authv2.authv2_pb2 import (
    SendPushResult,
)
from database import scope
from fcm import FCMSender

# class Notification(Base):
#     __tablename__ = "notifications"
#     __table_args__ = {"mysql_charset": "utf8mb4"}

#     id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
#     user_id = Column(
#         BIGINT(unsigned=True),
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=True,
#     )

#     title = Column(VARCHAR(1000), nullable=False)
#     body = Column(VARCHAR(1000), nullable=False)
#     created_at = Column(DATETIME, nullable=False, server_default=func.now())


async def SendPushInterface(self, request, context):
    try:
        async with scope() as sess:
            token = (
                await sess.execute(
                    select(FCMToken).where(FCMToken.user_id == request.userid)
                )
            ).scalar_one_or_none()

            if not token and not request.topic:
                return SendPushResult(success=False)
            
            sender = (
                FCMSender(topic=request.topic)
                if request.topic
                else FCMSender(token=token.token)
            )
            
            if request.saveinList:
                if token:
                    await sess.execute(
                        insert(Notification).values(
                            is_announcement=False,
                            user_id=request.userid,
                            title=request.title,
                            body=request.body,
                            link=request.link
                        )
                    )
                elif request.topic == "announcement":
                    await sess.execute(
                        insert(Notification).values(
                            is_announcement=True,
                            title=request.title,
                            body=request.body,
                            link=request.link
                        )
                    )

                await sess.commit()

            result_code = await sender.send(
                title=request.title,
                body=request.body,
                image=request.image,
                deeplink=request.link,
            )

            if result_code in [400, 404]:
                await sess.execute(
                    delete(FCMToken).where(FCMToken.user_id == request.userid)
                )
                await sess.commit()

                return SendPushResult(success=False)

        return SendPushResult(success=True)
    except Exception as e:
        traceback.print_exc()
