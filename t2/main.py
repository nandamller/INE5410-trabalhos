from validate_sudoku import validate_sudoku_puzzles
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Necessário argumentos: filename num_de_processos num_de_threads")
    else:
        validate_sudoku_puzzles(file_name=sys.argv[1], num_processes=int(sys.argv[2]), num_threads_per_process=int(sys.argv[3]))
