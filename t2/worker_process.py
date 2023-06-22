
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
            results = [thread_pool.submit(worker_thread, i, job_queue, job_lock,
                                        list_errors, puzzle) for i in range(num_threads)]
        
        for result in results:
            errors = result.result()
        print(f"Processo {process_id}: {sum(len(error) for error in errors)} erros encontrados: {errors}")
            
        # while job_queue:
        #     if len(thread_pool) < num_threads:
        #         thread = threading.Thread(target=work_thread, args=((job_queue.popleft()), list_errors[len(thread_pool)]))

        #         thread_pool.append(thread)
        #         thread.start()
        #     else:
        #         print(f'ainda sobraram {len(job_queue)} trabalhos na fila no processo {process_id}')
        #         break

        # for thread in thread_pool:
        #     thread.join()

        # for i in list_errors:
        #     print(i)

        # return 0


def worker_thread(id: int, job_queue: deque, job_lock:threading.Lock, list_errors: list, puzzle: list):
    print(f"Thread {id} inicializada")
    while job_queue:
        with job_lock:
            job = job_queue.popleft()
        lista = []

        for i in range(job[0][1], job[1][1]+1):
            for j in range(job[0][0], job[1][0]+1):
                if puzzle[i][j] in lista:
                    if (job[0][0] - job[1][0]) == 0:
                        list_errors[id].append(f'C{job[0][0]+1}')
                    elif (job[0][1] - job[1][1]) == 0:
                        list_errors[id].append(f'L{job[0][1]+1}')
                    else:
                        r = job[0][0] + job[0][1]//3 + 1
                        list_errors[id].append(f'R{r}')
                    print(f"Thread {id} contou erro")
                else:
                    lista.append(puzzle[i][j])

    # print(list_errors)
    return(list_errors)


def validate_sudoku(puzzle) -> bool: 
    # TODO: Implementar aqui a validação do quebra-cabeças Sudoku
    # Retorna True se a solução é válida e False caso contrário
    pass