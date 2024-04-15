import sys

def calculate_problem_size(base_problem_size, num_threads, problem_dimensions):
    return int(base_problem_size * (num_threads ** (1.0 / problem_dimensions)))

def main():
    if len(sys.argv) != 4:
        print("Usage: script.py <base_problem_size> <num_threads> <problem_dimensions>")
        sys.exit(1)

    try:
        base_problem_size = float(sys.argv[1])
        num_threads = float(sys.argv[2])
        problem_dimensions = float(sys.argv[3])
    except ValueError:
        print("All arguments must be numbers.")
        sys.exit(1)

    problem_size = calculate_problem_size(base_problem_size, num_threads, problem_dimensions)
    print(problem_size)

if __name__ == "__main__":
    result = main()
    # Optionally print the result if needed for debug, otherwise just store or use it.
    # print(result)
