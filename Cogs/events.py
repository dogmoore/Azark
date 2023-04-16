import nextcord
import yaml
from datetime import datetime
from nextcord.ext.application_checks import errors as application_errors
from nextcord.ext import commands
from Utils.console_logger import Log

current_time = datetime.now().strftime("%H:%M:%S")
config = yaml.load(open('./Config/config.yml', 'r'), Loader=yaml.FullLoader)
ids = yaml.load(open('./Config/id.yml', 'r'), Loader=yaml.FullLoader)
messages = yaml.load(open('./Config/messages.yml', 'r'), Loader=yaml.FullLoader)


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log = Log()

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        log_channel = self.client.get_channel(ids['mod_log'])
        delete_embed = nextcord.Embed(
            description=f'{msg.author.mention} deleted a message in {msg.channel.mention}',
            color=config['color']['default']
        )

        delete_embed.set_thumbnail(url=msg.author.avatar)
        delete_embed.add_field(name='Message:', value=msg.content, inline=False)
        delete_embed.set_footer(text=messages['footer'])

        await log_channel.send(embed=delete_embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):  # message log
        if not before.author.id == self.client.user.id:
            if not before.content == after.content:
                log_channel = self.client.get_channel(ids['mod_log'])

                edit_embed = nextcord.Embed(
                    description=f'Member {before.author.mention} edited a message in {before.channel.mention}\n['
                                f'Jump to message]({after.jump_url})',
                    color=config['color']['default']
                )

                edit_embed.set_thumbnail(url=before.author.avatar)
                edit_embed.add_field(name='Before:', value=f'{before.content}', inline=True)
                edit_embed.add_field(name='After:', value=f'{after.content}', inline=True)
                edit_embed.set_footer(text=messages['footer'])

                await log_channel.send(embed=edit_embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, message_number):  # message log
        log_channel = self.client.get_channel(ids['mod_log'])
        message = message_number[0]

        bulk_embed = nextcord.Embed(
            title=message.author,
            description=f'Deleted `{len(message_number)}` messages in {messages.channel.mention}',
            color=config['color']['default']
        )
        bulk_embed.set_footer(text=messages['footer'])

        await log_channel.send(embed=bulk_embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):  # member log
        log_channel = self.client.get_channel(ids['mod_log'])

        member_join_embed = nextcord.Embed(
            description=f'<@{member.id}> Joined',
            color=config['color']['green']
        )

        member_join_embed.set_thumbnail(url=member.avatar)
        member_join_embed.add_field(name='Bot:', value=member.bot, inline=False)
        member_join_embed.add_field(name='ID:', value=member.id, inline=True)
        member_join_embed.set_footer(text=messages['footer'])

        await log_channel.send(embed=member_join_embed)

        general = self.client.get_channel(ids['general'])
        welcome_channel = self.client.get_channel(ids['welcome'])

        welcome_embed = nextcord.Embed(
            description=f'Welcome <@{member.id}>!',
            color=config['color']['default']
        )

        await welcome_channel.send(embed=welcome_embed)
        await general.send(
            content=f'Welcome to the Moonlight Coders {member.mention}!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):  # member log

        log_channel = self.client.get_channel(ids['mod_log'])

        member_left_embed = nextcord.Embed(
            title=f'{member.name} left!',
            color=config['color']['default']
        )

        member_left_embed.set_thumbnail(url=member.avatar)
        role_array = []
        for role in member.roles:
            role_array.append(role.name)
        member_left_embed.add_field(name='Roles:', value=f'{" ".join(role_array[-1:])}')
        member_left_embed.set_footer(text=messages['footer'])

        await log_channel.send(embed=member_left_embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):  # invite log
        log_channel = self.client.get_channel(ids['mod_log'])

        invite_create_embed = nextcord.Embed(
            title=f'Invite created by {invite.inviter}',
            description=f'discord.gg/{invite.id}',
            color=config['color']['error']
        )

        invite_create_embed.set_footer(text=messages['footer'])

        await log_channel.send(embed=invite_create_embed)

    @commands.Cog.listener()
    async def on_member_ban(self, _guild, user):  # mod log
        log_channel = self.client.get_channel(ids['mod_log'])

        ban_embed = nextcord.Embed(
            title=f'{user.name} got banned!',
            color=config['color']['critical']
        )

        ban_embed.set_footer(text=messages['footer'])

        await log_channel.send(embed=ban_embed)

    @commands.Cog.listener()
    async def on_member_unban(self, _guild, user):  # mod log
        log_channel = self.client.get_channel(ids['mod_log'])

        unban_embed = nextcord.Embed(
            title=f'{user.name} got unbanned',
            color=config['color']['error']
        )

        await log_channel.send(embed=unban_embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_embed = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.",
            color=config["color"]['critical']
        )
        if isinstance(error, commands.errors.MissingRequiredArgument):
            error_embed.add_field(
                name="Error is described below.",
                value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```"
            )
            error_embed.set_footer(text=messages["footer"])
            return await ctx.send(embed=error_embed)
        await self.log.critical(f'Something went wrong, {error}')
        log_channel = self.client.get_channel(ids['admin_log'])
        critical_embed = nextcord.Embed(
            title=f'CRITICAL | {current_time}',
            description=str(error),
            color=config['color']['critical']
        )
        await log_channel.send(embed=critical_embed)

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error: Exception):
        if isinstance(error, application_errors.ApplicationMissingRole):
            role = interaction.guild.get_role(int(error.missing_role))
            return await interaction.send(f"{role.mention} role is required to use this command.", ephemeral=True)
        await interaction.send(f"This command raised an exception: `{type(error)}:{str(error)}`", ephemeral=True)
        await self.log.error(str(error))
        log_channel = self.client.get_channel(ids['admin_log'])
        error_embed = nextcord.Embed(
            title=f'ERROR | {current_time}',
            description=str(error),
            color=config['color']['error']
        )
        await log_channel.send(embed=error_embed)


def setup(client):
    client.add_cog(Events(client))
