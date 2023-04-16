import time
import nextcord
import yaml
import datetime

from typing import Optional
from nextcord import slash_command, SlashOption, Permissions
from nextcord.ext import commands
from Utils.console_logger import Log

config = yaml.load(open('./Config/config.yml', 'r'), Loader=yaml.FullLoader)
ids = yaml.load(open('./Config/id.yml', 'r'), Loader=yaml.FullLoader)
messages = yaml.load(open('./Config/messages.yml', 'r'), Loader=yaml.FullLoader)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config
        self.messages = messages
        self.ids = ids
        self.log = Log()

    @slash_command(name='kick',
                   default_member_permissions=Permissions(kick_members=True),
                   guild_ids=ids['guild'])
    async def kick(self, interaction: nextcord.Interaction,
                   target: Optional[nextcord.Member] = SlashOption(required=True),
                   reason: Optional[str] = SlashOption(required=True),
                   evidence: Optional[str] = SlashOption(required=False)):
        log_channel = self.client.get_channel(self.ids['mod_log'])
        kick_embed = nextcord.Embed(
            description=f'kicked user {target.mention} for {reason}',
            color=self.config['color']['default']
        )

        kick_log_embed = nextcord.Embed(
            title='Ban log',
            description=f'User {target.mention} got kicked',
            color=self.config['color']['default']
        )
        kick_log_embed.add_field(name='Reason:', value=reason)
        kick_log_embed.add_field(name='Evidence', value=evidence)
        kick_log_embed.set_footer(text=self.messages['footer'])

        kick_dm_embed = nextcord.Embed(
            title=f'You have been removed from {self.messages["server_name"]}',
            description=f'You have been kicked from {self.messages["server_name"]} for {reason}',
            color=self.config['color']['default']
        )
        kick_dm_embed.add_field(name='Evidence', value=evidence)
        kick_dm_embed.set_footer(text=self.messages['footer'])

        try:
            await target.send(embed=kick_dm_embed)
            await target.kick(reason=reason)
            await interaction.response.send_message(embed=kick_embed)
            await log_channel.send(embed=kick_log_embed)
        except Exception:
            await interaction.response.send_message(self.messages['kick_error'])

    @slash_command(name='ban',
                   default_member_permissions=Permissions(ban_members=True),
                   guild_ids=ids['guild'])
    async def ban(self, interaction: nextcord.Interaction,
                  target: Optional[nextcord.Member] = SlashOption(required=True),
                  reason: Optional[str] = SlashOption(required=True),
                  evidence: Optional[str] = SlashOption(required=True)):
        log_channel = self.client.get_channel(self.ids['mod_log'])
        ban_embed = nextcord.Embed(
            description=f'banned user {target.mention} for {reason}',
            color=self.config['color']['default']
        )

        ban_log_embed = nextcord.Embed(
            title='Ban log',
            description=f'User {target.mention} got banned',
            color=self.config['color']['default']
        )
        ban_log_embed.add_field(name='Reason:', value=reason)
        ban_log_embed.add_field(name='Evidence', value=evidence)
        ban_log_embed.set_footer(text=self.messages['footer'])

        ban_dm_embed = nextcord.Embed(
            title=f'You have been removed from {self.messages["server_name"]}',
            description=f'You have been banned from {self.messages["server_name"]} for {reason}',
            color=self.config['color']['default']
        )
        ban_dm_embed.add_field(name='Evidence', value=evidence)
        ban_dm_embed.set_footer(text=self.messages['footer'])

        try:
            await target.send(embed=ban_dm_embed)
            time.sleep(0.5)
            await target.ban(delete_message_days=7, reason=reason)
            await interaction.response.send_message(embed=ban_embed)
            await log_channel.send(embed=ban_log_embed)
        except Exception:
            await interaction.response.send_message(self.messages['ban_error'])

    @slash_command(name='mute',
                   default_member_permissions=Permissions(moderate_members=True),
                   guild_ids=ids['guild'])
    async def mute(self, interaction: nextcord.Interaction,
                   duration=SlashOption(
                       choices=[
                           '5 minutes',
                           '10 minutes',
                           '30 minutes',
                           '1 hour',
                           '2 hours',
                           '5 hours',
                           '8 hours',
                           '12 hours',
                           '1 day',
                           '3 days',
                           '1 week',
                           '2 weeks',
                           '1 month'  # max is 28 days
                       ],
                       required=True
                   ),
                   target: Optional[nextcord.Member] = SlashOption(required=True),
                   reason: Optional[str] = SlashOption(required=True),
                   evidence: Optional[str] = SlashOption(required=False)):
        log_channel = self.client.get_channel(self.ids['mod_logs'])

        def five_minutes():
            time_delta = datetime.timedelta(seconds=300)
            return time_delta

        def ten_minutes():
            time_delta = datetime.timedelta(seconds=600)
            return time_delta

        def thirty_minutes():
            time_delta = datetime.timedelta(seconds=1800)
            return time_delta

        def one_hour():
            time_delta = datetime.timedelta(seconds=3600)
            return time_delta

        def two_hours():
            time_delta = datetime.timedelta(seconds=7200)
            return time_delta

        def five_hours():
            time_delta = datetime.timedelta(seconds=18000)
            return time_delta

        def eight_hours():
            time_delta = datetime.timedelta(seconds=28800)
            return time_delta

        def twelve_hours():
            time_delta = datetime.timedelta(seconds=43200)
            return time_delta

        def one_day():
            time_delta = datetime.timedelta(days=1)
            return time_delta

        def three_days():
            time_delta = datetime.timedelta(days=3)
            return time_delta

        def one_week():
            time_delta = datetime.timedelta(days=7)
            return time_delta

        def two_weeks():
            time_delta = datetime.timedelta(days=14)
            return time_delta

        def one_month():
            time_delta = datetime.timedelta(days=28)
            return time_delta

        def default():
            time_delta = datetime.timedelta(seconds=300)
            return time_delta

        switcher = {
            '5 minutes': five_minutes,
            '10 minutes': ten_minutes,
            '30 minutes': thirty_minutes,
            '1 hour': one_hour,
            '2 hours': two_hours,
            '5 hours': five_hours,
            '8 hours': eight_hours,
            '12 hours': twelve_hours,
            '1 day': one_day,
            '3 days': three_days,
            '1 week': one_week,
            '2 weeks': two_weeks,
            '1 month': one_month
        }

        def time_delta_switcher(mute_duration):
            return switcher.get(mute_duration, default)()

        try:
            mute_embed = nextcord.Embed(
                title=f'{target.user} got muted for {duration}',
                description=f'Reason: {reason}',
                color=self.config['color']['default']
            )
            mute_embed.set_footer(text=self.messages['footer'])

            mute_log_embed = nextcord.Embed(
                title='Mute log',
                description=f'{target.user} for muted for {duration}',
                color=self.config['color']['default']
            )

            mute_log_embed.add_field(name='Reason', value=reason, inline=False)
            mute_log_embed.add_field(name='Evidence', value=evidence, inline=False)
            mute_log_embed.set_footer(text=self.messages['footer'])

            await target.edit(timeout=nextcord.utils.utcnow() + time_delta_switcher(duration))
            await interaction.response.send_message(embed=mute_embed)
            await log_channel.send(embed=mute_log_embed)
        except Exception as err:
            await interaction.response.send_message(self.messages['mute_error'])

    @slash_command(name='force', guild_ids=ids['guild'])
    async def force_main(self, interaction: nextcord.Interaction):
        pass

    @force_main.subcommand(name='nick', description='Change an inappropriate nickname')
    @commands.has_role('STAFF')
    async def nickname(self, interaction: nextcord.Interaction,
                       target: Optional[nextcord.Member] = SlashOption(required=True),
                       nickname: Optional[str] = SlashOption(required=True)):
        if len(nickname) > 64:
            await interaction.response.send_message(self.messages['nickname_length_error'], ephemeral=True)
        if len(nickname) <= 64:
            log_channel = self.client.get_channel(self.ids['mod_log'])
            nick_embed = nextcord.Embed(
                description=f'nicknamed {target.mention} to {nickname}',
                color=self.config['color']['default']
            )

            nick_log_embed = nextcord.Embed(
                title='nickname log',
                description=f'User {target.mention} was nicknamed to {nickname}',
                color=self.config['color']['default']
            )
            nick_log_embed.set_footer(text=self.messages['footer'])

            try:
                await target.edit(nick=nickname)
                await interaction.response.send_message(embed=nick_embed, ephemeral=True)
                await log_channel.send(embed=nick_log_embed)
            except Exception:
                await interaction.response.send_message(self.messages['nickname_error'])


def setup(client):
    client.add_cog(Moderation(client))
