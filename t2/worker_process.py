
import multiprocessing
import threading
import concurrent.futures as ft
from helper import create_job_queue
from collections import deque


def worker_process(process_id: int, num_threads: int, job_queue, puzzle_queue):
    # TODO: Implementar aqui o trabalho de cada processo (criando as Threads)
    while True:
        index, puzzle = puzzle_queue.get()
        if index == -1:
            break
        job_queue = create_job_queue()
        job_lock = threading.Lock()
        print(f"Processo {process_id+1}: resolvendo quebra-cabeças {index+1}")
        # lista de erros única p cada thread
        list_errors = [[] for _ in range(num_threads)]

        with ft.ThreadPoolExecutor(num_threads) as thread_pool:
            results = [thread_pool.submit(worker_thread, i, job_queue, 
                                          job_lock, puzzle) for i in range(num_threads)]
        s = ['' for _ in range(num_threads)]
        for i, result in enumerate(results):
            errors = result.result()
            list_errors.append(errors)
            s[i] = f"T{i}: " + ', '.join([*set(errors)])
        ne = sum(len(error) for error in list_errors)
        print(f"Processo {process_id+1}: {ne} erros encontrados", end='')
        if ne: print(f" ({'; '.join(s)})")
        else: print()


def worker_thread(id: int, job_queue: deque, job_lock:threading.Lock, puzzle: list):
    # print(f"Thread {id} inicializada")
    list_errors = []
    while job_queue:
        job = job_queue.popleft()
        lista = []
        for i in range(job[0][1], job[1][1]+1):
            for j in range(job[0][0], job[1][0]+1):
                if puzzle[i][j] in lista:
                    if (job[0][0] - job[1][0]) == 0:
                        list_errors.append(f'C{job[0][0]+1}')
                    elif (job[0][1] - job[1][1]) == 0:
                        list_errors.append(f'L{job[0][1]+1}')
                    else:
                        r = job[0][0] + job[0][1]//3 + 1
                        job_lock.acquire()
                        list_errors.append(f'R{r}')
                        job_lock.release()
                    # print(f"Thread {id} contou erro")
                else:
                    lista.append(puzzle[i][j])

    # print(list_errors)
    return(list_errors)


def validate_sudoku(puzzle) -> bool: 
    # TODO: Implementar aqui a validação do quebra-cabeças Sudoku
    # Retorna True se a solução é válida e False caso contrário
    pass