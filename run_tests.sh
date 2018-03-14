sudo apt-get update

sudo apt-get install maven

# load
/users/sweiss07/ycsb-0.5.0/bin/ycsb load mongodb-async -s -P workloads/workloadb -P /users/sweiss07/count.dat -p mongodb.url=mongodb://10.1.1.3:27016/ > ~/ycsb_results/outputLoad.txt

#async test
/users/sweiss07/ycsb-0.5.0/bin/ycsb run mongodb-async -s -P workloads/workloadb -P /users/sweiss07/count.dat -p mongodb.url=mongodb://10.1.1.3:27016/ > ~/ycsb_results/outputRun.txt