import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import datetime

# Read arguments from command line
threads = list(map(int, sys.argv[1].split()))
problem_sizes = list(map(int, sys.argv[2].split()))
num_reps = int(sys.argv[3])
error_bars = sys.argv[4]
connect_points = sys.argv[5]
fit_amdahl = sys.argv[6]
plot_ideal = sys.argv[7]

# Load the data
data = pd.read_csv('time.csv', header=None)
data.columns = ['problem_size', 'number_of_threads', 'execution_time']

# Create a plot
plt.figure(figsize=(10, 6))

# Plot data for each problem size
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # List of colors for plots

for i, ps in enumerate(problem_sizes):
    # Filter data for current problem size
    subset = data[data['problem_size'] == ps]
    
    # Calculate mean and standard deviation of execution time for each thread count
    stats = subset.groupby('number_of_threads')['execution_time'].agg(['mean', 'std'])
    
    # Calculate speedup: time with 1 thread / time with N threads
    speedup = stats.loc[1, 'mean'] / stats['mean']
    speedup_err = speedup * ((stats.loc[1, 'std'] / stats.loc[1, 'mean']) + (stats['std'] / stats['mean']))
    
    if fit_amdahl != '0':
        # fit a function of the form: y = 1 / (s + (1 - s) / threads)
        # to the speedup data
        def func(x, s):
            return 1 / (s + (1 - s) / x)
        
        popt, pcov = curve_fit(func, threads, speedup, bounds=(0, 1))
        
        # Generate a smoothe curve for the fitted function
        x_fitted = np.linspace(min(threads), max(threads), 100)
        y_fitted = func(x_fitted, *popt)
        
        plt.plot(x_fitted, y_fitted, linestyle='--', color=colors[i % len(colors)])
        plot_label=f'size = {ps},  s = {popt[0]:.3f}'
    else:
        plot_label=f'size = {ps}'

    # Connect points with lines or not based on the value of connect_points
    if connect_points == '0':
        points = 'o'
        lines = ''
    else:
        points = '-o'
        lines = '-'
    
    # Plot with or without error bars based on the value of error_bars
    if error_bars == '0':
        plt.plot(threads, speedup, label=plot_label, linestyle=lines, color=colors[i % len(colors)])
    else:
        plt.errorbar(threads, speedup, yerr=speedup_err, label=plot_label, fmt=points, capsize=5, color=colors[i % len(colors)])
        
# if plot_ideal != '0': plot the ideal speedup
if plot_ideal != '0':
    ideal_speedup = np.array(threads)
    plt.plot(threads, ideal_speedup, linestyle='--', color='k', label='Ideal speedup')
    

# Set plot properties
plt.xlabel('Number of Threads')
plt.ylabel('Speedup')
plt.title(f'Strong scaling for different problem sizes averaged over {num_reps} repetitions')
plt.legend()
plt.grid(True)

# Save the plot as a pdf
current_datetime = datetime.datetime.now().strftime("%m-%d_%H:%M")
filename = f'strong_scaling_plot_{current_datetime}.pdf'
plt.savefig(filename)