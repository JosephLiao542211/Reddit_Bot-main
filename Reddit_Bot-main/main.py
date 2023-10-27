import subprocess
import datetime
import os
import glob

scripts = ["Reddit_Scrapper.py", "srtfilefixer.py", "txt_to_srt.py", "Video_Edditor.py"]

with open("log.txt", "a") as log_file:
    for script in scripts:
        start_time = datetime.datetime.now()
        
        log_file.write(f"Started {script} at {start_time}\n")
        
        subprocess.run(["python", script])
        
        end_time = datetime.datetime.now()
        
        log_file.write(f"Finished {script} at {end_time}\n")

def clear_temp():
    files = glob.glob('temp_files/*')
    for f in files:
        os.remove(f)

a = input("Would you like to clear temp files? y/n ")
if a == 'y':
    clear_temp()
    print("Files cleared")
else:
    print("Files not cleared")
    None

