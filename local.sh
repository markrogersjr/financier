source local.rc
ssh -i "$PEMFILE" "$USER"@"$HOST" 'git clone https://github.com/markrogersjr/financier.git'
for f in $REMOTE_ENV $BANK_CREDS $BANK
do
	scp -i "$PEMFILE" "$USER"@"$HOST":$f financier/$f
done
