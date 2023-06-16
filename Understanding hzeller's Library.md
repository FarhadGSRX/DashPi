
# Chronologically
1. Hzeller created everything in /lib and /include. This is pure C++.
2. Some-Dev created the /bindings/python/rgbmatrix files: specifically writing the cppinc.pxd, core.pyx, core.pxd, graphics.pyx, and graphicx.pxd files. As I understand it...
	1. cppinc.pxd dictates what we want the Python module to connect to in the C Library. All the relevant classes, the functions, the variables within, the structure of inputs and expected dtypes of outputs.
	2. Then core.pxd and graphics.pxd sort of reference it for their definitions.
	3. This leaves the .pyx files, which have to take the definitions within .pxd and actually implement them.
	4. Then Some-Dev runs the Cython compiler to generate the core.cpp and graphics.cpp files. These are now pure c++ source code that can be used to build a C program compatible with the end-user system (the goal of "build")
3. This is all packaged up and pushed to Git.
4. End-User clones package and runs `make build-python` which runs another "make build" command, but this time inside the bindings/python folder. This runs `setup.py`, activating distutils to take a bunch of files including the aforementioned .cpp files, the C sources files (from /lib and /include) and compile them all together into a Package called `rgbmatrix` with 2 modules (core and graphics). This package serves as our C-extension.
# The Files
## Library Source Files (Files that exist before compiling)
- /lib
	- Makefile
	- bdf-font.cc
	- content-streamer.cc
	- framebuffer-internal.h
	- framebuffer.cc
	- gpio-bits.h
	- gpio.cc
	- gpio.h
	- graphics.cc
	- hardware-mapping.c
	- hardware-mapping.h
	- led-matrix-c.cc
	- led-matrix.cc
	- multiplex-mappers-internal.h
	- multiplex-mappers.cc
	- options-initialize.cc
	- pixel-mapper.cc
	- thread.cc
	- utf8-internal.h
- /include
	- canvas.h
	- content-streamer.h
	- graphics.h
	- led-matrix-c.h
	- led-matrix.h
	- pixel-mapper.h
	- thread.h
	- threaded-canvas-manipulator.h
- /bindings/python/rgbmatrix
	- Makefile
	- init.py
	- core.cpp
	- core.pxd
	- core.pyx
	- cppinc.pxd
	- graphics.cpp
	- graphics.pxd
	- graphics.pyx
# Canvas.h
## Coordinates
0,0 is top left corner

## Properties
- height
- width
## Functions
- SetPixel(int x, int y, uint8_t red, uint8_t green, uint8_t blue)
- Fill(uint8_t red, uint8_t green, uint8_t blue)
- Clear()

## content-streamer.h



# What happens during the compile
User> cd rpi-rgb-led-matrix
User> make clean
	Makefile> make clean: cleans everything up from prior compilations	
User> make build-python PYTHON=python3
	Makefile> build-python: The build-python command tells it to spawn a process, change directories to the python bindings directory, and run another "build" command.
User> sudo make install-python PYTHON=python3
	Makefile> install-python: Same as above, but it says to go run an "install" command instead. And would you look at that, **this** is what runs the `python3 setup.py` command to produce our final build module.

Root Makefile (build-python)
	➥ Python Makefile (build)
		➥ python setup.py (build-args: build --build-lib . --executable=/usr/bin/$(PYEXEC))
			➥

Setup.py
inst-args: install --no-compile -O0

1. Proclaims `core_ext` as an Extension, and gives it directions to the sources it will need: rgbmatrix/core.cpp 