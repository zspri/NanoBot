# NanoBot Rewrite
# Version 1.0.0-alpha
# Copyright (C) Nanomotion 2017

from discord.ext import commands
import discord
import asyncio
import os
import logging, traceback
import requests

log = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

os.chdir('data')

partners = []
partnered_servers = []
admin_ids = []
blocked_ids = []
staff = []
custom_cmds = {}
badges = {'partner':'<:partner:335963561106866178>',
'staff':'<:staff:314068430787706880>',
'voter':'<:voter:340903213035290627>',
'retired':'<:retired:343110154834935809>',
'bronze':'<:ow_bronze:338113846432628736>',
'silver':'<:ow_silver:338113846734618624>',
'gold':'<:ow_gold:338113846533292042>',
'platinum':'<:ow_platinum:338113846550200331>',
'diamond':'<:ow_diamond:338113846172450818>',
'master':'<:ow_master:338113846377971719>',
'grandmaster':'<:ow_grandmaster:338113846503931905>'}
cmds_this_session = []
songs_played = []
kicks = []
bans = []
version = "1.7-beta"
build = "17095"
_uuid = uuid.uuid1()
queue = {}
disabled_cmds = {} # Format: {'command_name', 'reason'}
errors = []
DEVELOPER_KEY = str(os.getenv('GAPI_TOKEN'))
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
owapi = overwatchpy.OWAPI()

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
with open('cmds.json', 'r') as f:
    try:
        custom_cmds = json.loads(str(f.read()))
    except Exception as e:
        logging.warn("Failed to retrieve JSON data from custom commands: {}".format(str(e)))
    f.close()

os.chdir('..')

class embeds:
    def error(error, ctx):
        if type(ctx) == str:
            ctx = ctx
        else:
            ctx = ctx.command
        e = discord.Embed(color=discord.Color.red(), title="Error", description="An unexpected error occurred in the command `{0}`\n\n```py\n{1}```\n\nDon't panic! Our support team can help you at the **[NanoBot Discord](https://discord.gg/eDRnXd6)**.".format(ctx, error))
        e.set_footer(text=str(datetime.datetime.now()))
        return e
    def warning(message):
        e = discord.Embed(color=discord.Color.gold())
        e.add_field(name="Warning", value=message)
        return e
    def invalid_syntax(message="You entered something wrong."):
        e = discord.Embed()
        e.add_field(name="Invalid Syntax", value=message)
        e.set_footer(text="Commands reference: http://nanomotion.xyz/NanoBot/commands.html")
        return e
    def permission_denied(message="You need a role named `Moderator` to do that."):
        e = discord.Embed()
        e.add_field(name="Permission Denied", value=message)
        e.set_footer(text="Permissions reference: http://nanomotion.xyz/NanoBot/permissions.html")
        return e
    def server_join(server):
        e = discord.Embed(color=discord.Color.green())
        if server.icon_url == "":
            e.set_author(name="Joined Guild")
        else:
            e.set_author(name="Joined Guild", icon_url=server.icon_url)
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
        return e
    def server_leave(server):
        e = discord.Embed(color=discord.Color.red())
        if server.icon_url == "":
            e.set_author(name="Left Guild")
        else:
            e.set_author(name="Left Guild", icon_url=server.icon_url)
        e.add_field(name="Name", value=server.name)
        e.add_field(name="ID", value=server.id)
        e.add_field(name="Joined", value=server.me.joined_at)
        usrs = 0
        bots = 0
        for usr in server.members:
            if usr.bot:
                bots += 1
            else:
                usrs += 1
        e.add_field(name="Users", value="{} members / {} bots".format(usrs, bots))
        e.add_field(name="Owner", value=server.owner)
        return e
    def user_kick(author, user, reason, case):
        e = discord.Embed(color=discord.Color.gold(), title="Kick | Case {}".format(case))
        e.add_field(name="User", value="{0} ({0.id})".format(user))
        e.add_field(name="Moderator", value=str(author))
        e.add_field(name="Reason", value=str(reason))
        return e
    def user_ban(author, user, reason, case):
        e = discord.Embed(color=discord.Color.red(), title="Ban | Case {}".format(case))
        e.add_field(name="User", value="{0} ({0.id})".format(user))
        e.add_field(name="Moderator", value=str(author))
        e.add_field(name="Reason", value=str(reason))
        return e

class config:
    prefix = ['!!', 'nano ']
    client_id = "294210459144290305"

async def post_stats():
    await bot.change_presence(game=discord.Game(name='!!help • {} Guilds'.format(len(bot.servers))))
    payload = {"server_count":int(len(bot.servers))}
    headers = {"Authorization":str(os.getenv('DBOTSPW_TOKEN'))}
    r = requests.post("https://bots.discord.pw/api/bots/{}/stats".format(str(bot.user.id)), data=json.dumps(payload, indent=4, separators=(',', ': ')), headers=headers)
    if not(r.status_code == 200 or r.status_code == 304):
        logging.error("1/Failed to post server count: " + str(r.status_code))
        logging.error("The following data was returned by the request:\n{}".format(r.text))
    headers = {"Authorization":str(os.getenv('DBOTSLIST_TOKEN'))}
    r = requests.post("https://discordbots.org/api/bots/{}/stats".format(str(bot.user.id)), data=payload, headers=headers)
    if not(r.status_code == 200 or r.status_code == 304):
        logging.error("2/Failed to post server count: " + str(r.status_code))
        logging.error("The following data was returned by the request:\n{}".format(r.text))

cogs = [
    'cogs.general',
    'cogs.fun',
    'cogs.moderation',
    'cogs.admin',
    'cogs.owner',
    'cogs.status',
    'cogs.overwatch'
]

bot = commands.Bot(command_prefix=['!!', 'nano '], description='A music, fun, moderation, and Overwatch bot for Discord.')

#####################################
# Bot Events                        #
#####################################

@bot.event
async def on_server_join(server): # When the bot joins a server
    print(color.GREEN + "Joined server " + str(server.id)+ " (" + str(server.name) + ")")
    logging.info("Joined server {0.name} (ID: {0.id})".format(server))
    await post_stats()
    try:
        await bot.send_message(server.default_channel, ':wave: Hi, I\'m NanoBot! For help on what I can do, type `!!help`. Join the NanoBot Discord for support and updates: https://discord.io/nano-bot')
    except:
        pass
    await bot.send_message(bot.get_channel(id="334385091482484736"), embed=embeds.server_join(server))

@bot.event
async def on_server_remove(server): # When the bot leaves a server
    print(color.RED + "Left server " + str(server.id) + " (" + str(server.name) + ")")
    logging.info("Left server {0.name} (ID: {0.id})".format(server))
    await post_stats()
    await bot.send_message(bot.get_channel(id="334385091482484736"), embed=embeds.server_leave(server))

@bot.event
async def on_member_join(member): # When a member joins a server
    if str(member.server.id) == "294215057129340938" and not args.use_beta_token:
        await bot.send_message(member.server.get_channel("314136139755945984"), ":wave: Welcome " + str(member.mention) + " to the server!")

@bot.event
async def on_member_ban(member): # When a member is banned from a server
    pass

@bot.event
async def on_command_error(error, ctx): # When a command error occurrs
    global errors
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass
    elif isinstance(error, discord.ext.commands.errors.CheckFailure):
        if str(ctx.command).startswith("cmd"):
            await bot.send_message(ctx.message.channel, embed=embeds.permission_denied("You need a role named `Admin` to do that."))
        else:
            await bot.send_message(ctx.message.channel, embed=embeds.permission_denied())
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, embed=embeds.invalid_syntax("You're missing required arguments! Type `!!help {}` for more help.".format(ctx.command)))
    elif isinstance(error, TimeoutError):
        pass
    elif isinstance(error, discord.ext.commands.DisabledCommand):
        await bot.send_message(ctx.message.channel, ":tools: This command is disabled!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        if ctx.command.name == "status":
            await bot.send_message(ctx.message.channel, embed=embeds.invalid_syntax("That isn't a valid subcommand. Try typing '!!status help' for help."))
        else:
            await bot.send_message(ctx.message.channel, embed=embeds.invalid_syntax("Invalid argument!"))
    elif isinstance(error, discord.errors.Forbidden) or isinstance(error, discord.Forbidden):
        pass
    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        await bot.send_message(ctx.message.channel, embed=embeds.error("This command can't be used in private messages.", ctx))
    else:
        if ctx.command:
            errors.append(error)
            _type, _value, _traceback = sys.exc_info()
            logging.error(error.original)
            if _traceback is not None:
                logging.error(_traceback)
            await bot.send_message(ctx.message.channel, embed=embeds.error(error, ctx))

@bot.event
async def on_message(message): # When a message is sent
    global cmds_this_session
    global custom_cmds
    global blocked_ids
    if (message.content.startswith('!!') and not message.content.startswith('!!!')) or message.content.startswith('nano'):
        if message.author.id in blocked_ids:
            await bot.send_message(message.channel, ":no_entry_sign: You have been banned from using NanoBot.")
        else:
            logger = logging.getLogger("{} ({})".format(str(message.author.id), str(message.author)))
            logger.info(message.content)
            cmds_this_session.append(objects.Command(message.content.split()[0], message.content))
            ccmds = None
            try:
                ccmds = custom_cmds[message.server.id]
            except:
                pass
            else:
                for c in ccmds.keys():
                    if message.content == "!!" + c or message.content == "nano " + c:
                        await bot.send_message(message.channel, ccmds[c])
            if message.content == "!!" or message.content == "nano":
                await bot.send_message(message.channel, ":thinking: Why did you even think that would work? Type `!!help` for help.")
            elif message.content == "!!help" or message.content == "nano help":
                color = discord.Color.default()
                extra = ""
                if message.server is not None:
                    color = message.server.me.color
                if str(message.channel).startswith("Direct Message with "):
                    extra += " Please note that some commands can't be used in Direct Messages."
                e = discord.Embed(title="NanoBot Help", description="For more help, type `!!help <command>` or `!!help <category>`.\nNeed even more help? Our support team can help you at the ***[NanoBot Discord](https://discord.gg/eDRnXd6)***.", color=color)
                e.add_field(name="> General", value="`!!help`, `!!hello`, `!!invite`, `!!info`, `!!user`, `!!guild`, `!!guilds`, `!!ping`")
                e.add_field(name="> Fun", value="`!!cat`, `!!dog`                                                                              ​")
                e.add_field(name="> Moderation", value="`!!prune`, `!!ban`, `!!kick`                                                                 ​")
                e.add_field(name="> Admin", value="`!!cmd add`, `!!cmd edit`, `!!cmd del`")
                e.add_field(name="> Music", value="`!!join`, `!!summon`, `!!play`, `!!yt`, `!!queue`, `!!volume`, `!!pause`, `!!resume`, `!!stop`, `!!skip`, `!!playing`")
                e.add_field(name="> Overwatch", value="`!!ow profile`, `!!ow hero`, `!!ow map`, `!!ow event`")
                e.set_footer(icon_url=message.author.avatar_url, text="Requested by {}{}".format(str(message.author), extra))
                e.set_thumbnail(url=bot.user.avatar_url)
                #f = open('help.txt', 'r')
                #await bot.send_message(message.channel, f.read())
                #f.close()
                await bot.send_message(message.channel, embed=e)
            else:
                await bot.process_commands(message)

@bot.event
async def on_ready():
    logging.info("Logged in as {0.name}#{0.discriminator}".format(bot.user))
    bot.partners = partners
    bot.partnered_servers = partnered_servers
    bot.admin_ids = admin_ids
    bot.blocked_ids = blocked_ids
    bot.staff = staff
    bot.custom_cmds = custom_cmds
    bot.badges = badges
    bot.cmds_this_session = []
    bot.songs_played = []
    bot.version = "1.0.0-alpha"
    bot.build = "100001"
    bot.queue = {}
    bot.errors = []
    bot.DEVELOPER_KEY = str(os.getenv('GAPI_TOKEN'))
    bot.YOUTUBE_API_SERVICE_NAME = "youtube"
    bot.YOUTUBE_API_VERSION = "v3"
    bot.owapi = overwatchpy.OWAPI()

    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            log.fatal("Failed to load cog {cog}!")
            log.fatal(traceback.format_exc())
        else:
            log.info("Successfully loaded cog {cog}")
    await post_stats()

@bot.command(hidden=True)
@checks.is_owner()
async def load(*, module : str):
    """Loads a module."""
    module = module.strip()
    try:
        bot.load_extension(module)
    except Exception as e:
        await bot.say('\U0001f52b')
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        await bot.say('\U0001f44c')

@bot.command(hidden=True)
@checks.is_owner()
async def unload(*, module : str):
    """Unloads a module."""
    module = module.strip()
    try:
        bot.unload_extension(module)
    except Exception as e:
        await bot.say('\U0001f52b')
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        await bot.say('\U0001f44c')

@bot.command(hidden=True)
@checks.is_owner()
async def announcement(*, message : str):
    # we copy the list over so it doesn't change while we're iterating over it
    servers = list(bot.servers)
    for server in servers:
        try:
            await bot.send_message(server, message)
        except discord.Forbidden:
            # we can't send a message for some reason in this
            # channel, so try to look for another one.
            me = server.me
            def predicate(ch):
                text = ch.type == discord.ChannelType.text
                return text and ch.permissions_for(me).send_messages

            channel = discord.utils.find(predicate, server.channels)
            if channel is not None:
                await bot.send_message(channel, message)
        finally:
            log.info('Sent message to {}'.format(server.name.encode('utf-8')))
            # to make sure we don't hit the rate limit, we send one
            # announcement message every 1 second.
            await asyncio.sleep(1)

if __name__ == "__main__":
    bot.run(os.getenv('NANOBOT_TOKEN'))
