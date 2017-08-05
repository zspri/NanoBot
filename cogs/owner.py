from discord.ext import commands
import discord
import ast
import requests

class Owner:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    async def config(self):
        pass

    @config.command(pass_context=True, name="reload")
    async def _reload(self, ctx):
        global admin_ids
        if ctx.message.author.id in admin_ids:
            global partners
            global partnered_servers
            global blocked_ids
            global staff
            os.chdir('data')
            partners = []
            partnered_servers = []
            admin_ids = []
            blocked_ids = []
            staff = []
            with open('partners.txt') as f:
                for line in f:
                    partners.append(line.rstrip('\n'))
                f.close()
            with open('partnered_servers.txt') as f:
                for line in f:
                    partnered_servers.append(line.rstrip('\n'))
                f.close()
            with open('admins.txt') as f:
                for line in f:
                    admin_ids.append(line.rstrip('\n'))
                f.close()
            with open('staff.txt') as f:
                for line in f:
                    staff.append(line.rstrip('\n'))
                f.close()
            with open('blocked.txt') as f:
                for line in f:
                    blocked_ids.append(line.rstrip('\n'))
                f.close()
            os.chdir('..')
            await self.bot.say(":ok_hand:")

    @config.command(name="list")
    async def _list(self):
        path = os.path.join(os.getcwd(), "data")
        for f in os.listdir(path):
            f2 = open(os.path.join(path, f), 'r')
            e = discord.Embed(title=str(f), description="```{}\n{}\n```".format(os.path.splitext(f)[1].replace('.',''), f2.read()[:2030]))
            e.set_footer(text=str(path))
            await self.bot.say(embed=e)
            f2.close()

    @commands.command(pass_context=True, hidden=True)
    async def announce(self, ctx, *, mesg):
        if ctx.message.author.id in admin_ids:
            tmp = await self.bot.say("Are you sure you want to send this message to all of NanoBot's servers?")
            await self.bot.add_reaction(tmp, "👍")
            await self.bot.add_reaction(tmp, "👎")
            tmp = await self.bot.wait_for_reaction(emoji=["👍"], user=ctx.message.author, timeout=10, message=tmp)
            if tmp is None or tmp == None:
                await self.bot.edit_message()
            else:
                tmp = self.bot.say("Sending message to `{}`servers...".format(len(self.bot.servers)))
                e = discord.Embed(title="Announcement", description=str(mesg))
                e.set_footer(text="NanoBot#2520")
                err = 0
                for s in self.bot.servers:
                    try:
                        await self.bot.send_message(s.default_channel, embed=e)
                    except discord.Forbidden:
                        pass
                    except Exception as e:
                        err += 1
                        logging.error(str(e))
                if err > 1:
                    await self.bot.edit_message(tmp, ":warning: Failed to send message to `{}` servers. Check console for more info.".format(err))
                else:
                    await self.bot.edit_message(tmp, ":ok_hand:")

    @commands.command(pass_context=True, hidden=True)
    async def embed(self, ctx, ecolor : str, *, content : str):
        if ctx.message.author.id in admin_ids:
            await self.bot.send_typing(ctx.message.channel)
            color = discord.Color.default()
            if ecolor.lower() == "red":
                color = discord.Color.red()
            elif ecolor.lower() == "green":
                color = discord.Color.green()
            elif e.color.lower() == "yellow":
                color = discord.Color.gold()
            e = discord.Embed(color=color)
            e.description = content
            await self.bot.say(embed=e)

    @commands.command(pass_context=True, hidden=True)
    async def say(self, ctx, *, mesg : str):
        if str(ctx.message.author.id) in admin_ids:
            await self.bot.say(mesg)
            await self.bot.delete_message(ctx.message)

    @commands.group(pass_context=True)
    async def request(self, ctx):
        pass

    @request.command(pass_context=True)
    async def get(self, ctx, url : str, headers = None):
        await self.bot.send_typing(ctx.message.channel)
        if headers is not None:
            headers = dict([headers.strip('{}').split(":"),])
        t = time.time()
        r = requests.get(url, headers=headers)
        et = (time.time() - t) * 1000
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        e = discord.Embed(color=color, title="Request", description="Finished in {}ms with HTTP code {}".format(et, r.status_code))
        e.add_field(name="Return data", value="```html\n{}\n```".format(r.text[:1015]))
        e.set_footer(text=url)
        await self.bot.say(embed=e)

    @commands.command(pass_context=True, hidden=True)
    async def eval(self, ctx, *, _eval : str): # !!eval
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(embed=embeds.permission_denied("You must be a bot admin to do this!"))
        else:
            res = "null"
            err = 0
            embed = discord.Embed()
            try:
                if "token" in _eval.lower() and not(ctx.message.author.id == "236251438685093889"):
                    err = 1
                    res = "PermissionError: Request denied."
                else:
                    res = eval(_eval)
                    logging.info("Evaluated " + str(_eval))
            except Exception as e:
                res = "{}: {}".format(str(type(e).__name__), str(e))
                err = 1
            if err == 1:
                embed = discord.Embed(color=discord.Color.red())
            else:
                embed = discord.Embed(color=discord.Color.green())
            if len(str(res)) > 899:
                res = str(res)[:880] + "\n\n(result trimmed)"
            embed.title = "NanoBot Eval"
            embed.set_footer(text="Code Evaluation")
            embed.add_field(name=":inbox_tray: Input", value="```py\n" + str(_eval) + "```")
            if err == 1:
                embed.add_field(name=":outbox_tray: Error", value="```py\n" + str(res)[:900] + "```")
            else:
                embed.add_field(name=":outbox_tray: Output", value="```py\n" + str(res)[:900] + "```")
            await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, hidden=True)
    async def exec(self, ctx, *, _eval : str): # !!exec
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(embed=embeds.permission_denied("You must be a bot admin to do this!"))
        else:
            res = "null"
            err = 0
            embed = discord.Embed()
            try:
                if ("exit" in _eval.lower() or "token" in _eval.lower()) and not(ctx.message.author.id == "236251438685093889"):
                    err = 1
                    res = "PermissionError: Request denied."
                else:
                    res = exec(_eval)
                    logging.info("Executed " + str(_eval))
            except Exception as e:
                res = "{}: {}".format(str(type(e).__name__), str(e))
                err = 1
            if err == 1:
                embed = discord.Embed(color=discord.Color.red())
            else:
                embed = discord.Embed(color=discord.Color.green())
            if len(str(res)) > 899:
                res = str(res)[:880] + "\n\n(result trimmed)"
            embed.title = "NanoBot Exec"
            embed.set_footer(text="Code Execution")
            embed.add_field(name=":inbox_tray: Input", value="```py\n" + str(_eval) + "```")
            if err == 1:
                embed.add_field(name=":outbox_tray: Error", value="```py\n" + str(res)[:900] + "```")
            else:
                embed.add_field(name=":outbox_tray: Output", value="```py\n" + str(res)[:900] + "```")
            await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, hidden=True)
    async def setplaying(self, ctx, *, game : str): # !!setplaying
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(embed=embeds.permission_denied("You must be a bot admin to do this!"))
        else:
            try:
                await self.bot.change_presence(game=discord.Game(name=game), status=ctx.message.server.me.status)
                logging.info("Set game to " + str(game))
            except Exception as e:
                await self.bot.say(embed=embeds.error("Failed to set game: {}".format(str(e)), ctx))

    @commands.command(pass_context=True, hidden=True)
    async def reload(self, ctx, *, module : str): # !!reload
        global errors
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(embed=embeds.permission_denied("You must be a bot admin to do this!"))
        else:
            try:
                logging.info('Reloading ' + module + '...')
                exec('importlib.reload(' + module + ')')
                await self.bot.say('Reloaded module `' + module + '`')
                logging.info('Successfully reloaded ' + module)
            except Exception as e:
                await self.bot.say(embed=embeds.error(str(e), ctx))
                logging.warn('Failed to reload ' + module)

    @commands.command(pass_context=True, hidden=True)
    async def setstatus(self, ctx, *, status : str): # !!setstatus
        global errors
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(embed=embeds.permission_denied("You must be a bot admin to do this!"))
        else:
            try:
                if status == "online":
                    await self.bot.change_presence(game=ctx.message.server.me.game, status=discord.Status.online)
                    await self.bot.say("Changed status to `online` <:online:313956277808005120>")
                elif status == "idle" or status == "away":
                    await self.bot.change_presence(game=ctx.message.server.me.game, status=discord.Status.idle)
                    await self.bot.say("Changed status to `idle` <:away:313956277220802560>")
                elif status == "dnd":
                    await self.bot.change_presence(game=ctx.message.server.me.game, status=discord.Status.dnd)
                    await self.bot.say("Changed status to `dnd` <:dnd:313956276893646850>")
                elif status == "offline" or status == "invisible":
                    await self.bot.change_presence(game=ctx.message.server.me.game, status=discord.Status.offline)
                    await self.bot.say("Changed status to `offline` <:offline:313956277237710868>")
                else:
                    await self.bot.say(":warning: Invalid status `" + status + "`. Possible values:\n```py\n['online', 'idle', 'away', 'dnd', 'offline', 'invisible']```")
                logging.info("Set status to " + str(status))
            except Exception as e:
                await self.bot.say(embed=embeds.error(str(e), ctx))

    @commands.command(pass_context=True, hidden=True)
    async def shutdown(self, ctx): # !!shutdown
        if str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":wave: Shutting down...")
            await self.bot.change_presence(status=discord.Status.offline)
            logging.warn("Shutting down... (Requester: {})".format(ctx.message.author))
            try:
                logging.info("Attempting to log out...")
                await self.bot.logout()
            except:
                logging.warn("Logout attempt failed")
            self.bot.loop.close()

    @commands.command(pass_context=True, hidden=True)
    async def restart(self, ctx): # !!restart
        if str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":wave: Restarting...")
            await self.bot.change_presence(status=discord.Status.idle)
            logging.warn("Restarting... (Requester: {})".format(ctx.message.author))
            os.system('start restart.bat')
            try:
                logging.info("Attempting to log out...")
                await self.bot.logout()
            except:
                logging.warn("Logout attempt failed")
            self.bot.loop.close()

def setup(bot):
    bot.add_cog(Owner(bot))
