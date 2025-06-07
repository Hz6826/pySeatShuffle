"""
Shuffler
"""
from model import *

import random


class Shuffler:
    def __init__(self, manager):
        self.manager = manager

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.manager.people) == 0 or self.manager.seat_table.count_available_seats() == 0:
            raise StopIteration
        else:
            return self.try_arranging_one()

    def shuffle_people(self):
        random.shuffle(self.manager.people)

    def try_arranging_one(self):
        person = random.choice(self.manager.people)
        if self.manager.seat_table.count_available_seats() > 0:
            seat = self.manager.seat_table.get_next_available_seat()
            seat.set_user(person)
            if self.manager.ruleset.check(seat.get_seat_group()):
                self.manager.people.remove(person)
                return IterationResult(True, self.manager.seat_table, seat, person)
            seat.clear_user()
            return IterationResult(False, self.manager.seat_table)
        else:
            return IterationResult(False, self.manager.seat_table)


class IterationResult:
    def __init__(self, success, seat_table, seat=None, person=None):
        self.success = success
        self.seat = seat
        self.person = person
        self.seat_table = seat_table

