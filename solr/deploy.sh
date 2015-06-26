#!/bin/bash

/opt/solr/server/scripts/cloud-scripts/zkcli.sh -zkhost 127.0.0.1:$1 -cmd putfile /configs/jobsearch/solrconfig.xml /root/Development/firstcrawl/solr/solrconfig.xml
/opt/solr/server/scripts/cloud-scripts/zkcli.sh -zkhost 127.0.0.1:$1 -cmd putfile /configs/jobsearch/managed-schema /root/Development/firstcrawl/solr/schema.xml
