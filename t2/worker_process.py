

import concurrent.futures as ft
from helper import create_job_queue


def worker_process(process_id: int, num_threads: int, puzzle_queue):
    # TODO: Implementar aqui o trabalho de cada processo (criando as Threads)
    job_queue = create_job_queue()
    while True:
        index, puzzle = puzzle_queue.get()
        if index == -1:
            break
        print(f"Processo {process_id+1}: resolvendo quebra-cabeças {index+1}")
        # lista de erros única p cada thread
        list_errors = [[] for _ in range(num_threads)]

        with ft.ThreadPoolExecutor(num_threads) as thread_pool:
            results = [thread_pool.submit(worker_thread, i, 
                                          job_queue[i*len(job_queue)//num_threads:(i+1)*len(job_queue)//num_threads], 
                                          puzzle) for i in range(num_threads)]
        s = ['' for _ in range(num_threads)]
        for i, result in enumerate(results):
            errors = result.result()
            list_errors.append(errors)
            temp = []
            for x in errors: 
                if x not in temp: 
                    temp.append(x)
            s[i] = f"T{i}: " + ', '.join(temp)
        ne = sum(len([*set(error)]) for error in list_errors)
        print(f"Processo {process_id+1}: {ne} erros encontrados", end='')
        if ne: print(f" ({'; '.join(s)})")
        else: print()


def worker_thread(id: int, job_queue: list, puzzle: list[list]):
    list_errors = []
    for job in job_queue:
        lista = []
        for i in range(job[0][0], job[1][0]+1):
            for j in range(job[0][1], job[1][1]+1):
                if puzzle[i][j] in lista:
                    if (job[0][0] == job[1][0]):
                        list_errors.append(f'L{job[0][0]+1}')
                    elif (job[0][1] == job[1][1]):
                        list_errors.append(f'C{job[0][1]+1}')
                    else:
                        r = job[0][0] + job[0][1]//3 + 1
                        list_errors.append(f'R{r}')
                else:
                    lista.append(puzzle[i][j])

    return(list_errors)
