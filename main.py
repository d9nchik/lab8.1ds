from copy import deepcopy


def get_data():
    data = []
    with open("input.txt") as iFile:
        while True:
            line = iFile.readline()
            if not line:
                break
            temp = list(map(int, (line[:len(line)] + line[len(line) + 1:]).split()))
            data.append(temp)
    return data


def create_adjacency_matrix(idata):
    matrix = [0] * idata[0][0]
    for x in range(idata[0][0]):
        matrix[x] = [0] * idata[0][0]

    for y in range(1, len(idata)):
        matrix[idata[y][0] - 1][idata[y][1] - 1] = idata[y][2]
    return matrix


def find_queue(adjacency_matrix):
    for x in range(len(adjacency_matrix)):
        total = 0
        for y in range(len(adjacency_matrix)):
            total += adjacency_matrix[y][x]
        if total == 0:
            return x
    print("Відсутнє джерело")
    exit(1)


def find_stock(adjacency_matrix):
    for x in range(len(adjacency_matrix)):
        total = 0
        for y in range(len(adjacency_matrix)):
            total += adjacency_matrix[x][y]
        if total == 0:
            return x
    print("Відсутній сток")
    exit(1)


def get_neighbours(adjacency_matrix, index, marker):
    neighbours = []
    for x in range(len(adjacency_matrix)):
        if adjacency_matrix[index][x] > 0 and not marker[x]:
            neighbours.append(x)
    return neighbours


def algorithm_ford_falkersona(adjacency_matrix, queue, stock):
    marker = [False] * len(adjacency_matrix)
    marker[queue] = True
    should_be_continued = True
    total_stream = 0
    while should_be_continued:
        should_be_continued = False
        neighbours = get_neighbours(adjacency_matrix, queue, marker)
        for neighbour in neighbours:
            size = adjacency_matrix[0][neighbour]
            part, weight = algorithm_ford_falkersona_middle_part(adjacency_matrix, stock, size, marker, neighbour,
                                                                 queue)
            if part:
                should_be_continued = True
                total_stream += weight
                break
    return total_stream


def algorithm_ford_falkersona_middle_part(adjacency_matrix, stock, size, marker, index, previous_index):
    if stock == index:
        adjacency_matrix[previous_index][index] -= size
        adjacency_matrix[index][previous_index] += size
        return True, size
    marker[index] = True
    for neighbour in get_neighbours(adjacency_matrix, index, marker):
        current_size = size
        if current_size > adjacency_matrix[index][neighbour]:
            current_size = adjacency_matrix[index][neighbour]
        falkersona_middle_part, weight = algorithm_ford_falkersona_middle_part(adjacency_matrix, stock, current_size,
                                                                               marker,
                                                                               neighbour, index)
        if falkersona_middle_part:
            adjacency_matrix[previous_index][index] -= weight
            adjacency_matrix[index][previous_index] += weight
            marker[index] = False
            return True, weight
    marker[index] = False
    return False, size


def show_all_node_stream(adjacency_matrix):
    for x in range(len(adjacency_matrix)):
        for y in range(x + 1, len(adjacency_matrix)):
            stream = adjacency_matrix[y][x]
            if stream == 0:
                continue
            if stream < 0:
                print("Потік ребра %d->%d = %d" % (y + 1, x + 1, -stream))
            else:
                print("Потік ребра %d->%d = %d" % (x + 1, y + 1, stream))


def subtract_matrices(matrix_a, matrix_b):
    matrix_c = deepcopy(matrix_a)
    for x in range(len(matrix_a)):
        for y in range(len(matrix_a[x])):
            matrix_c[x][y] -= matrix_b[x][y]
    return matrix_c


myAdjacencyMatrix = create_adjacency_matrix(get_data())
copyAdjacencyMatrix = deepcopy(myAdjacencyMatrix)
myQueue = find_queue(myAdjacencyMatrix)
myStock = find_stock(myAdjacencyMatrix)
print("Максимальний потік: " + str(algorithm_ford_falkersona(myAdjacencyMatrix, myQueue, myStock)))
matrixC = subtract_matrices(myAdjacencyMatrix, copyAdjacencyMatrix)
show_all_node_stream(matrixC)
print(matrixC)
