#!/bin/bash

curl -X POST -H 'Content-Type: application/json' -d @sentiment_spec.json http://localhost:8081/druid/indexer/v1/supervisor