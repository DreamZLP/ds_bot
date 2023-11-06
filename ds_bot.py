import random
import discord
import datetime
from pytube import extract
from discord.ext import commands, tasks

# import config
# from config import settings

# import disnake
# from disnake.ext import commands

intents = discord.Intents.all()

last_post_id = None

command_prefix = '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Создание экземпляра клиента Discord
client = discord.Client(intents=intents)

# ID канала, в который нужно отправлять обновленную информацию
CHANNEL_ID_FOR_SERVER_INFO = ###

# ID канала, в который нужно отправлять сообщение от бота
CHANNEL_ID_FOR_MESSAGE = ###

# Отключаем стандартную команду !help
bot.remove_command('help')


@bot.command()  # Приветствие?
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}! Бот Kawaii!-Universe dreamzpbot приветствует вас! ❤️❤️❤️')
    print(f"Пользователь '{author.mention}' вызвал команду '!hello'")


@bot.command()  # Рандомное число от 0 до 100
async def rand(ctx, *arg):
    author = ctx.message.author
    await ctx.reply(random.randint(0, 100))
    print(f"Пользователь '{author.mention}' вызвал команду '!rand'")


@bot.command()
async def latence(ctx):
    author = ctx.message.author
    guild = ctx.guild
    region_info = str(round(bot.latency * 1000)) + " ms"
    await ctx.send(f'Задержка сервера относительно региона: {region_info}')
    print(f"Пользователь '{author.mention}' вызвал команду '!latence'")


@bot.command()
async def help(ctx):
    author = ctx.message.author
    emb1 = discord.Embed(title="Информация о командах",
                         color=random.randint(1, 16777216))
    emb1.add_field(name=f"`{command_prefix}help` : ",
                   value="Вызовет это меню", inline=False)
    emb1.add_field(name=f"`{command_prefix}hello` : ",
                   value="Приветствие от бота", inline=False)
    emb1.add_field(name=f"`{command_prefix}rand` : ",
                   value="Рандомное число от 0 до 100", inline=False)
    emb1.add_field(name=f"`{command_prefix}serverinfo` : ",
                   value="Просмотра информации о сервере", inline=False)
    emb1.add_field(name=f"`{command_prefix}latence` : ",
                   value="Просмотра информации о задержке сервера", inline=False)
    emb1.add_field(name=f"`{command_prefix}createchannel` : ",
                   value="Создание нового текстового канала", inline=False)
    emb1.add_field(name=f"`{command_prefix}null` : ", value="?", inline=False)
    message = await ctx.send(embed=emb1)
    print(f"Пользователь '{author.mention}' вызвал команду '!help'")


@bot.event  # Сообщения пользователю в лс и на сервере
async def on_member_join(member):
    title = f'Добро пожаловать на {member.guild.name}'
    emb1 = discord.Embed(title=title, color=random.randint(1, 16777216))
    emb1.add_field(name=f"`{command_prefix}help` : ",
                   value="Используй эту команду на сервере, чтобы вызвать справку по командам.", inline=False)
    message = await member.send(embed=emb1)
    print(
        f"Пользователю '{member.mention}' отправлено приветсвенное собщение в лс")

    # Имя канала, куда бот будет отправлять приветствие
    channel = discord.utils.get(
        member.guild.channels, name="системные-сообщение")
    await channel.send(f'Привет, {member.mention}! Добро пожаловать на наш сервер!')
    print(
        f"Отправлено приветственное сообщение на сервере пользователю '{member.mention}'")

    # Имя роли, которую нужно присвоить новому участнику
    role = discord.utils.get(member.guild.roles, name="Лещ")
    await member.add_roles(role)
    # Имя канала, куда бот будет отправлять приветствие
    channel = discord.utils.get(
        member.guild.channels, name="системные-сообщение")
    # Получение цвета роли
    role_color = role.color if role.color.value != 0 else discord.Color.default()
    embed = discord.Embed(title="Роль присвоена",
                          description=f"Пользователю {member.mention} присвоена роль {role.mention}", color=role_color)
    await channel.send(embed=embed)
    print(f"Пользователю '{member.mention}' присвоена роль '{role.mention}'")


@bot.command()
async def createchannel(ctx):
    author = ctx.message.author
    guild = ctx.message.guild
    embed = discord.Embed(title="Важно! Системное сообщение для создании нового текстового канала!",
                          description=f"Для создания нового канала, придумайте ему новое имя!", color=random.randint(1, 16777216))
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    msg = await bot.wait_for("message", check=check)
    channel_name = msg.content
    if msg.content != null:
        print(f"Название нового канала '{msg.content}'")
    category = guild.get_channel(1124850068466434098)
    await category.create_text_channel(msg.content)
    await ctx.send(f"Создан новый текстовый канал '{msg.content}' в категории '{category}'")
    print(f"Пользователь '{author.mention}' вызвал команду '!createchannel'")
    print(
        f"Создан новый текстовый канал в категории '{category}' под именем '{channel_name}'")


@bot.command()
async def serverinfo(ctx):
    # guild = ctx.guild
    # total_members = len(guild.members)
    # online_members = sum(member.status != discord.Status.offline for member in guild.members)
    # text_channels = len(guild.text_channels)
    # voice_channels = len(guild.voice_channels)
    # region_info = str(round(bot.latency * 1000)) + " ms"
    # guild_icon_url = str(guild.icon.url)

    # embed = discord.Embed(title="Информация о сервере", description=guild.name, color=discord.Color.blurple())
    # embed.add_field(name="Участники", value=f"Общее количество: {total_members}\nОнлайн: {online_members}", inline=False)
    # embed.add_field(name="Каналы", value=f"Текстовые: {text_channels}\nГолосовые: {voice_channels}", inline=False)
    # embed.add_field(name="Задержка", value=region_info, inline=False)
    # embed.set_thumbnail(url=guild_icon_url)

    # await ctx.send(embed=embed)
    author = ctx.message.author
    emb1 = discord.Embed(title="Информационное сообщение!",
                         color=random.randint(1, 16777216))
    emb1.add_field(name="Ошибка команды!",
                   value=f"Команда `{command_prefix}serverinfo` в данный момент недоступна и скоро будет убрана, т.к. информация данной команды находится в канале 'статус-сервера'!", inline=False)
    message = await ctx.send(embed=emb1)
    print(f"Пользователь '{author.mention}' вызвал команду '!serverinfo'")


@bot.command()
async def null(ctx):
    author = ctx.message.author
    emb1 = discord.Embed(title="Информационное сообщение!",
                         color=random.randint(1, 16777216))
    emb1.add_field(name="Ошибка команды!",
                   value=f"Команда `{command_prefix}null` пуста или же ещё не существует!", inline=False)
    message = await ctx.send(embed=emb1)
    print(f"Пользователь '{author.mention}' вызвал команду '!null'")


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')
    # # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Kawaii!-Universe"))
    # Setting `Playing ` status
    await bot.change_presence(activity=discord.Game(name="Kawaii!-Universe"))
    update_server_info.start()


@bot.event  # Сообщения в текстовом канале о начале голосового чата
async def on_voice_state_update(member, before, after):
    if after.self_video != before.self_video:
        if after.self_video:  # Проверяем, изменилась ли передача видео
            channel = bot.get_channel(CHANNEL_ID_FOR_MESSAGE)
            await channel.send(f'{member.name} начал демонстрировать экран!')
            print(f"{member.activity.name} начал стрим в голосовом канале! Бот отправил сообщение об этом на канал '{channel}'")


@bot.event
async def on_message(message):
    global last_post_id
    if last_post_id is None or message.id != last_post_id:
        last_post_id = message.id
    if message.channel.id == last_post_id:
        channel = discord.utils.get(message.guild.text_channels, name='общее')
        content = message.content
        author = message.author.global_name
        post_url = message.jump_url
        forum_name = bot.get_channel(1128043675751026820)
        url = content
        id = extract.video_id(url)
        imgUrl = f"https://img.youtube.com/vi/{id}/maxresdefault.jpg"
        # Отправляем сообщение в указанный канал

        emb1 = discord.Embed(title=f"Новая публикация от `{author}`:",
                             color=random.randint(1, 16777216))
        emb1.add_field(name="",
                       value=f'\n\u2022 Ссылка: `{content}` \
                                 \n\u2022 Форум: `{forum_name}` \
                                 \n\u2022 Перессылка на пост: {post_url}', inline=False)
        emb1.set_image(url=imgUrl)
        message = await channel.send(embed=emb1)
        # await channel.send(f'{content}:')
        print(
            f'Отправлен уведомление о новой публикации №{last_post_id} в текстовый канал "общее"')
    await bot.process_commands(message)


@tasks.loop(minutes=1)
async def update_server_info():
    guild_id = GUILD_ID  # Замените GUILD_ID на ID вашего сервера
    channel = bot.get_channel(CHANNEL_ID_FOR_SERVER_INFO)
    if channel:
        guild = bot.get_guild(guild_id)
        if guild:
            total_members = len(guild.members)
            online_members = sum(
                member.status != discord.Status.offline for member in guild.members)
            active_members = sum(
                member.status == discord.Status.online for member in guild.members)
            idle_members = sum(
                member.status == discord.Status.idle for member in guild.members)
            do_not_disturb_members = sum(
                member.status == discord.Status.do_not_disturb for member in guild.members)
            # invisible_members = sum(member.status == discord.Status.invisible for member in guild.members)
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            region_info = str(round(bot.latency * 1000)) + " ms"
            help_info_status = "Информация обновляется каждую минуту!"
            guild_icon_url = str(guild.icon.url)

            async for message in channel.history(limit=1):
                if message.author == bot.user:
                    if message.embeds:
                        old_embed = message.embeds[0]
                        break
            else:  # Если нет предыдущего сообщения, создаем новое сообщение
                old_embed = None

            # Определение текущей даты и времени
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            embed = discord.Embed(title="Информация о сервере",
                                  description=f"\n\u2022 Имя сервера: {guild.name}", color=random.randint(1, 16777216))
            embed.add_field(name="Участники", value=f"\u2022 Общее количество: {total_members} \
                             \n\u2022 Онлайн: {online_members}, среди которых: \
                             \n\u2003 Активные: {active_members} \
                             \n\u2003 Неактивные: {idle_members} \
                             \n\u2003 В режиме 'не беспокоить': {do_not_disturb_members}", inline=False)
            embed.add_field(
                name="Каналы", value=f"\u2022 Текстовые: {text_channels}\n\u2022 Голосовые: {voice_channels}", inline=False)
            embed.add_field(name="Задержка",
                            value=f"\u2022 {region_info}", inline=False)
            embed.add_field(name="Внимание!",
                            value=f"\u2022 {help_info_status}", inline=False)
            embed.set_thumbnail(url=guild_icon_url)
            embed.set_image(url='https://i.imgur.com/NN6SDjD.jpg')
            embed.add_field(name='\u200b', value='\u200b', inline=False)
            embed.set_footer(
                text=f'Время последнего обновления информации: {current_time}')
            print(f"Статус сервера обновлён в '{current_time}'")

            if old_embed:
                await message.edit(embed=embed)
            else:  # Если нет предыдущего сообщения, отправляем новое
                await channel.send(embed=embed)

bot.run('discord_bot_token')
