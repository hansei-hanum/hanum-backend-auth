import os
import dotenv

# PWD = os.path.dirname(os.path.realpath(__file__))


# def path_join(filename):
#     return os.path.join(PWD, filename)


dotenv.load_dotenv()

# BASE_ENV = dotenv.dotenv_values(path_join(".env"))
# GRPC_ENV = dotenv.dotenv_values(path_join(".grpc.env"))
# DATABASE_ENV = dotenv.dotenv_values(path_join(".database.env"))
# AWS_ENV = dotenv.dotenv_values(path_join(".aws.env"))
# SENS_ENV = dotenv.dotenv_values(path_join(".sens.env"))
# REDIS_ENV = dotenv.dotenv_values(path_join(".redis.env"))
# FIREBASE_ENV = dotenv.dotenv_values(path_join(".firebase.env"))


class Env:
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 80))
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    TEST_PHONE_NUMBERS = os.environ.get("TEST_PHONE_NUMBERS", "").split(",")


class DatabaseEnv:
    HOST = os.environ.get("DATABASE_HOST")
    PORT = int(os.environ.get("DATABASE_PORT"))
    USERNAME = os.environ.get("DATABASE_USERNAME")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE = os.environ.get("DATABASE_NAME")


class gRPCEnv:
    PORT = int(os.environ.get("GRPC_PORT", 50051))


# class SENSEnv:
#     ACCESS_KEY = SENS_ENV.get("ACCESS_KEY")
#     SECRET_KEY = SENS_ENV.get("SECRET_KEY")
#     SERVICE_ID = SENS_ENV.get("SERVICE_ID")
#     PHONE_NUMBER = SENS_ENV.get("PHONE_NUMBER")


class SENSEnv:
    ACCESS_KEY = os.environ.get("SENS_ACCESS_KEY")
    SECRET_KEY = os.environ.get("SENS_SECRET_KEY")
    SERVICE_ID = os.environ.get("SENS_SERVICE_ID")
    PHONE_NUMBER = os.environ.get("SENS_PHONE_NUMBER")


# class RedisEnv:
#     HOST = REDIS_ENV.get("HOST")
#     PORT = int(REDIS_ENV.get("PORT"))
#     SESSION_MANAGER_DB = int(REDIS_ENV.get("SESSION_MANAGER_DB"))
#     PHONE_VERIFICATION_DB = int(REDIS_ENV.get("PHONE_VERIFICATION_DB"))
#     RATE_LIMITER_DB = int(REDIS_ENV.get("RATE_LIMITER_DB"))


class RedisEnv:
    HOST = os.environ.get("REDIS_HOST")
    PORT = int(os.environ.get("REDIS_PORT"))
    SESSION_MANAGER_DB = int(os.environ.get("REDIS_SESSION_MANAGER_DB"))
    PHONE_VERIFICATION_DB = int(os.environ.get("REDIS_PHONE_VERIFICATION_DB"))
    RATE_LIMITER_DB = int(os.environ.get("REDIS_RATE_LIMITER_DB"))


# class FirebaseEnv:
#     PROJECT_ID = FIREBASE_ENV.get("PROJECT_ID")
#     JSON_KEY_NAME = FIREBASE_ENV.get("JSON_KEY_NAME")


class FirebaseEnv:
    PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
    JSON_KEY_NAME = os.environ.get("FIREBASE_JSON_KEY_NAME")
