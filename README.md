# emulab_util
A utility for rapidly deploying Emulab experiments from the command line.

## What is this
I built this tool to aid in my own deployment but I also designed it to be easily modified for any application. So far I've implemented the following functionality:
1. Swapping Emulab Experiments in and out.
2. Copying files and directories to Emulab hosts.
3. Running local and remote scripts on Emulab hosts.
4. Running commands directly on Emulab hosts.

## How to use it
I've setup some example code (what I use for my own project) in the setup.py file. It can be run by using `python setup.py`. If you're interested in using the project you can modify that code directly, or simply include the setup file and use the EmulabUtil class in any other file.

## Planned Improvements:
1. Use the native python bindings for Emulab's XMLAPI.
2. Implement more checking all over the place.
3. Coordinate SSH connections so they're not created and deleted all over the place.
4. More (?)

