"""Fzf를 이용하여 lf의 Folder를 이동한다."""
# %% Import
# Standard library imports
import os
import pathlib
import subprocess
import sys

# %% Code
drive = str(pathlib.Path.cwd().drive) + "/"
if sys.argv[1] == "folder":
    output = subprocess.run(
        ["c:/codepy/clis/fzf_folder.bat"], capture_output=True, cwd=drive
    )
    cwd = drive
else:
    output = subprocess.run(["c:/codepy/clis/fzf_files.bat"], capture_output=True)
    cwd = str(pathlib.Path.cwd())
selected = output.stdout.decode("utf-8").strip()
selected = selected.split("\r\n")

if len(selected) == 1:  # Not selected
    sys.exit()
else:
    selected = selected[-1]

selected = os.path.join(cwd, selected).replace("\\", "/")

command = "cd"
if not os.path.isdir(selected):
    command = "select"


def get_cmd_str(target):
    """."""
    cmd_str = [
        "c:/pcsetup/lf/lf",
        "-remote",
        'send {id} {command} "{selected}"'.format(
            id=sys.argv[2], selected=target, command=command
        ),
    ]
    return cmd_str


subprocess.run(get_cmd_str(selected))
