import asyncio

import asqlite
import re


def extract_car_name_from_url(image_url):
    car_name = re.search(r'/([^/]+)_([^_/]+)\.', image_url)
    if car_name:
        return car_name.group(1).replace("_", " ")
    else:
        return ""


class CarDatabase:
    def __init__(self, db='car_data.db'):
        self.db = db
        self.pool = None

    async def get_pool(self):
        if self.pool is None:
            self.pool = await asqlite.create_pool(self.db)
        return self.pool

    async def execute_get(self, query, *args):
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchone()
        if result:
            # return result if (',' or '*') in query.split("SELECT")[1].split("FROM")[0] else result[0]
            selection = query.split("SELECT")[1].split("FROM")[0]
            if (',' in selection or '*' in selection) and ('COALESCE' not in selection) and ('COUNT' not in selection):
                print(f'Returned entire result {result} from:\n' + query)
                return result
            else:
                print(f'Returned top result {result[0]} from:\n' + query)
                return result[0]
        else:
            print('Returned None from:' + query)
            return None

    async def execute_get_all(self, query, *args):
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchall()
        if result:
            print(f'Returned entire result ({result}) from:\n' + query)
            return result
        else:
            print('Returned none from:' + query)
            return None

    async def execute_set(self, query, *args):
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                await conn.commit()

    async def get_car(self, car_name):
        return await self.execute_get('SELECT * FROM cars WHERE name = ?', car_name)
        # print(len(result))
        # for row in result:
        #     print(row)
        # return result

    async def get_total_car_count(self):
        return await self.execute_get('SELECT COUNT(*) FROM cars')

    async def has_car(self, car_name):
        car = await self.execute_get('SELECT name FROM cars WHERE name = ?;', car_name)
        return True if car else False

    async def get_general_info(self, car_name):
        return await self.execute_get('''
        SELECT image_url, color, year, rating, value, tier, part_count
        FROM cars WHERE name = ?;
        ''', car_name)

    async def get_performance_imperial(self, car_name):
        return await self.execute_get('''
        SELECT imperial_top_speed, imperial_acceleration, imperial_power, imperial_torque, imperial_weight
        FROM cars WHERE name = ?;
        ''', car_name)

    async def get_performance_metric(self, car_name):
        return await self.execute_get('''
        SELECT metric_top_speed, metric_acceleration, metric_power, metric_torque, metric_weight
        FROM cars WHERE name = ?;
        ''', car_name)

    async def get_dealership_page(self, page):
        return await self.execute_get_all('''
        SELECT name, value
        FROM cars LIMIT 2 OFFSET ?;
        ''', 2 * (page - 1))

    async def get_car_for_drag_race(self, tier):
        return await self.execute_get('''
        SELECT name, rating
        FROM cars WHERE tier = ?
        ORDER BY RANDOM() LIMIT 1;
        ''', tier)

    async def add_car(self, name, make, model, trim, year, nationality, urls, tier, rating, value, parts,
                      imperial_top_speed, metric_top_speed, top_speed_rating,
                      imperial_acceleration, metric_acceleration, acceleration_rating,
                      handling, handling_rating, range,
                      imperial_power, metric_power, imperial_torque, metric_torque, imperial_weight, metric_weight):
        await self.execute_set('''
        INSERT INTO cars (name, make, model, trim, year, nationality, urls, tier, rating, value, parts,
                      imperial_top_speed, metric_top_speed, top_speed_rating,
                      imperial_acceleration, metric_acceleration, acceleration_rating,
                      handling, handling_rating, range,
                      imperial_power, metric_power, imperial_torque, metric_torque, imperial_weight, metric_weight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', name, make, model, trim, year, nationality, urls, tier, rating, value, parts,
                               imperial_top_speed, metric_top_speed, top_speed_rating,
                               imperial_acceleration, metric_acceleration, acceleration_rating,
                               handling, handling_rating, range,
                               imperial_power, metric_power, imperial_torque, metric_torque, imperial_weight,
                               metric_weight)

    async def get_specifications(self, car_name):
        return await self.execute_get(
            'SELECT imperial_top_speed, metric_top_speed, imperial_acceleration, metric_acceleration,'
            'imperial_power, metric_power, imperial_toque, metric_torque FROM cars WHERE name = ?;', car_name)

    async def get_top_speeds(self, car_name):
        return await self.execute_get('SELECT imperial_top_speed, metric_top_speed FROM cars WHERE name = ?;', car_name)

    async def get_accelerations(self, car_name):
        return await self.execute_get('SELECT imperial_acceleration, metric_acceleration FROM cars WHERE name = ?;',
                                      car_name)

    async def get_models(self, make):
        result = await self.execute_get_all('SELECT DISTINCT model FROM cars WHERE make = ?;', make)
        result_list = [row[0] for row in result]
        return result_list

    async def get_car_value(self, car_name):
        return await self.execute_get('SELECT value FROM cars WHERE name = ?;', car_name)

    async def get_car_url(self, car_name):
        return await self.execute_get('SELECT image_url FROM cars WHERE name = ?;', car_name)

    async def get_name_from_row(self, row_index):
        return await self.execute_get('SELECT name FROM cars LIMIT 1 OFFSET ?', row_index)

    async def set_image_urls(self, image_urls):
        cars = await self.get_total_car_count()

        for image_url in image_urls:
            # Iterate through all car names until a match is found
            for car_index in range(cars):
                car_name = await self.get_name_from_row(car_index)

                if car_name:
                    # Extract car name from the image URL
                    car_name_from_url = extract_car_name_from_url(image_url)

                    # Check if extracted car name matches the actual car name
                    if car_name_from_url.lower().replace("_", " ") == car_name.lower():
                        # Set image URL for the car
                        await self.set_image_url(car_name, image_url)
                        break  # Break the inner loop once a match is found

            # If no match is found, print an error message
            else:
                print(f"Error: No matching car name found for image URL '{image_url}'.")

    async def set_image_url(self, car_name, image_url):
        await self.execute_set('UPDATE cars SET image_url = ? WHERE name = ?', image_url, car_name)
        print(f'Successfully set {car_name} url as {image_url}')

    async def create_car_database(self):
        await self.execute_set('''
        CREATE TABLE IF NOT EXISTS cars (
            name VARCHAR(64),
            make VARCHAR(32),
            model VARCHAR(32),
            trim VARCHAR(64),
            year SMALLINT,
            nationality VARCHAR(32),
            urls VARCHAR(80),
            tier VARCHAR(1),
            rating DECIMAL(5,2),
            value INT,
            parts TINYINT,
            imperial_top_speed DECIMAL(5,2),
            metric_top_speed DECIMAL(5,2),
            top_speed_rating DECIMAL(5,2),
            imperial_acceleration DECIMAL(4,2),
            metric_acceleration DECIMAL(4,2),
            acceleration_rating DECIMAL(5,2),
            handling DECIMAL(3,2),
            handling_rating DECIMAL(5,2),
            range SMALLINT,
            imperial_power SMALLINT,
            metric_power SMALLINT,
            imperial_torque SMALLINT,
            metric_torque SMALLINT,
            imperial_weight SMALLINT,
            metric_weight SMALLINT
        );''')
