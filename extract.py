"""."""
# Standard library imports
import os
import os.path as osp
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from platform import system
from zipfile import ZipFile


def get_outfolder_tmp(path: str):
    """압축을 풀 임시 폴더 이름을 생성한다."""
    folder_archive = osp.dirname(path)
    folder_tmp = osp.join(folder_archive, "_tmp_ok97465_")
    return folder_tmp


def move_output(path):
    """임시 폴더에 압축을 푼 후 임시 폴더의 파일을 유효한 폴더로 이동한다."""
    folder_base = osp.dirname(path)
    folder_tmp = get_outfolder_tmp(path)

    list_out = os.listdir(folder_tmp)

    if len(list_out) == 1:
        src = osp.join(folder_tmp, list_out[0])
        shutil.move(src, folder_base)
        shutil.rmtree(folder_tmp)
        return

    basename = osp.splitext(osp.basename(path))[0]
    folder_out = osp.join(folder_base, basename)

    idx = -1
    while osp.isdir(folder_out):
        idx += 1
        folder_out = osp.join(folder_base, f"{basename}_{idx}_")

    shutil.move(folder_tmp, folder_out)


def extract_zip(path):
    """Zip 확장자 파일의 압축을 푼다."""
    folder_tmp = get_outfolder_tmp(path)
    with ZipFile(path, "r") as zf:
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            break

    with ZipFile(path, "r") as zf:
        if is_encrypted:
            password = input("Input password: ")
            if system() == "Windows":
                zf.extractall(folder_tmp, pwd=bytes(password, "euc-kr"))
            else:
                zf.extractall(folder_tmp, pwd=bytes(password, "utf-8"))
        else:
            zf.extractall(folder_tmp)

    move_output(path)


def extract_gz(path):
    """tar.gz 확장자 파일의 압축을 푼다."""
    folder_tmp = get_outfolder_tmp(path)

    with tarfile.open(path, "r:gz") as tf:
        tf.extractall(folder_tmp)

    move_output(path)


def extract_bz2(path):
    """tar.bz2 확장자 파일의 압축을 푼다."""
    folder_tmp = get_outfolder_tmp(path)

    with tarfile.open(path, "r:bz2") as tf:
        tf.extractall(folder_tmp)

    move_output(path)


def extract_iso(path):
    """ISO 확장자 파일의 압축을 푼다."""
    folder_tmp = get_outfolder_tmp(path)
    proc = subprocess.Popen(
        ["7z", "x", path, f"-o{folder_tmp}"], stdout=subprocess.PIPE
    )
    out, err = proc.communicate()
    print(out.decode("utf-8"))
    move_output(path)


if len(sys.argv) < 2:
    sys.exit()

for arg in sys.argv[1:]:
    path = Path(arg)
    path = path.expanduser().resolve(strict=True)
    ext = path.suffix.lower()
    try:
        if ext == ".zip":
            extract_zip(path)
        elif ext == ".iso":
            extract_iso(path)
        elif ext == ".gz":
            extract_gz(path)
        elif ext == "bz2":
            extract_bz2(path)
    except Exception as e:
        print(e)
