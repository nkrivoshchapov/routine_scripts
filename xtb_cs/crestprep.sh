INPFILE=$1

echo "Maximum procs on task is $MAXPROC"

mkdir ${INPFILE/.xyz/}
cp $1 ${INPFILE/.xyz/}/start.xyz
