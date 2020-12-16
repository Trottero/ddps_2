NODE_INIT_PIDS=()

# For every worker in the list, copy over the hadoop and hive binaries to /local/user/
cat ~/ddps_2/hosts | while read worker;
do
  echo "Initializing worker: ${worker}"
  (echo "" | ssh $worker ~/ddps_2/) &
done