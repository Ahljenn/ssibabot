from enum import Enum
import random

cheap_cost = 3_333_333
black_cost = 2_000_000_000
sweet_cost = 2_500_000_000
dream_cost = 150_000_000
petite_cost = 20_000_000_000
key_cost = 5_000_000_000
cookie_cost = 1_600_000
water_cost = 60_000_000
mp_ratio = 17 * .95


class Items(Enum):
    CHEAP = 0
    BLACK = 1
    SWEET = 2
    DREAM = 3
    PETITE = 4
    COOKIE = 5
    WATER = 6
    KEY = 7


class WispRewards(Enum):
    CHEAP = Items.CHEAP
    COOKIE = Items.COOKIE
    WATER = Items.WATER
    BLACK = Items.BLACK


class BlackBlackRewards(Enum):
    SWEET = Items.SWEET
    PETITE = Items.PETITE
    KEY = Items.KEY


class SweetBlackRewards(Enum):
    DREAM = Items.DREAM
    PETITE = Items.PETITE
    KEY = Items.KEY


wonderberry_distribution = [(WispRewards.CHEAP, 0.60),
                            (WispRewards.COOKIE, 0.75),
                            (WispRewards.WATER, 0.90),
                            (WispRewards.BLACK, 1.00)]
black_black_distribution = [(BlackBlackRewards.SWEET, 0.864),
                            (BlackBlackRewards.PETITE, 0.960),
                            (BlackBlackRewards.KEY, 1.000)]
sweet_black_distribution = [(SweetBlackRewards.DREAM, 0.756),
                            (SweetBlackRewards.PETITE, 0.960),
                            (SweetBlackRewards.KEY, 1.000)]

nx_cost = int()
packs = int()
mp_balance = int()
mesos = int()
cheaps = int()
blacks = int()
sweets = int()
dreams = int()
petites = int()
cookies = int()
waters = int()
keys = int()


def init():
    global nx_cost
    global packs
    global mp_balance
    global mesos
    global cheaps
    global blacks
    global sweets
    global dreams
    global petites
    global cookies
    global waters
    global keys
    nx_cost = 0
    packs = 0
    mp_balance = 0
    mesos = 0
    cheaps = 0
    blacks = 0
    sweets = 0
    dreams = 0
    petites = 0
    cookies = 0
    waters = 0
    keys = 0


def find_item(roll, distribution):
    for t in distribution:
        if roll <= t[1]:
            return t[0]
    raise Exception(f"Unable to find the correct item given roll={roll}")


def open():
    global nx_cost
    global packs
    global wonderberry_distribution
    global cheaps
    global cookies
    global waters
    global blacks
    nx_cost += 36_000
    packs += 1
    PACK_SIZE = 10
    for i in range(PACK_SIZE):
        roll = random.uniform(0.0, 1.0)
        item = find_item(roll, wonderberry_distribution)
        if item == WispRewards.CHEAP:
            cheaps += 1
        elif item == WispRewards.COOKIE:
            cookies += 10
        elif item == WispRewards.WATER:
            waters += 1
        else:
            blacks += 1


def fuse_sweet_black():
    global sweets
    global blacks
    global dreams
    global petites
    global keys
    sweets -= 1
    blacks -= 1
    roll = random.uniform(0.0, 1.0)
    item = find_item(roll, sweet_black_distribution)
    if item == SweetBlackRewards.DREAM:
        dreams += 1
    elif item == SweetBlackRewards.PETITE:
        petites += 1
    else:
        keys += 1


def fuse_black_black():
    global blacks
    global sweets
    global petites
    global keys
    blacks -= 2
    roll = random.uniform(0.0, 1.0)
    item = find_item(roll, black_black_distribution)
    if item == BlackBlackRewards.SWEET:
        sweets += 1
    elif item == BlackBlackRewards.PETITE:
        petites += 1
    else:
        keys += 1


def fuse():
    global blacks
    global sweets
    global nx_cost
    while (sweets >= 1 and blacks >= 1) or (blacks >= 2):
        nx_cost += 3_900
        if (sweets >= 1):
            fuse_sweet_black()
        else:
            fuse_black_black()


def sell_not_petite():
    global mesos
    global cheaps
    global blacks
    global sweets
    global dreams
    global petites
    global keys
    global cookies
    global waters
    global mp_balance
    global mp_ratio
    if cheaps > 0:
        mesos += cheaps * cheap_cost
    if blacks > 0:
        mesos += blacks * black_cost
    if sweets > 0:
        mesos += sweets * sweet_cost
    if dreams > 0:
        mesos += dreams * dream_cost
    if keys > 0:
        mesos += keys * key_cost
    if cookies > 0:
        mesos += cookies * cookie_cost
    if waters > 0:
        mesos += waters * water_cost
    mp_balance = mesos / 1_000_000 * mp_ratio


def sell_not_black():
    global mesos
    global cheaps
    global blacks
    global sweets
    global dreams
    global petites
    global keys
    global cookies
    global waters
    global mp_balance
    global mp_ratio
    if cheaps > 0:
        mesos += cheaps * cheap_cost
    if sweets > 0:
        mesos += sweets * sweet_cost
    if dreams > 0:
        mesos += dreams * dream_cost
    if keys > 0:
        mesos += keys * key_cost
    if cookies > 0:
        mesos += cookies * cookie_cost
    if waters > 0:
        mesos += waters * water_cost
    if petites > 0:
        mesos += petites * petite_cost
    mp_balance = mesos / 1_000_000 * mp_ratio


def print_item(description, amount):
    print(f"{description}: {amount}")


def get_petites(n=1):
    init()
    while (petites < n):
        open()
        fuse()
    sell_not_petite()
    results = {
      'Petite Luna Pets' : n,
      'Initial Total Cost' : (format(nx_cost,',d')),
      'Sales' : (format(round(mesos),',d')),
      'Adjusted Total Cost' : (format(round(nx_cost-mp_balance),',d')),
      'Adjusted Average Pet Cost' : (format(round(((nx_cost-mp_balance)/n)),',d'))
    }
    return results


def get_blacks(n=1):
    init()
    while (blacks < n):
        open()
    sell_not_black()
    results = {
      'Wonder Black Pets' : n,
      'Wondrous Wonderberry x10 Package(s)' : packs,
      'Sales' : (format(round(mesos),',d')),
      'Adjusted Total Cost' : (format(round(nx_cost-mp_balance),',d')),
      'Adjusted Average Pet Cost' : (format(round(((nx_cost-mp_balance)/n)),',d'))
    }
    return results
