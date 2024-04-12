#!/bin/bash
#SBATCH --job-name=weak_scaling      # Job name    (default: sbatch)
#SBATCH --output=weak_scaling-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=weak_scaling-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128        # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:30:00           # Wall clock time limit

# Define settings for plot
NUM_THREADS=(1 2 4 8 16)
BASE_PROBLEM_SIZES=(64 128 256)
PROBLEM_DIMENSIONS=2
NUM_REPS=2

# Load some modules & list loaded modules
module load gcc
module load python
module list

# delete old files
rm time.csv

# Go back one directory 
cd ..

# Compile
make clean
make


# Run the program
for BASE_PROBLEM_SIZE in ${BASE_PROBLEM_SIZES[@]}; do
    for NUM_THREAD in ${NUM_THREADS[@]}; do
        export OMP_NUM_THREADS=$NUM_THREAD
        # set problem_size = int(base_problem_size * num_threads^(1 / problem_dimensions))
        problem_size=$(echo "$BASE_PROBLEM_SIZE * e(l($NUM_THREAD) / $PROBLEM_DIMENSIONS)" | bc -l)
        problem_size=${problem_size%.*}
        echo "PROBLEM SIZE: $problem_size"
        for REP in $(seq $NUM_REPS); do
            echo -n "$BASE_PROBLEM_SIZE, $NUM_THREAD, " >> ./strong_and_weak_plotting/time.csv
            ./main $problem_size 100 0.005
            echo "" >> ./strong_and_weak_plotting/time.csv
        done
        done
    done

    cd ./strong_and_weak_plotting

# Convert array to a string of space-separated values
num_threads="${NUM_THREADS[@]}"
problem_sizes="${BASE_PROBLEM_SIZES[@]}"

# Call Python script
python weak_plot.py "$num_threads" "$problem_sizes" $NUM_REPS
