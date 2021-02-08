INPFILE=$1

MAXPROC=1

echo "Maximum procs on task is $MAXPROC"

mkdir ${INPFILE/.xyz/}
cp $1 ${INPFILE/.xyz/}/start.xyz

nohup /home/xray/knvvv/runcrest.sh ${INPFILE/.xyz/} &
