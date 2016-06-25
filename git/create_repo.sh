#!/bin/bash
DIR="$2"

ssh git@$1 DIR="$DIR" 'bash -s' <<'ENDSSH'
    echo "Creating "$DIR""
    mkdir "$DIR.git"
    cd "$DIR.git"
    git init --bare
ENDSSH

mkdir "$DIR"
cd "$DIR"
git init
touch README.md
git add .
git commit -m "Initial Commit"
git remote add origin git@$1:$DIR;
git push origin master
