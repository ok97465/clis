"""Path to Clipboard."""
# %% Import
# Standard library imports
import os.path as osp
import sys

# Third party imports
import pyperclip as pc

if len(sys.argv) < 3:
    sys.exit()


# %% Functions
def get_full_path(arg: str) -> str:
    """."""
    return arg


def get_basename(arg: str) -> str:
    """."""
    return osp.basename(arg)


def get_basename_no_ext(arg: str) -> str:
    """."""
    return osp.splitext(osp.basename(arg))[0]


# %% Get Path
idx_mode = int(sys.argv[1])
func = {0: get_full_path, 1: get_basename, 2: get_basename_no_ext}[idx_mode]
paths = [func(p) for p in sys.argv[2:]]

ret = "\n".join(paths)
pc.copy(ret)

