from discord.ext import commands
import discord
import logging
import asyncio
import requests
import time
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
            embed.add_field(name="> Misc", value="**• Website:** [Go!](https://nanobot-discord.github.io)\n**• Discord:** [Join!](https://discord.gg/eDRnXd6)")
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
        
def setup(bot):
    n = Moderation(bot)
    bot.add_cog(n)