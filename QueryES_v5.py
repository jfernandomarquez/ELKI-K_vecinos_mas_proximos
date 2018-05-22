import datetime
import time

f = open("dataset_real.txt", "w")
f.write('Minute  Hour  Day   Count\n')
f.close()

from elasticsearch import Elasticsearch
es = Elasticsearch(['192.168.20.1:9200'])

while True:
	t=datetime.datetime.now()
	r = es.search(index="logstash-*", filter_path="hits.total", body={"query":{"bool":{"must":[{"match":{"task":"Logon"}},{"range":{"@timestamp":{"gte":"now-5m/m","lt":"now"}}}]}}})
	h=t.hour
	m=t.minute
	s=t.second
	count=r["hits"]["total"]
	f = open("dataset_real.txt", "a")
	f.write('  {}     {}    {}    {}  {}\n'.format(h, m, s, count, "Data"))
	f.close()
	print "..."
	time.sleep(300)
	
