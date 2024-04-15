#!/bin/bash
#SBATCH --job-name=weak_scaling      # Job name    (default: sbatch)
#SBATCH --output=weak_scaling-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=weak_scaling-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128        # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:30:00           # Wall clock time limit

# Settings for Benchmarking
NUM_THREADS=(1 4 16 64)
BASE_PROBLEM_SIZES=(64 128 256)
NUM_REPS=5
PROBLEM_DIMENSIONS=2

# Settings for Plot
ERROR_BARS=1
CONNECT_POINTS=0
FIT_GUSTAFSON=1
PLOT_IDEAL=1



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
        problem_size=$(python ./strong_and_weak_plotting/calc.py $BASE_PROBLEM_SIZE $NUM_THREAD $PROBLEM_DIMENSIONS)
        # Run once without saving the time 
        echo -n "$BASE_PROBLEM_SIZE, $NUM_THREAD, " >> ./strong_and_weak_plotting/time.csv
        ./main $problem_size 100 0.005
        echo "" >> ./strong_and_weak_plotting/time.csv
        sed -i '$ d' ./strong_and_weak_plotting/time.csv
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
python weak_plot.py "$num_threads" "$problem_sizes" $NUM_REPS $ERROR_BARS $CONNECT_POINTS $FIT_GUSTAFSON $PLOT_IDEAL
