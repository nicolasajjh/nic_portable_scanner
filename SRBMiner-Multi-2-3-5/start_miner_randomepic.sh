echo "Worker name : "
read worker_name
echo ./SRBMiner-MULTI --multi-algorithm-job-mode 1 --disable-gpu --algorithm randomepic --pool us.epicmine.io:3333 --wallet nicolasajjh2.$worker_name --password RichNicels1312m=pool --keepalive true
./SRBMiner-MULTI --multi-algorithm-job-mode 1 --disable-gpu --algorithm randomepic --pool us.epicmine.io:3333 --wallet nicolasajjh2.$worker_name --password RichNicels1312m=pool --keepalive true