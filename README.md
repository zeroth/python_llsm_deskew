# python_llsm_deskew
Simple Python script for deskewing Lattice Light Sheet Data


# Please install the following.
------------------------------------
```
conda install -c conda-forge pycudadecon
pip install tifffile
```
-----------
Ref:
pycudadecon : https://github.com/tlambert03/pycudadecon/

# Usages
```
python deskew.py [DIR] [OPTIONS]

positional arguments:
  input_dir

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -ag [ANGLE], --angle [ANGLE]
  -dx [XPIXEL], --xpixel [XPIXEL]
  -dz [ZPIXEL], --zpixel [ZPIXEL]

```
