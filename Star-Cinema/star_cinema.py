from typing import Dict, List, Tuple


class Star_Cinema:
    hall_list: List['Hall'] = []  # class attribute shared across all instances

    @classmethod
    def entry_hall(cls, hall: 'Hall') -> None:
        if not isinstance(hall, Hall):
            raise TypeError('entry_hall requires a Hall instance')
        cls.hall_list.append(hall)

    @classmethod
    def view_all_halls(cls) -> List['Hall']:
        return list(cls.hall_list)


class Hall(Star_Cinema):
    def __init__(self, rows: int, cols: int, hall_no: int):
        if rows <= 0 or cols <= 0:
            raise ValueError('rows and cols must be positive integers')
        self._rows = rows
        self._cols = cols
        self._hall_no = hall_no
        self._seats: Dict[str, List[List[str]]] = {}
        self._show_list: List[Tuple[str, str, str]] = []

        # register this hall to cinema
        self.entry_hall(self)

    def entry_show(self, show_id: str, movie_name: str, time: str) -> None:
        if show_id in self._seats:
            raise ValueError(f'Show id {show_id!r} already exists in hall {self._hall_no}')

        # validate inputs
        if not show_id or not movie_name or not time:
            raise ValueError('show_id, movie_name and time must be non-empty')

        self._show_list.append((show_id, movie_name, time))

        # allocate seats: 'O' indicates free, 'X' indicates booked
        self._seats[show_id] = [['O' for _ in range(self._cols)] for _ in range(self._rows)]

    def book_seats(self, show_id: str, requests: List[Tuple[int, int]]) -> None:
        if show_id not in self._seats:
            raise KeyError(f'Show id {show_id!r} does not exist in hall {self._hall_no}')

        seat_grid = self._seats[show_id]

        for r, c in requests:
            if not isinstance(r, int) or not isinstance(c, int):
                raise TypeError('row and col must be integers')
            if r < 0 or r >= self._rows or c < 0 or c >= self._cols:
                raise ValueError(f'Seat {r, c} is invalid for hall {self._hall_no}')
            if seat_grid[r][c] == 'X':
                raise ValueError(f'Seat {r, c} already booked for show {show_id}')

        for r, c in requests:
            seat_grid[r][c] = 'X'

    def view_show_list(self) -> List[Tuple[str, str, str]]:
        return list(self._show_list)

    def view_available_seats(self, show_id: str) -> List[Tuple[int, int]]:
        if show_id not in self._seats:
            raise KeyError(f'Show id {show_id!r} does not exist in hall {self._hall_no}')

        grid = self._seats[show_id]
        available = []
        for r in range(self._rows):
            for c in range(self._cols):
                if grid[r][c] == 'O':
                    available.append((r, c))
        return available

    def _pretty_seat_map(self, show_id: str) -> str:
        if show_id not in self._seats:
            raise KeyError(f'Show id {show_id!r} does not exist in hall {self._hall_no}')
        grid = self._seats[show_id]
        lines = [' '.join(row) for row in grid]
        return '\n'.join(lines)

    def display_seat_map(self, show_id: str) -> None:
        print(f"Hall {self._hall_no} seat map for show {show_id}:")
        print(self._pretty_seat_map(show_id))

    @property
    def hall_no(self) -> int:
        return self._hall_no

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols
