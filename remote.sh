#!/bin/bash
# set up a cron job as follows:
#   1. run `crontab -e`
#   2. add a line to crontab file with command
#        `sudo bash $HOME/financier/remote.sh`
cd $HOME/financier
source env.rc
rm -f results
python3.8 main.py --subscriptions_filename $SUBSCRIPTIONS \
                  --plaid_credentials_filename $PLAID_CREDS \
                  --bank_credentials_filename $BANK_CREDS \
                  --from_email $FROM_EMAIL \
                  --to_email $TO_EMAIL
chmod 777 results
cat results | sendmail -f $FROM_EMAIL -t $TO_EMAIL
