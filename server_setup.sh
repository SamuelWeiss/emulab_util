# get permissions setup correctly

sudo chmod -R 777 /mnt/ && mkdir /mnt/extra/logs


# move to the git repo
cd /var

# git pull

# build (this should happen on my machine now)
# python buildscripts/scons.py mongod mongo mongos

# get the correct arguments for the server

configName = ""
commandName = "./mongod"

if [$HOSTNAME = "Config.mongos.TuftsCC.emulab.net"]
then
	configName = "config.conf"
elif [$HOSTNAME = "Router.mongos.TuftsCC.emulab.net"]
then
	configName = "router.conf"
	commandName = "mongos"
elif [$HOSTNAME = "ShardR1.mongos.TuftsCC.emulab.net"] ||
	 [$HOSTNAME = "ShardR2.mongos.TuftsCC.emulab.net"] ||
	 [$HOSTNAME = "ShardR3.mongos.TuftsCC.emulab.net"]
then
	configName = "shard.conf"
fi

# start the server

nohup commandName --config configName &

