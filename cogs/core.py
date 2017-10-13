#Contains modified and unmodified functions from Red Discord Bot | https://github.com/Twentysix26/Red-DiscordBot
import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import pagify, box
import importlib
import traceback
import logging
import asyncio
import datetime
import time
import os
import aiohttp
import glob

log = logging.getLogger("bot.core")



class CogNotFoundError(Exception):
    pass


class CogLoadError(Exception):
    pass


class NoSetupError(CogLoadError):
    pass


class CogUnloadError(Exception):
    pass


class CoreUnloadError(CogUnloadError):
    pass

#async def post_stats():
#    await bot.change_presence(game=discord.Game(name='!!help • {} Guilds'.format(len(bot.servers))), status=discord.Status.online)
#    payload = {"server_count":int(len(bot.servers))}
#    headers = {"Authorization":str(os.getenv('DBOTSPW_TOKEN'))}
#    r = requests.post("https://bots.discord.pw/api/bots/{}/stats".format(str(bot.user.id)), data=json.dumps(payload, indent=4, separators=(',', ': ')), headers=headers)
#    if not(r.status_code == 200 or r.status_code == 304):
#        logging.error("1/Failed to post server count: " + str(r.status_code))
#        logging.error("The following data was returned by the request:\n{}".format(r.text))
#    headers = {"Authorization":str(os.getenv('DBOTSLIST_TOKEN'))}
#    r = requests.post("https://discordbots.org/api/bots/{}/stats".format(str(bot.user.id)), data=payload, headers=headers)
#    if not(r.status_code == 200 or r.status_code == 304):
#        logging.error("2/Failed to post server count: " + str(r.status_code))
#        logging.error("The following data was returned by the request:\n{}".format(r.text))

class Core:
    """All owner-only commands that relate to debug bot operations."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
		#post_stats()

    def __unload(self):
        self.session.close()
    
    def _load_cog(self, cogname):
        if not self._does_cogfile_exist(cogname):
            raise CogNotFoundError(cogname)
        try:
            mod_obj = importlib.import_module(cogname)
            importlib.reload(mod_obj)
            self.bot.load_extension(mod_obj.__name__)
        except SyntaxError as e:
            raise CogLoadError(*e.args)
        except:
            raise

    def _unload_cog(self, cogname, reloading=False):
        try:
            self.bot.unload_extension(cogname)
        except:
            raise CogUnloadError

    def _list_cogs(self):
        cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
        return ["cogs." + os.path.splitext(f)[0] for f in cogs]

    def _does_cogfile_exist(self, module):
        if "cogs." not in module:
            module = "cogs." + module
        if module not in self._list_cogs():
            return False
        return True

    @commands.command(name="cogs", hidden=True)
    @checks.is_dev()
    async def _cogs(self):
        """Shows loaded/unloaded cogs"""
        loaded = [c.__module__.split(".")[1] for c in self.bot.cogs.values()]
        unloaded = [c.split(".")[1] for c in self._list_cogs()
                    if c.split(".")[1] not in loaded]

        if not unloaded:
            unloaded = ["None"]

        msg = ("+ Active\n"
               "{}\n\n"
               "- Inactive\n"
               "{}"
               "".format(", ".join(sorted(loaded)),
                         ", ".join(sorted(unloaded)))
               )
        for page in pagify(msg, [" "], shorten_by=16):
            await self.bot.say(box(page.lstrip(" "), lang="diff"))

    @commands.command(hidden=True)
    @checks.is_dev()
    async def load(self, *, cog_name: str):
        """Loads a cog"""
        module = cog_name.strip()
        if "cogs." not in module:
            module = "cogs." + module
        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say("That cog could not be found.")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say("There was an issue loading the cog.")
        except Exception as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say('Cog was found and possibly loaded but '
                               'something went wrong.')
        else:
            await self.bot.say("The cog has been loaded.")

    @commands.command(pass_context=True, hidden=True)
    @checks.is_dev()
    async def restart(self, ctx):
        """Restarts Nano"""
        await self.bot.say(":wave: Restarting...")
        await self.bot.change_presence(status=discord.Status.idle)
        log.info("Restarting... (Requester: {})".format(ctx.message.author))
        try:
            log.info("Attempting to log out...")
            await self.bot.logout()
        except:
            log.warn("Logout attempt failed")
        self.bot.loop.close()

    @commands.command(name="reload", hidden=True)
    @checks.is_dev()
    async def _reload(self, *, cog_name: str):
        """Reloads a cog"""
        module = cog_name.strip()
        if "cogs." not in module:
            module = "cogs." + module

        try:
            self._unload_cog(module, reloading=True)
        except:
            pass

        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say("That cog cannot be found.")
        except NoSetupError:
            await self.bot.say("That cog does not have a setup function.")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say("Error. Check console.")
        else:
            await self.bot.say("The cog has been reloaded.")

    @commands.command(pass_context=True, hidden=True)
    async def ping(self,ctx):
        """Returns ping time(ms)"""
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await self.bot.send_typing(channel)
        t2 = time.perf_counter()
        await self.bot.say("Pong! **{}ms**".format(round((t2-t1)*1000)))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_dev()
    async def exec(self, ctx, *, code):
        """Executes python code"""
        def check(m):
            if m.content.strip().lower() == "more":
                return True
        
        if ("exit" in code.lower() or "token" in code.lower()):
            await self.bot.say("Access Denied")
            
        else:

            author = ctx.message.author
            channel = ctx.message.channel

            code = code.strip('` ')
            result = None

            global_vars = globals().copy()
            global_vars['bot'] = self.bot
            global_vars['ctx'] = ctx
            global_vars['message'] = ctx.message
            global_vars['author'] = ctx.message.author
            global_vars['channel'] = ctx.message.channel
            global_vars['server'] = ctx.message.server

            try:
                result = eval(code, global_vars, locals())
            except Exception as e:
                await self.bot.say(box('{}: {}'.format(type(e).__name__, str(e)),
                                       lang="py"))
                return

            if asyncio.iscoroutine(result):
                result = await result

            result = str(result)
            result = list(pagify(result, shorten_by=16))
            for i, page in enumerate(result):
                if i != 0 and i % 4 == 0:
                    last = await self.bot.say("There are still {} messages. "
                                              "Type `more` to continue."
                                              "".format(len(result) - (i+1)))
                    msg = await self.bot.wait_for_message(author=author,
                                                          channel=channel,
                                                          check=check,
                                                          timeout=10)
                    if msg is None:
                        try:
                            await self.bot.delete_message(last)
                        except:
                            pass
                        finally:
                            break
                await self.bot.say(box(page, lang="py"))

def setup(bot):
    n = Core(bot)
    bot.add_cog(n)
