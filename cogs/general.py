from discord.ext import commands
import discord
import urllib
import random
import sys
import time
import logging

log = logging.getLogger("bot.general")

class Fun:

    def __init__(self, bot):
        self.bot = bot

    def getdog():
        dog = urllib.request.urlopen('https://random.dog/woof')
        dog = str(dog.read())
        dog = dog[2:]
        dog = dog[:len(dog) - 1]
        return dog

    def getcat():
        cat = urllib.request.urlopen('https://random.cat/meow')
        cat = str(cat.read())
        cat = cat[11:]
        cat = cat[:len(cat) - 3]
        cat = cat.replace("\\", "")
        return cat

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
            embed.add_field(name="> Voice", value="**• Active Sessions:** {}\n**• Songs Played:** In Progress".format(len(self.bot.voice_clients)))
            embed.add_field(name="> Version", value="**• NanoBot:** 2.0\n**• discord.py:** {}\n**• Python:** {}".format(discord.__version__, pyver))
            embed.add_field(name="> Misc", value="**• Website:** [Go!](https://nanobot-discord.github.io)\n**• Discord:** [Join!](https://discord.gg/eDRnXd6)")
            log.info("Created Embed")
            await self.bot.say(embed=embed)
        except:
            raise

    @commands.command(pass_context=True)
    async def dog(self, ctx): # !!dog
        """Gets a random dog from http://random.dog"""
        await self.bot.send_typing(ctx.message.channel)
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        embed = discord.Embed(color=color)
        embed.title = "Random Dog"

        dog = "null"
        while 1:
            dog = Fun.getdog()
            if not dog.endswith(".mp4"):
                break
        embed.set_footer(text="{}".format("http://random.dog/" + str(dog)))
        embed.set_image(url="http://random.dog/" + str(dog))
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def cat(self, ctx): # !!cat
        """Gets a random cat from http://random.cat"""
        await self.bot.send_typing(ctx.message.channel)
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        embed = discord.Embed(color=color)
        embed.title = "Random Cat"
        cat = "null"
        while 1:
            cat = Fun.getcat()
            if not cat.endswith(".mp4"):
                break
        embed.set_footer(text="{}".format(str(cat)))
        embed.set_image(url=str(cat))
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="8ball")
    async def _8ball(self, *, question : str):
        """Ask a question."""
        responses = [["Signs point to yes.", "Yes.", "Without a doubt.", "As I see it, yes.", "You may rely on it.", "It is decidedly so.", "Yes - definitely.", "It is certain.", "Most likely.", "Outlook good."],
        ["Reply hazy, try again.", "Concentrate and ask again.", "Better not tell you now.", "Cannot predict now.", "Ask again later."],
        ["My sources say no.", "Outlook not so good.", "Very doubtful.", "My reply is no.", "Don't count on it."]]
        if "?" in question:
            await self.bot.say(":8ball:" + random.choice(random.choice(responses)))
        else:
            await self.bot.say("That doesn't look like a question.")

def setup(bot):
    n = Fun(bot)
    bot.add_cog(n)