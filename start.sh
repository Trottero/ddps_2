NODE_INIT_PIDS=()

SRC_PATH=~/source/repos/ddps_2/
cat ${SRC_PATH}hosts | while read worker;
do
  echo "Starting workers: ${worker}"
  wrk=($(echo $worker | tr ":" " "))

  # (echo "" | ssh ${wrk[0]} "cd ${SRC_PATH} && module load python/3.6.0 && python3 -m pip install -r ${SRC_PATH}requirements.txt --user && python3 server.py ${wrk[@]} log &") &
  (python server.py ${wrk[@]} ss) &
done

echo "Done!"