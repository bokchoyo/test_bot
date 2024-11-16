import math

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from car_database import CarDatabase
from account_database import AccountDatabase

car_db = CarDatabase()
account_db = AccountDatabase()
embed_color = 0x9c5ab3


class GarageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(GarageCog(bot))
