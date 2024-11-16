from discord.ext import commands
from discord.commands import SlashCommandGroup
from buttons.buttons import *
from account_database import AccountDatabase

embed_color = 0x9c5ab3
car_db = CarDatabase()
account_db = AccountDatabase()
total_car_count = 7
total_pages = int(math.ceil(total_car_count / 2))


# Remove sell from dealership group
# Add are you sure reaction


async def list_makes(ctx: discord.AutocompleteContext):
    makes = ['Lamborghini', 'Ferrari', 'Mclaren', 'Chevrolet', 'Ford', 'Aston Martin']
    return sorted([i for i in makes if i.lower().startswith(ctx.value.lower())])


async def list_models(ctx: discord.AutocompleteContext.options):
    make = ctx.options['make']
    models = await car_db.get_models(make)
    return sorted([i for i in models if i.lower().startswith(ctx.value.lower())])


class DealershipCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    dealership = SlashCommandGroup('dealership')

    @dealership.command()
    async def view(self, ctx, page: discord.Option(str, required=False, default=1)):
        page_number = int(page)
        dealership_page = await car_db.get_dealership_page(page_number)
        description = ''
        for row in dealership_page:
            description += '**{}**\u2003•\u2003₪ {:,d}\n\n'.format(row[0], row[1])
        embed = discord.Embed(color=embed_color, title='**Trackbite Dealership**', description=description)
        embed.set_footer(text=f'Page {page} of {total_pages}')
        await ctx.respond(embed=embed, view=PageButtons())

    @dealership.command(name="purchase", description="Start a typing race")
    async def purchase(self, ctx: discord.ApplicationContext,
                       make: discord.Option(str, "Select a car make", autocomplete=list_makes),
                       model: discord.Option(str, "Select a car model", autocomplete=list_models)
                       ):
        account_id = ctx.author.id
        car_name = f'{make} {model}'
        car_value = await car_db.get_car_value(car_name)
        embed = discord.Embed(color=embed_color)
        user_balance = await account_db.get_balance(account_id)
        if user_balance < car_value:
            coins_needed = car_value - user_balance
            embed.description = f'You do not have enough coins!\nYou need © {coins_needed:,d} more to purchase the {car_name}'
            await ctx.respond(embed=embed)
        else:
            embed.description = f'Are you sure you want to purchase the {car_name} for © {car_value:,d}?'
            await ctx.respond(embed=embed, view=PurchaseConfirmationButtons(account_id, car_name, car_value, await car_db.get_car_url(car_name)))


def setup(bot):
    bot.add_cog(DealershipCog(bot))
