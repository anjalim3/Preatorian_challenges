import requests

outer_circle = [1, 2, 3, 6, 9, 8, 7, 4]
right_diagonal = [1,5,9]
left_diagonal = [3,5,7]
vertical = [2,5,8]
horizontal = [4,5,6]

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

    global move_counter
    move_counter = move_counter + 1

    # print str(resp.json())
    return resp.json()

def api_call_status():
    return "-cppcc-p-"
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
def get_occupancy_in_position(position):
    board_raw = api_call_status()['data']['board']
    board_structured = list(str(board_raw))
    return board_structured[position-1]

def print_matrix():
    matrix = get_matrix()
    for i in xrange(3):
        print (matrix[i][0] + " " + matrix[i][1] + " " + matrix[i][2])
    print ("---------------")

def get_matrix():
    #board_1D = list(api_call_status()['data']['board'])
    board_1D = list(api_call_status())
    board_2D = [['-' for i in xrange(3)] for i in xrange(3)]
    for i in xrange(3):
        for j in xrange(3):
            board_2D[i][j] = board_1D[i*3+j]

    return board_2D

def set_A_minus_set_B(A, B):

    result = []

    for a in A:
        if a not in B:
            result.append(a)

    return result

def get_neighbours(position):

    neighbour_lookup = {
        1: [2,5,4],
        2: [1,5,3],
        3: [2,5,6],
        4: [1,5,7],
        5: [1,2,3,4,6,7,8,9],
        6: [3,5,9],
        7: [4,5,8],
        8: [7,5,9],
        9: [6,8,9]
    }

    return neighbour_lookup.get(position)

def c_last_winning_positions():
    result = {}
    winning_moves = ["c-c", "cpc", "-cc", "pcc", "ccp", "cc-"]
    #board_current = list("#"+api_call_status()['data']['board'])

    board_current = list("#" + api_call_status())

    concurrent_positions = [left_diagonal, right_diagonal, vertical, horizontal]

    for cp in concurrent_positions:
        board_in_cp = ""
        for i in cp:
            board_in_cp = board_in_cp + board_current[i]

        if board_in_cp in winning_moves:

            occupant_in_missing_piece = board_in_cp.replace("c", "")

            index_of_missing_piece = board_in_cp.find(occupant_in_missing_piece)

            # initialize if not already exists
            if index_of_missing_piece not in result:
                result[cp[index_of_missing_piece]] = []

            # create exception list B
            exception_list = []
            if index_of_missing_piece != 0:
                exception_list.append(cp[index_of_missing_piece - 1])
            if index_of_missing_piece != 2:
                exception_list.append(cp[index_of_missing_piece + 1])


            # Get allowance list A - B
            result[cp[index_of_missing_piece]].extend(
                set_A_minus_set_B(
                    get_neighbours(cp[index_of_missing_piece]),
                    exception_list)
            )


    for i in xrange(len(outer_circle)):
        board_in_outer_circle = board_current[outer_circle[i]] + board_current[outer_circle[(i+1)%len(outer_circle)]] + board_current[outer_circle[(i+2)%len(outer_circle)]]

        if board_in_outer_circle in winning_moves:
            occupant_in_missing_piece = board_in_outer_circle.replace("c", "")

            index_of_missing_piece = board_in_outer_circle.find(occupant_in_missing_piece)

            # initialize if not already exists
            if index_of_missing_piece not in result:
                result[outer_circle[(i+index_of_missing_piece)%len(outer_circle)]] = []

            # create exception list B
            exception_list = []
            if index_of_missing_piece != 0:
                ind = i+index_of_missing_piece-1
                if ind < 0:
                    ind = len(outer_circle) + ind
                exception_list.append(outer_circle[ind])
            if index_of_missing_piece != 2:
                exception_list.append(outer_circle[(i+index_of_missing_piece+1)%len(outer_circle)])

            print exception_list
            # Get allowance list A - B
            result[outer_circle[(i+index_of_missing_piece)%len(outer_circle)]].extend(
                set_A_minus_set_B(
                    get_neighbours(outer_circle[(i+index_of_missing_piece)%len(outer_circle)]),
                    exception_list)
            )
            print result[outer_circle[(i+index_of_missing_piece)%len(outer_circle)]]

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

    return row*3+col+1

if __name__ == '__main__':
    print (c_last_winning_positions())
    print_matrix()
