#!/bin/bash

# get permissions setup correctly

sudo chmod -R 777 /mnt/ && mkdir /mnt/extra/logs


# move to the git repo
cd /var

# git pull

# build (this should happen on my machine now)
# python buildscripts/scons.py mongod mongo mongos

# get the correct arguments for the server

configName=""
commandName="./mongod"

if [ "$HOSTNAME" == "config.mongos.tuftscc.emulab.net" ]; then
    configName="/users/sweiss07/config.conf"
elif [ "$HOSTNAME" == "router.mongos.tuftscc.emulab.net" ]; then
    configName="/users/sweiss07/router.conf"
    commandName="./mongos"
elif [ "$HOSTNAME"=="shardr1.mongos.tuftscc.emulab.net" ] || [ "$HOSTNAME" == "shardr2.mongos.tuftscc.emulab.net" ] || [ "$HOSTNAME" == "shardr3.mongos.tuftscc.emulab.net" ]; then
    configName="/users/sweiss07/shard.conf"
fi

chmod +x $commandName

# start the server

pwd

echo nohup $commandName --config $configName &

nohup $commandName --config $configName &

