import grpc
from declaration.auth_pb2_grpc import AuthServiceStub
from declaration.auth_pb2 import AuthorizeRequest

channel = grpc.insecure_channel("localhost:50051")

client = AuthServiceStub(channel)

response = client.Authorize(AuthorizeRequest(token="tes"))

print(response)
