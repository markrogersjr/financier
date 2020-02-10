#!/bin/bash
source $HOME/financier/remote.rc
python3.8 main.py
cat $HOME/financier/results | sendmail -f $FROM_EMAIL -t $TO_EMAIL
