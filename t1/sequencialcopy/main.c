#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include "gol.h"

int main(int argc, char **argv)
{
    int size, steps;
    cell_t **prev, **next, **tmp;
    FILE *f;
    stats_t stats_step = {0, 0, 0, 0};
    stats_t stats_total = {0, 0, 0, 0};

    if (argc != 3)
    {
        printf("ERRO! Você deve digitar %s <nome do arquivo do tabuleiro> <número de threads>!\n\n", argv[0]);
        return 0;
    }

    if ((f = fopen(argv[1], "r")) == NULL)
    {
        printf("ERRO! O arquivo de tabuleiro '%s' não existe!\n\n", argv[1]);
        return 0;
    }

    int n_threads = atoi(argv[2]);

    fscanf(f, "%d %d", &size, &steps);

    if (n_threads > size)
        n_threads = size;

    prev = allocate_board(size);
    next = allocate_board(size);

    read_file(f, prev, size);

    fclose(f);

#ifdef DEBUG
    printf("Initial:\n");
    print_board(prev, size);
    print_stats(stats_step);
#endif

    pthread_t threads[n_threads];
    thread_args args[n_threads];

    // int op_thread = a_size/n_threads;
    // int resto = a_size%n_threads;

    for (int i = 0; i < n_threads; i++)
    {
        args[i].i = i*(ceil(size/n_threads));
        args[i].f = i*(ceil(size/n_threads)) + ceil(size/n_threads);
        if (i==n_threads-1) args[i].f = size;
        args[i].size = size;
    }

    for (int i = 0; i < steps; i++)
    {
        stats_step = play(prev, next, args, threads, size, n_threads);
        
        stats_total.borns += stats_step.borns;
        stats_total.survivals += stats_step.survivals;
        stats_total.loneliness += stats_step.loneliness;
        stats_total.overcrowding += stats_step.overcrowding;

#ifdef DEBUG
        printf("Step %d ----------\n", i + 1);
        print_board(next, size);
        print_stats(stats_step);
#endif
        tmp = next;
        next = prev;
        prev = tmp;
    }

#ifdef RESULT
    printf("Final:\n");
    print_board(prev, size);
    print_stats(stats_total);
#endif

    free_board(prev, size);
    free_board(next, size);
}
