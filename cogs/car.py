from discord.ext import commands
from discord.commands import SlashCommandGroup
from buttons.buttons import *
import random

car_db = CarDatabase()
account_db = AccountDatabase()
embed_color = 0x9c5ab3
attachment_channel_id = '1078045767262023740'


async def specs_format(account_id, car_id):
    car_general_info = await account_db.get_general_info(account_id, car_id)
    level, rating, quality, top_speed_level, acceleration_level, top_speed_quality, acceleration_quality, year, color, image_url, car_name = \
        car_general_info[0], car_general_info[1], car_general_info[2], car_general_info[3], car_general_info[4], \
            car_general_info[5], car_general_info[6], car_general_info[7], car_general_info[8], car_general_info[9], \
        car_general_info[10]
    user_uses_imperial = await account_db.get_imperial(account_id)
    embed = discord.Embed(color=embed_color, title=f'**Level {level} {car_name}**')
    embed.set_image(url=f'https://cdn.discordapp.com/attachments/{attachment_channel_id}/' + image_url)
    embed.add_field(name='Details', inline=True,
                    value=f'Performance Rating: `{rating:.2f}`\n'
                          f'Quality: `{quality:.2f}`')
    embed.add_field(name='', inline=True, value='')
    if user_uses_imperial:
        car_performance = await account_db.get_performance_imperial(account_id, car_id)
        embed.add_field(name='Specifications', inline=True,
                        value=f'Power: `{car_performance[2]:,d} hp`\n'
                              f'Torque: `{car_performance[3]:,d} lb-ft`')
        embed.add_field(name='Top Speed', inline=True,
                        value=f'Top Speed: `{car_performance[0]:.2f} mph`\n'
                              f'\u2003|\u2003Level: `{top_speed_level}`\n'
                              f'\u2003|\u2003Quality: `{top_speed_quality:.2f}`')
        embed.add_field(name='', inline=True, value='')
        embed.add_field(name='Acceleration', inline=True,
                        value=f'0-60 mph: `{car_performance[1]:.2f} sec`\n'
                              f'\u2003|\u2003Level: `{acceleration_level}`\n'
                              f'\u2003|\u2003Quality: `{acceleration_quality:.2f}`')
    else:
        car_performance = await account_db.get_performance_metric(account_id, car_id)
        embed.add_field(name='Specifications', inline=True,
                        value=f'Power: `{car_performance[2]:,d} ps`\n'
                              f'Torque: `{car_performance[3]:,d} Nm`')
        embed.add_field(name='Top Speed', inline=True,
                        value=f'Top Speed: `{car_performance[0]:.2f} kph`\n'
                              f'\u2003|\u2003Level: `{top_speed_level}`\n'
                              f'\u2003|\u2003Quality: `{top_speed_quality:.2f}`')
        embed.add_field(name='', inline=True, value='')
        embed.add_field(name='Acceleration', inline=True,
                        value=f'0-100 kph: `{car_performance[1]:.2f} sec`\n'
                              f'\u2003|\u2003Level: `{acceleration_level}`\n'
                              f'\u2003|\u2003Quality: `{acceleration_quality:.2f}`')
    embed.set_footer(text=f'{year} {car_name} in {color}\nDisplaying Car #{car_id}')
    return embed


async def generate_qualities():
    top_speed_quality = round(100 * sum([random.randint(0, 9) for _ in range(3)]) / 27, 2)
    acceleration_quality = round(100 * sum([random.randint(0, 9) for _ in range(3)]) / 27, 2)
    car_quality = round((top_speed_quality + acceleration_quality) / 2, 2)
    return car_quality, top_speed_quality, acceleration_quality


async def tune_options(ctx: discord.AutocompleteContext):
    return ['Acceleration', 'Top Speed']


async def list_makes(ctx: discord.AutocompleteContext):
    makes = ['Lamborghini', 'Ferrari', 'Mclaren', 'Chevrolet', 'Ford', 'Aston Martin']
    return sorted([i for i in makes if i.lower().startswith(ctx.value.lower())])


async def list_models(ctx: discord.AutocompleteContext.options):
    make = ctx.options['make']
    models = await car_db.get_models(make)
    return sorted([i for i in models if i.lower().startswith(ctx.value.lower())])


class CarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    car = SlashCommandGroup('car')

    # Showcase at a random show based on location, more popular show = more reward
    @car.command(name='flex', description='Showcase your car')
    async def flex(self, ctx, car_id: discord.Option(str, required=False, default=None)):
        account_id = ctx.author.id
        if car_id is None:
            car_id = await account_db.get_driving_car_id(account_id)
        user_car = await account_db.get_car_for_showcase(account_id, car_id)
        user_car_name, user_car_value, user_car_rating = user_car[0], user_car[1], user_car[2]
        reward = int(math.floor((user_car_value / 10000) + (user_car_rating / 10) ** 2))
        await account_db.add_to_balance(account_id, reward)
        multiplier = random.randint(75, 125) / 100
        description = f'The spectators were awestruck by your {user_car_name}!\nYou earned © {int(math.floor(reward * multiplier))}'
        embed = discord.Embed(color=embed_color, description=description)
        await ctx.respond(embed=embed)

    @car.command(name='tune', description='')
    async def tune(self, ctx: discord.ApplicationContext, car_id):
        account_id = ctx.author.id
        url_and_msrp = await account_db.get_url_and_msrp(account_id, car_id)
        await ctx.respond(embed=await specs_format(account_id, car_id),
                          view=TuneButtons(account_id, car_id, url_and_msrp[0], url_and_msrp[1]))

    @car.command(name='specs', description='')
    async def specs(self, ctx, car_id: discord.Option(int, required=False, default=0)):
        account_id = ctx.author.id
        if car_id == 0:
            car_id = await account_db.get_driving_car_id(account_id)
        car_general_info = await account_db.get_general_info(account_id, car_id)
        if car_general_info is None:
            await ctx.respond(
                embed=discord.Embed(color=embed_color, description=f'You do not own a car with ID: `{car_id}`'))
        (level, rating, quality, top_speed_level, acceleration_level, top_speed_quality, acceleration_quality, year,
         color, image_url, car_name) = \
            car_general_info[0], car_general_info[1], car_general_info[2], car_general_info[3], car_general_info[4], \
            car_general_info[5], car_general_info[6], car_general_info[7], car_general_info[8], car_general_info[9], \
            car_general_info[10]
        user_uses_imperial = await account_db.get_imperial(ctx.author.id)
        embed = discord.Embed(color=embed_color, title=f'**Level {level} {car_name}**')
        embed.set_image(url=f'https://cdn.discordapp.com/attachments/{attachment_channel_id}/' + image_url)
        embed.add_field(name='Details', inline=True,
                        value=f'Performance Rating: `{rating:.2f}`\n'
                              f'Quality: `{quality:.2f}`')
        embed.add_field(name='', inline=True, value='')
        if user_uses_imperial:
            car_performance = await account_db.get_performance_imperial(account_id, car_id)
            embed.add_field(name='Specifications', inline=True,
                            value=f'Power: `{car_performance[2]:,d} hp`\n'
                                  f'Torque: `{car_performance[3]:,d} lb-ft`')
            embed.add_field(name='Top Speed', inline=True,
                            value=f'Top Speed: `{car_performance[0]:.2f} mph`\n'
                                  f'\u2003|\u2003Level: `{top_speed_level}`\n'
                                  f'\u2003|\u2003Quality: `{top_speed_quality:.2f}`')
            embed.add_field(name='', inline=True, value='')
            embed.add_field(name='Acceleration', inline=True,
                            value=f'0-60 mph: `{car_performance[1]:.2f} sec`\n'
                                  f'\u2003|\u2003Level: `{acceleration_level}`\n'
                                  f'\u2003|\u2003Quality: `{acceleration_quality:.2f}`')
        else:
            car_performance = await account_db.get_performance_metric(account_id, car_id)
            embed.add_field(name='Specifications', inline=True,
                            value=f'Power: `{car_performance[2]:,d} ps`\n'
                                  f'Torque: `{car_performance[3]:,d} Nm`')
            embed.add_field(name='Top Speed', inline=True,
                            value=f'Top Speed: `{car_performance[0]:.2f} kph`\n'
                                  f'\u2003|\u2003Level: `{top_speed_level}`\n'
                                  f'\u2003|\u2003Quality: `{top_speed_quality:.2f}`')
            embed.add_field(name='', inline=True, value='')
            embed.add_field(name='Acceleration', inline=True,
                            value=f'0-100 kph: `{car_performance[1]:.2f} sec`\n'
                                  f'\u2003|\u2003Level: `{acceleration_level}`\n'
                                  f'\u2003|\u2003Quality: `{acceleration_quality:.2f}`')
        embed.set_footer(text=f'{year} {car_name} in {color}\nDisplaying Car #{car_id}')
        await ctx.respond(embed=embed)

    @car.command()
    async def add(self, ctx: discord.ApplicationContext,
                  make: discord.Option(str, "Select a car make", autocomplete=list_makes),
                  model: discord.Option(str, "Select a car model", autocomplete=list_models)
                  ):
        account_id = ctx.author.id
        car_name = f'{make} {model}'
        car_quality, top_speed_quality, acceleration_quality = await generate_qualities()
        await account_db.add_to_garage(account_id, car_name, car_quality, top_speed_quality, acceleration_quality)
        await ctx.respond(f'You got a {car_quality} quality car!\n'
                          f'Top speed quality: {top_speed_quality}\n'
                          f'Acceleration quality: {acceleration_quality}')

    @car.command(name='meet', description='')
    async def meet(self, ctx):
        await ctx.respond('meet')

    @car.command(name='paint', description='')
    async def paint(self, ctx):
        await ctx.respond('paint')


def setup(bot):
    bot.add_cog(CarCog(bot))
