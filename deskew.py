import argparse
from pycudadecon.affine import deskewGPU
import tifffile as tf
from pathlib import Path
import os

"""
Author: Abhishek Patil <abhishek@zeroth.me>
"""
"""
please install the following
------------------------------------
conda install -c conda-forge pycudadecon
pip install tifffile

-----------
FYI:
pycudadecon https://github.com/tlambert03/pycudadecon/
"""


def deskew_file(input_file_path, output_dir, angle: float = 31.8, dx: float = 0.104, dz: float = 0.4):
    """Deskews a file at `input_file_path`.

    Args:
    ----
        input_file_path (str): input tiff file path
        output_dir (str): output dir , where the output file will be written
        angle: LSSM acqusition in degree, defaults = 31.8.
        dx: X pixel size, default = 0.104. (normally Y size is same as X)
        dz: Z step size, default = 0.4.
    """
    input_file = Path(input_file_path)
    output_dir = Path(output_dir)
    output_file = output_dir.joinpath(input_file.name)

    im = tf.imread(input_file)
    deskewed = deskewGPU(im=im, dxdata=dx, dzdata=dz, angle=angle)
    tf.imwrite(output_file, deskewed)
    print(f"deskewed {output_file}")


def deskew_dir(input_dir: Path, angle: float = 31.8, dx: float = 0.104, dz: float = 0.4):
    """Deskews a files at `input_dir`.
    This function automatically create a `deskewed` output dir inside the input_dir

    Args:
    ----
        input_dir (str): input tiff directory path
        angle: LSSM acqusition in degree, defaults = 31.8.
        dx: X pixel size, default = 0.104. (normally Y size is same as X)
        dz: Z step size, default = 0.4.
    """
    print(f"Deskewing dir {input_dir.absolute()}")
    input_dir = Path(input_dir.absolute())
    output_dir = input_dir.joinpath("deskewed")
    print(f"output dir {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    files = list(input_dir.glob("*.tif*"))
    print(f"found {len(files)} file(s)")
    for f in files:
        deskew_file(f, output_dir=output_dir, angle=angle, dx=dx, dz=dz)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [DIR]..."
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('input_dir', type=Path)
    parser.add_argument('-ag', '--angle', nargs='?', const=float, default=31.8)
    parser.add_argument('-dx', '--xpixel', nargs='?', const=float, default=0.104)
    parser.add_argument('-dz', '--zpixel', nargs='?', const=float, default=0.4)

    return parser


if __name__ == "__main__":
    import argparse
    parser = init_argparse()
    args = parser.parse_args()
    print(args.input_dir, args.angle, args.xpixel, args.zpixel)
    deskew_dir(args.input_dir, args.angle, args.xpixel, args.zpixel)
