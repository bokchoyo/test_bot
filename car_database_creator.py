from car_database import CarDatabase
import asyncio

car_db = CarDatabase()

asyncio.run(car_db.create_car_database())
