import environ

from .development import *

env = environ.Env()

DEBUG = env.bool("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": env.db("CLEARDB_DATABASE_URL"),
}
