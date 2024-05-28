import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import logging
import datetime
import asyncio
import wave

logging.basicConfig(level=logging.DEBUG)


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')

@bot.command(name='join')
async def join(ctx):
    logging.debug("join: Command invoked")
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}")
        logging.debug(f"join: Joined channel {channel.name}")
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command(name='leave')
async def leave(ctx):
    logging.debug("leave: Command invoked")
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel")
        logging.debug("leave: Disconnected from the voice channel")

@bot.command(name='play')
async def play(ctx, url):
    logging.debug("play: Command invoked")
    if ctx.voice_client:
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: logging.error(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')
        logging.debug(f"play: Now playing {player.title}")
    else:
        await ctx.send("I am not connected to a voice channel.")

@bot.command(name='stop')
async def stop(ctx):
    logging.debug("stop: Command invoked")
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Stopped playing.")
        logging.debug("stop: Stopped playing")
    else:
        await ctx.send("I am not connected to a voice channel.")

@bot.command(name='startrecord')
async def start_record(ctx):
    logging.debug("startrecord: Command invoked")
    if ctx.voice_client:
        sink = discord.sinks.WaveSink()
        ctx.voice_client.start_recording(
            sink, 
            finished_callback, 
            ctx
        )
        await ctx.send("Recording started.")
        logging.debug("startrecord: Recording started")
    else:
        await ctx.send("I am not connected to a voice channel.")

@bot.command(name='stoprecord')
async def stop_record(ctx):
    logging.debug("stoprecord: Command invoked")
    if ctx.voice_client:
        ctx.voice_client.stop_recording()
        await ctx.send("Recording stopped.")
        logging.debug("stoprecord: Recording stopped")

def finished_callback(sink, ctx):
    logging.debug("finished_callback: Recording finished")
    for user_id, audio in sink.audio_data.items():
        audio.file.seek(0)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"voice_recording_{timestamp}.wav"
        
        with wave.open(file_name, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            wf.writeframes(audio.file.read())

        file_size = os.path.getsize(file_name)
        logging.info(f"Recording saved as {file_name}, size: {file_size} bytes")
        asyncio.run_coroutine_threadsafe(
            ctx.send(f"Recording finished. File saved as {file_name}, size: {file_size} bytes"), 
            bot.loop
        )

@bot.event
async def on_disconnect():
    logging.debug("on_disconnect: Cleaning up before shutting down")
    if bot.voice_clients:
        for vc in bot.voice_clients:
            if vc.is_connected():
                await vc.disconnect(force=True)

@play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

bot.run('TOKEN')

