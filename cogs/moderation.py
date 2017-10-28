from discord.ext import commands
import discord
import logging
import asyncio
import requests
import time
import sys
from .utils import checks
from .utils.embed import Embeds

log = logging.getLogger("bot.moderation")

class Moderation:

    def __init__(self, bot):
        self.bot = bot
        self.embeds = Embeds()

    async def process_deletion(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1.5)

    @commands.command(pass_context=True, no_pm=True, aliases=['botinfo', 'stats', 'about'])
    async def info(self, ctx): # !!info
        """Shows bot info."""
        try:
            await self.bot.send_typing(ctx.message.channel)
            pyver = ""
            for x in sys.version_info[0:3]:
                if x == sys.version_info[2]:
                    pyver += str(x)
                else:
                    pyver += str(x) + "."
            elapsed_time = time.gmtime(time.time() - self.bot.start_time)
            log.info("Got bot uptime")
            stp = str(elapsed_time[7] - 1) + " days, " + str(elapsed_time[3]) + " hours, " + str(elapsed_time[4]) + " minutes"
            log.info("Formatted bot uptime")
            users = sum(1 for _ in self.bot.get_all_members())
            log.info("Got all bot users")
            color = discord.Color.default()
            if ctx.message.server is not None:
                color = ctx.message.server.me.color
            embed = discord.Embed(color=color, title="NanoBot Statistics", description="Made by **Der#4587** and **Kalico#5669**")
            embed.set_footer(text="NanoBot#2520")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name="> Uptime", value=stp)
            embed.add_field(name="> Usage", value="**• Guilds:** {}\n**• Users:** {}".format(len(self.bot.servers), users))
            embed.add_field(name="> Commands", value="**• Total Received:** {}\n**• Errors:** {} ({}%)".format(len(self.bot.cmds_this_session), len(self.bot.errors), round(len(self.bot.errors)/len(self.bot.cmds_this_session) * 100)))
            embed.add_field(name="> Voice", value="**• Active Sessions:** {}\n**• Songs Played:** Unknown".format(len(self.bot.voice_clients)))
            embed.add_field(name="> Version", value="**• NanoBot:** 2.0\n**• discord.py:** {}\n**• Python:** {}".format(discord.__version__, pyver))
            embed.add_field(name="> Misc", value="**• Website:** [Go!](https://nanobot-discord.github.io)\n**• Discord:** [Join!](https://discord.gg/eDRnXd6)\n**• Status:** [status.kalico.io](http://status.kalico.io)")
            log.info("Created Embed")
            await self.bot.say(embed=embed)
        except:
            raise

    @commands.command(pass_context=True, no_pm=True, aliases=['purge', 'clear'])
    @checks.mod_or_permissions(manage_messages=True)
    async def prune(self, ctx, number: int):
        """Deletes the specified amount of messages."""
        if ctx.invoked_subcommand is None:
            channel = ctx.message.channel
            author = ctx.message.author
            server = author.server
            is_bot = self.bot.user.bot
            has_permissions = channel.permissions_for(server.me).manage_messages

            to_delete = []

            if not has_permissions:
                await self.bot.say("I'm not allowed to delete messages.")
                return

            async for message in self.bot.logs_from(channel, limit=number+1):
                to_delete.append(message)

            log.info("{}({}) deleted {} messages in channel {}".format(author.name, author.id, number, channel.name))
            await self.process_deletion(to_delete)

    @commands.command(pass_context=True, no_pm=True, aliases=['server', 'guildinfo', 'serverinfo'])
    async def guild(self, ctx):
        """Shows guild info."""
        await self.bot.send_typing(ctx.message.channel)
        server = ctx.message.server
        badge = "​"
        if server.id in self.bot.partnered_guilds:
            badge += self.bot.badges['partner']
        roles = []
        for r in server.roles:
            roles.append(r.name)
        stp2 = ", ".join(roles)
        embed = discord.Embed(color=ctx.message.server.me.color, title="Guild Info")
        embed.set_author(name=server.name, icon_url=server.icon_url)
        embed.set_footer(text="NanoBot#2520")
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Name", value=server.name + " {}".format(badge))
        embed.add_field(name="ID", value=str(server.id))
        embed.add_field(name="Roles", value=stp2)
        embed.add_field(name="Owner", value=str(server.owner))
        embed.add_field(name="Members", value=server.member_count)
        embed.add_field(name="Channels", value=len(server.channels))
        embed.add_field(name="Region", value=server.region)
        embed.add_field(name="Custom Emoji", value=len(server.emojis))
        embed.add_field(name="Created At", value=server.created_at)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, no_pm=True, aliases=['userinfo', 'member', 'memberinfo', 'profile'])
    async def user(self, ctx, *, user : discord.User = None):
        """Gets a user's information"""
        await self.bot.send_typing(ctx.message.channel)
        # Get user badges
        badge = []
        if user is None or user == None:
            user = ctx.message.author
        r = requests.get("https://discordbots.org/api/bots/294210459144290305/votes?onlyids=1", headers={"Authorization":self.bot.settings.discordbotsorg_token})
        if r.status_code == 200:
            r = r.json()
            if user.id in r:
                badge.append(self.bot.badges["voter"])
        else:
            logging.error("Failed to get voting data / Error {}".format(r.status_code))
            await self.bot.say("I couldn't get voting info. (Error {})".format(r.status_code))
        if user.id == self.bot.settings.dev or user.id == self.bot.settings.owner:
            badge.append(self.bot.badges["staff"])
        if user.id in self.bot.partners:
            badge.append(self.bot.badges["partner"])
        # Get user roles
        roles = []
        for r in user.roles:
            roles.append(r.name)
        usr_roles = ", ".join(roles)
        bgs = " ".join(badge)
        e = discord.Embed(color=user.color, title="User Info")
        e.set_author(name=user.name, icon_url=user.avatar_url)
        e.add_field(name="User", value=str(user) + bgs)
        try:
            e.add_field(name="Playing", value=user.game.name[:1000])
        except:
            e.add_field(name="Playing", value="(Nothing)")
        e.add_field(name="Account Created", value=user.created_at)
        e.add_field(name="Joined Guild", value=user.joined_at)
        e.add_field(name="Roles", value=usr_roles)
        e.add_field(name="Color", value=str(ctx.message.author.color))
        e.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=e)

def setup(bot):
    n = Moderation(bot)
    bot.add_cog(n)
