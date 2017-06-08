import importlib
import discord
import logging
import asyncio
import traceback
import youtube_dl
import time
import uuid
import sys
import os
from discord.ext import commands
import colorama
import urllib.request
import ast
import timeit

colorama.init(autoreset=True)
class color:
    BLUE = colorama.Fore.WHITE + colorama.Back.BLUE
    YELLOW = colorama.Fore.WHITE + colorama.Back.YELLOW
    RED = colorama.Fore.WHITE + colorama.Back.RED
    GREEN = colorama.Fore.WHITE + colorama.Back.GREEN

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
cmds_this_session = []
admin_ids = ["233325229395410964", "236251438685093889", "294210459144290305", "233366211159785473"]
start_time = "null"
version = "1.2-beta"
_uuid = uuid.uuid1()

class Admin:
    @commands.command(pass_context=True)
    async def eval(self, ctx, *, _eval : str): # !!eval
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":warning: You need to be **NanoBot Owner** to do that.")
        else:
            res = "null"
            err = 0
            embed = discord.Embed()
            try:
                if "exit" in _eval.lower():
                    err = 1
                    res = "PermissionError: Request denied."
                else:
                    res = eval(_eval)
                    logging.info("Evaluated " + str(_eval))
            except Exception as e:
                res = str(e)
                err = 1
            if err == 1:
                embed = discord.Embed(color=0xFF0000)
            else:
                embed = discord.Embed(color=0x00FF00)
            if len(str(res)) > 899:
                res = str(res)[:880] + "\n\n(result trimmed)"
            embed.title = "NanoBot Eval"
            embed.set_footer(text="Code Evaluation")
            '''embed.set_image(url=ctx.message.server.me.avatar_url)'''
            embed.add_field(name=":inbox_tray: Input", value="```py\n" + str(_eval) + "```")
            if err == 1:
                embed.add_field(name=":outbox_tray: Error", value="```py\n" + str(res)[:900] + "```")
            else:
                embed.add_field(name=":outbox_tray: Output", value="```py\n" + str(res)[:900] + "```")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def exec(self, ctx, *, _eval : str): # !!exec
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":warning: You need to be **NanoBot Owner** to do that.")
        else:
            res = "null"
            err = 0
            embed = discord.Embed()
            try:
                if "exit" in _eval.lower():
                    err = 1
                    res = "PermissionError: Request denied."
                else:
                    res = exec(_eval)
                    logging.info("Executed " + str(_eval))
            except Exception as e:
                res = str(e)
                err = 1
            if err == 1:
                embed = discord.Embed(color=0xFF0000)
            else:
                embed = discord.Embed(color=0x00FF00)
            if len(str(res)) > 899:
                res = str(res)[:880] + "\n\n(result trimmed)"
            embed.title = "NanoBot Exec"
            embed.set_footer(text="Code Execution")
            '''embed.set_image(url=ctx.message.server.me.avatar_url)'''
            embed.add_field(name=":inbox_tray: Input", value="```py\n" + str(_eval) + "```")
            if err == 1:
                embed.add_field(name=":outbox_tray: Error", value="```py\n" + str(res)[:900] + "```")
            else:
                embed.add_field(name=":outbox_tray: Output", value="```py\n" + str(res)[:900] + "```")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def setplaying(self, ctx, *, game : str): # !!setplaying
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":warning: You need to be **NanoBot Owner** to do that.")
        else:
            try:
                await self.bot.change_presence(game=discord.Game(name=game))
                logging.info("Set game to " + str(game))
            except Exception as e:
                await self.bot.say(":warning: Failed to set playing: `" + str(e)[:1900] + "`")

    @commands.command(pass_context=True)
    async def reload(self, ctx, *, module : str): # !!reload
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":warning: You need to be **NanoBot Owner** to do that.")
        else:
            try:
                logging.info('Reloading ' + module + '...')
                exec('importlib.reload(' + module + ')')
                await self.bot.say('Reloaded module `' + module + '`')
                logging.info('Successfully reloaded ' + module)
            except Exception as e:
                await self.bot.say(':warning: Failed to reload module: `' + str(e) + '`')
                logging.warn('Failed to reload ' + module)
    
    @commands.command(pass_context=True)
    async def setstatus(self, ctx, *, status : str): # !!setstatus
        if not str(ctx.message.author.id) in admin_ids:
            await self.bot.say(":warning: You need to be **NanoBot Owner** to do that.")
        else:
            try:
                if status == "online":
                    await self.bot.change_presence(status=discord.Status.online)
                    await self.bot.say("Changed status to `online` <:online:313956277808005120>")
                elif status == "idle" or status == "away":
                    await self.bot.change_presence(status=discord.Status.idle)
                    await self.bot.say("Changed status to `idle` <:away:313956277220802560>")
                elif status == "dnd":
                    await self.bot.change_presence(status=discord.Status.dnd)
                    await self.bot.say("Changed status to `dnd` <:dnd:313956276893646850>")
                elif status == "offline" or status == "invisible":
                    await self.bot.change_presence(status=discord.Status.offline)
                    await self.bot.say("Changed status to `offline` <:offline:313956277237710868>")
                elif status == "streaming":
                    await self.bot.change_presence(game=discord.Game(name="Type !!help", type=1))
                    await self.bot.say("Changed status to `streaming` <:streaming:313956277132853248>")
                else:
                    await self.bot.say(":warning: Invalid status `" + status + "`. Possible values:\n```py\n['online', 'idle', 'away', 'dnd', 'offline', 'invisible', 'streaming']```")
                logging.info("Set status to " + str(status))
            except Exception as e:
                await self.bot.say(":warning: Failed to set status: `" + str(e)[:1900] + "`")
