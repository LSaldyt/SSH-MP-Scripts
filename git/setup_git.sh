#!/bin/bash
scp sudo_git_setup.sh "$1:"
ssh $1 -t 'sudo sh sudo_git_setup.sh'

echo Starting another ssh to add public key to the git repo
../ssh/setup_ssh.sh $1
echo Setup Complete. Call ./setup_ssh.sh from each additional computer that needs access to the repo
