from discord.ext import commands
import discord
import ffmpy
import youtube_dl
import concurrent.futures

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

    def isenabled(ctx):
        global disabled_cmds

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
        global errors
        if channel is None:
            channel = ctx.message.author.voice_channel
        """Joins a voice channel."""
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

def setup(bot):
    bot.add_cog(Music(bot))
    bog.add_cog(YouTube(bot))
