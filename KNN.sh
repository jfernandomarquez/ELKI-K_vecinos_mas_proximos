#!/bin/bash

dataset=${1?Error: no data given}
k=${2?Error: no k given}

java -jar elki-bundle-0.7.1.jar KDDCLIApplication -verbose -dbc.in $dataset -algorithm outlier.distance.KNNOutlier -knno.k $k
