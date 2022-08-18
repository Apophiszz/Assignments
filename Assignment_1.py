import time
import psutil
import os


def write_file(process_id):
    # Grab process object for given pid
    process = psutil.Process(process_id)
    process.cpu_percent()
    cpu_count = psutil.cpu_count()

    # Loop until the process is no longer available
    while(True):
        # Wait for the given time interval
        time.sleep(time_interval)
        try:
            # Grab the necessary info
            cpu_usage = process.cpu_percent() / cpu_count
            working_set = process.memory_info().wset
            committed_memory = process.memory_info().private
            no_of_working_handles = len(process.open_files())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("process no longer exists")
            break
        else:
            # Write info to file
            with open(filename, "w") as f:
                collected_data = {
                    "cpu_usage": cpu_usage,
                    "working_set": working_set,
                    "committed_memory": committed_memory,
                    "no_of_working_handles": no_of_working_handles
                }
                f.write(json.dumps(collected_data))


# Grab user input
path_to_exe = input("insert path to executable ")
process_name = path_to_exe.split("\\")[-1]
time_interval = int(input("add interval "))

# Launch given executable
os.startfile(path_to_exe)
filename = process_name + ".jl"

# Find pid of given executable
process_id = 0
for proc in psutil.process_iter():
    try:
        if process_name == proc.name():
            process_id = proc.pid
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
if process_id:
    write_file(process_id)
