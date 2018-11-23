# ObserveNoise Project

This repository contains Bash and Python code which reads decibel levels and record audio from a connected USB sound level meter, in order to analyze and saves data and plot related to it. All tests were done with a Rasbperry Pi 2 Model B.

## How to install

 1. Create a new virtual environment inside the directory:
 ```
 virtualenv env
 ```
 2. then activate the virtual environment  
 ```
 source env/bin/activate
 ```
 3. install [soundmeter](https://github.com/shichao-an/soundmeter)
 4. install library dependencies
 ```
 pip install -r requirements.txt
 ```
 5. create the following directory
 ```
 mkdir gathered_data gathered_mp3 plot_data
 ```
## How to use
1. add your personal ROOT in `analyze.py`
2. launch init.sh: `sh init.sh`
3. enjoy! :)
