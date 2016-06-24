#!/bin/bash
# Remove ourselves incase anything goes wrong - the script will remain loaded anyways

rm sudo_git_setup.sh
adduser git
cd /home/git/
mkdir .ssh && chmod 700 .ssh
touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys

# Install git if it doesn't exist. Assume Ubuntu :)
hash git 2>/dev/null || { apt-get update; apt-get install git-core; }

#Restrict ssh access to git-shell only
if [ ! -f /etc/shells ]
then echo "No Shells file"
     touch /etc/shells;
else echo "Shells file found";
fi

hash git-shell 2>/dev/null || { echo "WARNING: git-shell not found, ssh users will have normal access"; }

hash git-shell 2>/dev/null && { echo "/usr/bin/git-shell" >> /etc/shells; }

chsh git -s /usr/bin/git-shell
