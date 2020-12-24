NODE_INIT_PIDS=()

SRC_PATH = ~/source/repos/ddps_2/
cat ${SRC_PATH}hosts | while read worker;
do
  echo "Stopping worker: ${worker}"
  wrk=$(echo $worker | tr ":" "\n")
  # kill $(ps -a | grep "python" | awk '{print $1}')

done

kill $(ps -a | grep "python" | awk '{print $1}')

echo "Done!"