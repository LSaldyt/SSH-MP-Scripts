#/bin/bash

KEYFILE=~/.ssh/id_rsa.pub
AUTHFILE=~/.ssh/authorized_keys

if [ ! -f $KEYFILE ]
then
    echo "No keyfile found, regenerating"
    cd ~/.ssh
    ssh-keygen;
else
    echo "Keyfile already exists, proceeding";
fi

echo "Logging in..."
ssh $1 "[[ -d .ssh ]] || mkdir .ssh && [[ -e $AUTHFILE ]] || touch $AUTHFILE && chmod 0600 $AUTHFILE && cat - >> $AUTHFILE" < $KEYFILE;
# "[[ -d .ssh ]] || mkdir .ssh && [[ -e $AUTHFILE ]] || touch $AUTHFILE && chmod 0600 $AUTHFILE && cat - >> $AUTHFILE" < $KEYFILE;

