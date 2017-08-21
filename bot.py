##########################################
# NanoBot                                #
#                                        #
# Copyright (c) Nanomotion, 2017         #
# See the LICENSE.txt file for more info #
##########################################

import logging
logging.basicConfig(format='[%(asctime)s/%(levelname)s] %(name)s: %(message)s', level=logging.INFO, datefmt='%I:%M:%S %p')
import importlib
import discord
import asyncio
import aiohttp
import traceback
import youtube_dl
import json
import time
import uuid
import sys
import os, os.path
import ctypes
from discord.ext import commands
from apiclient.discovery import build as gapibuild
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import colorama
import urllib.request
import ast
import timeit
import argparse
from tkinter import messagebox
import concurrent.futures
import overwatchpy
import math
import requests
import getpass
import datetime
import random

parser = argparse.ArgumentParser()
parser.add_argument("-debug", "--debug", help="Change logger level to logging.DEBUG instead of logging.INFO", action="store_true")
parser.add_argument("-ver", "--version", help="Prints the application version", action="store_true")
parser.add_argument("-sptest", "--speedtest", help="Pings gateway.discord.gg", action="store_true")
parser.add_argument("-m", "--maintenance", help="Runs the bot in maintenance mode", action="store_true")
parser.add_argument("-gtoken", "--gapi-token", help="Runs the bot with a custom Google API token")
parser.add_argument("-nc", "--no-color", help="Runs the bot without logger colors", action="store_true")
parser.add_argument("-beta", "--use-beta-token", help="Runs the bot without logger colors", action="store_true")
args = parser.parse_args()
if args.version:
    print(version)
    sys.exit(0)
elif args.speedtest:
    sys.exit(x)
elif args.debug:
    logging.basicConfig(format='[%(asctime)s/%(levelname)s] %(name)s: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S %p')
    logging.debug("Logging level set to DEBUG")
elif args.maintenance:
    x = os.system('python maintenance.py')
    sys.exit(x)
if args.gapi_token:
    DEVELOPER_KEY = args.gapi_token
if args.no_color:
    color.BLUE = ""
    color.YELLOW = ""
    color.RED = ""
    color.GREEN = ""

async def post_stats():
    await bot.change_presence(game=discord.Game(name='!!help • {} Guilds'.format(len(bot.servers))), status=discord.Status.online)
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

os.chdir('data')
logging.debug("Setting up configuration...")

partners = []
partnered_servers = []
admin_ids = []
blocked_ids = []
staff = []
custom_cmds = {}
badges = {
'partner':'<:partner:335963561106866178>',
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

class mp_thumbnails:
    dorado = 'http://www.owfire.com/images/maps/dorado-3.jpg'
    eichenwalde = 'http://media1.gameinformer.com/imagefeed/screenshots/Overwatch/OW_Eichenwalde_17.jpg'
    rio = 'http://images.pushsquare.com/news/2016/08/hands_on_overwatchs_olympian_ps4_update_scores_with_rocket_league_mode/attachment/2/original.jpg'
    hanamura = 'http://www.owfire.com/images/maps/hanamura-1.jpg'
    hollywood = 'http://i0.wp.com/www.geeksandcom.com/wp-content/uploads/2015/11/Overwatch-Hollywood.jpg'
    ilios = 'http://tse3.mm.bing.net/th?id=OIP._w8hoVAgibFCc5vabEgJJQEsCo&pid=15.1'
    kings_row = 'http://www.helderpinto.com/wp-content/uploads/2014/11/Helder_Pinto_Kings_Row_02.jpg'
    lijiang_tower = 'http://vignette2.wikia.nocookie.net/overwatch/images/e/ed/Lijiang_screenshot_34.jpg/revision/latest/scale-to-width-down/2000?cb=20160711182404'
    route_66 = 'http://www.offgamers.com/blog/wp-content/uploads/2016/03/dtftgbyvrmcxqwrnid76.jpg'
    numbani = 'http://www.owfire.com/images/maps/numbani-4.jpg'
    nepal = 'http://www.gameinformer.com/resized-image.ashx/__size/610x0/__key/CommunityServer-Components-SiteFiles/imagefeed-featured-blizzard-overwatch-gamer_2D00_culture/nepal_5F00_overwatch_5F00_610.jpg'
    temple_of_anubis = 'http://cdn.mos.cms.futurecdn.net/QmgmSXRZ4SmoWA7yi7ekWm-650-80.jpg'
    volskaya_industries = 'https://4.bp.blogspot.com/-U2msLyRa6uo/V0QZlLDn7MI/AAAAAAAAAkA/_9mROobNtG4eycJrtfEREhFaud0EwkS6QCLcB/s1600/Volskaya_011.jpg'
    watchpoint_gibraltar = 'http://wiki.teamliquid.net/commons/images/thumb/8/8b/Gibraltar.jpg/600px-Gibraltar.jpg'
    ecopoint_antarctica = 'http://2static.fjcdn.com/pictures/New+overwatch+map+ecopoint+antarctica_85f8d3_6077872.jpg'

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

cmds_this_session = []
songs_played = []
kicks = []
bans = []
start_time = None
st_servers = None
version = "1.7-beta"
build = "17101"
_uuid = uuid.uuid1()
queue = {}
errors = []
DEVELOPER_KEY = str(os.getenv('GAPI_TOKEN'))
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
owapi = overwatchpy.OWAPI()

colorama.init(autoreset=True)
class color:
    BLUE = colorama.Fore.WHITE + colorama.Back.BLUE
    YELLOW = colorama.Fore.WHITE + colorama.Back.YELLOW
    RED = colorama.Fore.WHITE + colorama.Back.RED
    GREEN = colorama.Fore.WHITE + colorama.Back.GREEN
    RESET = colorama.Style.RESET_ALL

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
        e.set_footer(text="Commands reference: http://nanomotion.github.io/NanoBot/commands.html")
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

class objects:
    class Command:
        def __init__(self, name, original):
            self.name = name
            self.original = original
    class Banne:
        def __init__(self, case : int, server : discord.Server, user : discord.User, mod : discord.User, reason = None):
            self.case = case
            self.server = server
            self.user = user
            self.mod = mod
            self.moderator = mod
            self.reason = reason
            self.embed = embeds.user_ban(self.mod, self.user, self.reason, self.case)
        def to_dict(self):
            d = {"case": self.case, "server": self.server, "user": self.user, "mod": self.mod, "reason": self.reason}
            return d
        class Kick:
            def __init__(self, case : int, server : discord.Server, user : discord.User, mod : discord.User, reason = None):
                self.case = case
                self.server = server
                self.user = user
                self.mod = mod
                self.moderator = mod
                self.reason = reason
                self.embed = embeds.user_kick(self.mod, self.user, self.reason, self.case)
            def to_dict(self):
                d = {"case": self.case, "server": self.server, "user": self.user, "mod": self.mod, "reason": self.reason}
                return d
logging.debug('done')

logging.debug('Defining commands...')
def get_voters(mode=0):
    r = requests.get("https://discordbots.org/api/bots/294210459144290305/votes", headers={"Authorization":os.getenv("DBOTSLIST_TOKEN")})
    if r.status_code == 200:
        voters = []
        for user in r.json():
            if mode == 0:
                voters.append("{0}#{1}".format(user['username'], user['discriminator']))
            elif mode == 1:
                voters.append(user['id'])
        return voters
    else:
        raise ConnectionError("Request returned status code {}".format(r.status_code))
def queue_get_all(q, m=10):
    items = []
    maxItemsToRetreive = m
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            items.append(q.get_nowait())
        except:
            break
    for x in items:
        try:
            q.put_nowait(x)
        except:
            break
    return items

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* by **{0.uploader}** requested by `{1.name}#{1.discriminator}` '
        duration = self.player.duration
        if duration:
            fmt = fmt + '`[length: {0[0]}m {0[1]}s]`'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        global errors
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, ':notes: Now playing ' + str(self.current))
            try:
                self.current.player.start()
                await self.play_next_song.wait()
            except concurrent.futures._base.CancelledError:
                pass
            except Exception as e:
                await self.bot.say(embed=embeds.error(str(e), ctx))
                logging.error(str(e))
                logging.error(traceback.format_exc())

class Music:

    # TODO: "!!repeat" command for audio

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel = None): # !!join
        """Joins a voice channel."""
        global errors
        if channel is None:
            channel = ctx.message.author.voice_channel
        await self.bot.send_typing(ctx.message.channel)
        try:
            await self.create_voice_client(channel)
        except discord.errors.ClientException:
            await self.bot.say(embed=embeds.error("Already in a voice channel!", ctx))
        except TimeoutError:
            await self.bot.say(embed=embeds.error("Connection timed out.", ctx))
        except discord.errors.Forbidden:
            await self.bot.say(embed=embeds.error("I don't have permission to join that voice channel!", ctx))
        except discord.errors.InvalidArgument:
            await self.bot.say(embed=embeds.invalid_syntax("{} is not a valid voice channel.".format(ctx.message.author.voice_channel)))
        except Exception as e:
            logging.error(str(e))
            errors.append(e)
            await self.bot.say(embed=embeds.error("I couldn't connect to that voice channel.", ctx))
        else:
            await self.bot.say(':notes: Ready to play audio in `' + channel.name + '`')

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx): # !!summon
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        await self.bot.send_typing(ctx.message.channel)
        if summoned_channel is None:
            await self.bot.say(embed=embeds.error("You aren't in a voice channel!", ctx))
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.bot.say(":notes: Ready to play music in `" + str(summoned_channel.name) + "`!")
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str): # !!play
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        global songs_played
        global errors
        songs_played.append(song)
        await self.bot.send_typing(ctx.message.channel)
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                pass
        vc = ctx.message.server.me.voice.voice_channel
        if vc is not None and ctx.message.author in vc.voice_members:
            try:
                player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            except OSError as e:
                errors.append(e)
                logging.fatal(str(e))
                await self.bot.say(embed=embeds.error(str(e), ctx))
            except youtube_dl.utils.GeoRestrictedError:
                await self.bot.say(embed=errors.error("This video is not available in your country."))
            except youtube_dl.utils.DownloadError as e:
                await self.bot.say("An error occurred while downloading this video: {}".format(str(e)))
            except Exception as e:
                e = str(e)
                logging.error(e)
                logging.error(traceback.format_exc())
                await self.bot.say(embed=embeds.error(e, ctx))
            else:
                player.volume = 0.6
                try:
                    entry = VoiceEntry(ctx.message, player)
                except Exception as e:
                    logging.error(str(e))
                    errors.append(e)
                    await self.bot.say(embed=embeds.error(str(e), ctx))
                else:
                    try:
                        await state.songs.put(entry)
                        await self.bot.say(':notes: Added ' + str(entry) + ' to the queue.')
                    except asyncio.QueueFull:
                        await self.bot.say(':no_entry_sign: You can only have 10 songs in queue at a time!')
        else:
            if vc is not None:
                await self.bot.say(embed=embeds.permission_denied("You are not in the current voice channel."))


    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int): # !!volume
        """Sets the volume of the currently playing song."""
        vc = ctx.message.server.me.voice.voice_channel
        if vc is not None and ctx.message.author in vc.voice_members:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                player.volume = value / 100
                await self.bot.say(':speaker: :notes: Set the volume to {:.0%}'.format(player.volume))
        else:
            await self.bot.say(embed=embeds.permission_denied("You are not in the current voice channel or the player is stopped."))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx): # !!pause
        """Pauses the currently played song."""
        vc = ctx.message.server.me.voice.voice_channel
        if vc is not None and ctx.message.author in vc.voice_members:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                player.pause()
                await self.bot.say(":pause_button: Paused the player. Use `!!resume` to resume the player.")
        else:
            await self.bot.say(embed=embeds.permission_denied("You are not in the current voice channel or the player is stopped."))

    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, ctx): # !!queue
        """Shows all songs waiting to be played."""
        state = self.get_voice_state(ctx.message.server)
        songs = queue_get_all(state.songs)
        msg = ":notes: Songs in queue:\n"
        num = 1
        if len(songs) == 0:
            await self.bot.say(":speaker::no_entry_sign: No songs in queue.")
        else:
            for song in songs:
                msg += str(num) + ". " + str(song) + "\n"
                num += 1
            await self.bot.say(msg[:2000])

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx): # !!resume
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            await self.bot.say(":notes: Resumed the player.")

    @commands.command(pass_context=True, no_pm=True, aliases=['leave', 'disconnect'])
    async def stop(self, ctx): # !!stop
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)
        vc = ctx.message.server.me.voice.voice_channel
        if vc is not None and ctx.message.author in vc.voice_members:
            if state.is_playing():
                player = state.player
                player.stop()

            try:
                state.audio_player.cancel()
                del self.voice_states[server.id]
                await state.voice.disconnect()
            except:
                pass
        else:
            await self.bot.say(embed=embeds.permission_denied("You are not in the current voice channel or the player is stopped."))

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx): # !!skip
        """Vote to skip a song.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say(':no_entry_sign: Not playing any music right now.')
            return

        voter = ctx.message.author
        is_dj = False
        for r in voter.roles:
            if r.name == "DJ":
                is_dj = True
        users_in_channel = len(ctx.message.server.me.voice.voice_channel.voice_members) - 1
        if state.is_playing() and voter in ctx.message.server.me.voice.voice_channel.voice_members:
            total_votes = len(state.skip_votes)
            if voter == state.current.requester or is_dj:
                await self.bot.say(':fast_forward: Skipping song...')
                state.skip()
            elif (voter.id not in state.skip_votes) or total_votes >= users_in_channel:
                state.skip_votes.add(voter.id)
                if total_votes >= users_in_channel:
                    e = discord.Embed()
                    e.title = "Skip Song"
                    e.description = "Skip vote passed. Skipping song..."
                    e.set_footer(text="Users with a role named 'DJ' can automatically skip songs.")
                    await self.bot.say(':fast_forward: Skip vote passed, skipping song...')
                    state.skip()
                else:
                    e = discord.Embed()
                    e.title = "Skip Song"
                    e.description = "Skip vote added."
                    e.add_field(name='Total Votes', value=total_votes)
                    e.add_field(name='Votes Needed', value=users_in_channel)
                    e.set_footer(text="Users with a role named 'DJ' can automatically skip songs.")
                    await self.bot.say(embed=e)
            else:
                await self.bot.say(embed=embeds.permission_denied("You have already voted to skip this song!"))
        else:
            await self.bot.say(embed=embeds.permission_denied("You are not in the current voice channel or the player is stopped."))

    @commands.command(pass_context=True, no_pm=True, aliases=['np', 'nowplaying'])
    async def playing(self, ctx): # !!playing
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything. Type `!!play <query>` to play a song.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {}'.format(state.current, skip_count))

class Moderation:

    # TODO: Add moderator commands

    def __init__(self, bot):
        self.bot = bot

    def ismod(ctx):
        passed = False
        for role in ctx.message.author.roles:
            if role.name.lower() == "nanobot mod" or role.name.lower() == "moderator" or role.name.lower() == "mod" or role.name.lower() == "discord mod":
                passed = True
        return passed

    @commands.command(no_pm=True)
    async def modhelp(self):
        e = discord.Embed(color=ctx.message.server.me.color, title="Moderation Help")
        e.add_field(name="!!modhelp", value="Shows help on moderation commands.")
        e.add_field(name="!!prune <amount>", value="Prunes the last `<amount>` of messages.")
        e.add_field(name="!!kick <user> [reason]", value="Kicks `<user>` with an optional `[reason]`.")
        e.add_field(name="!!ban <user> [reason]", value="Bans `<user>` with an optional `[reason]`.")
        e.set_footer(text="All commands in this category require a role named \"NanoBot Mod\"")
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await self.bot.say(embed=e)


    @commands.command(pass_context=True, no_pm=True, aliases=['purge', 'clear'])
    @commands.check(ismod)
    async def prune(self, ctx, limit : int): # !!prune
        """Deletes the specified amount of messages."""
        global errors
        if not limit > 1:
            await self.bot.say(":no_entry_sign: You can only delete more than 1 message!")
        else:
            counter = -1
            await self.bot.send_typing(ctx.message.channel)
            try:
                async for log in self.bot.logs_from(ctx.message.channel, limit=limit + 1):
                    await self.bot.delete_message(log)
                    counter += 1
                    if counter % 5 == 0:
                        await self.bot.send_typing(ctx.message.channel)
            except Exception as e:
                logging.error(str(e))
                await self.bot.say(embed=embeds.error(str(e), ctx))
            else:
                await self.bot.say(':zap: Deleted {} messages.'.format(counter))

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(ismod)
    async def ban(self, ctx, user : discord.Member, *, reason : str = "*No reason was provided.*"):
        try:
            await self.bot.send_message(user, "You were banned from **{}** by the moderator **{}** for the reason: {}".format(ctx.message.server.name, ctx.message.author, reason))
            await self.bot.ban(user, delete_message_days=0)
            case = uuid.uuid4()
            bans.append(objects.Banne(case, ctx.message.server, user, ctx.message.author, reason))
            try:
                for channel in ctx.message.server.channels:
                    if channel.name == "mod-log" or channel.name == "mod_log":
                        await self.bot.send_message(channel, embed=embeds.user_ban(ctx.message.author, user, reason, case))
                        break
            except:
                await self.bot.say("**ProTip:** Having a channel named `#mod_log` or `#mod-log` will allow me to post moderation info.")
        except discord.Forbidden:
            await self.bot.say(embed=embeds.error("I don't have the correct permissions to do that.", ctx))
        except:
            raise
        else:
            await self.bot.say("Successfully banned " + str(user))

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(ismod)
    async def kick(self, ctx, user : discord.Member, *, reason : str = "*No reason was provided.*"):
        try:
            await self.bot.send_message(user, "You were kicked from **{}** by the moderator **{}** for the reason: {}".format(ctx.message.server.name, ctx.message.author, reason))
            await self.bot.kick(user)
            case = uuid.uuid4()
            kicks.append(objects.Kick(case, ctx.message.server, user, ctx.message.author, reason))
            try:
                for channel in ctx.message.server.channels:
                    if channel.name == "mod-log" or channel.name == "mod_log":
                        await self.bot.send_message(channel, embed=embeds.user_kick(ctx.message.author, user, reason, case))
                        break
            except:
                await self.bot.say("**ProTip:** Having a channel named `#mod_log` or `#mod-log` will allow me to post moderation info.")
        except discord.Forbidden:
            await self.bot.say(embed=embeds.error("I don't have the correct permissions to do that.", ctx))
        except:
            raise
        else:
            await self.bot.say("Successfully kicked " + str(user))

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

class YouTube:

    def __init__(self, bot):
        self.bot = bot

    def search(q, max_results=10):
        ytsearch = gapibuild(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = ytsearch.search().list(q=q, part="id,snippet", maxResults=max_results).execute()


        videos = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append({"id":search_result["id"]["videoId"], "title":search_result["snippet"]["title"], "description":search_result['snippet']['description'], "uploader":search_result['snippet']['channelTitle'], "thumbnail":search_result['snippet']['thumbnails']['default']['url']})

        return videos

    @commands.command(pass_context=True)
    async def yt(self, ctx, *, query : str): # !!yt
        """Searches YouTube for videos with the specified query."""
        await self.bot.send_typing(ctx.message.channel)
        q = ""
        try:
            q = YouTube.search(query)
        except HttpError as e:
            errors.append(e)
            logging.error(str(e))
            await self.bot.say(embed=embeds.error(str(e), ctx))
        else:
            q = q[0]
            embed = discord.Embed(color=discord.Color.red())
            embed.title = "YouTube Search Result"
            embed.add_field(name="Title", value=q['title'][:1020])
            embed.add_field(name="Uploader", value=q['uploader'][:1020])
            embed.add_field(name="URL", value="https://youtube.com/watch?v=" + q['id'])
            embed.set_thumbnail(url=q['thumbnail'])
            embed.add_field(name="Description", value=q['description'][:1000])
            await self.bot.send_message(ctx.message.channel, embed=embed)

class General:

    def __init__(self, bot):
        self.bot = bot

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
            logging.error("Failed to get voting info!")
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
        """Shows info on NanoBot's guilds."""
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

    @commands.command(pass_context=True, no_pm=True, aliases=['botinfo', 'stats', 'about'])
    async def info(self, ctx): # !!info
        """Shows bot info."""
        try:
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
            logging.debug("Got bot uptime")
            stp = str(elapsed_time[7] - 1) + " days, " + str(elapsed_time[3]) + " hours, " + str(elapsed_time[4]) + " minutes"
            logging.debug("Formatted bot uptime")
            users = sum(1 for _ in self.bot.get_all_members())
            logging.debug("Got all bot users")
            color = discord.Color.default()
            if ctx.message.server is not None:
                color = ctx.message.server.me.color
            embed = discord.Embed(color=color, title="NanoBot Statistics", description="Made by **Der#4587**")
            embed.set_footer(text="NanoBot#2520")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name="> Uptime", value=stp)
            embed.add_field(name="> Usage", value="**• Guilds:** {}\n**• Users:** {}".format(len(self.bot.servers), users))
            embed.add_field(name="> Commands", value="**• Total Received:** {}\n**• Errors:** {} ({}%)".format(len(cmds_this_session), len(errors), round(len(errors)/len(cmds_this_session) * 100)))
            embed.add_field(name="> Voice", value="**• Active Sessions:** {}\n**• Songs Played:** {}".format(len(self.bot.voice_clients), len(songs_played)))
            embed.add_field(name="> Version", value="**• NanoBot:** {}\n**• discord.py:** {}\n**• Python:** {}".format(version, discord.__version__, pyver))
            embed.add_field(name="> Misc", value="**• Website:** [Go!](https://nanomotion.github.io/pages/bot)\n**• Discord:** [Join!](https://discord.gg/eDRnXd6)")
            logging.debug("Created Embed")
            await self.bot.say(embed=embed)
        except:
            raise

    @commands.command(pass_context=True, no_pm=True, aliases=['server', 'guildinfo', 'serverinfo'])
    async def guild(self, ctx): # !!guild
        """Shows guild info."""
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
        """Shows bot developers."""
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

    @commands.command(aliases=['hi', 'bot'])
    async def hello(self): # !!hello
        """Hello, world!"""
        await self.bot.say(':wave: Hi, I\'m NanoBot! I can make your Discord server better with all of my features! Type `!!help` for more info, or go to https://nanobot-discord.github.io')

    @commands.command(pass_context=True)
    async def invite(self, ctx): # !!invite
        """Shows a link to invite NanoBot to a guild."""
        await self.bot.say('{}, you can invite me to your server with this link: https://discordapp.com/oauth2/authorize?client_id=294210459144290305&scope=bot&permissions=405924918'.format(ctx.message.author.mention))

    @commands.command(pass_context=True)
    async def logs(self, ctx, limit : int = 100): # !!logs
        """Gets the latest messages from a channel and compiles them in a text file."""
        tmp = await self.bot.say(embed=discord.Embed(description=":clock2: Retrieving the last **{} messages**".format(limit)))
        await self.bot.send_typing(ctx.message.channel)
        if limit > 1000:
            await self.bot.edit_message(tmp, embed=discord.Embed(color=discord.Color.red(), description=":x: I can only retrieve less than 1000 messages!"))
        elif limit < 1:
            await self.bot.edit_message(tmp, embed=discord.Embed(color=discord.Color.red(), description=":x: I can only retrieve more than 1 message!"))
        else:
            stp = "Logs provided by NanoBot#250\n{}\n\n".format("="*28)
            async for msg in self.bot.logs_from(ctx.message.channel, limit = limit):
                stp += "{0.author} at {0.timestamp} (ID: {0.id})\n{0.clean_content}\n\n"
            try:
                f = open('logs.txt.tmp', 'w')
                f.write(stp)
                f.close()
            except:
                raise
            else:
                await self.bot.send_file(ctx.message.channel, os.path.join(os.getcwd(), "logs.txt.tmp"), filename="logs.txt")
                os.remove(os.path.join(os.getcwd(), "logs.txt.tmp"))

    @commands.group(pass_context=True)
    async def upvote(self, ctx): # !!upvote
        """Upvote NanoBot to receive special perks!"""
        if ctx.invoked_subcommand is None:
            e = discord.Embed(description="{0} **[Click Here]({1})** to upvote NanoBot and get **premium features**! {0}".format(badges['voter'], "https://discordbots.org/bot/294210459144290305"))
            e.set_footer(text="Type !!upvote features to see the full list.")
            await self.bot.say(embed=e)

    @upvote.command(name="help", pass_context=True)
    async def _help(self, ctx):
        """Shows help."""
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        e = discord.Embed(color=color, title="Upvote Help")
        e.add_field(name="> How do I upvote NanoBot?", value="Go to [this link]({0}) and press the button named **Upvote**. If the button is disabled, log in to your Discord account via [here]({1}). If the upvote button is green, you're good to go!".format("https://discordbots.org/bot/294210459144290305", "https://discordbots.org/login"))
        e.add_field(name="> What features are included with the voter status?", value="For starters, get a sweet badge on your user profile like this one: {0}. You'll also get access to a premium music player, and lots more! Type **!!upvote features** to learn more.")
        e.set_footer(text="{} upvoters".format(len(get_voters())))
        await self.bot.say(embed=e)

    @upvote.command()
    async def features(self):
        """Shows upvoter features."""
        await self.bot.say(":tools: This command isn't ready yet!")

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
        print("https://random.dog/" + str(dog))
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
        print(cat)
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

class Status:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def status(self, ctx): # !!status
        """Shows statuspage.io info."""
        if ctx.invoked_subcommand is None:
            f = open('status_help.txt')
            await self.bot.say(f.read())
            f.close()

    @status.command()
    async def help(self):
        f = open('status_help.txt')
        await self.bot.say(f.read())
        f.close()

    @status.command(pass_context=True)
    async def all(self, ctx): # All Statuses
        await self.bot.send_typing(ctx.message.channel)
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        embed = discord.Embed(color=color)
        class discord_st:
            st = urllib.request.urlopen('https://srhpyqt94yxb.statuspage.io/api/v2/status.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']['indicator']
            desc = st['status']['description']
            timestamp = st['page']['updated_at']
        await self.bot.send_typing(ctx.message.channel)
        class github_st:
            st = urllib.request.urlopen('https://status.github.com/api/last-message.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']
            desc = st['body']
            timestamp = st['created_on']
        await self.bot.send_typing(ctx.message.channel)
        class reddit_st:
            st = urllib.request.urlopen('http://2kbc0d48tv3j.statuspage.io/api/v2/status.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']['indicator']
            desc = st['status']['description']
            timestamp = st['page']['updated_at']
        await self.bot.send_typing(ctx.message.channel)
        class hi_rez_st:
            st = urllib.request.urlopen('http://stk4xr7r1y0r.statuspage.io/api/v2/status.json')
            st = str(st.read())
            st = st[2:]
            st = st[:len(st) - 1]
            st = ast.literal_eval(st)
            status = st['status']['indicator']
            desc = st['status']['description']
            timestamp = st['page']['updated_at']
        await self.bot.send_typing(ctx.message.channel)
        embed.title = "Website Status"
        embed.set_footer(text="StatusPage.io")
        embed.add_field(name="Discord", value=discord_st.status)
        embed.add_field(name="GitHub", value=github_st.status)
        embed.add_field(name="Reddit", value=reddit_st.status)
        embed.add_field(name="Hi-Rez Studios", value=hi_rez_st.status)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def discord(self, ctx): # Discord Status
        """Shows Discord status (From https://status.discordapp.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('https://srhpyqt94yxb.statuspage.io/api/v2/status.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']['indicator']
        desc = st['status']['description']
        timestamp = st['page']['updated_at']
        color = discord.Color.default()
        if status == "none":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="Discord Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        embed.set_thumbnail(url="https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def github(self, ctx): # GitHub Status
        """Shows GitHub status (From https://status.github.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('https://status.github.com/api/last-message.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']
        desc = st['body']
        timestamp = st['created_on']
        color = discord.Color.default()
        if status == "good":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="GitHub Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        embed.set_thumbnail(url="https://maxcdn.icons8.com/iOS7/PNG/75/Logos/github_copyrighted_filled-75.png")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def reddit(self, ctx): # Reddit Status
        """Shows Reddit status (From https://redditstatus.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('http://2kbc0d48tv3j.statuspage.io/api/v2/status.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']['indicator']
        desc = st['status']['description']
        timestamp = st['page']['updated_at']
        color = discord.Color.default()
        if status == "none":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="Reddit Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        embed.set_thumbnail(url="http://img.washingtonpost.com/rf/image_1024w/2010-2019/WashingtonPost/2012/08/15/National-Enterprise/Images/reddit-alien.jpg")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @status.command(pass_context=True)
    async def hi_rez(self, ctx): # Hi-Rez Studios Status
        """Shows Hi-Rez Studios status (From https://status.hirezstudios.com)"""
        await self.bot.send_typing(ctx.message.channel)
        st = urllib.request.urlopen('http://stk4xr7r1y0r.statuspage.io/api/v2/status.json')
        st = str(st.read())
        st = st[2:]
        st = st[:len(st) - 1]
        st = ast.literal_eval(st)
        status = st['status']['indicator']
        desc = st['status']['description']
        timestamp = st['page']['updated_at']
        color = discord.Color.default()
        if status == "none":
            color = discord.Color.green()
        elif status == "minor" or status == "maintenance":
            color = discord.Color.gold()
        elif status == "major":
            color = discord.Color.red()
        embed = discord.Embed(color=color)
        embed.title="Hi-Rez Studios Status"
        embed.set_footer(text="Last updated " + timestamp)
        embed.add_field(name=":vertical_traffic_light: Status", value=status)
        embed.add_field(name=":speech_balloon: Description", value=desc)
        await self.bot.send_message(ctx.message.channel, embed=embed)

class Overwatch:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=['ow'])
    async def overwatch(self, ctx):
        """Overwatch commands!"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type `!!overwatch help` for proper usage.")

    @overwatch.command(pass_context=True, name="help")
    async def _help(self, ctx):
        """Shows help."""
        await self.bot.send_typing(ctx.message.channel)
        color = discord.Color.default()
        if ctx.message.server is not None:
            color = ctx.message.server.me.color
        e = discord.Embed(title="Overwatch Commands", color=color)
        e.add_field(name="!!overwatch help", value="Shows this message.")
        e.add_field(name="!!overwatch profile <battletag>", value="Shows quick play and competitive stats for the specified battle.net user. E.g. `!!overwatch profile Dad#12262`")
        e.add_field(name="!!overwatch hero <name>", value="Shows hero info by name. E.g. `!!overwatch hero Genji`")
        e.add_field(name="!!overwatch map <name|id>", value="Shows map info by name or id. E.g. `!!overwatch map Ilios`")
        e.add_field(name="!!overwatch event <id>", value="Shows event info by id. E.g. `!!overwatch event 1`")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/314140565329543188/341962877424369667/overwatch-logo.png")
        await self.bot.say(embed=e)

    @overwatch.command(pass_context=True)
    async def event(self, ctx, *, name = None):
        """Shows info for an event by name."""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say("*Work in progress...*")

    @overwatch.command(pass_context=True)
    async def profile(self, ctx, *, user):
        """Shows info for a battle.net user."""
        await self.bot.send_typing(ctx.message.channel)
        qu = user.replace('#', '-')
        r = requests.get('https://owapi.net/api/v3/u/{}/stats'.format(qu), headers={"user-agent":"NanoBot/{}".format(version)})
        try:
            c = r.json()["us"]["stats"]["competitive"]["overall_stats"]
            q = r.json()["us"]["stats"]["quickplay"]["overall_stats"]
        except KeyError:
            await self.bot.say(":no_entry_sign: Couldn't find any stats in the `US` region.")
        if r.status_code == 200:
            e = discord.Embed(color=0xFC9A23, title="{}'s Overwatch Profile".format(user))
            e.add_field(name="Level", value=c['level'])
            e.add_field(name="Competitive Rank", value="{} {}".format(badges[c['tier']], c['comprank']))
            e.add_field(name="Games Played", value="**• Competitive:** {}\n**• Quick Play:** {}".format(c['games'], q['games']))
            e.add_field(name="Wins/Losses", value="**> Competitive**\n{} Wins / {} Losses ({}%)\n**> Quick Play**\n{} Wins / {} Losses ({}%)".format(c['wins'], c['losses'], c['win_rate'], q['wins'], q['losses'], q['win_rate']))
            e.set_thumbnail(url=q['avatar'])
            await self.bot.say(embed=e)
        elif r.status_code == 404:
            await self.bot.say("The user `{}` wasn't found.".format(user))
        else:
            await self.bot.say(embed=embeds.error("Request returned status code " + str(r.status_code), ctx))

    @overwatch.command(pass_context=True)
    async def hero(self, ctx, *, name):
        """Shows info on a hero by name."""
        name = name.lower()
        hero = None
        await self.bot.send_typing(ctx.message.channel)
        if name == "d.va":
            name = "dva"
        elif name == "soldier: 76" or name == "soldier 76" or name == "soldier76":
            name = "soldier-76"
        if name == "ana":
            hero = owapi.get_hero(1)
        elif name == "bastion":
            hero = owapi.get_hero(2)
        elif name == "dva":
            hero = owapi.get_hero(3)
        elif name == "genji":
            hero = owapi.get_hero(4)
        elif name == "hanzo":
            hero = owapi.get_hero(5)
        elif name == "junkrat":
            hero = owapi.get_hero(6)
        elif name == "lucio":
            hero = owapi.get_hero(7)
        elif name == "mccree":
            hero = owapi.get_hero(8)
        elif name == "mei":
            hero = owapi.get_hero(9)
        elif name == "mercy":
            hero = owapi.get_hero(10)
        elif name == "pharah":
            hero = owapi.get_hero(11)
        elif name == "reaper":
            hero = owapi.get_hero(12)
        elif name == "reinhardt":
            hero = owapi.get_hero(13)
        elif name == "roadhog":
            hero = owapi.get_hero(14)
        elif name == "soldier-76":
            hero = owapi.get_hero(15)
        elif name == "symmetra":
            hero = owapi.get_hero(16)
        elif name == "torbjorn":
            hero = owapi.get_hero(17)
        elif name == "tracer":
            hero = owapi.get_hero(18)
        elif name == "widowmaker":
            hero = owapi.get_hero(19)
        elif name == "winston":
            hero = owapi.get_hero(20)
        elif name == "zarya":
            hero = owapi.get_hero(21)
        elif name == "zenyatta":
            hero = owapi.get_hero(22)
        elif name == "sombra":
            hero = owapi.get_hero(23)
        elif name == "orisa":
            hero = owapi.get_hero(24)
        elif name == "doomfist":
            hero = overwatchpy.Hero(25, 'Doomfist', 'Doomfist’s cybernetics make him a highly-mobile, powerful frontline fighter. In addition to dealing ranged damage with his Hand Cannon, Doomfist can slam the ground, knock enemies into the air and off balance, or charge into the fray with his Rocket Punch. When facing a tightly packed group, Doomfist leaps out of view, then crashes down to earth with a spectacular Meteor Strike.', 250, 0, 0, 'Akande Ogundimu', 45, None, 'Talon', 'Oyo, Nigeria', 3, overwatchpy.Role(1, "offense"), None, None, None)
        else:
            await self.bot.say(embed=embeds.invalid_syntax("The requested hero '{}' wasn't found".format(name)))
        if hero is not None:
            color = discord.Color.default()
            if ctx.message.server is not None:
                color = ctx.message.server.me.color
            e = discord.Embed(color=color, title="Hero: {}/{}".format(hero.name, hero.id), description=hero.description)
            e.set_thumbnail(url="https://blzgdapipro-a.akamaihd.net/hero/{}/hero-select-portrait.png".format(name))
            e.add_field(name="Health", value="{} HP / {} Armor / {} Shield".format(hero.health, hero.armor, hero.shield))
            e.add_field(name="Real Name", value=hero.real_name)
            e.add_field(name="Age", value=hero.age)
            e.add_field(name="Affiliation", value=hero.affiliation)
            e.add_field(name="Base of Operations", value=hero.base_of_operations)
            e.add_field(name="Difficulty", value=hero.difficulty)
            e.add_field(name="Role", value=hero.role.name)
            e.set_footer(text="Tracking 25 Heroes")
            await self.bot.say(embed=e)

    @overwatch.command(pass_context=True, name="map")
    async def _map(self, ctx, *, name = None):
        """Shows info on a map by name or ID."""
        name = name.lower()
        mp = None
        thumb = None
        if name == "dorado" or name == "1":
            mp = owapi.get_map(1)
            thumb = mp_thumbnails.dorado
        elif name == "eichenwalde" or name == "2":
            mp = owapi.get_map(2)
            thumb = mp_thumbnails.eichenwalde
        elif name == "rio" or name == "estudio de ras" or name == "3":
            mp = owapi.get_map(3)
            thumb = mp_thumbnails.rio
        elif name == "hanamura" or name == "4":
            mp = owapi.get_map(4)
            thumb = mp_thumbnails.hanamura
        elif name == "hollywood" or name == "5":
            mp = owapi.get_map(5)
            thumb = mp_thumbnails.hollywood
        elif name == "ilios" or name == "6":
            mp = owapi.get_map(6)
            thumb = mp_thumbnails.ilios
        elif name == "kings row" or name == "7":
            mp = owapi.get_map(7)
            thumb = mp_thumbnails.kings_row
        elif name == "lijang tower" or name == "8":
            mp = owapi.get_map(8)
            thumb = mp_thumbnails.lijiang_tower
        elif name == "route 66" or name == "9":
            mp = owapi.get_map(9)
            thumb = mp_thumbnails.route_66
        elif name == "numbani" or name == "10":
            mp = owapi.get_map(10)
            thumb = mp_thumbnails.numbani
        elif name == "nepal" or name  == "11":
            mp = owapi.get_map(11)
            thumb = mp_thumbnails.nepal
        elif name == "temple of anubis" or name == "12":
            mp = owapi.get_map(12)
            thumb = mp_thumbnails.temple_of_anubis
        elif name == "volskaya industries" or name == "13":
            mp = owapi.get_map(13)
            thumb = mp_thumbnails.volskaya_industries
        elif name == "watchpoint: gibraltar" or name == "14":
            mp = owapi.get_map(14)
            thumb = mp_thumbnails.watchpoint_gibraltar
        elif name == "ecopoint: antarctica" or name == "15":
            mp = owapi.get_map(15)
            thumb = mp_thumbnails.ecopoint_antarctica
        else:
            await self.bot.say(embed=embeds.invalid_syntax("The map '{}' wasn't found".format(name)))
        if mp is not None:
            color = discord.Color.default()
            if ctx.message.server is not None:
                color = ctx.message.server.me.color
            e = discord.Embed(color=color, title="Map: {}/{}".format(mp.name, mp.id))
            e.add_field(name="Location", value=mp.location)
            e.add_field(name="Mode", value=mp.mode.name)
            st = None
            for stage in mp.stages:
                if st is None:
                    st = ""
                st += "`{}` ".format(stage.name)
            e.add_field(name="Stages", value=st)
            e.set_image(url=thumb)
            await self.bot.say(embed=e)

logging.debug('done')
logging.debug('Creating bot...')
bot = None
if args.use_beta_token:
    bot = commands.Bot(command_prefix=['!!beta ', 'nano beta '], description='A music, fun, moderation, and Overwatch bot for Discord.')
else:
    bot = commands.Bot(command_prefix=['!!', 'nano '], description='A music, fun, moderation, and Overwatch bot for Discord.')
logging.debug('done')
logging.debug('Adding cogs...')
bot.add_cog(Music(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Admin(bot))
bot.add_cog(Owner(bot))
bot.add_cog(General(bot))
bot.add_cog(Fun(bot))
bot.add_cog(YouTube(bot))
bot.add_cog(Status(bot))
bot.add_cog(Overwatch(bot))
logging.debug('done')

logging.debug('Defining events...')
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
                await bot.send_typing(message.channel)
                color = discord.Color.default()
                extra = ""
                if message.server is not None:
                    color = message.server.me.color
                if str(message.channel).startswith("Direct Message with "):
                    extra += " Please note that some commands can't be used in Direct Messages."
                e = discord.Embed(title="NanoBot Help", description="For more help, type `!!help <command>` or `!!help <category>`.\nNeed even more help? Our support team can help you at the **[NanoBot Discord](https://discord.gg/eDRnXd6)**.", color=color)
                e.add_field(name="> General", value="`!!help`, `!!hello`, `!!invite`, `!!info`, `!!user`, `!!guild`, `!!guilds`, `!!ping`")
                e.add_field(name="> Fun", value="`!!cat`, `!!dog`, `!!8ball`                                                                    ​")
                e.add_field(name="> Moderation", value="`!!modhelp`, `!!prune`, `!!ban`, `!!kick`                                                                 ​")
                e.add_field(name="> Admin", value="`!!cmd add`, `!!cmd edit`, `!!cmd del`")
                e.add_field(name="> Music", value="`!!join`, `!!summon`, `!!play`, `!!yt`, `!!queue`, `!!volume`, `!!pause`, `!!resume`, `!!stop`, `!!skip`, `!!playing`")
                e.add_field(name="> Overwatch", value="`!!ow profile`, `!!ow hero`, `!!ow map`, `!!ow event`")
                e.add_field(name="Voting", value="Vote for NanoBot [here](https://discordbots.org/bot/294210459144290305) and receive special perks! Type `!!upvote` for more info.")
                e.add_field(name="Notice", value="*By using NanoBot, you agree to the [Terms and Conditions](https://nanomotion.github.io/pages/faq/policies/).*")
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
    global start_time
    global st_servers
    start_time = time.time()
    st_servers = bot.servers
    logging.info("Logged in as {0.name}#{0.discriminator}".format(bot.user))
    await post_stats()
logging.debug('done')

if __name__ == "__main__":
    logging.info("Finished with setup")
    logging.info("NanoBot version {0} // build {1}".format(version, build))
    try:
        if args.use_beta_token:
            logging.info("Logging in using beta token")
            bot.run(os.getenv('NANOBOT_BETA_TOKEN'))
        else:
            bot.run(os.getenv('NANOBOT_TOKEN'))
    except ConnectionResetError as e:
        logging.fatal("The connection was reset!")
        logging.fatal("{}: {}".format(type(e).__name__, e))
    except OSError as e:
        logging.fatal("A fatal system error occurred!")
        logging.fatal("{}: {}".format(type(e).__name__, e))
    except Exception as e:
        logging.fatal("Bot session crashed!")
        logging.fatal("{}: {}".format(type(e).__name__, e))
    except SystemExit as e:
        logging.fatal("Bot session was terminated prematurely!")
        logging.fatal("{}: {}".format(type(e).__name__, e))
    except KeyboardInterrupt as e:
        logging.fatal("Bot session was terminated prematurely!")
        logging.fatal("{}: {}".format(type(e).__name__, e))
    input("Press enter to continue...")
