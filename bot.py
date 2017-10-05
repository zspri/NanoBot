#Nanobot 2.0 | format based upon Red for modularity | https://github.com/Twentysix26/Red-DiscordBot
from discord.ext import commands
from optparse import OptionParser
import asyncio
import datetime
import discord
import logging
import logging.handlers
import os
import sys
import traceback
from cogs.utils.dataIO import dataIO
from cogs.utils.settings import Settings
from cogs.utils.embed import Embeds

clist = ['cogs.core', 'cogs.dev', 'cogs.audio', 'cogs.general', 'cogs.overwatch']
errors = []

class Bot(commands.Bot):
	def __init__(self, *args, **kwargs):
		
		def prefix_mgr(bot, message):
			return bot.settings.get_prefixes(message.server)
			
		self.settings = Settings()
		self.uptime = datetime.datetime.utcnow()
		self.logger = logger_config(self)
		self.embeds = Embeds()
		super().__init__(*args, command_prefix=prefix_mgr, **kwargs)

def initialize(bot_class=Bot):
	bot = bot_class(description="A music, fun, moderation, and Overwatch bot for Discord.")
	
	import __main__
	__main__.settings = bot.settings
	
	for extension in clist:
		try:
			check_folders()
			bot.load_extension(extension)
			print("Loaded {}".format(str(extension)))
		except Exception as e:
			print("{}: {}".format(type(e).__name__, e))
	
	@bot.event
	async def on_message(message):
		if (message.content.startswith('`') and not message.content.startswith('``')) or message.content.startswith('beta '):
			bot.logger.info(message.content)
			ccmds = None
			if message.content == "`" or message.content == "beta ":
				await bot.send_message(message.channel, ":thinking: Why did you even think that would work? Type `!!help` for help.")
			else:
				await bot.process_commands(message)
	
	@bot.event
	async def on_server_join(server):
		logging.info("Joined server {0.name} (ID: {0.id})".format(server))
		try:
			await bot.send_message(server.default_channel, ':wave: Hi, I\'m NanoBot! For help on what I can do, type `!!help`. Join the NanoBot Discord for support and updates: https://discord.io/nano-bot')
		except:
			pass
		await bot.send_message(bot.get_channel(id="334385091482484736"), embed=bot.embeds.server_join(server))

	@bot.event
	async def on_server_remove(server):
		logging.info("Left server {0.name} (ID: {0.id})".format(server))
		await bot.send_message(bot.get_channel(id="334385091482484736"), embed=bot.embeds.server_leave(server))

	@bot.event
	async def on_member_join(member):
		if str(member.server.id) == "294215057129340938":
			await bot.send_message(member.server.get_channel("314136139755945984"), ":wave: Welcome " + str(member.mention) + " to the server!")

	@bot.event
	async def on_member_ban(member):
		pass
	
	@bot.event
	async def on_command_error(error, ctx):
		global errors
		if isinstance(error, discord.ext.commands.errors.CommandNotFound):
			pass
		elif isinstance(error, discord.ext.commands.errors.CheckFailure):
			if str(ctx.command).startswith("cmd"):
				await bot.send_message(ctx.message.channel, embed=bot.embeds.permission_denied("You lack the required permissions to execute this command"))
			else:
				await bot.send_message(ctx.message.channel, embed=bot.embeds.permission_denied())
		elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
			await bot.send_message(ctx.message.channel, embed=bot.embeds.invalid_syntax("You're missing required arguments! Type `!!help {}` for more help.".format(ctx.command)))
		elif isinstance(error, TimeoutError):
			pass
		elif isinstance(error, discord.ext.commands.DisabledCommand):
			await bot.send_message(ctx.message.channel, ":tools: This command is disabled!")
		elif isinstance(error, discord.errors.Forbidden) or isinstance(error, discord.Forbidden):
			pass
		elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
			await bot.send_message(ctx.message.channel, embed=bot.embeds.error("This command can't be used in private messages.", ctx))
		else:
			if ctx.command:
				errors.append(error)
				_type, _value, _traceback = sys.exc_info()
				bot.logger.error(error.original)
				if _traceback is not None:
					bot.logger.error(_traceback)
				await bot.send_message(ctx.message.channel, embed=bot.embeds.error(error, ctx))
	
	@bot.event
	async def on_ready():
		print("Bot Initialized...")
		print("Logged in as " + bot.user.name + " with ID " + bot.user.id)
		await bot.change_presence(game=discord.Game(name="Nanobot v2.0 Beta"))
		
	return bot
	
def check_folders():
    folders = ("data", "data/bot", "cogs", "cogs/utils")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder(s)...")
            os.makedirs(folder)
	
def logger_config(bot):
	logger = logging.getLogger("bot")
	logger.setLevel(logging.INFO)
	log_format = logging.Formatter(
		'%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
		'%(message)s', datefmt='[%I:%M:%S %p]')	
	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setFormatter(log_format)
	stdout_handler.setLevel(logging.INFO)
	logger.setLevel(logging.INFO)
	file_handler = logging.handlers.RotatingFileHandler(
		filename='data/bot/bot.log', encoding='utf-8', mode='a', maxBytes=10**8, backupCount=5)
	file_handler.setFormatter(log_format)
	logger.addHandler(file_handler)
	logger.addHandler(stdout_handler)
	api_logger = logging.getLogger("discord")
	api_logger.setLevel(logging.WARNING)
	api_handler = logging.FileHandler(
		filename='data/bot/discord.log', encoding='utf-8', mode='a')
	api_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
		'%(message)s', datefmt='[%I:%M:%S %p]'))
	api_logger.addHandler(api_handler)
	
	return logger
	
def main(bot):
	check_folders()
	bot.run(bot.settings.token)
	
if __name__ == "__main__":
	bot = initialize()
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(main(bot))
	except discord.LoginFailure:
		bot.logger.error(traceback.format_exc())
	except KeyboardInterrupt:
		loop.run_until_complete(bot.logout())
	except Exception as e:
		bot.logger.exception("Fatal Exception", exc_info=e)
		loop.run_until_complete(bot.logout())
	finally:
		loop.close()
		exit(0)