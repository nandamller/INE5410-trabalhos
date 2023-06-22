from collections import deque

def create_job_queue():
    '''
    TODO: explicar a função aqui
    '''

    queue = deque()
    for i in range(9):
        # adicionando as linhas na fila
        queue.append(((i,0), (i,8)))

    for i in range(9):
        # adicioando as colunas na fila
        queue.append(((0,i), (8,i)))
    
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # adicioando as regiões na fila
            queue.append(((i, j), ((i + 2, j + 2))))

    return queue

