import re

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
url_head = 'https://cdn.discordapp.com/attachments/1078045767262023740/'


class RaceButtons(discord.ui.View):
    def __init__(self, embed, account_id, car_name, top_speed, acceleration_rating, handling_rating):
        super().__init__()
        self.embed = embed
        self.account_id = account_id
        self.car_name = car_name
        self.top_speed = top_speed
        self.acceleration_rating = acceleration_rating
        self.handling_rating = handling_rating
        self.track = [
            ['', '1206663189182292028/1.png', '1206663190935502908/2.png'],
            ['1206663196409069610/5.png', '1206663194458857542/4.png', '1206663192621752331/3.png'],
            ['1206663199433428992/6.png', '1206663201123475486/7.png', '']
        ]
        self.row = 0
        self.column = 0

    async def finish_race(self, interaction, car_name, speed, unit):
        prize = random.randint(1000, 2000)
        await account_db.add_to_balance(self.account_id, prize)
        await interaction.message.edit(
            embed=discord.Embed(title='Racetrack', description=f'Car: {car_name}\n'
                                                               f'Speed: {speed} {unit}\n'
                                                               f'You finished the race and won © {prize}!',
                                color=embed_color),
            view=None)

    async def accelerate(self, speed):
        return speed + ((self.top_speed - speed) / 3) * (self.acceleration_rating / 100) ** 2

    async def brake(self, speed):
        return (2 * speed / 3) * (self.handling_rating / 100) ** 2

    async def corner(self, speed):
        return speed * (2 - self.handling_rating / 100) ** 2

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank1(self, button, interaction):
        pass

    @discord.ui.button(custom_id="up", label="", style=discord.ButtonStyle.primary, emoji="🔼")
    async def up(self, button, interaction):
        self.embed.description = 'You crashed!'
        self.embed.set_image(url=None)
        await interaction.message.edit(embed=self.embed)
        await interaction.response.defer()

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank2(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank3(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank4(self, button, interaction):
        pass

    @discord.ui.button(custom_id="left", label="", style=discord.ButtonStyle.primary, emoji="◀️")
    async def left(self, button, interaction):
        coordinates = (self.row, self.column)
        if coordinates in ((1, 2), (1, 1)):
            description = self.embed.description
            unit = description.split()[-1]
            current_speed = float(re.search(r'\d+\.?\d*', description[::-1]).group()[::-1])
            if coordinates == (1, 2):
                new_speed = await self.accelerate(current_speed)
            else:
                new_speed = self.brake(current_speed)
            self.embed.description = f'Car: {self.car_name}\nSpeed: {round(new_speed, 1)} {unit}'
            self.column -= 1
            self.embed.set_image(url=(url_head + self.track[self.row][self.column]))
            print(url_head + self.track[self.row][self.column])
            await interaction.message.edit(embed=self.embed)
        else:
            await interaction.message.edit(
                embed=discord.Embed(title='Racetrack', description='You crashed!', color=embed_color), view=None)
        await interaction.response.defer()

    @discord.ui.button(custom_id="down", label="", style=discord.ButtonStyle.primary, emoji="🔽")
    async def down(self, button, interaction):
        coordinates = (self.row, self.column)
        if coordinates in ((0, 2), (1, 0)):
            description = self.embed.description
            unit = description.split()[-1]
            current_speed = float(re.search(r'\d+\.?\d*', description[::-1]).group()[::-1])
            new_speed = current_speed * (2 - self.handling_rating / 100) ** 2
            self.embed.description = f'Car: {self.car_name}\nSpeed: {round(new_speed, 1)} {unit}'
            self.row += 1
            self.embed.set_image(url=(url_head + self.track[self.row][self.column]))
            print(url_head + self.track[self.row][self.column])
            await interaction.message.edit(embed=self.embed)
        else:
            await interaction.message.edit(
                embed=discord.Embed(title='Racetrack', description='You crashed!', color=embed_color), view=None)
        await interaction.response.defer()

    @discord.ui.button(custom_id='right', label='', style=discord.ButtonStyle.primary, emoji='▶️')
    async def right(self, button, interaction):
        coordinates = (self.row, self.column)
        if coordinates in ((0, 0), (0, 1), (2, 0), (2, 1)):
            description = self.embed.description
            unit = description.split()[-1]
            current_speed = float(re.search(r'\d+\.?\d*', description[::-1]).group()[::-1])
            if coordinates in ((2, 0), (2, 1)):
                new_speed = current_speed + ((self.top_speed - current_speed) / 3) * (self.acceleration_rating / 100) ** 2
                if coordinates == (2, 1):
                    await self.finish_race(interaction, self.car_name, round(new_speed, 1), unit)
                    return
            elif coordinates == (0, 0):
                new_speed = (3 * self.top_speed / 4) * (self.acceleration_rating / 100) ** 2
            else:
                new_speed = (2 * current_speed / 3) * (self.handling_rating / 100) ** 2
            self.embed.description = f'Car: {self.car_name}\nSpeed: {round(new_speed, 1)} {unit}'
            self.column += 1
            self.embed.set_image(url=(url_head + self.track[self.row][self.column]))
            print(url_head + self.track[self.row][self.column])
            await interaction.message.edit(embed=self.embed)
        else:
            await interaction.message.edit(
                embed=discord.Embed(title='Racetrack', description='You crashed!', color=embed_color), view=None)
        await interaction.response.defer()

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank5(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank6(self, button, interaction):
        pass


class DisabledRaceButtons(discord.ui.View):
    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank1(self, button, interaction):
        pass

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="🔼", disabled=True)
    async def up(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank2(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank3(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank4(self, button, interaction):
        pass

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="◀️", disabled=True)
    async def left(self, button, interaction):
        pass

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="🔽", disabled=True)
    async def down(self, button, interaction):
        pass

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="▶️", disabled=True)
    async def right(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank5(self, button, interaction):
        pass

    @discord.ui.button(label="-", style=discord.ButtonStyle.grey, disabled=True)
    async def blank6(self, button, interaction):
        pass