"""
Shuffler
"""
from model import *

import random


class Shuffler:
    def __init__(self, people: list[Person], seat_table: SeatTable, ruleset: Ruleset):
        self.people = people
        self.seat_table = seat_table
        self.ruleset = ruleset

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.people) == 0 or self.seat_table.count_available_seats() == 0:
            raise StopIteration
        else:
            return self.try_arranging_one()

    def shuffle_people(self):
        random.shuffle(self.people)

    def try_arranging_one(self):
        person = random.choice(self.people)
        if self.seat_table.count_available_seats() > 0:
            seat = self.seat_table.get_next_available_seat()
            seat.set_user(person)
            if self.ruleset.check(seat.get_seat_group()):
                self.people.remove(person)
                return IterationResult(True, self.seat_table, seat, person)
            seat.clear_user()
            return IterationResult(False, self.seat_table)
        else:
            return IterationResult(False, self.seat_table)


class IterationResult:
    def __init__(self, success, seat_table, seat=None, person=None):
        self.success = success
        self.seat = seat
        self.person = person
        self.seat_table = seat_table
