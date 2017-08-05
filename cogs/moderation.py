from discord.ext import commands
import discord

class Moderation:

    # TODO: Add moderator commands

    def __init__(self, bot):
        self.bot = bot

    def ismod(ctx):
        passed = False
        for role in ctx.message.author.roles:
            if role.name.lower() == "nanobot mod" or role.name.lower() == "moderator" or role.name.lower() == "mod" or role.name.lower() == "discord mod":
                passed = True
        return passed

    @commands.command(pass_context=True, no_pm=True, aliases=['purge', 'clear'])
    @commands.check(ismod)
    async def prune(self, ctx, limit : int): # !!prune
        """Deletes the specified amount of messages."""
        global errors
        if not limit > 1:
            await self.bot.say(":no_entry_sign: You can only delete more than 1 message!")
        else:
            counter = -1
            await self.bot.send_typing(ctx.message.channel)
            try:
                async for log in self.bot.logs_from(ctx.message.channel, limit=limit + 1):
                    await self.bot.delete_message(log)
                    counter += 1
                    if counter % 5 == 0:
                        await self.bot.send_typing(ctx.message.channel)
            except Exception as e:
                logging.error(str(e))
                await self.bot.say(embed=embeds.error(str(e), ctx))
            else:
                await self.bot.say(':zap: Deleted {} messages.'.format(counter))

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(ismod)
    async def ban(self, ctx, user : discord.Member, *, reason : str = "*No reason was provided.*"):
        try:
            await self.bot.send_message(user, "You were banned from **{}** by the moderator **{}** for the reason: {}".format(ctx.message.server.name, ctx.message.author, reason))
            await self.bot.ban(user, delete_message_days=0)
            case = uuid.uuid4()
            bans.append(objects.Banne(case, ctx.message.server, user, ctx.message.author, reason))
            try:
                for channel in ctx.message.server.channels:
                    if channel.name == "mod-log" or channel.name == "mod_log":
                        await self.bot.send_message(channel, embed=embeds.user_ban(ctx.message.author, user, reason, case))
                        break
            except:
                await self.bot.say("**ProTip:** Having a channel named `#mod_log` or `#mod-log` will allow me to post moderation info.")
        except discord.Forbidden:
            await self.bot.say(embed=embeds.error("I don't have the correct permissions to do that.", ctx))
        except:
            raise
        else:
            await self.bot.say("Successfully banned " + str(user))

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(ismod)
    async def kick(self, ctx, user : discord.Member, *, reason : str = "*No reason was provided.*"):
        try:
            await self.bot.send_message(user, "You were kicked from **{}** by the moderator **{}** for the reason: {}".format(ctx.message.server.name, ctx.message.author, reason))
            await self.bot.kick(user)
            case = uuid.uuid4()
            kicks.append(objects.Kick(case, ctx.message.server, user, ctx.message.author, reason))
            try:
                for channel in ctx.message.server.channels:
                    if channel.name == "mod-log" or channel.name == "mod_log":
                        await self.bot.send_message(channel, embed=embeds.user_kick(ctx.message.author, user, reason, case))
                        break
            except:
                await self.bot.say("**ProTip:** Having a channel named `#mod_log` or `#mod-log` will allow me to post moderation info.")
        except discord.Forbidden:
            await self.bot.say(embed=embeds.error("I don't have the correct permissions to do that.", ctx))
        except:
            raise
        else:
            await self.bot.say("Successfully kicked " + str(user))

def setup(bot):
    bot.add_cog(Moderation(bot))
