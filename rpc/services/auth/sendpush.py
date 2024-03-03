from sqlalchemy import select, delete
from database import FCMToken
from rpc.declaration.auth.auth_pb2 import (
    SendPushResult,
)
from database import scope
from fcm import FCMSender


# message SendPushRequest {
#     optional int64 userid = 1;
#     optional string topic = 2;
#     string title = 3;
#     string body = 4;
#     string image = 5;
#     string link = 6;
# }

# message SendPushResult {
#     bool success = 1;
# }


async def SendPushInterface(self, request, context):
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
