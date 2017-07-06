import discord
import logging
import asyncio
import traceback
import time
import uuid
import sys
import os
from discord.ext import commands

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

client = discord.Client()

@client.event
async def on_server_join(server): # When the bot joins a server
    logging.info("Joined server " + str(server.id)+ " (" + str(server.name) + ")")
    await client.send_message(server.default_channel, ':wave: Hi, I\'m NanoBot! Thanks for adding me to your server. I\'m in maintenance mode right now, so I won\'t be able to help you with anything.')
    await client.send_message(server.default_channel, 'Need help? Join the NanoBot Discord server at https://discord.gg/eDRnXd6')

@client.event
async def on_server_leave(server): # When the bot leaves a server
    logging.info("Left server " + str(server.id) + " (" + str(server.name) + ")")

@client.event
async def on_member_join(member): # When a member joins a server
    if str(member.server.id) == "294215057129340938":
        await client.send_message(member.server.get_channel("314136139755945984"), ":wave: Welcome " + str(member.mention) + " to the server!")

@client.event
async def on_error(event, *args, **kwargs): # When an error occurrs
    global exc_msg
    try:
        await client.send_message(discord.User(id="236251438685093889"), ":warning: An error occurred in `" + str(event) + "`: ```python" + traceback.format_exc() + "```")
    except Exception as e:
        logging.warn("Failed to create direct message: " + str(e))

@client.event
async def on_message(message): # When a message is sent
    if message.content.startswith('!!'):
        logging.info(message.author.name + " entered command " + message.content)
    if message.content.lower() == "!!shutdown"and message.author.id == "236251438685093889": # !!shutdown
        await client.send_message(message.channel, ":wave: Shutting down...")
        await client.change_presence(status=discord.Status.offline)
        sys.exit(0)
    elif message.content.startswith('!!') and not message.content.startswith('!!!'):
        await client.send_message(message.channel, ":tools: I'm in maintenance mode right now!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.dnd, game=discord.Game(name='Maintenance'))

client.run(os.getenv('NANOBOT_TOKEN'))
