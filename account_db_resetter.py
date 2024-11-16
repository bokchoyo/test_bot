from account_database import AccountDatabase
import asyncio
import random

table = AccountDatabase()


# async def generate_qualities():
#     top_speed_quality = round(100 * sum([random.randint(0, 7) for _ in range(4)]) / 32, 2)
#     acceleration_quality = round(100 * sum([random.randint(0, 7) for _ in range(4)]) / 32, 2)
#     car_quality = round((top_speed_quality + acceleration_quality) / 2, 2)
#     return car_quality, top_speed_quality, acceleration_quality


async def update():
    await table.create_account_database()
    await table.create_account(783282103374053417, 'bokchoyo.')
    await table.add_to_garage(783282103374053417, 'Koenigsegg One:1')
    await table.add_to_garage(783282103374053417, 'Koenigsegg Gemera')
asyncio.run(update())
