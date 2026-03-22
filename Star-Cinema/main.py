from star_cinema import Hall, Star_Cinema


def setup_sample_data():
    hall1 = Hall(rows=5, cols=8, hall_no=1)
    hall1.entry_show('S1', 'Spider-Man', '12:30')
    hall1.entry_show('S2', 'Frozen II', '15:00')

    hall2 = Hall(rows=4, cols=6, hall_no=2)
    hall2.entry_show('S3', 'Inception', '13:00')

    return [hall1, hall2]


def find_hall(hall_no: int):
    for h in Star_Cinema.view_all_halls():
        if h.hall_no == hall_no:
            return h
    return None


def main():
    setup_sample_data()

    while True:
        print('\n=== Star Cinema Counter ===')
        print('1. View all running shows')
        print('2. View available seats for a show')
        print('3. Book seats for a show')
        print('4. Exit')
        choice = input('Select option: ').strip()

        if choice == '1':
            for hall in Star_Cinema.view_all_halls():
                print(f'Hall {hall.hall_no}:')
                for show_id, movie_name, time in hall.view_show_list():
                    print(f'  {show_id}: {movie_name} at {time}')

        elif choice == '2':
            try:
                hall_no = int(input('Hall no: ').strip())
                show_id = input('Show id: ').strip()
                hall = find_hall(hall_no)
                if hall is None:
                    print('Wrong hall number')
                    continue
                available = hall.view_available_seats(show_id)
                print(f'Available seats ({len(available)}): {available}')
                hall.display_seat_map(show_id)
            except Exception as e:
                print('Error:', e)

        elif choice == '3':
            try:
                hall_no = int(input('Hall no: ').strip())
                show_id = input('Show id: ').strip()
                hall = find_hall(hall_no)
                if hall is None:
                    print('Wrong hall number')
                    continue

                seat_input = input('Enter seats as row,col pairs separated by semicolon (e.g. 0,0;0,1): ')
                pairs = []
                for chunk in seat_input.split(';'):
                    chunk = chunk.strip()
                    if not chunk:
                        continue
                    r, c = map(int, chunk.split(','))
                    pairs.append((r, c))

                hall.book_seats(show_id, pairs)
                print('Successfully booked seats:', pairs)
                hall.display_seat_map(show_id)
            except Exception as e:
                print('Error:', e)

        elif choice == '4':
            print('Goodbye!')
            break

        else:
            print('Invalid option.')


if __name__ == '__main__':
    main()
