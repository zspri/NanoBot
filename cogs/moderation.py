from discord.ext import commands
import discord
import logging
import asyncio
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

    @commands.group(pass_context=True, no_pm=True, aliases=['purge', 'clear'])
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