source remote.rc
python3.8 main.py
cat results | sendmail -f $FROM_EMAIL -t $TO_EMAIL