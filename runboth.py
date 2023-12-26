import subprocess
import sys
import time
import matplotlib.pyplot as plt

# Paths to the client and server scripts
client_script_path = r'C:\Users\Andrew\OneDrive\Documents\PyFolderTest\Client.py'
server_script_path = r'C:\Users\Andrew\OneDrive\Documents\PyFolderTest\Server.py'

def run_scripts():
    server_process = subprocess.Popen([sys.executable, server_script_path])

    start_time = time.perf_counter()
    client_process = subprocess.Popen([sys.executable, client_script_path])
    client_process.wait()
    end_time = time.perf_counter()

    server_process.terminate()

    return end_time - start_time

if __name__ == "__main__":
    number_of_runs = 1000
    run_times = []
    run_scripts()
    # for _ in range(number_of_runs):
    #     total_time = run_scripts()
    #     run_times.append(total_time)
    #     print(f"Run {_+1}: {total_time} seconds")
        
    # average_time = sum(run_times) / number_of_runs
    # print(f"Average run time: {average_time} seconds")
    # # Plotting the distribution
    # plt.hist(run_times, bins=50, edgecolor='black')
    # plt.title('Distribution of Run Times over 10,000 Runs')
    # plt.xlabel('Run Time (seconds)')
    # plt.ylabel('Frequency')
    # plt.show()