# gdb-custom-scripts
This repository will host my gdb scripts for various things. I mostly code them when I solve a hackthebox challenge :)

## tinyalloc.py
This script is useful when https://github.com/thi-ng/tinyalloc is used.
* `dump_tiny_alloc` command dumps the content of the heap
* Every call to `ta_alloc` will be logged in the console