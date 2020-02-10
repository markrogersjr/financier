source local.rc
ssh -i "$PEMFILE" "$USER"@"$HOST" 'rm -rf financier; git clone https://github.com/markrogersjr/financier.git'
for f in $REMOTE_ENV $BANK_CREDS $PLAID_CREDS $SUBSCRIPTIONS
do
	scp -i "$PEMFILE" $f "$USER"@"$HOST":financier/$f
done
