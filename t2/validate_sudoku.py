import multiprocessing
import threading
from collections import deque
import time
from helper import create_job_queue
from worker_process import worker_process

def validate_sudoku_puzzles(file_name: str, num_processes: int, num_threads_per_process: int):
    '''
    TODO: explicar o método aqui
    '''
    # puzzle_sem = multiprocessing.Semaphore(0) # Semaforo desativado. multiprocessing.Queue ja implementa um semaforo
    puzzles_queue = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    cond = multiprocessing.Condition(lock)
    job_queue = create_job_queue()
    # print(job_queue)
    process_pool = []
    for i in range(num_processes):
        process_pool.append(multiprocessing.Process(target=worker_process, args=(i, num_threads_per_process, 
                                                    job_queue, puzzles_queue)))
        process_pool[i].start()

    with open(file_name, 'r') as file:
        for index, puzzle in enumerate(file.read().split('\n\n')):
            puzzle = [list(map(int, line)) for line in puzzle.split('\n')]
            puzzles_queue.put((index,puzzle))
            # puzzle_sem.release()

    for _ in range(num_processes):
        puzzles_queue.put((-1,-1))

    for process in process_pool:
        process.join()

            # print(puzzle)
            # print(puzzle_sem.get_value())

            # if len(process_pool) < num_processes:
            #     # retirando um jogo da fila de jogos
            #     puzzle = puzzles_queue.popleft()

            #     #process_puzzles = puzzle
            #     process = multiprocessing.Process(
            #         target=worker_process,
            #         args=(len(process_pool), num_threads_per_process, job_queue)
            #     )
            #     process_pool.append(process)
            #     process.start()

    # while fila nao vazia
    # se num_de_processos_ativos < max_de_processos
    #         cria processo e retira matriz da fila

    # for process in process_pool:
    #     process.join()

    # print(f'ainda sobraram {len(puzzles_queue)} jogos na fila.')

