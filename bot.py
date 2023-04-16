import yaml
import os
import nextcord
import pathlib

from nextcord.ext import commands
from nextcord.ext.commands import Bot
from Utils.console_logger import Log

config = yaml.load(open("./Config/config.yml", "r"), Loader=yaml.FullLoader)
msg = yaml.load(open("./Config/messages.yml", "r"), Loader=yaml.FullLoader)

loaded_cogs = []


class Azark(commands.Bot):
    def __init__(self):
        self.log = Log()
        intents = nextcord.Intents.default()
        intents.message_content = True

        activity = nextcord.Activity(name=msg["activity"], type=nextcord.ActivityType.playing)

        super().__init__(
            command_prefix=config["prefix"],
            help_command=None,
            activity=activity,
            intents=intents,
            case_insensitive=True
        )

        for i in os.listdir("Cogs"):
            if i.endswith('.py'):
                Bot.load_extension(self, name=f'Cogs.{i[:-3]}')
                loaded_cogs.append(i)

    async def on_ready(self):
        for i in os.listdir('Cogs'):
            if i.endswith('.py'):
                cog_name = i[:-3]
                if i in loaded_cogs:
                    await self.log.debug(f'Cog {cog_name} loaded')
                else:
                    await self.log.critical(f'Cog {cog_name} not loaded')

        # if pathlib.Path('Utils/word_list.txt').exists():
        #     print(f'word list loaded')
        # else:
        #     print(f'word list not loaded')

        await self.log.start_up('~~~~~~~~~~')
        if config['dev_mode']:
            await self.log.critical(f'**DEV MODE ENABLED**')
        await self.log.start_up(f'Logged in as: {self.user.name}')
        await self.log.start_up(f'ID: {self.user.id}')
        await self.log.start_up(f'Loaded {len(loaded_cogs)} cogs')
        await self.log.start_up(f'Bot Online')
        await self.log.start_up('~~~~~~~~~~')
