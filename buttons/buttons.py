import discord
from car_database import CarDatabase
import math
from account_database import AccountDatabase
import asyncio
import random

car_db = CarDatabase()
account_db = AccountDatabase()
embed_color = 0x9c5ab3
total_car_count = 7
total_pages = int(math.ceil(total_car_count / 2))
attachment_channel_id = '1078045767262023740'


async def generate_qualities():
    top_speed_quality = round(100 * sum([random.randint(0, 7) for _ in range(4)]) / 32, 2)
    acceleration_quality = round(100 * sum([random.randint(0, 7) for _ in range(4)]) / 32, 2)
    car_quality = round((top_speed_quality + acceleration_quality) / 2, 2)
    return car_quality, top_speed_quality, acceleration_quality


class PageButtons(discord.ui.View):
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="◀")
    async def page_back(self, button, interaction):
        current_page = int(interaction.message.embeds[0].footer.text.split()[1])
        previous_page = max(1, current_page - 1)
        dealership_page = await car_db.get_dealership_page(previous_page)
        description = ''
        for row in dealership_page:
            description += '**{}**\u2003•\u2003₪ {:,d}\n\n'.format(row[0], row[1])
        embed = discord.Embed(color=embed_color, title=f'**Trackbite Dealership**', description=description)
        embed.set_footer(text=f'Page {previous_page} of {total_pages}')
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="▶")
    async def page_next(self, button, interaction):
        current_page = int(interaction.message.embeds[0].footer.text.split()[1])
        next_page = min(total_pages, current_page + 1)
        dealership_page = await car_db.get_dealership_page(next_page)
        description = ''
        for row in dealership_page:
            description += '**{}**\u2003•\u2003₪ {:,d}\n\n'.format(row[0], row[1])
        embed = discord.Embed(color=embed_color, title=f'**Trackbite Dealership**', description=description)
        embed.set_footer(text=f'Page {next_page} of {total_pages}')
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()


class SellConfirmationButtons(discord.ui.View):
    def __init__(self, account_id, car_id, car_name, car_sell_value):
        super().__init__()
        self.account_id = account_id
        self.car_id = car_id
        self.car_name = car_name
        self.car_sell_value = car_sell_value

    @discord.ui.button(style=discord.ButtonStyle.green, label="Yes", custom_id="confirm_sell")
    async def confirm_button(self, button, interaction):
        try:
            await account_db.add_to_balance(self.account_id, self.car_sell_value)
            await account_db.remove_car(self.account_id, self.car_id)
            if await account_db.get_driving_car_id(self.account_id) == self.car_id:
                await account_db.set_driving_car(self.account_id, await account_db.get_lowest_car_id(self.account_id))
            await interaction.message.edit(embed=discord.Embed(color=embed_color,
                                                               description=f'You sold your `#{self.car_id} {self.car_name}` for ₪ {self.car_sell_value:,d}!',),
                                           view=None)
            await interaction.response.defer()
        except asyncio.TimeoutError:
            self.cancel_button(self, button, interaction)

    @discord.ui.button(style=discord.ButtonStyle.red, label="No", custom_id="cancel_sell")
    async def cancel_button(self, button, interaction):
        try:
            await interaction.message.edit(embed=discord.Embed(color=embed_color,
                                                               description='Aborted.'),
                                           view=None)
            await interaction.response.defer()
        except asyncio.TimeoutError:
            self.cancel_button(self, button, interaction)


class PurchaseConfirmationButtons(discord.ui.View):
    def __init__(self, account_id, car_name, car_price, car_url):
        super().__init__()
        self.account_id = account_id
        self.car_name = car_name
        self.car_price = car_price
        self.car_url = car_url

    @discord.ui.button(style=discord.ButtonStyle.green, label="Yes", custom_id="confirm_sell")
    async def confirm_button(self, button, interaction):
        try:
            embed = discord.Embed(color=embed_color, description=f'Congratulations <@{self.account_id}>\nYou purchased the {self.car_name}!')
            embed.set_footer(text='Enjoy your new ride!')
            embed.set_image(url=f'https://cdn.discordapp.com/attachments/{attachment_channel_id}/' + self.car_url)
            car_qualities = await generate_qualities()
            await interaction.message.edit(embed=embed, view=None)
            await interaction.response.defer()
            await account_db.subtract_from_balance(self.account_id, self.car_price)
            await account_db.add_to_garage(self.account_id, self.car_name, car_qualities[0], car_qualities[1], car_qualities[2])
        except asyncio.TimeoutError:
            self.cancel_button(self, button, interaction)

    @discord.ui.button(style=discord.ButtonStyle.red, label="No", custom_id="cancel_sell")
    async def cancel_button(self, button, interaction):
        try:
            await interaction.message.edit(embed=discord.Embed(color=embed_color,
                                                               description='Aborted.'),
                                           view=None)
            await interaction.response.defer()
        except asyncio.TimeoutError:
            self.cancel_button(self, button, interaction)


async def specs_format(account_id, car_id):
    car_general_info = await account_db.get_general_info(account_id, car_id)
    level, rating, quality, top_speed_level, acceleration_level, top_speed_quality, acceleration_quality, year, color, image_url, car_name = \
        car_general_info[0], car_general_info[1], car_general_info[2], car_general_info[3], car_general_info[4], \
            car_general_info[5], car_general_info[6], car_general_info[7], car_general_info[8], car_general_info[9], car_general_info[10]
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


import asyncio

class TuneButtons(discord.ui.View):
    def __init__(self, account_id, car_id, car_url, car_msrp):
        super().__init__()
        self.account_id = account_id
        self.car_id = car_id
        self.tune_cost = round(car_msrp / 100)
        self.car_url = car_url

        self.children[0].label = f'Upgrade Top Speed (© {self.tune_cost})'
        self.children[1].label = f'Upgrade Acceleration (© {self.tune_cost})'

    @discord.ui.button(style=discord.ButtonStyle.green, custom_id="tune_top_speed")
    async def tune_top_speed(self, button, interaction):
        await account_db.upgrade_top_speed(self.account_id, self.car_id)
        button.label = f'Upgrade Top Speed (© {self.tune_cost})'
        if await account_db.get_top_speed_level(self.account_id, self.car_id) == 10:
            button.disabled = True
        else:
            await account_db.subtract_from_balance(self.account_id, self.tune_cost)
        await interaction.message.edit(embed=await specs_format(self.account_id, self.car_id), view=self)
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.green, custom_id="tune_acceleration")
    async def tune_acceleration(self, button, interaction):
        await account_db.upgrade_acceleration(self.account_id, self.car_id)
        button.label = f'Upgrade Acceleration (© {self.tune_cost})'
        if await account_db.get_acceleration_level(self.account_id, self.car_id) == 10:
            button.disabled = True
        else:
            await account_db.subtract_from_balance(self.account_id, self.tune_cost)
        await interaction.message.edit(embed=await specs_format(self.account_id, self.car_id), view=self)
        await interaction.response.defer()
