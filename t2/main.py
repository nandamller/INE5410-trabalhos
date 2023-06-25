from validate_sudoku import validate_sudoku_puzzles

if __name__ == '__main__':
    validate_sudoku_puzzles(file_name='input-sample-big.txt', num_processes=1, num_threads_per_process=1)
