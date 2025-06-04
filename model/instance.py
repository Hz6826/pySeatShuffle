"""
Instance Model
"""
from .ruleset import *
from .seat_table import *
from .person import *


class Instance:
    def __init__(self, name: str = None, people: list[Person] = None, seat_table: SeatTable = None, ruleset: Ruleset = None):
        self.name = name
        self.people = people
        self.seat_table = seat_table
        self.ruleset = ruleset

    def get_seat_table(self) -> SeatTable:
        return self.seat_table

    def get_ruleset(self) -> Ruleset:
        return self.ruleset

    def get_people(self) -> list[Person]:
        return self.people

    def get_name(self) -> str:
        return self.name

    def set_seat_table(self, seat_table: SeatTable):
        self.seat_table = seat_table

    def set_ruleset(self, ruleset: Ruleset):
        self.ruleset = ruleset

    def set_people(self, people: list[Person]):
        self.people = people

    def set_name(self, name: str):
        self.name = name
