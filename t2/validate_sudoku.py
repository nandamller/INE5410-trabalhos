

import multiprocessing
from worker_process import worker_process


def validate_sudoku_puzzles(file_name: str, num_processes: int, num_threads_per_process: int):
    '''
    TODO: explicar o método aqui
    '''
    if num_threads_per_process > 27:
        num_threads_per_process = 27
    puzzles_queue = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    process_pool = []
    for i in range(num_processes):
        process_pool.append(multiprocessing.Process(target=worker_process, args=(i, num_threads_per_process, 
                                                    puzzles_queue)))
        process_pool[i].start()

    with open(file_name, 'r') as file:
        for index, puzzle in enumerate(file.read().split('\n\n')):
            puzzle = [list(map(int, line)) for line in puzzle.split('\n')]
            puzzles_queue.put((index,puzzle))

    for _ in range(num_processes):
        puzzles_queue.put((-1,-1))

    for process in process_pool:
        process.join()

