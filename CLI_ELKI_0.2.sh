#!/bin/bash

java -jar elki-bundle-0.7.1.jar KDDCLIApplication -dbc.in mydata/mouse.csv -algorithm clustering.kmeans.KMedoidsEM -kmeans.k 1 -resulthandler ResultWriter -out.gzi -out output/k-1


