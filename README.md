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
 3. install [inspectNoise](https://github.com/LorenzoMonti/inspectNoise/tree/master)
 4. install library dependencies
 ```
 pip install -r requirements.txt
 ```
 5. create the following directory
 ```
 mkdir gathered_data
 ```
## How to use
1. add your personal ROOT in `analyze.py`
2. launch init.sh: `sh init.sh`
3. enjoy! :)


## Optional configuration
in util folder you can find:
1. `ssh_reverse_tunnel.sh` in order to create SSH Reverse Tunnel. Change port (over 1024), user, server_URL.
2. `check_tunneling_alive.sh` in order to check if SSH Reverse Tunnel is alive. Change server_ip with your server IP.

insert scripts in /etc/rc.local if you want execute at boot-time.
