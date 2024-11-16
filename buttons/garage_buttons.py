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


class GarageButtons(discord.ui.View):
    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    @discord.ui.button(label="🞀🞀", style=discord.ButtonStyle.grey)
    async def double_left(self, button, interaction):
        pass

    @discord.ui.button(label="◀", style=discord.ButtonStyle.grey)
    async def left(self, button, interaction):
        pass

    @discord.ui.button(label="▶", style=discord.ButtonStyle.grey)
    async def right(self, button, interaction):
        pass

    @discord.ui.button(label="🞂🞂", style=discord.ButtonStyle.grey)
    async def double_right(self, button, interaction):
        pass
