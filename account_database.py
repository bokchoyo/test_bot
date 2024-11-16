from decimal import Decimal

import asqlite
from prettytable import PrettyTable
from car_database import CarDatabase
import asyncio


class AccountDatabase:
    def __init__(self, db='account_data.db'):
        self.db = db
        self.car_db = CarDatabase()
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
            print('Returned none from:' + query)
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

    async def create_account_database(self):
        await self.execute_set('''
            CREATE TABLE IF NOT EXISTS accounts (
                id BIGINT PRIMARY KEY,
                username VARCHAR(32),
                imperial BOOLEAN DEFAULT TRUE,
                level TINYINT DEFAULT 0,
                xp BIGINT DEFAULT 0,
                balance BIGINT DEFAULT 0,
                garage_value BIGINT DEFAULT 0,
                inventory_value BIGINT DEFAULT 0,
                location VARCHAR(18) DEFAULT 'United States',
                driving_car_id MEDIUMINT DEFAULT 1,
                commands_sent BIGINT
            );''')

        await self.execute_set('''
            CREATE TABLE garage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                metric_weight SMALLINT,
                in_showroom BOOLEAN DEFAULT FALSE,
                account_id BIGINT,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );''')

        await self.execute_set('''
            CREATE TABLE showroom (
                id INT,
                name VARCHAR(64),
                image_url VARCHAR(80),
                color VARCHAR(32),
                year SMALLINT,
                rating DECIMAL(5,2),
                quality DECIMAL(5,2),
                msrp INT,
                imperial_top_speed DECIMAL(5,2),
                imperial_acceleration DECIMAL(4,2),
                metric_top_speed DECIMAL(5,2),
                metric_acceleration DECIMAL(4,2),
                account_id BIGINT,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );''')

    async def get_account(self, account_id):
        return await self.execute_get('SELECT * FROM accounts WHERE id = ?', account_id)

    async def add_to_garage(self, account_id, car_name):
        car_data = await self.car_db.get_car(car_name)
        await self.execute_set('''
        INSERT INTO garage (name, make, model, trim, year, nationality, urls, tier, rating, value, parts,
                      imperial_top_speed, metric_top_speed, top_speed_rating,
                      imperial_acceleration, metric_acceleration, acceleration_rating,
                      handling, handling_rating, range,
                      imperial_power, metric_power, imperial_torque, metric_torque, imperial_weight, metric_weight,
                      account_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', *car_data, account_id)

    async def get_highest_car_id(self, account_id):
        return await self.execute_get('SELECT COALESCE(MAX(id), 0) FROM garage WHERE account_id = ?;', account_id)

    async def get_lowest_car_id(self, account_id):
        return await self.execute_get('SELECT MIN(id) FROM garage WHERE account_id = ?', account_id)

    async def remove_car(self, account_id, car_id):
        await self.execute_set('DELETE FROM garage WHERE account_id = ? AND id = ?', account_id, car_id)

    async def has_car(self, account_id, car_id):
        car = await self.execute_get('SELECT id FROM garage WHERE account_id = ? AND id = ?', account_id, car_id)
        return True if car else False

    async def get_car_msrp(self, account_id, car_id):
        return await self.execute_get('SELECT msrp FROM garage WHERE account_id = ? AND id = ?;', account_id,
                                      car_id)

    async def get_location(self, account_id):
        return await self.execute_get('SELECT location FROM accounts WHERE id = ?;', account_id)

    async def has_one_car(self, account_id):
        car_count = await self.execute_get('SELECT COUNT(id) FROM garage WHERE account_id = ?;', account_id)
        return True if car_count == 1 else False

    async def get_top_speeds(self, account_id, car_id):
        return await self.execute_get(
            'SELECT imperial_top_speed, metric_top_speed FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def get_top_speed_quality(self, account_id, car_id):
        return await self.execute_get(
            'SELECT top_speed_quality FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id
        )

    async def get_acceleration_quality(self, account_id, car_id):
        return await self.execute_get(
            'SELECT acceleration_quality FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id
        )

    async def get_accelerations(self, account_id, car_id):
        return await self.execute_get(
            'SELECT imperial_acceleration, metric_acceleration FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def get_qualities(self, account_id, car_id):
        return await self.execute_get(
            'SELECT top_speed_quality, acceleration_quality FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def get_top_speed_levels(self, account_id, car_id):
        return await self.execute_get(
            'SELECT level, top_speed_level FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def get_acceleration_levels(self, account_id, car_id):
        return await self.execute_get(
            'SELECT level, acceleration_level FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def get_top_speed_level(self, account_id, car_id):
        return await self.execute_get(
            'SELECT top_speed_level FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def get_acceleration_level(self, account_id, car_id):
        return await self.execute_get(
            'SELECT acceleration_level FROM garage WHERE account_id = ? AND id = ?;',
            account_id, car_id)

    async def upgrade_top_speed(self, account_id, car_id):
        levels = await self.get_top_speed_levels(account_id, car_id)
        top_speed_quality = await self.get_top_speed_quality(account_id, car_id)
        base_top_speeds = await self.car_db.get_top_speeds(await self.get_car_name_by_id(account_id, car_id))
        current_top_speeds = await self.get_top_speeds(account_id, car_id)
        increment = top_speed_quality / 10000
        new_imperial_top_speed = current_top_speeds[0] + (base_top_speeds[0] * increment)
        new_metric_top_speed = current_top_speeds[1] + (base_top_speeds[1] * increment)
        new_level = levels[0] + 1
        new_top_speed_level = levels[1] + 1
        await self.execute_set('''
        UPDATE garage
        SET level = ?, top_speed_level = ?, imperial_top_speed = ?, metric_top_speed = ?
        WHERE account_id = ? and id = ?;''', new_level, new_top_speed_level, new_imperial_top_speed, new_metric_top_speed, account_id, car_id)

    async def upgrade_acceleration(self, account_id, car_id):
        levels = await self.get_acceleration_levels(account_id, car_id)
        acceleration_quality = await self.get_acceleration_quality(account_id, car_id)
        base_accelerations = await self.car_db.get_accelerations(await self.get_car_name_by_id(account_id, car_id))
        current_accelerations = await self.get_accelerations(account_id, car_id)
        increment = acceleration_quality / 10000
        new_imperial_acceleration = current_accelerations[0] - (base_accelerations[0] * increment)
        new_metric_acceleration = current_accelerations[1] - (base_accelerations[1] * increment)
        new_level = levels[0] + 1
        new_acceleration_level = levels[1] + 1
        await self.execute_set('''
                UPDATE garage
                SET level = ?, acceleration_level = ?, imperial_acceleration = ?, metric_acceleration = ?
                WHERE account_id = ? and id = ?;''', new_level, new_acceleration_level, new_imperial_acceleration, new_metric_acceleration, account_id, car_id)

    # async def qualify_car(self, account_id, car_id, car_quality, top_speed_quality, acceleration_quality):
    #     car_name = await self.get_car_name_by_id(account_id, car_id)
    #     car_specs = await self.car_db.get_specifications(car_name)
    #     await self.qualify_base_top_speed(account_id, car_id, top_speed_quality, car_specs[0], car_specs[1])
    #     await self.qualify_base_acceleration(account_id, car_id, acceleration_quality, car_specs[2], car_specs[3])
    #
    # async def qualify_power_and_torque(self, account_id, car_id, car_quality, imperial_power, metric_power, imperial_torque, metric_torque):
    #     pass
    #
    # async def qualify_base_top_speed(self, account_id, car_id, top_speed_quality, imperial_top_speed, metric_top_speed):
    #     multiplier = 1 + ((top_speed_quality - 50) / 500)
    #     new_imperial_top_speed = round(imperial_top_speed * multiplier, 2)
    #     new_metric_top_speed = round(metric_top_speed * multiplier, 2)
    #     await self.execute_set('''
    #     UPDATE garage
    #     SET imperial_top_speed = ?, metric_top_speed = ?
    #     WHERE account_id = ? and id = ?;''', new_imperial_top_speed, new_metric_top_speed, account_id, car_id)
    #
    # async def qualify_base_acceleration(self, account_id, car_id, acceleration_quality, imperial_acceleration, metric_acceleration):
    #     multiplier = 1 + ((acceleration_quality - 50) / 500)
    #     new_imperial_acceleration = round(imperial_acceleration * multiplier, 2)
    #     new_metric_acceleration = round(metric_acceleration * multiplier, 2)
    #     await self.execute_set('''
    #     UPDATE garage
    #     SET imperial_acceleration = ?, metric_acceleration = ?
    #     WHERE account_id = ? and id = ?;''', new_imperial_acceleration, new_metric_acceleration, account_id, car_id)

    async def get_garage_msrp(self, account_id):
        return await self.execute_set('''
        SELECT COALESCE(SUM(garage.msrp), 0) FROM accounts
        LEFT JOIN garage ON accounts.id = garage.account_id
        WHERE accounts.id = ?;
        ''', account_id)

    async def get_garage_size(self, account_id):
        return await self.execute_get('''
        SELECT COALESCE(COUNT(garage.name), 0) FROM accounts
        LEFT JOIN garage ON accounts.id = garage.account_id WHERE accounts.id = ?;
        ''', account_id)

    async def get_garage_list(self, account_id):
        return await self.execute_get_all('''
        SELECT id, name, rating, quality
        FROM garage WHERE account_id = ?;
        ''', account_id)
        # for i, row in enumerate(result):
        #     if row is None:
        #         print(f'{i}: None')
        #     else:
        #         print(f'Garage row {i}: {row}')
        # return result

    async def set_driving_car(self, account_id, car_id):
        await self.execute_set('UPDATE accounts SET driving_car_id = ? WHERE id = ?;', car_id, account_id)

    async def get_balance(self, account_id):
        return await self.execute_get('SELECT balance FROM accounts WHERE id = ?;', account_id)

    async def add_to_balance(self, account_id, amount):
        current_balance = await self.get_balance(account_id)
        await self.execute_set('UPDATE accounts SET balance = ? WHERE id = ?', current_balance + int(amount), account_id)

    async def subtract_from_balance(self, account_id, amount):
        current_balance = await self.get_balance(account_id)
        await self.execute_set('UPDATE accounts SET balance = ? WHERE id = ?', current_balance - amount, account_id)

    async def get_car_name_by_id(self, account_id, car_id):
        return await self.execute_get('SELECT name FROM garage WHERE account_id = ? AND id = ?;', account_id,
                                      car_id)

    async def get_driving_car_id(self, account_id):
        return await self.execute_get('SELECT driving_car_id FROM accounts WHERE id = ?;', account_id)

    async def get_general_info(self, account_id, car_id):
        return await self.execute_get('''
        SELECT level, rating, quality, top_speed_level, acceleration_level, top_speed_quality, acceleration_quality, year, color, image_url, name, msrp
        FROM garage WHERE account_id = ? AND id = ?;
        ''', account_id, car_id)

    async def get_performance_imperial(self, account_id, car_id):
        return await self.execute_get('''
        SELECT imperial_top_speed, imperial_acceleration, imperial_power, imperial_torque
        FROM garage WHERE account_id = ? AND id = ?;
        ''', account_id, car_id)

    async def get_performance_metric(self, account_id, car_id):
        return await self.execute_get('''
        SELECT metric_top_speed, metric_acceleration, metric_power, metric_torque
        FROM garage WHERE account_id = ? AND id = ?;
        ''', account_id, car_id)

    async def get_url_and_msrp(self, account_id, car_id):
        return await self.execute_get('''
        SELECT image_url, msrp
        FROM garage WHERE account_id = ? AND id = ?;
        ''', account_id, car_id)

    async def get_car_for_drag_race(self, account_id):
        return await self.execute_get('''
        SELECT name, rating, tier
        FROM garage WHERE account_id = ? AND id = ?;
        ''', account_id, await self.get_driving_car_id(account_id))

    async def get_car_for_track_race(self, account_id):
        return await self.execute_get('''
        SELECT name, imperial_top_speed, acceleration_rating, handling_rating
        FROM garage WHERE account_id = ? AND id = ?;
        ''', account_id, await self.get_driving_car_id(account_id))

    async def get_car_for_sell(self, account_id, car_id):
        return await self.execute_get('SELECT name, msrp FROM garage WHERE account_id = ? AND id = ?;',
                                      account_id, car_id)

    async def get_car_for_showcase(self, account_id, car_id):
        return await self.execute_get('SELECT name, msrp, rating FROM garage WHERE account_id = ? AND id = ?;',
                                      account_id, car_id)

    async def create_account(self, account_id, username):
        await self.execute_set('INSERT INTO accounts (id, username) VALUES (?, ?);', account_id, username)

    async def get_imperial(self, account_id):
        return await self.execute_get('SELECT imperial FROM accounts WHERE id = ?;', account_id)

    async def set_imperial(self, account_id, boolean):
        await self.execute_set('UPDATE accounts SET imperial = ? WHERE id = ?;', boolean, account_id)

    async def print_garage_table(self):
        query_columns = "PRAGMA table_info(garage);"
        columns_info = await self.execute_get_all(query_columns)

        if not columns_info:
            print("Error: Unable to retrieve column information.")
            return

        column_names = [column[1] for column in columns_info]

        query_data = f'SELECT {", ".join(column_names)} FROM garage;'
        result = await self.execute_get_all(query_data)

        if result:
            table = PrettyTable()
            table.field_names = column_names

            for row in result:
                table.add_row(row)

            print(table)
        else:
            print("No data found in the garage table.")
