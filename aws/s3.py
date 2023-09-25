# import aioboto3
# from env import AWSEnv
# import utils


# class AWSS3:
#     @staticmethod
#     async def upload(bucket: str, file: bytes | bytearray):
#         sess = aioboto3.Session(
#             aws_access_key_id=AWSEnv.ACCESS_KEY,
#             aws_secret_access_key=AWSEnv.SECRET_KEY,
#         )

#         while True:
#             file_key = utils.random_string(32)
#             if not await AWSS3.isexists(bucket, file_key):
#                 break

#         async with sess.client("s3") as client:
#             await client.put_object(Bucket=bucket, Body=file, Key=file_key)

#         return file_key

#     @staticmethod
#     async def delete(bucket: str, file_key: str):
#         sess = aioboto3.Session(
#             aws_access_key_id=AWSEnv.ACCESS_KEY,
#             aws_secret_access_key=AWSEnv.SECRET_KEY,
#         )

#         async with sess.client("s3") as client:
#             await client.delete_object(Bucket=bucket, Key=file_key)

#     @staticmethod
#     async def isexists(bucket: str, file_key: str):
#         sess = aioboto3.Session(
#             aws_access_key_id=AWSEnv.ACCESS_KEY,
#             aws_secret_access_key=AWSEnv.SECRET_KEY,
#         )

#         async with sess.client("s3") as client:
#             try:
#                 await client.head_object(Bucket=bucket, Key=file_key)
#                 return True
#             except:
#                 return False
