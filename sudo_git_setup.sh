#!/bin/bash
# Remove ourselves incase anything goes wrong - the script will remain loaded anyways

rm sudo_git_setup.sh
adduser git
cd /home/git/
mkdir .ssh && chmod 700 .ssh
touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys
