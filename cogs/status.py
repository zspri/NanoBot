from discord.ext import commands
import discord
import urrlib.request
import asyncio

class Status:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def status(self, ctx): # !!status
            if ctx.invoked_subcommand is None:
                f = open('status_help.txt')
                await self.bot.say(f.read())
                f.close()

    @status.command()
    async def help(self):
        f = open('status_help.txt')
        await self.bot.say(f.read())
        f.close()

    @status.command(pass_context=True)
    async def all(self, ctx): # All Statuses
        await self.bot.send_typing(ctx.message.channel)
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        embed = discord.Embed(color=color)
        class discord_st:
            st = urllib.request.urlopen('https://srhpyqt94yxb.statuspage.io/api/v2/status.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']['indicator']
            desc = st['status']['description']
            timestamp = st['page']['updated_at']
        await self.bot.send_typing(ctx.message.channel)
        class github_st:
            st = urllib.request.urlopen('https://status.github.com/api/last-message.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']
            desc = st['body']
            timestamp = st['created_on']
        await self.bot.send_typing(ctx.message.channel)
        class reddit_st:
            st = urllib.request.urlopen('http://2kbc0d48tv3j.statuspage.io/api/v2/status.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']['indicator']
            desc = st['status']['description']
            timestamp = st['page']['updated_at']
        await self.bot.send_typing(ctx.message.channel)
        class hi_rez_st:
            st = urllib.request.urlopen('http://stk4xr7r1y0r.statuspage.io/api/v2/status.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']['indicator']
            desc = st['status']['description']
            timestamp = st['page']['updated_at']
        await self.bot.send_typing(ctx.message.channel)
        embed.title = "Website Status"
        embed.set_footer(text="StatusPage.io")
        embed.add_field(name="Discord", value=discord_st.status)
        embed.add_field(name="GitHub", value=github_st.status)
        embed.add_field(name="Reddit", value=reddit_st.status)
        embed.add_field(name="Hi-Rez Studios", value=hi_rez_st.status)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def discord(self, ctx): # Discord Status
        """Shows Discord status (From https://status.discordapp.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('https://srhpyqt94yxb.statuspage.io/api/v2/status.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']['indicator']
        desc = st['status']['description']
        timestamp = st['page']['updated_at']
        color = discord.Color.default()
        if status == "none":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="Discord Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        embed.set_thumbnail(url="https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def github(self, ctx): # GitHub Status
        """Shows GitHub status (From https://status.github.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('https://status.github.com/api/last-message.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']
        desc = st['body']
        timestamp = st['created_on']
        color = discord.Color.default()
        if status == "good":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="GitHub Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        embed.set_thumbnail(url="https://maxcdn.icons8.com/iOS7/PNG/75/Logos/github_copyrighted_filled-75.png")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def reddit(self, ctx): # Reddit Status
        """Shows Reddit status (From https://redditstatus.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('http://2kbc0d48tv3j.statuspage.io/api/v2/status.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']['indicator']
        desc = st['status']['description']
        timestamp = st['page']['updated_at']
        color = discord.Color.default()
        if status == "none":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="Reddit Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        embed.set_thumbnail(url="http://img.washingtonpost.com/rf/image_1024w/2010-2019/WashingtonPost/2012/08/15/National-Enterprise/Images/reddit-alien.jpg")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def hi_rez(self, ctx): # Hi-Rez Studios Status
        """Shows Hi-Rez Studios status (From https://status.hirezstudios.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('http://stk4xr7r1y0r.statuspage.io/api/v2/status.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']['indicator']
        desc = st['status']['description']
        timestamp = st['page']['updated_at']
        color = discord.Color.default()
        if status == "none":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="Hi-Rez Studios Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    bot.add_cog(Status(bot))
