NODE_INIT_PIDS=()

SRC+PATH = ~/source/repos/ddps_2/
cat ${SRC_PATH}hosts | while read worker;
do
  echo "Starting workers: ${worker}"
  wrk=$(echo $worker | tr ":" "\n")
  (echo "" | ssh ${wrk[0]} python ${SRC_PATH}server.py ${wrk[@]}) &
done

echo "Done!"