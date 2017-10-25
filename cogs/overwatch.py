from discord.ext import commands
import discord
import overwatchpy
import aiohttp
import logging
import asyncio
import requests
import json
from cogs.utils.maps import OW_Map

log = logging.getLogger("bot.overwatch")
owapi = overwatchpy.OWAPI()
mp_thumbnails = OW_Map()

class Overwatch:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.group(pass_context=True, aliases=['ow'])
    async def overwatch(self, ctx):
        """Overwatch commands, type `!!help overwatch` for more info."""
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
        r = requests.get('https://owapi.net/api/v3/u/{}/stats'.format(qu), headers={"user-agent":"NanoBot/V2"})
        try:
            c = r.json()["us"]["stats"]["competitive"]["overall_stats"]
            q = r.json()["us"]["stats"]["quickplay"]["overall_stats"]
        except KeyError:
            await self.bot.say(":no_entry_sign: Couldn't find any stats in the US region or the profile does not exist.")
            return
        if r.status_code == 200:
            e = discord.Embed(color=0xFC9A23, title="{}'s Overwatch Profile".format(user))
            e.add_field(name="Level", value=c['level'])
            e.add_field(name="Competitive Rank", value="{} {}".format(self.bot.badges[c['tier']], c['comprank']))
            e.add_field(name="Games Played", value="**â€¢ Competitive:** {}\n**â€¢ Quick Play:** {}".format(c['games'], q['games']))
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
            hero = overwatchpy.Hero(25, 'Doomfist', 'Doomfistâ€™s cybernetics make him a highly-mobile, powerful frontline fighter. In addition to dealing ranged damage with his Hand Cannon, Doomfist can slam the ground, knock enemies into the air and off balance, or charge into the fray with his Rocket Punch. When facing a tightly packed group, Doomfist leaps out of view, then crashes down to earth with a spectacular Meteor Strike.', 250, 0, 0, 'Akande Ogundimu', 45, None, 'Talon', 'Oyo, Nigeria', 3, overwatchpy.Role(1, "offense"), None, None, None)
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
            e.add_field(name="Role", value=hero.role.name.title())
            e.set_footer(text="Tracking 25 Heroes")
            await self.bot.say(embed=e)

    @overwatch.command(pass_context=True, name="map")
    async def _map(self, ctx, *, name = None):
        """Shows info on a map by name or ID."""
        if name is None:
            await self.bot.say(embed=self.bot.embeds.invalid_syntax("No map was given"))
            return
        else:
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
                await self.bot.say(embed=self.bot.embeds.invalid_syntax("The map '{}' wasn't found".format(name)))
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

def setup(bot):
    n = Overwatch(bot)
    bot.add_cog(n)
