"""Archive files."""
# %% Import
import sys
from pathlib import Path
import os.path as osp
from zipfile import ZipFile, ZIP_DEFLATED

if len(sys.argv) < 2:
    sys.exit()

if len(sys.argv) == 2:
    root_folder, filename = osp.split(sys.argv[1])
    name = osp.splitext(filename)[0]
else:
    root_folder, _ = osp.split(sys.argv[1])
    name = osp.split(root_folder)[1]

path = osp.join(root_folder, name + '.zip')
idx_name = -1
while osp.isfile(path):
    path = osp.join(root_folder, name + f'{idx_name}.zip')

with ZipFile(path, 'w', ZIP_DEFLATED) as zf:
    for arg in sys.argv[1:]:
        zf.write(arg, osp.basename(arg))
        if not osp.isdir(arg):
            continue
        path_subdir = Path(arg).expanduser().resolve(strict=True)

        for path_file in path_subdir.glob('**/*'):
            if '__pycache__' in path_file.parts:
                continue
            zf.write(path_file, path_file.relative_to(root_folder))

