import random
import discord
from discord.ext import commands, tasks
import datetime
# import config
# from config import settings

command_prefix = '!'
bot = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

# ID канала, в который нужно отправлять обновленную информацию (для получения id необходимо включить режим разработчика в Discord)
CHANNEL_ID = channel_id
# Отключаем стандартную команду !help
bot.remove_command('help')



@bot.command()  #Приветствие (тест-функция)
async def hello(ctx): 
    author = ctx.message.author 
    await ctx.send(f'Привет, {author.mention}! Бот Kawaii!-Universe dreamzpbot приветствует вас! ❤️❤️❤️')  # 'Kawaii!-Universe dreamzpbot' = bot_name

@bot.command()  #Рандомное число от 0 до 100 (тест-функция)
async def rand(ctx, *arg):
    await ctx.reply(random.randint(0,100))

@bot.command() #Задержка относительно сервера (тест-функция)
async def latence(ctx):
    guild = ctx.guild
    region_info = str(round(bot.latency * 1000)) + " ms"
    await ctx.send(f'Задержка сервера относительно региона: {region_info}')


@bot.command() #Вызов справки по командам
async def help(ctx):
    emb1 = discord.Embed(title="Информация о командах", color=random.randint(1, 16777216))
    emb1.add_field(name = f"`{command_prefix}help` : ", value="Вызовет это меню", inline=False)
    emb1.add_field(name = f"`{command_prefix}hello` : ", value="Приветствие от бота", inline=False)
    emb1.add_field(name = f"`{command_prefix}rand` : ", value="Рандомное число от 0 до 100", inline=False)
    emb1.add_field(name = f"`{command_prefix}serverinfo` : ", value="Просмотра информации о сервере", inline=False)
    emb1.add_field(name = f"`{command_prefix}null` : ", value="?", inline=False)
    message = await ctx.send(embed = emb1)

@bot.event   #Сообщения пользователю в лс и на сервере при вступлении в сервер 
async def on_member_join(member):
    title = f'Добро пожаловать на {member.guild.name}'
    emb1 = discord.Embed(title = title, color=random.randint(1, 16777216))
    emb1.add_field(name = f"`{command_prefix}help` : ", value="Используй эту команду на сервере, чтобы вызвать справку по командам.", inline=False)
    message = await member.send(embed = emb1)

    channel = discord.utils.get(member.guild.channels, name="системные-сообщение")  # Имя канала, куда бот будет отправлять приветствие
    await channel.send(f'Привет, {member.mention}! Добро пожаловать на наш сервер!')

    role = discord.utils.get(member.guild.roles, name="Лещ")  # Имя роли, которую нужно присвоить новому участнику
    await member.add_roles(role)
    channel = discord.utils.get(member.guild.channels, name="системные-сообщение")  # Имя канала, куда бот будет отправлять приветствие
    role_color = role.color if role.color.value != 0 else discord.Color.default()  # Получение цвета роли
    embed = discord.Embed(title="Роль присвоена", description=f"Пользователю {member.mention} присвоена роль {role.mention}", color=role_color)
    await channel.send(embed=embed)

@bot.command() #Команда, которая будет удалена
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

    emb1 = discord.Embed(title="Информационное сообщение!", color=random.randint(1, 16777216))
    emb1.add_field(name = "Ошибка команды!", value=f"Команда `{command_prefix}serverinfo` в данный момент недоступна и скоро будет убрана, т.к. информация данной команды находится в канале 'статус-сервера'!", inline=False)
    message = await ctx.send(embed = emb1)


@bot.command() #Пустая команда
async def null(ctx):
    emb1 = discord.Embed(title="Информационное сообщение!", color=random.randint(1, 16777216))
    emb1.add_field(name = "Ошибка команды!", value=f"Команда `{command_prefix}null` пуста или же ещё не существует!", inline=False)
    message = await ctx.send(embed = emb1)


@bot.event  #Персональный статус бота
async def on_ready(): 
    print(f'Bot connected as {bot.user.name}')
    # # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Kawaii!-Universe"))
    # Setting `Playing ` status
    await bot.change_presence(activity=discord.Game(name="Kawaii!-Universe"))
    update_server_info.start()

@tasks.loop(minutes=1)  #Обновление статуса сервера в отдельном канале
async def update_server_info():
    guild_id = GUILD_ID  # Замените GUILD_ID на ID вашего сервера
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        guild = bot.get_guild(guild_id)
        if guild:
            total_members = len(guild.members)
            online_members = sum(member.status != discord.Status.offline for member in guild.members)
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

            embed = discord.Embed(title="Информация о сервере", description=f"\u2022 {guild.name}", color=random.randint(1, 16777216))
            embed.add_field(name="Участники", value=f"\u2022 Общее количество: {total_members}\n\u2022 Онлайн: {online_members}", inline=False)
            embed.add_field(name="Каналы", value=f"\u2022 Текстовые: {text_channels}\n\u2022 Голосовые: {voice_channels}", inline=False)
            embed.add_field(name="Задержка", value=f"\u2022 {region_info}", inline=False)
            embed.add_field(name="Внимание!", value=f"\u2022 {help_info_status}", inline=False)
            embed.set_thumbnail(url=guild_icon_url)
            embed.set_image(url='https://i.imgur.com/NN6SDjD.jpg')
            embed.add_field(name='\u200b', value='\u200b', inline=False)
            embed.set_footer(text=f'Время последнего обновления информации: {current_time}')

            if old_embed:
                await message.edit(embed=embed)
            else:  # Если нет предыдущего сообщения, отправляем новое
                await channel.send(embed=embed)

bot.run('discord_bot_token')
