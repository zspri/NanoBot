from discord.ext import commands
import discord
import time
import os
import asyncio, requests
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def invite(self, ctx): # !!invite
        """Shows a link to invite NanoBot to your server."""
        await self.bot.say(ctx.message.author.mention + ", you can invite me to a server with this link: http://bot.nanomotion.xyz/invite")

    @commands.command(pass_context=True, no_pm=True, aliases=['userinfo', 'member', 'memberinfo', 'profile'])
    async def user(self, ctx, *, user : discord.User = None): # !!user
        """Gets the specified user's info."""
        await self.bot.send_typing(ctx.message.channel)
        global staff
        global partners
        global badges
        global blocked_ids
        badge = ""
        if user is None or user == None:
            user = ctx.message.author
        r = requests.get("https://discordbots.org/api/bots/294210459144290305/votes", headers={"Authorization":os.getenv("DBOTSLIST_TOKEN")})
        if r.status_code == 200:
            r = r.json()
            for u in r:
                if u['id'] == user.id:
                    badge += badges['voter'] + " "
        else:
            log.error("Failed to get voting info!")
            await self.bot.say(":no_entry_sign: Failed to get voter info. If you voted, your badge will not show up temporarily.")
        if user.id in staff:
            badge += badges['staff'] + " "
        if user.id in partners:
            badge += badges['partner'] + " "
        member = self.bot.get_server("294215057129340938").get_member(user.id)
        if member is not None:
            for role in member.roles:
                if role.name.lower() == "retired":
                    badge += badges['retired'] + " "
        if user.id in blocked_ids:
            badge = ":no_entry_sign:"
        if badge == "":
            badge = "None"
        stp2 = ""
        for role in user.roles:
            if not role == ctx.message.server.default_role:
                if role.name == user.roles[len(user.roles) - 1].name:
                   stp2 = stp2 + role.name
                else:
                    stp2 = stp2 + role.name + ", "
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

    @commands.command(pass_context=True, aliases=["guilds"])
    async def servers(self, ctx): # !!servers
        await self.bot.send_typing(ctx.message.channel)
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        e = discord.Embed(color=color, title="NanoBot Guilds", description="An average guild has...")
        tot = len(self.bot.servers)
        roles = []
        verification = 0
        for s in bot.servers:
            if str(s.verification_level) == "low":
                verification += 1
            elif str(s.verification_level) == "medium":
                verification += 2
            elif str(s.verification_level) == "high":
                verification += 3
            elif str(s.verification_level) == 4:
                verification += 4
            for r in s.roles:
                roles.append(r)
        e.add_field(name="Users", value=sum(1 for _ in self.bot.get_all_members()) / tot)
        e.add_field(name="Channels", value=sum(1 for _ in self.bot.get_all_channels()) / tot)
        e.add_field(name="Emojis", value=sum(1 for _ in self.bot.get_all_emojis()) / tot)
        e.add_field(name="Roles", value=len(roles) / tot)
        e.set_footer(text="{} guilds total".format(tot))
        verification = verification / tot
        verif_name = None
        if round(verification) == 0:
            verif_name = "None"
        elif round(verification) == 1:
            verif_name = "Low"
        elif round(verification) == 2:
            verif_name = "Medium"
        elif round(verification) == 3:
            verif_name = "High / (╯°□°）╯︵ ┻━┻"
        elif round(verification) == 4:
            verif_name = "Extreme / ┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻"
        e.add_field(name="Verification", value="{} ({})".format(verification, verif_name))
        await self.bot.say(embed=e)

    @commands.command(pass_context=True, no_pm=True, aliases=['botinfo', 'stats'])
    async def info(self, ctx): # !!info
        try:
            """Shows bot info."""
            global start_time
            global errors
            global st_servers
            await self.bot.send_typing(ctx.message.channel)
            pyver = ""
            for x in sys.version_info[0:3]:
                if x == sys.version_info[2]:
                    pyver += str(x)
                else:
                    pyver += str(x) + "."
            elapsed_time = time.gmtime(time.time() - start_time)
            log.debug("Got bot uptime")
            stp = str(elapsed_time[7] - 1) + " days, " + str(elapsed_time[3]) + " hours, " + str(elapsed_time[4]) + " minutes"
            log.debug("Formatted bot uptime")
            users = sum(1 for _ in self.bot.get_all_members())
            log.debug("Got all bot users")
            color = discord.Color.default()
            if ctx.message.server is not None:
                color = ctx.message.server.me.color
            embed = discord.Embed(color=color, title="NanoBot Statistics", description="Made by **Der ナノボット#4587**")
            embed.set_footer(text="NanoBot#2520")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name="> Uptime", value=stp)
            embed.add_field(name="> Usage", value="**• Guilds:** {}\n**• Users:** {}".format(len(self.bot.servers), users))
            embed.add_field(name="> Commands", value="**• Total Received:** {}\n**• Errors:** {} ({}%)".format(len(cmds_this_session), len(errors), round(len(errors)/len(cmds_this_session) * 100)))
            embed.add_field(name="> Voice", value="**• Active Sessions:** {}\n**• Songs Played:** {}".format(len(self.bot.voice_clients), len(songs_played)))
            embed.add_field(name="> Version", value="**• NanoBot:** {}\n**• discord.py:** {}\n**• Python:** {}".format(version, discord.__version__, pyver))
            embed.add_field(name="> Misc", value="**• Website:** [Go!](http://bot.nanomotion.xyz)\n**• Discord:** [Join!](https://discord.gg/eDRnXd6)")
            log.debug("Created Embed")
            await self.bot.say(embed=embed)
        except:
            raise

    @commands.command(pass_context=True, no_pm=True, aliases=['server', 'guildinfo', 'serverinfo'])
    async def guild(self, ctx): # !!guild
        global partnered_servers
        global badges
        badge = ""
        if ctx.message.server.id in partnered_servers:
            badge += badges['partner']
        """Shows guild info."""
        await self.bot.send_typing(ctx.message.channel)
        server = ctx.message.server
        owner = server.owner.name + "#" + str(server.owner.discriminator)
        stp2 = ""
        for role in server.roles:
            if role.name == server.roles[len(server.roles) - 1].name:
               stp2 = stp2 + role.name
            else:
                stp2 = stp2 + role.name + ", "
        embed = discord.Embed(color=ctx.message.server.me.color)
        embed.title = "Guild Info"
        embed.set_footer(text="NanoBot#2520")
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Name", value=server.name + " {}".format(badge))
        embed.add_field(name="ID", value=str(server.id))
        embed.add_field(name="Roles", value=stp2)
        embed.add_field(name="Owner", value=owner)
        embed.add_field(name="Members", value=server.member_count)
        embed.add_field(name="Channels", value=len(server.channels))
        embed.add_field(name="Region", value=server.region)
        embed.add_field(name="Custom Emoji", value=len(server.emojis))
        embed.add_field(name="Created At", value=server.created_at)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="staff", pass_context=True)
    async def _staff(self, ctx):
        global staff
        global badges
        global partners
        global admin_ids
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        e = discord.Embed(color=color, title="NanoBot Staff")
        for pid in staff:
            _badge = ""
            user = self.bot.get_server("294215057129340938").get_member(pid)
            if pid in partners:
                _badge += badges['partner']
            _badge += badges['staff']
            e.add_field(name=str(user), value=_badge)
        await self.bot.say(embed=e)

    @commands.command(pass_context=True)
    async def ping(self, ctx): # !!ping
        """Pong!"""
        t = time.time()
        mesg = await self.bot.say("Pong!")
        t2 = time.time() - t
        await self.bot.edit_message(mesg, "Pong! **{}ms**".format(round(t2*1000)))

    @commands.command(aliases=['hi'])
    async def hello(self): # !!hello
        """Hello, world!"""
        await self.bot.say(':wave: Hi, I\'m NanoBot! I can make your Discord server better with all of my features! Type `!!help` for more info, or go to http://bot.nanomotion.xyz')

    @commands.command(pass_context=True)
    async def invite(self, ctx): # !!invite
        await self.bot.say('{}, you can invite me to your server with this link: https://discordapp.com/oauth2/authorize?client_id=294210459144290305&scope=bot&permissions=405924918'.format(ctx.message.author.mention))

    @commands.command(pass_context=True)
    async def logs(self, ctx, limit : int = 100): # !!logs
        await self.bot.send_typing(ctx.message.channel)
        stp = ""
        logs = self.bot.logs_from(ctx.message.channel, limit = limit)
        for msg in logs:
            stp += """
            <div class='message' id='{0.id}'>
            <b>{0.author} at {0.timestamp}</b> ({0.id})<br>
            <p>{1}</p>
            </div><br>
            """.format(msg, msg.clean_content.replace("<", "&lt;").replace(">", "&gt;"))
        await self.bot.say(embed=discord.Embed(description="[Logs for #{0}](https://nanobot-discord.github.io/logs/?channel_name={0}&logs={1}".format(ctx.message.channel.name, stp[:1800])))

def setup(bot):
    bot.add_cog(General(bot))
