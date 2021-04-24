import datetime
import os
import pathlib
from qstat import qstat
import shutil
import subprocess
import tempfile
import time


def submit_python_job(cmdline, base_working_dir, wallclock_time, required_ram, init_commands=["module load python3/recommended"]):
    jobscript_file = tempfile.NamedTemporaryFile("w")
    job_name = os.path.basename(jobscript_file.name)
    working_dir = os.path.join(base_working_dir, job_name)
    pathlib.Path(working_dir).mkdir()
    output_file = os.path.join(working_dir, "output.pickle")
    jobscript_file.writelines([
        "#!/bin/bash -l\n"
    ] + [
        init_command + "\n" for init_command in init_commands
    ] + [
        f"#$ -N {job_name}\n"
        f"#$ -l h_rt={str(datetime.timedelta(seconds=wallclock_time))}\n",
        f"#$ -l mem={required_ram}G\n",
        f"#$ -wd {working_dir}\n",
        cmdline
    ])
    jobscript_file.flush()
    subprocess.call(f"qsub {jobscript_file.name}", shell=True)
    jobscript_file.close()
    return job_name, working_dir

def wait_job(job_info, callback=None, sleep_time=10):
    job_name, working_dir = job_info
    while True:
        queue_info, job_info = qstat()
        if job_name in {job["JB_name"] for job in queue_info + job_info}:
            time.sleep(sleep_time)
        else:
            break
    if callback is not None:
        callback(working_dir)

def wait_and_cleanup_job(job_info, callback=None, sleep_time=10):
    wait_job(job_info, callback, sleep_time)
    shutil.rmtree(working_dir)