# $1 The server
# $2 The command for running
# $3 The file or directory to run

scp -r $4 "$1:Remote/"
ssh $1 COMMAND="$2" INPUT="$3" 'bash -s' <<'ENDSSH'
    echo "Beginning Run"
    cd Remote/
    echo "Command: $COMMAND $INPUT"
    "$COMMAND" "$INPUT" | tee out.txt;
ENDSSH
scp "$1:Remote/out.txt" out.txt
