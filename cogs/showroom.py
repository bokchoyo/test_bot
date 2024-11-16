import math

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from car_database import CarDatabase
from account_database import AccountDatabase

car_db = CarDatabase()
account_db = AccountDatabase()
embed_color = 0x9c5ab3


async def list_makes(ctx: discord.AutocompleteContext):
    makes = ['Lamborghini', 'Ferrari', 'Mclaren', 'Chevrolet', 'Ford', 'Aston Martin']
    return sorted([i for i in makes if i.lower().startswith(ctx.value.lower())])


async def list_models(ctx: discord.AutocompleteContext.options):
    make = ctx.options['make']
    models = await car_db.get_models(make)
    return sorted([i for i in models if i.lower().startswith(ctx.value.lower())])


class ShowroomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    showroom = SlashCommandGroup('showroom', default='view', invoke_without_command=True)

    # Showcase at a random show based on location, more popular show = more reward
    @showroom.command(name='add', description='')
    async def add(self, ctx):
        await ctx.respond('add')

    @showroom.command(name='remove', description='')
    async def remove(self, ctx):
        await ctx.respond('remove')

    @showroom.command(name='view', description='')
    async def view(self, ctx, user: commands.MemberConverter = None):
        if user is not None:
            account_id = user.id
        else:
            account_id = ctx.author.id
        await ctx.respond(f'view: {account_id}')


def setup(bot):
    bot.add_cog(ShowroomCog(bot))
