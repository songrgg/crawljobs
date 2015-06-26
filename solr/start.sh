#!/bin/bash

# start mongo server
mongod --dbpath=/data/db --port=27017 --replSet "job0" --logpath=/var/log/mongodb/27017.log &
mongod --dbpath=/data/db2 --port=28000 --replSet "job0" --logpath=/var/log/mongodb/28000.log &

state1=`echo "rs.status().myState" | mongo --port=27017 --quiet`
state2=`echo "rs.status().myState" | mongo --port=28000 --quiet`
primary=0

if [ "$state1" = "1" ];then
	echo "27017 is PRIMARY\n"
	primary=27017
elif [ "$state2" = "1" ];then
	echo "28000 is PRIMARY\n"
	primary=28000
else
	echo "Something wrong with the mongod initialization!\n"
	echo "Please check the situation\n"
fi

/opt/solr-5.2.1/bin/solr start -e cloud

# mongo-connector
#mongo-connector -m localhost:$primary -t http://localhost:$2/solr/gettingstarted_shard1_replica1 -d solr_doc_manager
