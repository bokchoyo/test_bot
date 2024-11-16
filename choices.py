import random
import math
from database import Database


user_db = Database('account_data.json')
car_list = Database('car_list.json')


def choose_car_r(authorid):
    count = 0
    while random.randint(1, 100) <= 80 + math.floor(user_db.get_key(['account data', str(authorid), 'level']) / 10):
        count += 1
    return random.choice(car_list.get_key(['cars', 'r'])), count


def choose_car_s(authorid):
    count = 0
    while random.randint(1, 100) <= 80 + math.floor(user_db.get_key(['account data', str(authorid), 'level']) / 10):
        count += 1
    return random.choice(car_list.get_key(['cars', 's'])), count


def choose_car_a(authorid):
    user_level = user_db.get_key(['account data', str(authorid), 'level'])
    count = 0
    if user_level < 60:
        while random.randint(1, 100) <= 60 + 5 * (math.floor(user_level / 10)):
            count += 1
    else:
        while random.randint(1, 100) <= 80 + user_level / 10:
            count += 1
    return random.choice(car_list.get_key(['cars', 'a'])), count


def choose_car_b(authorid):
    user_level = user_db.get_key(['account data', str(authorid), 'level'])
    count = 0
    if user_level < 60:
        while random.randint(1, 100) <= 60 + 5 * (math.floor(user_level / 10)):
            count += 1
    else:
        while random.randint(1, 100) <= 80 + user_level / 10:
            count += 1
    return random.choice(car_list.get_key(['cars', 'b'])), count


def choose_car_c(authorid):
    user_level = user_db.get_key(['account data', str(authorid), 'level'])
    count = 0
    if 20 <= user_level < 60:
        while random.randint(1, 100) <= 60 + 5 * (math.floor(user_level / 10)):
            count += 1
    elif user_level < 20:
        while random.randint(1, 100) <= 60:
            count += 1
    else:
        while random.randint(1, 100) <= 80 + user_level / 10:
            count += 1
    return random.choice(car_list.get_key(['cars', 'c'])), count


def choose_car_d(authorid):
    user_level = user_db.get_key(['account data', str(authorid), 'level'])
    count = 0
    if 20 <= user_level < 60:
        while random.randint(1, 100) <= 60 + 5 * (math.floor(user_level / 10)):
            count += 1
    elif user_level < 20:
        while random.randint(1, 100) <= 50 + 10 * (math.floor(user_level / 10)):
            count += 1
    else:
        while random.randint(1, 100) <= 80 + user_level / 10:
            count += 1
    return random.choice(car_list.get_key(['cars', 'd'])), count


def choose_car_f(authorid, win):
    user_level = user_db.get_key(['account data', str(authorid), 'level'])
    count = 0
    if win:
        if user_level < 20:
            repeat_chance = 50 + 10 * (math.floor(user_level / 10))
        elif 20 <= user_level < 60:
            repeat_chance = 60 + 5 * (math.floor(user_level / 10))
        else:
            repeat_chance = 80 + user_level / 10
    else:
    while random.randint(1, 100) <= repeat_chance:
                count += 1
    return random.choice(car_list.get_key(['cars', 'f'])), count


def user0x(authorid, win):
    i = random.randint(1, 100)
    if win:
        if i <= 75:
            choose_car_d(authorid) # 75%
        else:
            choose_car_f(authorid) # 25%
    if not win:
        if random.randint(1, 100) <= 20:
            if i <= 25:
                choose_car_d(authorid) # 25%
            else:
                choose_car_f(authorid) # 75%


def user1x(authorid, win):
    i = random.randint(1, 100)
    if win:
        if i <= 20:
            choose_car_c(authorid) # 20%
        elif 20 < i <= 80:
            choose_car_d(authorid) # 60%
        else:
            choose_car_f(authorid) # 20%
    if not win:
        if i <= 10:
            choose_car_c(authorid) # 10%
        elif 10 < i <= 40:
            choose_car_d(authorid) # 30%
        else:
            choose_car_f(authorid) # 60%


def user2x(authorid, win):
    i = random.randint(1, 100)
    if win:
        if i <= 5:
            choose_car_b(authorid)
        elif 5 < i <= 20:
            choose_car_c(authorid)
        elif 20 < i <= 80:
            choose_car_d(authorid)
        else:
            choose_car_f(authorid)
    if not win:
        if i <= 10:
            choose_car_c(authorid)
        elif 10 < i <= 40:
            choose_car_d(authorid)
        else:
            choose_car_f(authorid)


def user3x(authorid):


def user4x(authorid):


def user5x(authorid):


def user6x(authorid):


def user7x(authorid):


def user8x(authorid):


def user9x(authorid):


def userxxx(authorid):