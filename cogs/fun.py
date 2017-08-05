from discord.ext import commands
import discord
import urrlib.request
import asyncio

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
            dog = General.getdog()
            if not dog.endswith(".mp4"):
                break
        print("https://random.dog/" + str(dog))
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
            cat = General.getcat()
            if not cat.endswith(".mp4"):
                break
        print(cat)
        embed.set_footer(text="{}".format(str(cat)))
        embed.set_image(url=str(cat))
        await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
