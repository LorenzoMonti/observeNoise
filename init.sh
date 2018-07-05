#!/bin/bash

# per editare il crontab questo è il comando: crontab -e
# per visualizzare i log di crontab attivi:
# TODO generalizza il path, soprattutto quello nello script Python
# TODO pensare a come immagazzinare gli mp3 una volta salvati

TIME=30
SOUNDMETER_SPATH=~/.soundmeter/
echo "Hello, start bash script..."


# guardo il meteo, se piove/nevica/grandina prendo i dati per fine statistico ma l'analyzer ritornerà che non è stata fatta festa.
# questo perchè avendo solamente un microfono a disposizione le condizioni atmosferiche rendono impossibile analizzare, unito al fatto che si
# suppone che se ci sono schiamazzi saranno fatti all'interno diminuendo sicuramente i db complessivi.
ansiweather -l Bologna -f 1 -a false -s true | tail -c 5 > $SOUNDMETER_SPATH/weather.csv

# utilizziamo soundmeter per collezionare i dati dalle 20:00pm alle 5:00am, vengono campionati i dati ogni 10 secondi.
# in questo modo i due comandi sono lanciati in parallelo (vedi simbolo & alla fine del comando) e sono bloccanti per i comandi successivi.
#arecord -vv -d "$TIME" -t raw | lame -r -h -V 0 -b 128 -B 224 - gathered_mp3/arecord$(date +%F).mp3 &
arecord -d "$TIME" -r 44100 $SOUNDMETER_SPATH/gathered_mp3/$(date +%F).wav &
soundmeter -s "$TIME" --segment 10 --log /dev/stdout 2>/dev/null | unbuffer -p perl -p -e 's/\s*(\d+)\s+(.{19})(.*)/"$2,". 20*log($1)/e' > $SOUNDMETER_SPATH/meter_tmp.csv &
wait

# comando per trovare il PID di soundmeter
# soundmeter_pid=$!
# killiamo il processo soundmeter, altrimenti continua a campionare
# kill -9 $soundmeter_pid


# eliminiamo le ultime 3 righe dal file csv generato da soundmeter. In output ci sono timeout e quando il processo viene stoppato.
head -n -3 $SOUNDMETER_SPATH/meter_tmp.csv > $SOUNDMETER_SPATH/meter.csv
# rimuoviamo il file temporaneo
rm $SOUNDMETER_SPATH/meter_tmp.csv

# convertiamo il file wav generato comprimendolo
lame -b 128 -m j -h -V 1 -B 256 -F $SOUNDMETER_SPATH/gathered_mp3/$(date +%F).wav $SOUNDMETER_SPATH/gathered_mp3/$(date +%F).mp3
# compress file mp3
tar -czvf $SOUNDMETER_SPATH/gathered_mp3/$(date +%F).tar.gz $SOUNDMETER_SPATH/gathered_mp3/$(date +%F).mp3
# rimuoviamo il file wav
#rm gathered_mp3/$(date +%F).wav
# rimuoviamo il file mp3
#rm gathered_mp3/$(date +%F).mp3

echo "Great job, data gathered... now we analyze them!"

# script python atto ad analizzare i dati raccolti al fine di notificare o meno l'aumento di db durante la notte
python $SOUNDMETER_SPATH/analyzer.py

echo "saving data"

# i dati della giornata verranno poi salvati nella cartella gathered_data
cp $SOUNDMETER_SPATH/meter.csv $SOUNDMETER_SPATH/gathered_data/meter$(date +%F).csv
# rimuoviamo meter.csv dopo averlo salvato sulla cartella gathered_data
rm $SOUNDMETER_SPATH/meter.csv
echo "sending whatsapp message..."

# TODO installa tool e aggiungi comando per inviare i messaggi
