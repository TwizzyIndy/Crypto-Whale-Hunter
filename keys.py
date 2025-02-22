from dotenv import dotenv_values

config = dotenv_values(".env")

ApiKey = config['API_KEY']
SecretKey= config['SECRET']