import requests


move_counter = 0

max_moves = 30

cookies = 0

won = 0

def c_last_winning_positions_empty():
    outer_circle = [1, 2, 3, 6, 9, 8, 7, 4]
    right_diagonal = [1, 5, 9]
    left_diagonal = [3, 5, 7]

    vertical = [2, 5, 8]
    horizontal = [4, 5, 6]

    result = []
    winning_moves = ["c-c", "cpc"]
    board_current = list("#"+api_call_status()['data']['board'])

    concurrent_positions = [outer_circle, left_diagonal, right_diagonal, vertical, horizontal]

    for cp in concurrent_positions:

        for i in xrange(len(cp)):

            prev = 0
            prev_prev = 0
            if i == 0:
                prev = board_current[cp[len(cp) - 1]]
                prev_prev = board_current[cp[len(cp) - 2]]
            elif i == 1:
                prev = board_current[cp[i - 1]]
                prev_prev = board_current[cp[len(cp) - 1]]
            else:
                prev = board_current[cp[i - 1]]
                prev_prev = board_current[cp[i - 2]]

            oc_current = prev+board_current[cp[i]]
            if oc_current == "cc":
                result.append(cp[(i+1) % len(cp)])
                if i == 0:
                    result.append(cp[len(cp) - 2])
                elif i != 1:
                    result.append(cp[len(cp) - 1])
                else:
                    result.append(cp[i - 2])

            oc_current = prev_prev + oc_current

            if oc_current in winning_moves:
                if i != 0:
                    result.append(cp[i-1])
                else:
                    result.append(cp[len(cp) - 1])

    result = list(dict.fromkeys(result))
    return result

def get_unoccupied_row_col():
    matrix = get_matrix()
    row = -1
    col = -1
    for i in xrange(3):
        found_row = False
        for j in xrange(3):
            if matrix[i][j] == 'p':
                found_row = True
                break
        if not found_row:
            row = i
            break

    for i in xrange(3):
        found_column = False
        for j in xrange(3):
            if matrix[j][i] == 'p':
                found_column = True
                break
        if not found_column:
            col = i
            break

    print ("row: "+str(row)+" col: "+str(col))
    return row*3+col+1


def my_compute(x, change):
    outer_circle = [1,4,7,8,9,6,3,2]

    x_position = outer_circle.index(x)

    compute_position = x_position + change

    if compute_position < 0:
        compute_position = len(outer_circle) + compute_position
    else:
        compute_position = compute_position % len(outer_circle)

    return outer_circle[compute_position]

def get_positions_of_blue():
    board = list(api_call_status()['data']['board'])
    positions_of_blue = [i+1 for i, x in enumerate(board) if x == 'c']
    return positions_of_blue

'''
    Yellow starts
'''
def empty_board_case():
    api_call_place(8)
    api_call_place(6)
    api_call_place(1)
    api_call_move(6, 3)
    api_call_move(3, 6)
    while move_counter < max_moves:
        api_call_move(1, 5)
        api_call_move(5, 1)


def get_matrix():
    board_1D = list(api_call_status()['data']['board'])
    board_2D = [['-' for i in xrange(3)] for i in xrange(3)]
    for i in xrange(3):
        for j in xrange(3):
            board_2D[i][j] = board_1D[i*3+j]
    for i in xrange(3):
        print (board_2D[i][0] + " " + board_2D[i][1] + " " + board_2D[i][2])
    print ("---------------")
    return board_2D

'''
    Matrix based
'''
def solution():
    api_call_place(str(api_call_status()['data']['board']).find('-') + 1)


'''
    Blue starts from middle
'''
def blue_starts_from_middle_1():
    get_matrix()
    api_call_place(8)
    get_matrix()
    a = 0
    for x in get_positions_of_blue():
        if x != 5:
            a = x
            break
    api_call_place(my_compute(a, +4))
    get_matrix()

    next_place = 0
    if get_occupancy_status_in_position(1) and get_occupancy_status_in_position(3):
        next_place = 2
        #api_call_place(2)
    elif get_occupancy_status_in_position(3) and get_occupancy_status_in_position(9):
        next_place = 6
        #api_call_place(6)
    #elif get_occupancy_status_in_position(9) and get_occupancy_status_in_position(7):
        #next_place = 8
        #api_call_place(8)
    elif get_occupancy_status_in_position(7) and get_occupancy_status_in_position(1):
        next_place = 4
        #api_call_place(4)
    else:
        for x in get_positions_of_blue():
            if x != 5 and x != a and not get_occupancy_status_in_position(my_compute(x, +4)) and not get_occupancy_status_in_position_for_me(my_compute(x, +4)):
                next_place = my_compute(x, +4)
                break
        if next_place == 0: #and not get_occupancy_status_in_position(my_compute(x, +4)) and not get_occupancy_status_in_position_for_me(my_compute(x, +4)):
            next_place = get_unoccupied_row_col()

    print (str(next_place))
    api_call_place(next_place)


    start_location = 8
    while move_counter < max_moves:
        new_location = 5
        if start_location == 8 and get_occupancy_status_in_position(5):
            if get_occupancy_status_in_position(3) and not get_occupancy_status_in_position(7):
                new_location = 7
            elif get_occupancy_status_in_position(2) and get_occupancy_status_in_position(4):
                new_location = 7
            elif get_occupancy_status_in_position(2) and get_occupancy_status_in_position(6):
                new_location = 9
            elif get_occupancy_status_in_position(2) and (get_occupancy_status_in_position(7) or get_occupancy_status_in_position(9)):
                if get_occupancy_status_in_position_for_me(4) and get_occupancy_status_in_position_for_me(3):
                    api_call_move(4,1)
                    if not get_occupancy_status_in_position(4):
                        api_call_move(1,4)
                    else:
                        api_call_move(3,6)
                if get_occupancy_status_in_position_for_me(1) and get_occupancy_status_in_position_for_me(6):
                    api_call_move(1,4)
                    if not get_occupancy_status_in_position(1):
                        api_call_move(4,1)
                    else:
                        api_call_move(6,3)
            elif not get_occupancy_status_in_position(9):
                new_location = 9
            else:
                new_location = 7
        elif start_location == 9 and get_occupancy_status_in_position(5) and get_occupancy_status_in_position(1) and get_occupancy_status_in_position(6):
            if get_occupancy_status_in_position_for_me(3):
                api_call_move(3,2)
                api_call_move(2,3)
            elif get_occupancy_status_in_position_for_me(2):
                api_call_move(2,3)
                api_call_move(3,2)

        elif start_location == 5:
            new_location = 8
            #if get_occupancy_status_in_position(3):
            #    new_location = 7
            #elif get_occupancy_status_in_position(1):
            #    new_location = 9
            #else:
            #    new_location = 8
        elif get_occupancy_status_in_position(new_location):
            new_location = 8

        api_call_move(start_location, new_location)

        start_location = new_location

        get_matrix()

def blue_starts_from_middle_3():
    get_matrix()
    api_call_place(8)
    get_matrix()
    a = 0
    for x in get_positions_of_blue():
        if x != 5:
            a = x
            break
    api_call_place(my_compute(a, +4))
    get_matrix()

    next_place = 0
    if get_occupancy_status_in_position(1) and get_occupancy_status_in_position(3):
        next_place = 2
        #api_call_place(2)
    elif get_occupancy_status_in_position(3) and get_occupancy_status_in_position(9):
        next_place = 6
        #api_call_place(6)
    #elif get_occupancy_status_in_position(9) and get_occupancy_status_in_position(7):
        #next_place = 8
        #api_call_place(8)
    elif get_occupancy_status_in_position(7) and get_occupancy_status_in_position(1):
        next_place = 4
        #api_call_place(4)
    else:
        for x in get_positions_of_blue():
            if x != 5 and x != a and not get_occupancy_status_in_position(my_compute(x, +4)) and not get_occupancy_status_in_position_for_me(my_compute(x, +4)):
                next_place = my_compute(x, +4)
                break
        if next_place == 0: #and not get_occupancy_status_in_position(my_compute(x, +4)) and not get_occupancy_status_in_position_for_me(my_compute(x, +4)):
            next_place = get_unoccupied_row_col()

    print (str(next_place))
    api_call_place(next_place)


    start_location = 8
    while move_counter < max_moves:
        new_location = 5
        if start_location == 8 and get_occupancy_status_in_position(5):
            if get_occupancy_status_in_position(3) and not get_occupancy_status_in_position(7):
                new_location = 7
            elif get_occupancy_status_in_position(2) and get_occupancy_status_in_position(4):
                new_location = 7
            elif get_occupancy_status_in_position(2) and get_occupancy_status_in_position(6):
                new_location = 9
            elif get_occupancy_status_in_position(2) and (get_occupancy_status_in_position(7) or get_occupancy_status_in_position(9)):
                if get_occupancy_status_in_position_for_me(4) and get_occupancy_status_in_position_for_me(3):
                    api_call_move(4,1)
                    if not get_occupancy_status_in_position(4):
                        api_call_move(1,4)
                    else:
                        api_call_move(3,6)
                if get_occupancy_status_in_position_for_me(1) and get_occupancy_status_in_position_for_me(6):
                    api_call_move(1,4)
                    if not get_occupancy_status_in_position(1):
                        api_call_move(4,1)
                    else:
                        api_call_move(6,3)
            elif not get_occupancy_status_in_position(9):
                new_location = 9
            else:
                new_location = 7
        elif start_location == 9 and get_occupancy_status_in_position(5) and get_occupancy_status_in_position(1) and get_occupancy_status_in_position(6):
            if get_occupancy_status_in_position_for_me(3):
                api_call_move(3,2)
                api_call_move(2,3)
            elif get_occupancy_status_in_position_for_me(2):
                api_call_move(2,3)
                api_call_move(3,2)

        elif start_location == 5:
            new_location = 8
            #if get_occupancy_status_in_position(3):
            #    new_location = 7
            #elif get_occupancy_status_in_position(1):
            #    new_location = 9
            #else:
            #    new_location = 8
        elif get_occupancy_status_in_position(new_location):
            new_location = 8

        api_call_move(start_location, new_location)

        start_location = new_location

        get_matrix()

'''
    Blue starts from middle
'''
def blue_starts_from_middle():
    get_matrix()
    api_call_place(8)
    get_matrix()
    a = 0
    for x in get_positions_of_blue():
        if x != 5:
            a = x
            break
    api_call_place(my_compute(a, +4))
    get_matrix()

    next_place = 0
    if get_occupancy_status_in_position(1) and get_occupancy_status_in_position(3):
        next_place = 2
        #api_call_place(2)
    elif get_occupancy_status_in_position(3) and get_occupancy_status_in_position(9):
        next_place = 6
        #api_call_place(6)
    #elif get_occupancy_status_in_position(9) and get_occupancy_status_in_position(7):
        #next_place = 8
        #api_call_place(8)
    elif get_occupancy_status_in_position(7) and get_occupancy_status_in_position(1):
        next_place = 4
        #api_call_place(4)
    else:
        for x in get_positions_of_blue():
            if x != 5 and x != a and not get_occupancy_status_in_position(my_compute(x, +4)) and not get_occupancy_status_in_position_for_me(my_compute(x, +4)):
                next_place = my_compute(x, +4)
                break
        if next_place == 0: #and not get_occupancy_status_in_position(my_compute(x, +4)) and not get_occupancy_status_in_position_for_me(my_compute(x, +4)):
            next_place = get_unoccupied_row_col()

    print (str(next_place))
    api_call_place(next_place)


    start_location = 8
    while move_counter < max_moves:
        new_location = 5

        if get_occupancy_status_in_position_for_me(5):
            start_location = 5
        elif get_occupancy_status_in_position_for_me(8):
            start_location = 8
        elif get_occupancy_status_in_position_for_me(7):
            start_location = 7
        else:
            start_location = 9

        if start_location == 8 and get_occupancy_status_in_position(5):
            if get_occupancy_status_in_position(4) and get_occupancy_status_in_position(9) and not get_occupancy_status_in_position_for_me(6) and get_occupancy_status_in_position_for_me(3):
                api_call_move(3,6)
            if get_occupancy_status_in_position(6) and get_occupancy_status_in_position(7) and not get_occupancy_status_in_position_for_me(4) and get_occupancy_status_in_position_for_me(1):
                api_call_move(1,4)

            if get_occupancy_status_in_position(7) and get_occupancy_status_in_position(9) and not get_occupancy_status_in_position_for_me(4) and not get_occupancy_status_in_position_for_me(6):
                if get_occupancy_status_in_position_for_me(1):
                    api_call_move(1, 4)
                    continue
            elif get_occupancy_status_in_position(3) and not get_occupancy_status_in_position(7):
                new_location = 7
            elif get_occupancy_status_in_position(2) and get_occupancy_status_in_position(4):
                new_location = 7
            elif get_occupancy_status_in_position(2) and get_occupancy_status_in_position(6):
                new_location = 9
            elif get_occupancy_status_in_position(2) and (get_occupancy_status_in_position(7) or get_occupancy_status_in_position(9)):
                if get_occupancy_status_in_position(7):
                    if get_occupancy_status_in_position_for_me(4) and get_occupancy_status_in_position_for_me(3):
                        api_call_move(4,1)
                        if not get_occupancy_status_in_position(4):
                            api_call_move(1,4)
                        else:
                            api_call_move(3,6)
                    elif get_occupancy_status_in_position_for_me(1) and get_occupancy_status_in_position_for_me(6):
                        api_call_move(6,3)
                        if not get_occupancy_status_in_position(6):
                            api_call_move(3,6)
                        else:
                            api_call_move(1,4)
                    elif get_occupancy_status_in_position_for_me(1) and get_occupancy_status_in_position_for_me(3):
                        api_call_move(1,4)
                elif get_occupancy_status_in_position(9):
                    if get_occupancy_status_in_position_for_me(4) and get_occupancy_status_in_position_for_me(3):
                        api_call_move(4,1)
                        if not get_occupancy_status_in_position(4):
                            api_call_move(1,4)
                        else:
                            api_call_move(3,6)
                    if get_occupancy_status_in_position_for_me(1) and get_occupancy_status_in_position_for_me(6):
                        api_call_move(6,3)
                        if not get_occupancy_status_in_position(6):
                            api_call_move(3,6)
                        else:
                            api_call_move(1,4)
            elif not get_occupancy_status_in_position(9):
                new_location = 9
            else:
                new_location = 7
        elif start_location == 9 and get_occupancy_status_in_position(5) and get_occupancy_status_in_position(1) and get_occupancy_status_in_position(6):
            if get_occupancy_status_in_position_for_me(3):
                api_call_move(3,2)
                api_call_move(2,3)
            elif get_occupancy_status_in_position_for_me(2):
                api_call_move(2,3)
                api_call_move(3,2)
        elif start_location == 7 and get_occupancy_status_in_position(5) and get_occupancy_status_in_position(3) and get_occupancy_status_in_position(4):
            if get_occupancy_status_in_position_for_me(1):
                api_call_move(1,2)
                api_call_move(2,1)
            elif get_occupancy_status_in_position_for_me(2):
                api_call_move(2,1)
                api_call_move(1,2)
        elif get_occupancy_status_in_position(5) and get_occupancy_status_in_position(8) and not get_occupancy_status_in_position_for_me(2):
            if get_occupancy_status_in_position_for_me(1):
                api_call_move(1, 2)
                if get_occupancy_status_in_position_for_me(6):
                    api_call_move(6, 9)
            elif get_occupancy_status_in_position_for_me(3):
                api_call_move(3, 2)
            continue
        elif start_location == 5:

            if not get_occupancy_status_in_position(8):
                new_location = 8
            elif not get_occupancy_status_in_position(7):
                new_location = 7
            else:
                new_location = 9
            #if get_occupancy_status_in_position(3):
            #    new_location = 7
            #elif get_occupancy_status_in_position(1):
            #    new_location = 9
            #else:
            #    new_location = 8
        elif get_occupancy_status_in_position(new_location):
            new_location = 8



        api_call_move(start_location, new_location)



        start_location = new_location

        get_matrix()
        print (c_last_winning_positions_empty())



'''
    Blue starts from non-middle
    @:param x is the position of first blue
'''
def blue_starts_from_non_middle(x):
    api_call_place(my_compute(x, -1))
    api_call_place(my_compute(x, +4))

    is_blue_in_position_4 = get_occupancy_status_in_position(my_compute(x, +2))
    is_blue_in_position_5 = get_occupancy_status_in_position(my_compute(x, +3))
    is_blue_in_position_7 = get_occupancy_status_in_position(my_compute(x, +5))
    is_blue_in_position_8 = get_occupancy_status_in_position(my_compute(x, +6))

    api_call_place(my_compute(x, +1))

    #Blue in position x+2 (4)
    if is_blue_in_position_4:
        api_call_move(my_compute(x,-1), 5)
        api_call_move(5, my_compute(x,-1))
        while move_counter < max_moves:
            api_call_move(my_compute(x, -1), my_compute(x, +7))
            api_call_move(my_compute(x, +7), my_compute(x, -1))
    #Blue in position x+3 (5)
    elif is_blue_in_position_5:
        while move_counter < max_moves:
            api_call_move(my_compute(x, +1), my_compute(x, +2))
            api_call_move(my_compute(x, +2), my_compute(x, +1))
    #Blue in position x+5 (7)
    elif is_blue_in_position_7:
        while move_counter < max_moves:
            api_call_move(my_compute(x, +4), 5)
            api_call_move(5, my_compute(x, +4))
    #Blue in position x+6 (8)
    elif is_blue_in_position_8:
        api_call_move(my_compute(x, +4), my_compute(x, +5))

        blue_moved_from_8_to_9 = not get_occupancy_status_in_position(my_compute(x,+6))
        blue_moved_from_2_to_9 = not get_occupancy_status_in_position(x)

        if blue_moved_from_8_to_9:
            while move_counter < max_moves:
                api_call_move(my_compute(x, +5), my_compute(x, +4))
                api_call_move(my_compute(x, +4), my_compute(x, +5))
        elif blue_moved_from_2_to_9:
            api_call_move(my_compute(x, +1), my_compute(x, +2))
            while move_counter < max_moves:
                api_call_move(my_compute(x, +5), my_compute(x, +4))
                api_call_move(my_compute(x, +4), my_compute(x, +5))


def api_call_new():
    resp = requests.post("http://rota.praetorian.com/rota/service/play.php?request=new&email=a@illinois.edu")
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json())
    global cookies
    cookies = resp.cookies
    return resp.json()

def api_call_place(location):
    resp = requests.post("http://rota.praetorian.com/rota/service/play.php?request=place&location="+str(location), cookies = cookies)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json())
    # print str(resp.json())
    return resp.json()

def api_call_move(froM, to):
    resp = requests.post("http://rota.praetorian.com/rota/service/play.php?request=move&from="+str(froM)+"&to="+str(to), cookies = cookies)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json())

    print ("move made: "+ str(froM) + " " + str(to) + " " + str(resp.json()))

    try:
        global move_counter
        move_counter = resp.json()['data']['moves']
    except Exception as x:
        print (resp.json())
        raise x

    # print str(resp.json())
    return resp.json()

def api_call_status():
    resp = requests.post("http://rota.praetorian.com/rota/service/play.php?request=status", cookies = cookies)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json())
    return resp.json()

def api_call_next():
    resp = requests.post("http://rota.praetorian.com/rota/service/play.php?request=next", cookies = cookies)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json())
    return resp.json()

'''
    @:returns True is position is filled by blue
'''
def get_occupancy_status_in_position(position):
    board_raw = api_call_status()['data']['board']
    board_structured = list(str(board_raw))
    return board_structured[position-1] == 'c'

'''
    @:returns True is position is filled by me
'''
def get_occupancy_status_in_position_for_me(position):
    board_raw = api_call_status()['data']['board']
    board_structured = list(str(board_raw))
    return board_structured[position-1] == 'p'

if __name__ == '__main__':
    location_of_first_blue = -1
    output = api_call_new()


    try:
        while 1:

            location_of_first_blue = str(api_call_status()['data']['board']).find('c') + 1
            while location_of_first_blue != 5:
                output = api_call_new()
                location_of_first_blue = str(api_call_status()['data']['board']).find('c') + 1

            #while 1:
            #location_of_first_blue = str(api_call_status()['data']['board']).find('c') + 1
            #print (output)
            #get_matrix()
            if location_of_first_blue == 0:
                blue_starts_from_middle()
                #empty_board_case()
            elif location_of_first_blue == 5:
                blue_starts_from_middle()
            else:
                blue_starts_from_middle_3()
                #blue_starts_from_non_middle(location_of_first_blue)

            get_matrix()

            global move_counter
            move_counter = 0

            print ("status: " + str(api_call_status()))
            get_matrix()
            print ("next: " + str(api_call_next()))
            global won
            won = won+int(api_call_status()['data']['games_won'])
            print ("Games Won Inner Loop: " + str(won))
    except Exception as x:
        print ("Games Won: " + str(won))
        raise x

