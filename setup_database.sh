# Connect to a replica set member and initiate the replica set
mongo --host 10.1.1.5 --port 27018 --eval "rs.initiate(
  {
    _id : \"rs1\",
    members: [
      { _id : 0, host : \"10.1.1.5:27018\" },
      { _id : 1, host : \"10.1.1.6:27018\" },
      { _id : 2, host : \"10.1.1.7:27018\" }
    ]
  }
)"

# Connect to a replica set member and initiate the replica set
mongo --host 10.1.1.4 --port 27019 --eval "rs.initiate(
  {
    _id : \"crs\",
    members: [
      { _id : 0, host : \"10.1.1.4:27019\" }
    ]
  }
)"

# sleep for 1 minute
sleep 1m

# connect to the router and add the shard
mongo --host 10.1.1.3 --port 27016 --eval "sh.addShard( \"rs1/ShardR1.mongos.TuftsCC.emulab.net:27018\")"

# configure the database to be sharded.
mongo --host 10.1.1.3 --port 27016 --eval "sh.enableSharding(\"ycsb\")"