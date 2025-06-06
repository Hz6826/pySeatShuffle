"""
Seat Table Model
"""

from core.constants import *


class Seat:
    def __init__(self, pos: tuple[int, int], name: str = None):
        self.pos = pos  # row, col
        self.name = name
        self.user = None

    def is_available(self):
        return self.user is not None

    def get_pos(self):
        """
        :return: row, column
        """
        return self.pos

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def clear_user(self):
        self.user = None

    def __str__(self):
        return f"Seat({self.pos}, {self.name}, {self.user})"

    def to_dict(self):
        return {
            "pos": self.pos,
            "name": self.name,
            "user": self.user.to_dict() if self.user is not None else None
        }


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

    def __str__(self):
        return f"SeatGroup({self.name}, {self.count_seats()}, [" + ", ".join([str(seat) for seat in self.seats]) + "])"

    def to_dict(self):
        return {
            "name": self.name,
            "seats": [seat.to_dict() for seat in self.seats]
        }


class SeatTable:
    def __init__(self, seat_groups: list[SeatGroup], size, name=None, metadata=None):
        """
        :param seat_groups: list of SeatGroup
        :param size: row, column
        :param name:
        :param metadata:
        """
        self.seat_groups = seat_groups
        self.size = size
        self.name = name

        if metadata is None:
            self.metadata = SeatTableMetadata("unknown", "")
        else:
            self.metadata = metadata

        self._cursor = 0

    def get_offset(self):
        """
        :return: row, column
        """
        min_r = min([seat.get_pos()[0] for group in self.seat_groups for seat in group.get_seats()])
        min_c = min([seat.get_pos()[1] for group in self.seat_groups for seat in group.get_seats()])
        return min_r, min_c

    def set_user_in_pos(self, pos: tuple[int, int], user):
        """
        Set user in the specified position.
        :param pos: (row, column)
        :param user: User object
        :return: True if successful, False otherwise
        """
        for seat_group in self.seat_groups:
            for seat in seat_group.get_seats():
                if seat.get_pos() == pos:
                    seat.set_user(user)
                    return True
        return False

    def remove_user_in_pos(self, pos: tuple[int, int]):
        """
        Remove user in the specified position.
        :param pos: (row, column)
        :return: True if successful, False otherwise
        """
        for seat_group in self.seat_groups:
            for seat in seat_group.get_seats():
                if seat.get_pos() == pos:
                    seat.clear_user()
                    return True
        return False

    def clear_all_users(self):
        """
        Clear all users in the seat table.
        """
        for seat_group in self.seat_groups:
            for seat in seat_group.get_seats():
                seat.clear_user()

    def get_seat_groups(self):
        return self.seat_groups

    def get_size(self):
        """
        :return: rows, columns
        """
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

    def __str__(self):
        return f"SeatTable({self.name}, {self.size}, \n" + "\n".join([str(seat_group) for seat_group in self.seat_groups]) + "\n)"

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "seat_groups": [seat_group.to_dict() for seat_group in self.seat_groups]
        }


class SeatTableMetadata:
    def __init__(self, format, file_path):
        self.format = format
        self.file_path = file_path

    def __str__(self):
        return f"SeatTableMetadata(format={self.format}, file_path={self.file_path})"


class SeatTableMetadataXlsx(SeatTableMetadata):
    def __init__(self, file_path):
        super().__init__(F_XLSX, file_path)
        self.gen_time_cell_pos = None  # 存储格式为 (column, row)，都从1开始
        self.offset_row = 0
        self.offset_col = 0


class SeatTableMetadataJson(SeatTableMetadata):
    def __init__(self, file_path):
        super().__init__(F_JSON, file_path)
