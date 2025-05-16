"""
Shuffler
"""
from model import *

import random


class Shuffler:
    def __init__(self, ins: Instance):
        self.instance = ins

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.instance.people) == 0 or self.instance.seat_table.count_available_seats() == 0:
            raise StopIteration
        else:
            return self.try_arranging_one()

    def shuffle_people(self):
        random.shuffle(self.instance.people)

    def try_arranging_one(self):
        person = random.choice(self.instance.people)
        if self.instance.seat_table.count_available_seats() > 0:
            seat = self.instance.seat_table.get_next_available_seat()
            seat.set_user(person)
            if self.instance.ruleset.check(seat.get_seat_group()):
                self.instance.people.remove(person)
                return IterationResult(True, self.instance.seat_table, seat, person)
            seat.clear_user()
            return IterationResult(False, self.instance.seat_table)
        else:
            return IterationResult(False, self.instance.seat_table)


class IterationResult:
    def __init__(self, success, seat_table, seat=None, person=None):
        self.success = success
        self.seat = seat
        self.person = person
        self.seat_table = seat_table

