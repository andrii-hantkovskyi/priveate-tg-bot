from environs import Env

env = Env()
env.read_env()

DB_NAME = env.str('DB_NAME')
DB_USERNAME = env.str('DB_USERNAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')

API_TOKEN = env.str('API_TOKEN')
CHANNEL_ID = env.int('CHANNEL_ID')

JAR_ID = env.str('MONO_JAR_ID')
TOKEN = env.str('MONO_USER_TOKEN')
MONO_JAR_URL = env.str('MONO_JAR_URL')
