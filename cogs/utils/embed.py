import discord
from discord.ext import commands
import datetime

class Embeds:
    def error(self, error, ctx):
        if type(ctx) == str:
            ctx = ctx
        else:
            ctx = ctx.command
        e = discord.Embed(color=discord.Color.red(), title="Error", description="An unexpected error occurred in the command `{0}`\n\n```py\n{1}```\n\nDon't panic! Our support team can help you at the **[NanoBot Discord](https://discord.gg/eDRnXd6)**.".format(ctx, error))
        e.set_footer(text=str(datetime.datetime.now()))
        return e
    def warning(self, message):
        e = discord.Embed(color=discord.Color.gold())
        e.add_field(name="Warning", value=message)
        return e
    def invalid_syntax(self, message="You entered something wrong."):
        e = discord.Embed()
        e.add_field(name="Invalid Syntax", value=message)
        e.set_footer(text="Commands reference: http://nanomotion.github.io/NanoBot/commands.html")
        return e
    def permission_denied(self, message="You lack the required permissions to execute this command!"):
        e = discord.Embed()
        e.add_field(name="Permission Denied", value=message)
        e.set_footer(text="Permissions reference: http://nanomotion.xyz/NanoBot/permissions.html")
        return e
    def server_join(self, server):
        e = discord.Embed(color=discord.Color.green(), title="Joined Guild")
        if not server.icon_url == "":
            e.set_thumbnail(url=server.icon_url)
        e.add_field(name="Name", value=server.name)
        e.add_field(name="ID", value=server.id)
        usrs = 0
        bots = 0
        for usr in server.members:
            if usr.bot:
                bots += 1
            else:
                usrs += 1
        e.add_field(name="Users", value="{} members / {} bots".format(usrs, bots))
        e.add_field(name="Owner", value=server.owner)
        e.add_field(name="Total Guilds", value=len(self.bot.servers))
        return e
    def server_leave(self, server):
        e = discord.Embed(color=discord.Color.red(), title="Left Guild")
        if not server.icon_url == "":
            e.set_thumbnail(url=server.icon_url)
        e.add_field(name="Name", value=server.name)
        e.add_field(name="ID", value=server.id)
        usrs = 0
        bots = 0
        for usr in server.members:
            if usr.bot:
                bots += 1
            else:
                usrs += 1
        e.add_field(name="Users", value="{} members / {} bots".format(usrs, bots))
        e.add_field(name="Owner", value=server.owner)
        e.add_field(name="Total Guilds", value=len(self.bot.servers))
        return e
    def user_kick(self, author, user, reason, case):
        e = discord.Embed(color=discord.Color.gold(), title="Kick | Case {}".format(case))
        e.add_field(name="User", value="{0} ({0.id})".format(user))
        e.add_field(name="Moderator", value=str(author))
        e.add_field(name="Reason", value=str(reason))
        return e
    def user_ban(self, author, user, reason, case):
        e = discord.Embed(color=discord.Color.red(), title="Ban | Case {}".format(case))
        e.add_field(name="User", value="{0} ({0.id})".format(user))
        e.add_field(name="Moderator", value=str(author))
        e.add_field(name="Reason", value=str(reason))
        return e
