import multiprocessing
import subprocess

def run_script(script_path):
    command = ["python3", script_path]
    process = multiprocessing.Process(target=subprocess.run, args=(command,))
    process.start()
    return process

if __name__ == "__main__":
    # Specify the paths to your Python files
    python_file1 = "Pi.py"
    python_file2 = "Camera.py"

    # Run the Python files simultaneously
    process1 = run_script(python_file1)
    process2 = run_script(python_file2)

    # Wait for both processes to finish
    process1.join()
    process2.join()

    print("Both scripts have finished.")
