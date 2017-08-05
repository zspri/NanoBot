from discord.ext import commands
import discord

class Admin:

    def __init__(self, bot):
        self.bot = bot

    def isadmin(ctx):
        passed = False
        for role in ctx.message.author.roles:
            if role.name.lower() == "nanobot admin" or role.name.lower() == "administrator" or role.name.lower() == "admin" or role.name.lower() == "discord admin":
                passed = True
        return passed

    def updatecmds(self, data):
        os.chdir('data')
        try:
            with open('cmds.json', 'w') as f:
                f.write(json.dumps(data))
                f.close()
        except Exception as e:
            logging.error("Failed to write new data for custom commands: {}".format(str(e)))
        os.chdir('..')

    @commands.group(pass_context=True, no_pm=True)
    @commands.check(isadmin)
    async def cmd(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type `!!cmd help` for proper usage.")

    @cmd.command(no_pm=True, name="help")
    @commands.check(isadmin)
    async def _help(self):
        e = discord.Embed(color=ctx.message.server.me.color, title="Custom Commands")
        e.add_field(name="!!cmd help", value="Shows this message.")
        e.add_field(name="!!cmd add <name> <value>", value="Creates a custom command named `<name>` with the value `<value>`.")
        e.add_field(name="!!cmd edit <name> <new_value>", value="Changes the `<name>` custom command's value to be `<new_value>`. *(Command must already exist!)*")
        e.add_field(name="!!cmd del <name>", value="Deletes the custom value for the `<name>` command.")
        e.set_footer(text="Custom Commands Help")
        await self.bot.say(embed=e)

    @cmd.command(pass_context=True, no_pm=True)
    @commands.check(isadmin)
    async def add(self, ctx, name : str, *, value : str):
        global custom_cmds
        if name == "help" or name == "info":
            await self.bot.say(":no_entry_sign: You cannot overwrite that command.")
        else:
            try:
                custom_cmds[ctx.message.server.id][name] = value
            except KeyError:
                custom_cmds[ctx.message.server.id] = {}
                custom_cmds[ctx.message.server.id][name] = value
            self.updatecmds(custom_cmds)
            await self.bot.say(":ok_hand: Created a custom command named `{}` with the value `{}`".format(name, value))

    @cmd.command(pass_context=True, no_pm=True)
    @commands.check(isadmin)
    async def edit(self, ctx, name : str, *, value : str):
        global custom_cmds
        try:
            if custom_cmds[ctx.message.server.id][name] is not None:
                custom_cmds[ctx.message.server.id][name] = value
        except KeyError:
            await self.bot.say(":no_entry_sign: That custom command doesn't exist.")
        else:
            self.updatecmds(custom_cmds)
            await self.bot.say(":ok_hand: Edited the custom value for the `{}` command to be `{}`".format(name, value))

    @cmd.command(pass_context=True, no_pm=True, name="del")
    @commands.check(isadmin)
    async def _del(self, ctx, name : str):
        global custom_cmds
        try:
            if custom_cmds[ctx.message.server.id][name] is not None:
                del custom_cmds[ctx.message.server.id][name]
        except KeyError:
            await self.bot.say(":no_entry_sign: That custom command doesn't exist.")
        else:
            self.updatecmds(custom_cmds)
            await self.bot.say(":ok_hand: Deleted the custom value for the `{}` command".format(name))

def setup(bot):
    bot.add_cog(Admin(bot))
