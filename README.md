# Source code for iUrop fall 2017
Authors: Marcus Wallberg & Johanna Gustafsson

## Ignored directories 
* *src:* Put the csv source file here, we used: wifi_passive_trajectory_node.csv
* *data:* This directory is for saving versions of the original csv for quicker access

## File structure
- jwalk_HDB.py
- src
.. -wifi_passive_trajectory_node.csv

## Dependencies
Only python version 3 has been tested, it should work 
To install the dependencies simply use pip (or pip3 if python 2 and 3 are used)

```
pip install numpy
pip install matplotlib
pip install seaborn
pip install tqdm
pip install pandas
```

## How to use
All python code is collected into a singe file: jwalk_HDB.py simply run this file from a command line `python jwalk_HDB.py` or import the file and call each function `from jwalk_HDB import *`. Every function is documented and some help text is included that can be printed like this:
```python
>>> from jwalk_HDB import *
>>> print(plotTimeHDB_jwalk.__doc__)

	This function plots a histogram on what time people from the HDB area goes to jwalk
	The x axis is the hour of the day and the y axis is the frequency
	
```

Read the description of each function (or pront the `__doc__` as shown above)

Most of the functions could be used as queries that either plots or prints the result.

Some functions are helper functions, this is denoted at the top of the function