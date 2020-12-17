NODE_INIT_PIDS=()

SRC_PATH = ~/source/repos/ddps_2/
cat ${SRC_PATH}hosts | while read worker;
do
  echo "Stopping worker: ${worker}"
  wrk=$(echo $worker | tr ":" "\n")
  echo "" | ssh ${wrk[0]} kill $(ps -a | grep "python" | awk '{print $1}')
#   kill $(ps -a | grep "python" | awk '{print $1}')

done

echo "Done!"