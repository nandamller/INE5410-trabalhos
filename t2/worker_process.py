
import multiprocessing
import threading

from collections import deque


def worker_process(process_id: int, puzzle, num_threads: int, job_queue):
    # TODO: Implementar aqui o trabalho de cada processo (criando as Threads)
    thread_pool = []

    # lista de erros única p cada thread
    list_errors = [[] for _ in range(num_threads)]

    while job_queue:
        if len(thread_pool) < num_threads:
            thread = threading.Thread(target=work_thread, args=((job_queue.popleft()), list_errors[len(thread_pool)], puzzle))

            thread_pool.append(thread)
            thread.start()
        else:
            print(f'ainda sobraram {len(job_queue)} trabalhos na fila no processo {process_id}')
            break

    for thread in thread_pool:
        thread.join()

    for i in list_errors:
        print(i)

    return 0


def work_thread(job: tuple, list_errors: list, puzzle: list):
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
                    list_errors.append(f'R{r}')
            else:
                lista.append(puzzle[i][j])

    print(list_errors)


def validate_sudoku(puzzle) -> bool: 
    # TODO: Implementar aqui a validação do quebra-cabeças Sudoku
    # Retorna True se a solução é válida e False caso contrário
    pass