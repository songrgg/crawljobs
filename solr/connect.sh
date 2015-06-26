#!/bin/bash

if [ $# -lt 2 ];then
	echo "Connect error: at least 2 parameters needed, actually "$#" given."
	exit
fi

mongo-connector -m localhost:$1 -t http://localhost:$2/solr/jobsearch_shard1_replica1 http://localhost:$2/solr/jobsearch_shard2_replica1 -d solr_doc_manager solr_doc_manager
