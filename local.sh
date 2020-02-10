source local.rc
ssh -i "$PEMFILE" "$USER"@"$HOST" 'sudo rm -rf financier; git clone https://github.com/markrogersjr/financier.git; chmod 777 financier/remote.sh'
for f in $REMOTE_ENV $BANK_CREDS $PLAID_CREDS $SUBSCRIPTIONS
do
	scp -i "$PEMFILE" $f "$USER"@"$HOST":financier/$f
done
