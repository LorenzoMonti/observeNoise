#!/bin/sh

#echo "$(netstat -n --protocol inet | grep 'server_ip:22')"

if [ -n "$(netstat -n --protocol inet | grep 'server_ip:22')" ];
	then echo "connessione ssh verso server_ip:22 eseguita con successo!"
	else "$(sudo reboot)"
fi

