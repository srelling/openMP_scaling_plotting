# Strong and Weak Scaling Benchmarking

This folder contains bash scripts for benchmarking an OpenMP program using strong and weak scaling.

## Usage

Follow these steps to use the scripts:

1. Add the `strong_and_weak_plotting` folder to the directory where your Makefile is located.

2. Adjust the line `./main` in the bash scripts to run your own program. Pass `PROBLEM_SIZE` as an argument to your program.

3. Add the following code to the execution of your OpenMP C++ program to write the execution time to a CSV file:

    ```c++
    FILE *file = fopen("strong_and_weak_plotting/time.csv", "a"); 
    if (file == NULL) {
      printf("Error opening file!\n");
      return 1;
    }
    fprintf(file, "%.8f, ", time_end - time_start);
    fclose(file);
    ```

4. Adjust the settings (`NUM_THREADS`, `BASE_PROBLEM_SIZE`, `PROBLEM_DIMENSIONS`, `NUM_REPS`) at the top of the bash scripts to match your requirements.

5. Run the scripts using the `sbatch` command. Use `sbatch run_strong_scaling.sh` for strong scaling and `sbatch run_weak_scaling.sh` for weak scaling.

Please note that these scripts are designed to be run on a system with the Slurm workload manager installed. If you're using a different workload manager, you may need to adjust the scripts accordingly.
