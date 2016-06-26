#!/bin/bash
scp install.sh "$1:"

package=$2
if [ -z ${package+x} ]; 
then scp $2 "$1:"; 
fi

ssh $1 -t 'sudo sh install.sh'

