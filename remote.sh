#!/bin/bash
source $HOME/financier/remote.rc
rm -f $HOME/financier/results
python3.8 $HOME/financier/main.py
chmod 777 $HOME/financier/results
cat $HOME/financier/results | sendmail -f $FROM_EMAIL -t $TO_EMAIL
