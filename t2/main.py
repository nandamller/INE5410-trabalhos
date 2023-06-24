from validate_sudoku import validate_sudoku_puzzles

if __name__ == '__main__':
    validate_sudoku_puzzles(file_name='input-sample.txt', num_processes=4, num_threads_per_process=2)
