import pandas as pd
import matplotlib.pyplot as plt
import sys

# Read arguments from command line
threads = list(map(int, sys.argv[1].split()))
problem_sizes = list(map(int, sys.argv[2].split()))
num_reps = int(sys.argv[3])

# Load the data
data = pd.read_csv('time.csv', header=None)
data.columns = ['problem_size', 'number_of_threads', 'execution_time']

# Create a plot
plt.figure(figsize=(10, 6))

# Plot data for each problem size
for ps in problem_sizes:
    # Filter data for current problem size
    subset = data[data['problem_size'] == ps]
    
    # Calculate mean and standard deviation of execution time for each thread count
    stats = subset.groupby('number_of_threads')['execution_time'].agg(['mean', 'std'])
    
    # Calculate speedup: time with 1 thread / time with N threads
    speedup = stats.loc[1, 'mean'] / stats['mean']
    speedup_err = speedup * ((stats.loc[1, 'std'] / stats.loc[1, 'mean']) + (stats['std'] / stats['mean']))

    # Plot with error bars
    plt.errorbar(threads, speedup, yerr=speedup_err, fmt='-o', capsize=5, label=f'Size = {ps}')

# Set plot properties
plt.xlabel('Number of Threads')
plt.ylabel('Speedup')
plt.title(f'Speedup by Number of Threads and Problem Size averaged over {num_reps} repetitions')
plt.legend()
plt.grid(True)

# Save the plot as a pdf
plt.savefig('strong_scaling_plot.pdf')