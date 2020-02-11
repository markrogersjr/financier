#!/bin/bash
cd $HOME/financier
source remote.rc
rm -f results
python3.8 main.py
chmod 777 results
cat results | sendmail -f $FROM_EMAIL -t $TO_EMAIL
