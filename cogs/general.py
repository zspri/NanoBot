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
    async def user(self, ctx, *, user : discord.User = None): # !!user
        """Gets the specified user's info."""
        await self.bot.send_typing(ctx.message.channel)
        badge = ""
        if user is None or user == None:
            user = ctx.message.author
        r = requests.get("https://discordbots.org/api/bots/294210459144290305/votes", headers={"Authorization":os.getenv("DBOTSLIST_TOKEN")})
        if r.status_code == 200:
            r = r.json()
            for u in r:
                if u['id'] == user.id:
                    badge += self.badges['voter'] + " "
        else:
            logging.error("Failed to get voting info!")
            await self.bot.say(":no_entry_sign: Failed to get voter info. If you voted, your badge will not show up temporarily.")
        if user.id in staff:
            badge += self.badges['staff'] + " "
        if user.id in self.partners:
            badge += self.badges['partner'] + " "
        member = self.bot.get_server("294215057129340938").get_member(user.id)
        if member is not None:
            for role in member.roles:
                if role.name.lower() == "retired":
                    badge += self.badges['retired'] + " "
        if badge == "":
            badge = "None"
        stp2 = ""
        for role in user.roles:
            if not role == ctx.message.server.default_role:
                if role.name == user.roles[len(user.roles) - 1].name:
                   stp2 = stp2 + role.name
                else:
                    stp2 = stp2 + role.name + ", "
        if stp2 == "": stp2 = "None"
        embed = discord.Embed(color=user.color)
        embed.add_field(name="Username", value=str(user)[:1000])
        embed.add_field(name="Nickname", value=str(user.nick)[:1000])
        embed.add_field(name="Badges", value=str(badge))
        try:
            embed.add_field(name="Playing", value=user.game.name[:1000])
        except:
            embed.add_field(name="Playing", value="(Nothing)")
        embed.add_field(name="Account Created", value=user.created_at)
        embed.add_field(name="Joined Guild", value=user.joined_at)
        embed.add_field(name="Roles", value=stp2[:1000])
        embed.add_field(name="Color", value=str(ctx.message.author.color))
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=embed)

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
