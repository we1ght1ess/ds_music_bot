import discord
from discord.ext import commands
from config import token
import typing
import os
import yt_dlp
from discord.errors import ClientException
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False
intents.message_content = True
intents.voice_states = True
PREFIX = '!'
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command('help')
queue = []



@bot.event
async def on_ready():
    print('Бот запущен')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!help'))

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, members: commands.Greedy[discord.Member],
                   delete_days: typing.Optional[int] = 0, *,
                   reason: str):
    """Массовый бан участников с необязательным параметром delete_days"""
    delete_seconds = delete_days * 86400  #один день
    for member in members:
        await member.ban(delete_message_seconds=delete_seconds, reason=reason)

@ban.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет прав на выполнение этой команды.")
    else:
        raise error

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(546035658268082187)
    """Автовыдача ролей и оповещение в канал"""
    role = discord.utils.get(member.guild.roles, id=699224434195693600)
    await member.add_roles(role)
    await channel.send(embed=discord.Embed(description=f"Пользователь {member.name} присоединился к серверу!"))
    print(f"Выдана роль {role.name} для {member.name}")
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


client = discord.Client(intents=intents)  # Создаем подключение к Discord
# @bot.command()
# async def play(ctx, url):
#     global queue
#     voice_channel = await ctx.message.author.voice.channel.connect()
#     ydl_opts = {'format': 'bestaudio/best',
#                 'noplaylist': 'True',
#                 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
#                 'outtmpl': 'downloads/%(title)s.%(ext)s',
#                 'quiet': True}
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#         info = ydl.extract_info(url, download=False)
#
#     filename = f'downloads/{info["title"]}.mp3'
#
#     try:
#
#         audio_source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
#
#         def after_playing(error):
#             asyncio.run_coroutine_threadsafe(voice_channel.disconnect(), bot.loop)
#
#         voice_channel.play(audio_source, after=lambda e: after_playing(e))
#         await ctx.channel.send(f'Играет: {info["title"]}')
#                 #ожидаем 5 минут перед отключением
#     except ClientException as e:
#         print(e)
#     except Exception as e:
#         print(e)
#         await ctx.channel.send('Что-то пошло не так...')
#
#     def after_playing(error):
#         coro = voice_channel.disconnect()
#         fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
#         fut.result()
#         os.remove(filename)



# @bot.command()
# async def play(ctx, url):
#     global queue
#
#     # Если бот не в канале,зайти в него
#     if not ctx.voice_client:
#         voice_channel = await ctx.author.voice.channel.connect()
#     else:
#         voice_channel = ctx.voice_client
#
#     ydl_opts = {'format': 'bestaudio/best',
#                 'noplaylist': 'True',
#                 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
#                 'outtmpl': 'downloads/%(title)s.%(ext)s',
#                 'quiet': True}
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#         info = ydl.extract_info(url, download=False)
#         queue.append({'ctx': ctx, 'info': info, 'url': url})
#
#     if not voice_channel.is_playing():
#         await play_next(ctx)
#
#
# async def play_next(ctx):
#     global queue
#
#     if len(queue) == 0:
#         return
#
#     song = queue.pop(0)
#     voice_channel = ctx.voice_client
#     filename = f'downloads/{song["info"]["title"]}.mp3'
#
#     try:
#         audio_source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
#
#
#         def after_playing(error):
#             asyncio.run_coroutine_threadsafe(async_lambda(ctx), bot.loop)
#
#         async_lambda = lambda ctx: on_song_end(ctx)
#
#
#         async def on_song_end(ctx):
#             os.remove(filename)
#
#             if len(queue) > 0:
#                 await play_next(ctx)
#             else:
#
#                 await ctx.voice_client.disconnect()
#
#         voice_channel.play(audio_source, after=after_playing)
#
#     except ClientException as e:
#         print(e)
#     except Exception as e:
#         print(e)
#         await ctx.channel.send('Что-то пошло не так...')
#
# @bot.command()
# async def skip(ctx):
#     global queue
#
#     if not ctx.voice_client or not ctx.voice_client.is_playing():
#         await ctx.send('Нечего пропускать, сейчас ничего не играет.')
#         return
#
#     try:
#         ctx.voice_client.stop()  # Останавливаем воспроизведение текущей песни
#         await ctx.send('Skipped')
#         await play_next(ctx)  # Воспроизводим следующую песню в очереди, если таковая имеется
#     except Exception as e:
#         print(e)
#         await ctx.channel.send('Что-то пошло не так...')


        # """Нужно сделать"""
# @bot.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!play'):
#         voice_channel = message.author.voice.channel
#         if voice_channel:
#             url = message.content[6:]
#
#             ytdlp_format_options = {
#                 'format': 'bestaudio',
#                 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#                 'restrictfilenames': True,
#                 'noplaylist': True,
#                 'nocheckcertificate': True,
#                 'ignoreerrors': False,
#                 'logtostderr': False,
#                 'quiet': True,
#                 'no_warnings': True,
#                 'default_search': 'auto',
#                 'source_address': '0.0.0.0'
#             }
#
#             MAX_DURATION_SEC = 600  # Maximum duration in seconds, here is 10 minutes
#
#             with yt_dlp.YoutubeDL(ytdlp_format_options) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 duration = info['duration']
#
#                 # if duration is longer than allowed, limit it to MAX_DURATION_SEC
#                 limited_duration = min(duration, MAX_DURATION_SEC)
#                 url2 = info['url']
#                 source = await discord.FFmpegOpusAudio.from_probe(url2, before_options=f'-ss 0 -t {limited_duration}')
#
#                 voice_client = await voice_channel.connect()
#                 voice_client.play(source)
#         else:
#             await message.channel.send("Чтобы использовать эту команду, вам необходимо подключиться к голосовому каналу.")
#
#             def after_playing(error):
#                 # Check if an error occurred
#                 if error:
#                     print(f'An error occured: {error}')
#                 coro = voice_client.disconnect()
#                 future = asyncio.run_coroutine_threadsafe(coro, client.loop)
#                 try:
#                     future.result()
#                 except:
#                     # an error happened sending the message
#                     print('disconnection failed')
#
#                 voice_client.play(source, after=after_playing)

# ytdlp_format_options = {
#     'format': 'bestaudio',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0'
#
#
#
# @bot.command()
# async def play(ctx, *, url):
#     if not ctx.author.voice:
#         await ctx.send("Чтобы использовать эту команду, вам необходимо подключиться к голосовому каналу.")
#         return
#
#     voice_channel = ctx.author.voice.channel
#
#     with yt_dlp.YoutubeDL(ytdlp_format_options) as ydl:
#         info = ydl.extract_info(url, download=False)
#         url2 = info['url']
#         source = await discord.FFmpegOpusAudio.from_probe(url2)
#
#     voice_client = await voice_channel.connect()
#     voice_client.play(source)
#
#
# @bot.command()
# async def stop(ctx):
#     if ctx.voice_client:
#         await ctx.voice_client.disconnect()
#     else:
#         await ctx.send("Бот не подключен к голосовому каналу.")



# @bot.command()
# async def stop(ctx):
#     """Команда для выхода бота с голосового канала"""
#     voice_client = ctx.guild.voice_client
#     if voice_client.is_connected():
#         await voice_client.disconnect()
#     else:
#         await ctx.send("Бот не подключен к голосовому каналу.")


# @bot.command()
# async def help(ctx):
#     await ctx.channel.purge(limit=1)
#     emb = discord.Embed(title='Навигация по командам')
#     emb.add_field(name='{}clear'.format(PREFIX), value='Очистка чата')
#     emb.add_field(name='{}ban'.format(PREFIX), value='Бан участника(доступ только администрации)')
#     emb.add_field(name='{}play'.format(PREFIX), value='Включить музыку')
#     emb.add_field(name='{}skip'.format(PREFIX), value='Включить следующий трек')
#     await ctx.send(embed=emb)
#
# @bot.command(pass_context=True)
# async def clear(ctx, amount: int): # задаем количество удаляемых сообщений по умолчанию
#     await ctx.channel.purge(limit=amount+1) # удаляем заданное количество сообщений + само сообщение команды
#     await ctx.send(f'{amount} сообщений были удалены.') # отправляем уведомление о удалении сообщений
#
#
# @clear.error
# async def clear_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send(f'{ctx.author.name}, Не указан аргумент')
def run_bot():
    bot.run(token)

if __name__ == "__main__":
    run_bot()
# bot.add_command(play)

# bot.add_command(clear)
bot.add_command(join)
bot.add_command(joined)
bot.event(on_member_join)
