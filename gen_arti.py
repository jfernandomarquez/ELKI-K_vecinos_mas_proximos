#Basado en algoritmo usado por patrick kostjens en su tesis de maestria

#!/usr/bin/env python3
# coding=utf-8
import datetime
import math
import random
import sys
import numpy as np

file_prefix = sys.argv[1] #indentificador del dataset
weekend_ratio = float(sys.argv[2]) # porcentaje en que se reducen los acceso en los fines 
anomaly_prob = float(sys.argv[3]) # probabilidad de una anomalia 
anomaly_ratio = float(sys.argv[4])
mean = float(sys.argv[5])
out_office_ratio= float(sys.argv[6])


start = datetime.datetime(2018, 7, 3, 0, 0, 0) #
end = start + datetime.timedelta(days=30) #un mes

data = []
current = start

while current < end:
 count = mean + random.choice([-1, 1]) * np.random.poisson(20)
 # Horas no laborales
 if current.weekday() >= 5:
  count *= weekend_ratio
 elif 18 <current.hour< 24 or 0 < current.hour < 7: 
  count *= out_office_ratio
 # Anomalia
 anomalia = random.uniform(0, 1) < anomaly_prob #0.005
 if anomalia:
  count *= anomaly_ratio

 data.append((current.year,current.month,current.day,current.weekday(),current.hour,current.minute,int(count),anomalia))
 #data.append((current.year+current.month+current.day+current.weekday()+current.hour+current.minute+int(count)+anomalia))
 current += datetime.timedelta(seconds = 300)

def write_elki(path, data):
    with open(path, 'w') as f:
        f.write('Año	Mes	Dia	DiaSemana	Hora	Minuto	Cuenta	A/N\n')
        for i in data:
            f.write('{}	{}	{}	{}	{}	{}	{}	{}\n'.format(i[0], i[1], i[2], i[3],i[4],i[5],i[6], "Anomalia" if i[7] else "Normal"))


write_elki(file_prefix + '_dataset_artificial.txt', data)
