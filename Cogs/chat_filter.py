import nextcord
import yaml
import datetime
from nextcord.ext import commands
from Utils.console_logger import Log

config = yaml.load(open("./Config/config.yml", "r"), Loader=yaml.FullLoader)
ids = yaml.load(open('./Config/id.yml', 'r'), Loader=yaml.FullLoader)
messages = yaml.load(open('./Config/messages.yml', 'r'), Loader=yaml.FullLoader)


class InviteDetection(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Log()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        # invite filter
        hit_list = ['discord.gg', 'discord. gg', 'discord .gg']
        channel = self.client.get_channel(msg.channel)
        log_channel = self.client.get_channel(ids['mod_log'])

        log_embed = nextcord.Embed(
            title='INVITE DETECTED',
            description=f'User {msg.author.mention} said\n{msg.content}',
            color=config['color']['default']
        )

        if msg.content in hit_list:
            if msg.channel.id not in config['ignored_channels']:
                await msg.author.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=3600))
                await channel.send(content=f'{msg.author.mention} {messages["invite_filter"]}')
                await log_channel.send(embed=log_embed)
                await msg.delete()


def setup(client):
    client.add_cog(InviteDetection(client))
