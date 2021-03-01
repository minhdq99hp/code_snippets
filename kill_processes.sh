touch running_pids.txt
for i in $(cat running_pids.txt); do
kill -9 $i
done
wait