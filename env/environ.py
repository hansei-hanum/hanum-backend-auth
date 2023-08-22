import os
import dotenv

PWD = os.path.dirname(os.path.realpath(__file__))


def path_join(filename):
    return os.path.join(PWD, filename)


BASE_ENV = dotenv.dotenv_values(path_join(".env"))
GRPC_ENV = dotenv.dotenv_values(path_join(".grpc.env"))
DATABASE_ENV = dotenv.dotenv_values(path_join(".database.env"))


class Env:
    HOST = BASE_ENV.get("HOST", "0.0.0.0")
    PORT = int(BASE_ENV.get("PORT", 80))
    DEBUG = BASE_ENV.get("DEBUG", "False") == "True"


class DatabaseEnv:
    HOST = DATABASE_ENV.get("HOST")
    PORT = int(DATABASE_ENV.get("PORT"))
    USERNAME = DATABASE_ENV.get("USERNAME")
    PASSWORD = DATABASE_ENV.get("PASSWORD")
    DATABASE = DATABASE_ENV.get("DATABASE")


class gRPCEnv:
    PORT = int(GRPC_ENV.get("PORT", 50051))
