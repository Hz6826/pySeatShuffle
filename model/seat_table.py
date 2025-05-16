"""
Seat Table Model
"""

class Seat:
    def __init__(self, pos: tuple[int, int], name: str=None):
        self.pos = pos
        self.name = name
        self.user = None

    def is_available(self):
        return self.user is not None

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def clear_user(self):
        self.user = None


class SeatGroup:
    def __init__(self, seats: list[Seat], name=None):
        self.seats = seats
        self.name = name

        self._cursor = 0

    def get_seats(self):
        return self.seats

    def get_name(self):
        return self.name

    def count_seats(self):
        return len(self.seats)

    def count_available_seats(self):
        return len([seat for seat in self.seats if seat.is_available()])

    def get_next_available_seat(self):
        return next((seat for seat in self.seats if seat.is_available()), None)


class SeatTable:
    def __init__(self, seat_groups: list[SeatGroup], size, name=None):
        self.seat_groups = seat_groups
        self.size = size
        self.name = name

        self._cursor = 0

    def get_seat_groups(self):
        return self.seat_groups

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

    def count_seats(self):
        return sum([seat_group.count_seats() for seat_group in self.seat_groups])

    def count_available_seats(self):
        return sum([seat_group.count_available_seats() for seat_group in self.seat_groups])

    def get_next_available_seat(self):
        if self._cursor < self.count_seats():
            candidate = self.seat_groups[self._cursor].get_next_available_seat()
            if candidate is None:
                self._cursor += 1
                return self.get_next_available_seat()
            return candidate
        self._cursor = 0
        return None

