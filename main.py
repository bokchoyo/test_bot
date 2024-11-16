import os
import time

from discord.ext import commands

import typerace_texts as texts
from database import Database
from buttons.buttons import *
from buttons.garage_buttons import GarageButtons

# Invite Link: https://discord.com/oauth2/authorize?client_id=1160263342628274236&permissions=0&scope=bot%20applications.commands

# Sell for 75% value
# Build with parts and 80% value
# Buy from dealership for 110% value
# Higher experience = higher chance to beat higher performance rating

account_db = AccountDatabase()
car_db = CarDatabase()
car_json_db = Database('car_data.json')
account_json_db = Database('account_data.json')
car_list = Database('car_list.json')
emoticon_db = Database('emoticons.json')
makes_list = Database('makes.json')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)
embed_color = 0x9c5ab3
attachment_channel_id = '1078045767262023740'
total_car_count = 7
total_pages = int(math.ceil(total_car_count / 2))


def load_cogs(cog=None):
    if cog is None:
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                bot.load_extension(f'cogs.{file[:-3]}')
    else:
        bot.load_extension(f'cogs.{cog}')


load_cogs()


def count_command(authorid):
    command_count = account_json_db.get_key(['accounts', str(authorid), 'stats', 'commands']) + 1
    account_json_db.set_key(['accounts', str(authorid), 'stats', 'commands'], command_count)


def count_errors(prompt, text):
    errors = 0
    text = ' '.join(text.strip().split())
    prompt_words = prompt.split()
    input_words = text.split()
    if len(input_words) > len(prompt_words):
        input_words = input_words[:len(prompt_words)]
        text = ' '.join(input_words)

    if len(input_words) < len(prompt_words):
        for i in range(len(prompt_words) - len(input_words)):
            wordId = len(input_words)
            while wordId in range(len(prompt_words)):
                input_words.append('|' * (len(prompt_words[wordId])))
                wordId += 1

    for wordId in range(len(prompt_words)):
        prompt_word = prompt_words[wordId].strip()
        input_word = input_words[wordId].strip()

        if len(input_word) < len(prompt_word):
            input_words[wordId] = input_word + "|" * (len(prompt_word) - len(input_word))
            input_word = input_words[wordId]

        elif len(input_word) > len(prompt_word):
            errors += 1

        for charId in range(len(prompt_word)):
            if prompt_word[charId] != input_word[charId]:
                errors += 1

    errors += len(prompt.split()) - len(text.split())
    return errors


def calculate_accuracy(prompt, text):
    accuracy = round((len(prompt) - count_errors(prompt, text)) / len(prompt), 3)
    return accuracy


def count_spaces(text):
    return text.count(' ')


def check_account_exists(author_id, author_name):
    if str(author_id) not in account_json_db.get_key('accounts'):
        account_json_db.set_key(['accounts', str(author_id)], {
            "username": author_name,
            "imperial": 0,
            "stats": {
                "level": 0,
                "xp": 0,
                "balance": 0,
                "value": 0,
                "garage value": 0,
                "inventory value": 0,
                "driving": "",
                "commands": 0
            },
            "cars": [],
            "car counts": {}
        })


def check_part(authorid, part):
    if part not in account_json_db.get_key(['accounts', str(authorid), 'parts']):
        account_json_db.set_key(['accounts', str(authorid), 'parts', part], 0)


def check_car(authorid, car):
    if car not in account_json_db.get_key(['accounts', str(authorid), 'cars']):
        account_json_db.set_key(['accounts', str(authorid), 'cars', car], 0)


def level_up(authorid):
    user_data = account_json_db.get_key(['accounts', str(authorid), 'stats'])
    xp_req = math.ceil(100 * 1.04761575 ** (user_data['level'] - 1)) * 100
    if user_data['xp'] >= xp_req:
        while user_data['xp'] >= xp_req:
            xp_req = math.ceil(100 * 1.04761575 ** (user_data['level'] - 1)) * 100
            user_data['xp'] -= xp_req
            user_data['level'] += 1
            account_json_db.set_key(['accounts', str(authorid), 'stats'], user_data)


def add_xp(authorid, xp):
    new_xp = account_json_db.get_key(['accounts', str(authorid), 'stats', 'xp']) + xp
    account_json_db.set_key(['accounts', str(authorid), 'stats', 'xp'], new_xp)


def command_routine(author_id, author_name, xp):
    check_account_exists(author_id, author_name)
    add_xp(author_id, xp)
    level_up(author_id)
    count_command(author_id)


def list_user_makes(authorid):
    user_makes = []
    for car_name in account_json_db.get_key(['accounts', authorid]):
        words = car_name.split()
        for i in range(1, len(words) + 1):
            make = ' '.join(words[:i])
            if make in makes_list.get_key('makes'):
                user_makes.append(make)
    return None


def calculate_speed(prompt, text, seconds):
    return (len(prompt) - count_errors(prompt, text)) * 12 / seconds


async def list_makes(ctx: discord.AutocompleteContext):
    makes = ['Lamborghini', 'Ferrari', 'Mclaren', 'Chevrolet', 'Ford', 'Aston Martin']
    return sorted([i for i in makes if i.lower().startswith(ctx.value.lower())])


async def list_models(ctx: discord.AutocompleteContext.options):
    make = ctx.options['make']
    models = Database(f"models_{make.replace(' ', '').lower()}.json").get_key(make)
    return sorted([i for i in models if i.lower().startswith(ctx.value.lower())])


async def list_systems(ctx: discord.AutocompleteContext.options):
    systems = ["Imperial", "Metric"]
    return [i for i in systems if i.lower().startswith(ctx.value.lower())]


@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')


@bot.slash_command()
async def sql(ctx: discord.ApplicationContext,
              make: discord.Option(str, "Select a car make", autocomplete=list_makes),
              model: discord.Option(str, "Select a car model", autocomplete=list_models)
              ):
    command_routine(ctx.author.id, ctx.author.name, 100)
    car_name = f'{make} {model}'
    car = await car_db.get_car(car_name)
    await ctx.respond(str(car))


# @bot.slash_command()
# async def showroom(ctx):
#     await ctx.respond('hi')


@bot.slash_command()
async def balance(ctx):
    command_routine(ctx.author.id, ctx.author.name, 1)
    user_data = account_json_db.get_key(['accounts', str(ctx.author.id)])
    embed = discord.Embed(color=embed_color)

    embed.title = f'''**{user_data["username"]}'s Balance**'''
    embed.description = (f'**Wallet** \n'
                         f'₪ {user_data["balance"]}')
    await ctx.respond(embed=embed)


@bot.slash_command()
async def build(ctx, make, model):
    command_routine(ctx.author.id, ctx.author.name, 50)
    car = f'{make.lower()} {model.lower()}'
    user_data = account_json_db.get_key(['accounts', str(ctx.author.id)])
    car_data = car_json_db.get_key(['cars', f'{car.lower()}'])
    part_reqs = [car_data['chassis count'], car_data['engine count'], car_data['electric motor count']]
    engine, motor, chassis = "", "", ""
    check_part(ctx.author.id, f'chassis {car.lower()}')
    user_parts = account_json_db.get_key(['accounts', str(ctx.author.id), 'parts'])
    if user_parts[f'chassis {car.lower()}'] < part_reqs[0]:
        chassis = f"{car.title()} Chassis: {part_reqs[0] - user_parts[f'chassis {car.lower()}']}"
    check_part(ctx.author.id, 'engine')
    user_parts = account_json_db.get_key(['accounts', str(ctx.author.id), 'parts'])
    if user_parts['engine'] < part_reqs[1]:
        engine = f"Engines: {part_reqs[1] - user_parts['engine']} \n"
    check_part(ctx.author.id, 'electric motor')
    user_parts = account_json_db.get_key(['accounts', str(ctx.author.id), 'parts'])
    if user_parts['electric motor'] < part_reqs[2]:
        motor = f"Electric Motors: {part_reqs[2] - user_parts['electric motor']} \n"
    if user_parts[f'chassis {car.lower()}'] >= part_reqs[0] and user_parts['engine'] >= part_reqs[1] and \
            user_parts['electric motor'] >= part_reqs[2]:
        user_parts[f'chassis {car.lower()}'] -= part_reqs[0]
        user_data['inventory value'] -= 10000 * part_reqs[0]
        user_parts['engine'] -= part_reqs[1]
        user_data['inventory value'] -= 15000 * part_reqs[1]
        user_parts['electric motor'] -= part_reqs[2]
        user_data['inventory value'] -= 25000 * part_reqs[2]
        user_data['garage value'] += car_data['value']
        account_json_db.set_key(['accounts', str(ctx.author.id), 'parts'], user_parts)
        check_car(ctx.author.id, f'{car.lower()}')
        user_data = account_json_db.get_key(['accounts', str(ctx.author.id)])
        user_data['cars'][f'{car.lower()}'] += 1
        account_json_db.set_key(['accounts', str(ctx.author.id)], user_data)
        await ctx.respond(f'You built a {car.title()}!')
    else:
        embed = discord.Embed(color=embed_color)

        embed.title = f'Missing Parts for {car.title()}'
        embed.description = f'{engine} {motor} {chassis}'
        await ctx.respond(embed=embed)


@bot.slash_command()
async def purchase(ctx: discord.ApplicationContext,
                   make: discord.Option(str, "Select a car make", autocomplete=list_makes),
                   model: discord.Option(str, "Select a car model", autocomplete=list_models)
                   ):
    car_name = f'{make} {model}'
    await account_db.add_to_garage(ctx.author.id, car_name)


@bot.slash_command()
async def drive(ctx, id):
    embed = discord.Embed(color=embed_color)
    id = int(id)
    if await account_db.has_car(ctx.author.id, id):
        car_name = await account_db.get_car_name_by_id(ctx.author.id, id)
        await account_db.set_driving_car(ctx.author.id, id)
        description = f'You are now driving your `#{id} {car_name}`'
    else:
        description = 'You do not have that many cars!'
    embed.description = description
    await ctx.respond(embed=embed)


@bot.slash_command()
async def rob(ctx, amount):
    await account_db.add_to_balance(ctx.author.id, amount)
    await ctx.respond(f'Added {amount} to your balance')


# garage_cogs: sort
@bot.slash_command()
async def garage(ctx):
    account_id = ctx.author.id
    command_routine(account_id, ctx.author.name, 1)
    user_garage_list = await account_db.get_garage_list(account_id)
    user_car_count = await account_db.get_garage_size(account_id)
    digits = len(str(user_car_count))
    embed = discord.Embed(color=embed_color)
    embed.set_author(name=f"{ctx.author.name}'s Garage", icon_url=ctx.author.avatar)
    description = ''
    for car in user_garage_list:
        description += '`{:>{}}`\u2003`{:>.2f}`\u2003•\u2003**{}**\u2003•\u2003{}%\n'.format(car[0], digits, car[2], car[1], car[3])
    embed.description = description
    await ctx.respond(embed=embed, view=GarageButtons(account_id))
    await ctx.interaction.response.defer()


@bot.slash_command()
async def inventory(ctx):
    command_routine(ctx.author.id, ctx.author.name, 1)
    user_data = account_json_db.get_key(['accounts', str(ctx.author.id)])
    embed = discord.Embed(color=embed_color)

    embed.title = f'''{user_data["username"]}'s Inventory'''
    description = ""
    for i in user_data["parts"]:
        if user_data['parts'][i] > 0:
            description += f"\n**{i}** — {user_data['parts'][i]}\n"
    embed.description = description.title()
    await ctx.respond(embed=embed)


@bot.slash_command()
async def profile(ctx):
    command_routine(ctx.author.id, ctx.author.name, 1)
    user_data = await account_db.get_account(ctx.author.id)
    embed = discord.Embed(title=f'''**{user_data['username']}'s Profile**''', color=embed_color)
    embed.set_thumbnail(url=ctx.author.avatar)
    await account_db.update_garage_value(ctx.author.id)
    embed.description = (
        f'**Level:** {user_data["level"]:,d}\n'
        f'**XP:** {user_data["xp"]:,d}/{math.ceil(100 * 1.04761575 ** (user_data["level"] - 1)) * 100}\n'
        f'**Balance:** ₪ {user_data["balance"]:,d}\n'
        f'**Account Value:** ₪ {user_data["value"]:,d}\n'
        f'**Cars:** {await account_db.get_garage_size(ctx.author.id) :,d}\n'
        f'**Driving:** {user_data["driving_car_id"]}\n'
        f'**Commands Sent:** {user_data["commands_sent"]:,d}')
    await ctx.respond(embed=embed)


def calculate_reward(wpm, accuracy, top_speed, acceleration):
    ts_bonus = top_speed ** 1.25
    acceleration_multiplier = 7 / (acceleration + 3)
    wpm_reward = math.ceil(wpm * 10)
    accuracy_reward = math.floor((1 - accuracy ** 3) * wpm_reward)
    base_reward = wpm_reward - accuracy_reward
    total_reward = math.floor(base_reward * acceleration_multiplier + ts_bonus)
    car_bonus = total_reward - base_reward
    return wpm_reward, accuracy_reward, car_bonus, total_reward


# Image for text so no copy paste
@bot.slash_command()
async def typerace(ctx):
    command_routine(ctx.author.id, ctx.author.name, 10000)
    user_car = account_json_db.get_key(['accounts', str(ctx.author.id), 'stats', 'driving'])
    user_car_stats = car_json_db.get_key(['cars', user_car, 'performance imperial'])
    prompt = texts.get_random_sentence()
    embed = discord.Embed(title='Race', description=f'**Track:** Circuit de la Sarthe\n**Car:** {user_car}',
                          color=embed_color)
    embed.set_image(url='https://cdn.discordapp.com/attachments/1078045767262023740/1189087788247814216/open-uri20121011-15375-m9iw3c.png?ex=659ce34c&is=658a6e4c&hm=8a24e028e89178fdda5342bc8e1c2bc033421a74f980776157dff48c317509dc&')
    bot_message = await ctx.respond(embed=embed)
    time.sleep(3)
    embed.set_image(url=None)
    for i in reversed(range(1, 4)):
        embed.description = f'Type the text shown in: **{i}**'
        await bot_message.edit(embed=embed)
        time.sleep(1)
    embed.description = f"```{prompt}```"
    await bot_message.edit(embed=embed)

    race_start = time.time()

    try:
        user_message = await bot.wait_for(
            "message",
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
            timeout=60,
        )

        race_finish = time.time()
        text = user_message.content.strip()
        await user_message.delete()
        speed = round(calculate_speed(prompt, text, race_finish - race_start - 1), 1)
        accuracy = round(calculate_accuracy(prompt, text), 3)
        reward = calculate_reward(speed, accuracy, user_car_stats['top speed'], user_car_stats['acceleration'])
        embed.title = 'Race Results'
        embed.description = ''
        embed.add_field(name='',
                        value=f'{speed} WPM\n{round(accuracy * 100, 1)}% Accuracy\n{user_car} Bonus\n**Total**',
                        inline=True)
        embed.add_field(name='', value='', inline=True)
        embed.add_field(name='',
                        value=f'₪ {reward[0]:,d}\n₪ \u2013 {reward[1]:,d}\n₪ {reward[2]:,d}\n**₪ {reward[3]:,d}**',
                        inline=True)
        await bot_message.edit(embed=embed)

        current_balance = account_json_db.get_key(['accounts', str(ctx.author.id), 'stats', 'balance'])
        account_json_db.set_key(['accounts', str(ctx.author.id), 'stats', 'balance'], current_balance + reward[3])

    except asyncio.TimeoutError:
        await ctx.respond("You took too long to respond")


@bot.slash_command()
async def map(ctx):
    user_location = await account_db.get_location(ctx.author.id)
    embed = discord.Embed(color=embed_color, title=f"{ctx.author.name}'s Location", description=f'Location: {user_location}')
    embed.set_image(url='https://cdn.discordapp.com/attachments/1078045767262023740/1200203644822376519/World_map_blank_without_borders.png?ex=65c553bf&is=65b2debf&hm=9d6dc88a56cff233187fef100afa580b05b336f5016c068aa6e694203a4f0776&')
    await ctx.respond(embed=embed)


@bot.slash_command(description='Lists the required parts to build a car')
async def requirements(ctx: discord.ApplicationContext,
                       make: discord.Option(str, "Select a car make", autocomplete=list_makes),
                       model: discord.Option(str, "Select a car model", autocomplete=list_models)
                       ):
    command_routine(ctx.author.id, ctx.author.name, 1)
    car = f'{make.lower()} {model.lower()}'
    check_car(ctx.author.id, car)
    parts = car_json_db.get_key(['cars', f'{car.lower()}', 'part requirements'])
    embed = discord.Embed(color=embed_color)

    requirement_list = ''
    for i in parts:
        if i.split()[:1] == ['unit']:
            break
        if parts[i] != 0 and parts[i] != '':
            requirement_list += f"{i.title()}: ``{parts[i]}``\n"
    embed.description = requirement_list
    embed.title = f'Required Parts for {car.title()}'
    await ctx.respond(embed=embed)


@bot.slash_command()
async def bal(ctx):
    balance = await account_db.get_balance(ctx.author.id)
    await ctx.respond(f'Your balance: {balance:,d}')


@bot.slash_command()
async def sell(ctx, car_id):
    account_id = ctx.author.id
    embed = discord.Embed(color=embed_color)
    if not await account_db.has_car(account_id, car_id):
        embed.description = 'You do not own a car with that id.'
        await ctx.respond(embed=embed)
    elif await account_db.has_one_car(account_id):
        embed.description = "You can't sell the only car you own bruh"
        await ctx.respond(embed=embed)
    else:
        car_to_sell = await account_db.get_car_for_sell(account_id, car_id)
        car_name = car_to_sell[0]
        car_value = car_to_sell[1]
        car_sell_value = int(math.floor(car_value * 0.5))
        embed.description = f'Are you sure you want to sell your `#{car_id} {car_name}` for © {car_sell_value:,d}?'
        await ctx.respond(embed=embed, view=SellConfirmationButtons(account_id, car_id, car_name, car_sell_value))


@bot.slash_command(description='View the specifications of a car')
async def specs(ctx: discord.ApplicationContext,
                         make: discord.Option(str, "Select a car make", autocomplete=list_makes),
                         model: discord.Option(str, "Select a car model", autocomplete=list_models)
                         ):
    command_routine(ctx.author.id, ctx.author.name, 1)
    car_name = f'{make} {model}'
    car_general_info = await car_db.get_general_info(car_name)
    if car_general_info is None:
        await ctx.respond(embed=discord.Embed(color=embed_color, description='That car does not exist'))
    user_uses_imperial = await account_db.get_imperial(ctx.author.id)
    embed = discord.Embed(color=embed_color, title=f'**{car_general_info[2]} {car_name}**')
    for i in car_general_info:
        print(i)
    embed.set_image(url=f'https://cdn.discordapp.com/attachments/{attachment_channel_id}/' + car_general_info[0])
    embed.add_field(name='General Information', inline=True, value=f'Performance Rating: `{car_general_info[3]:.2f}`\n'
                                                                   f'Value: `₪ {car_general_info[4]:,d}`\n'
                                                                   f'Tier: `{car_general_info[5]}`\n'
                                                                   f'Class: `{car_general_info[6]}`\n'
                                                                   f'Parts: `{car_general_info[7]}`')
    embed.add_field(name='', value='', inline=True)
    if user_uses_imperial:
        car_performance = await car_db.get_performance_imperial(car_name)
        embed.add_field(name='Performance', inline=True, value=f'Top Speed: `{car_performance[0]} mph`\n'
                                                               f'0-60 mph: `{car_performance[1]} sec`\n'
                                                               f'Power: `{car_performance[2]:,d} hp`\n'
                                                               f'Torque: `{car_performance[3]:,d} lb-ft`\n'
                                                               f'Weight: `{car_performance[4]:,d} lb.`')
    else:
        car_performance = await car_db.get_performance_metric(car_name)
        embed.add_field(name='Performance', inline=True, value=f'Top Speed: `{car_performance[0]} kph`\n'
                                                               f'0-100 kph: `{car_performance[1]} sec`\n'
                                                               f'Power: `{car_performance[2]:,d} ps`\n'
                                                               f'Torque: `{car_performance[3]:,d} Nm`\n'
                                                               f'Weight: `{car_performance[4]:,d} kg`')
    embed.set_footer(text=f'{car_general_info[2]} {car_name} in {car_general_info[1]}')
    await ctx.respond(embed=embed)


@bot.slash_command()
async def units(ctx: discord.ApplicationContext,
                system: discord.Option(str, "Select a system", autocomplete=list_systems)):
    command_routine(ctx.author.id, ctx.author.name, 1)
    if system == 'Imperial':
        await account_db.set_imperial(ctx.author.id, True)
    else:
        await account_db.set_imperial(ctx.author.id, False)
    embed = discord.Embed(color=embed_color, description=f'You are now using the {system.lower()} system')
    await ctx.respond(embed=embed)


bot.run('')
