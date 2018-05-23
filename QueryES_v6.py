import datetime
import time


def tiempo():
        st = datetime.datetime.fromtimestamp(time.time())
        Y= st.strftime('%Y')
        m= st.strftime('%m')
        d= st.strftime('%d')
        H= st.strftime('%H')
        M= st.strftime('%M')
        return Y,m,d,H,M

Y,m,d,H,M=tiempo()
id_doc=d
f = open("mydata/dataset_real_{0}".format(id_doc)+".txt", "w")
f.write('  Ano  Mes     Dia     Hora    Minutos          Count\n')
f.write(' \n')
f.close()

from elasticsearch import Elasticsearch
es = Elasticsearch(['10.100.64.229:9200'])

while True:
	Y,m,d,H,M=tiempo()
	r = es.search(index="windows-*", filter_path="hits.total", body={"query":{"bool":{"must":[{"match":{"task":"Logon"}},{"range":{"@timestamp":{"gte":"now-5m/m","lt":"now"}}}]}}})
	count=r["hits"]["total"]
	f = open("mydata/dataset_real_{0}".format(id_doc)+".txt", "a")
	f.write('  {}	{}	{}	{}	{}		{}	  {}\n'.format(Y,m,d,H,M,count,"Data"))
	f.close()
	print "Querying..."+ " Hora:" + str(H) + " Minuto:" + str(M) + " dia:" + str(d)
	time.sleep(300)
	

