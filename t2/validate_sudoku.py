import multiprocessing
import threading

from collections import deque

from helper import create_job_queue
from worker_process import worker_process

def validate_sudoku_puzzles(file_name: str, num_processes: int, num_threads_per_process: int):
    '''
    TODO: explicar o método aqui
    '''
    process_pool = []

    puzzles_queue = deque()
    job_queue = create_job_queue()

    with open(file_name, 'r') as file:
        for index, puzzle in enumerate(file.read().split('\n\n')):
            puzzle = [list(map(int, line)) for line in puzzle.split('\n')]
            puzzles_queue.append(puzzle)

            if len(process_pool) < num_processes:
                # retirando um jogo da fila de jogos
                puzzle = puzzles_queue.popleft()

                #process_puzzles = puzzle
                process = multiprocessing.Process(
                    target=worker_process,
                    args=(len(process_pool), puzzle, num_threads_per_process, job_queue)
                )
                process_pool.append(process)
                process.start()
            
    # while fila nao vazia
    # se num_de_processos_ativos < max_de_processos
    #         cria processo e retira matriz da fila

    for process in process_pool:
        process.join()
    
    print(f'ainda sobraram {len(puzzles_queue)} jogos na fila.')

