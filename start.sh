NODE_INIT_PIDS=()

SRC_PATH = ~/source/repos/ddps_2/
cat ${SRC_PATH}hosts | while read worker;
do
  echo "Starting workers: ${worker}"
  wrk=$(echo $worker | tr ":" " ")
  echo ${wrk[@]}
  (echo "" | ssh ${wrk[0]} 'python ${SRC_PATH}server.py ${wrk[@]}') &
  # (python ${SRC_PATH}server.py ${wrk[@]} ss) &
done

echo "Done!"