from discord.ext import commands
import discord
import urllib
import random
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
