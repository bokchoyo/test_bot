import math
import time

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from car_database import CarDatabase
from account_database import AccountDatabase
from buttons.race_buttons import *

car_db = CarDatabase()
account_db = AccountDatabase()
embed_color = 0x9c5ab3


class RaceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    race = SlashCommandGroup('race')

    @race.command(name="track", description="Race")
    async def track(self, ctx):
        account_id = ctx.author.id
        attachment_head = 'https://cdn.discordapp.com/attachments/1078045767262023740/'
        car_data = await account_db.get_car_for_track_race(account_id)
        embed = discord.Embed(color=embed_color, title='Race', description=f'Car: {car_data[0]}\nSpeed: 0 MPH')
        if not await account_db.get_imperial(account_id):
            embed.description = f'Car: {car_data[0]}\nSpeed: 0 KPH'
        embed.set_image(url=(attachment_head + '1206647698866835466/1.png'))
        interaction = await ctx.respond(embed=embed, view=DisabledRaceButtons())
        for i, image in enumerate(['1206647702117556294/2.png',
                                   '1206647704051261440/3.png',
                                   '1206647705473122355/4.png',
                                   '1206647706999726140/5.png',
                                   '1206647710078476369/6.png']):
            await asyncio.sleep(max(0, 1 - self.bot.latency * 2))
            embed.set_image(url=(attachment_head + image))
            await interaction.edit_original_response(embed=embed)
        await asyncio.sleep(random.randint(10, 30) / 10)
        embed.set_image(url=(attachment_head + '1206647698866835466/1.png'))
        await interaction.edit_original_response(embed=embed, view=RaceButtons(embed, account_id, car_data[0],
                                                                               car_data[1], car_data[2], car_data[3]))

    @race.command(name="drag", description="Compete in a drag race")
    async def drag(self, ctx):
        user_car = await account_db.get_car_for_drag_race(ctx.author.id)
        opponent_car = await car_db.get_car_for_drag_race(user_car[2])
        user_car_name = user_car[0]
        user_car_rating = user_car[1]
        opponent_car_name = opponent_car[0]
        opponent_car_rating = opponent_car[1]
        if user_car_rating > opponent_car_rating:
            reward = int(math.floor(opponent_car_rating ** 2 / 20))
            margin_reward = int(math.floor(user_car_rating ** 2 / 20))
            description = f'Congratulations {ctx.author.mention}! You beat a {opponent_car_name} and won `₪ {reward + margin_reward}`!'
        elif user_car_rating < opponent_car_rating:
            description = f'You unfortunately lost to a {opponent_car_name} {ctx.author.mention}. Better luck next time!'
        else:
            reward = int(math.floor(opponent_car_rating ** 2 / 20))
            description = f'What a close race {ctx.author.mention}! You tied with a {opponent_car_name} and won `₪ {reward}`!'
        embed = discord.Embed(color=embed_color, title=f"{ctx.author.name}'s Drag Race", description=description)
        await ctx.respond(embed=embed)

    @race.command(name="typing", description="Start a typing race")
    async def typing(self, ctx):
        await ctx.respond("Get ready to type! The typing race begins now.")


def setup(bot):
    bot.add_cog(RaceCog(bot))
