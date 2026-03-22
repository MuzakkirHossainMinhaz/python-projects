# Star Cinema

A simple cinema booking system with two classes:

- `Star_Cinema`: class-level `hall_list`, tracks all halls.
- `Hall`: represents a hall with rows, cols, shows, and per-show seat maps.

## Features

- Add halls and shows
- View running shows
- Book seats with validation
- View available seats and seat maps
- Error handling for:
  - wrong show id
  - invalid seat coordinates
  - already booked seats

## Run

```sh
python main.py
```

Use menu options to view shows, view seats, and book tickets.

## Data privacy

- `Hall` uses protected attributes (`_rows`, `_cols`, `_show_list`, `_seats`) to discourage direct external access.
- `Star_Cinema.hall_list` is intentionally global at class scope and filled via `entry_hall`.
