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
            embed.add_field(name="> Voice", value="**• Active Sessions:** {}\n**• Songs Played:** Unknown".format(len(self.bot.voice_clients)))
            embed.add_field(name="> Version", value="**• NanoBot:** 2.0\n**• discord.py:** {}\n**• Python:** {}".format(discord.__version__, pyver))
            embed.add_field(name="> Misc", value="**• Website:** [Go!](https://nanobot-discord.github.io)\n**• Discord:** [Join!](https://discord.gg/eDRnXd6)")
            log.info("Created Embed")
            await self.bot.say(embed=embed)
        except:
            raise

    @commands.command(pass_context=True, no_pm=True, aliases=['server', 'guildinfo', 'serverinfo'])
    async def guild(self, ctx):
        """Shows guild info."""
        await self.bot.send_typing(ctx.message.channel)
        server = ctx.message.server
        badge = "​"
        if server.id in self.partnered_guilds:
            badge += self.self.badges['partner']
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
    async def user(self, ctx, *, user : discord.User = ctx.message.author)
         """Gets a user's information"""
         await self.bot.send_typing(ctx.message.channel)
         # Get user badges
         badge = []
         r = requests.get("https://discordbots.org/api/bots/294210459144290305/votes?onlyids=1", headers={"Authorization":self.settings.discordbotsorg_token})
         if r.status_code = 200:
             r = r.json()
             if user.id in r:
                 badge.append(self.badges["voter"])
         else:
             logging.error("Failed to get voting data / Error {}".format(r.status_code))
             await self.bot.say("I couldn't get voting info. (Error {})".format(r.status_code))
         if user.id == self.settings.dev or user.id == self.settings.owner:
             badge.append(self.badges["staff"])
         if user.id in self.partners:
             badge.append(self.badges["partner"])
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
