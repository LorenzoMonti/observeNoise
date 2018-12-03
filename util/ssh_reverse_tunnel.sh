#!/bin/bash
su pi -c "nohup ssh -T -N -R *:port:localhost:22 user@server > /dev/null"



