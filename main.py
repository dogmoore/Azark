import bot
import yaml

token = yaml.load(open("./Config/secret_token.yml", "r"), Loader=yaml.FullLoader)

client = bot.Azark()
client.run(token["token"])
