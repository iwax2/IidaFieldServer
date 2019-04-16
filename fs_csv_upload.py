#!/usr/bin/python3
import pyfiap
import datetime
import sys
import codecs
import math
import glob

url_prefix = 'http://strawberry.iida.lab/syokkaen1/'

def temp2svp( temp ):
  temp = temp+273.15
  a = -6096.9385 / temp
  b = 21.2409642
  c = -2.711193 / 100 * temp
  d = 1.673952 / 100000 * temp * temp
  e = 2.433502 * math.log(temp)
  return( math.exp( a + b + c + d + e ) )

def calc_vpd( temp, humi ):
  svp = temp2svp(temp)   # Saturated Vapour Pressure [Pa]
  vp  = svp * humi / 100 # Vapour Pressure [Pa]
  vpd = (svp-vp)/1000    # Vapour Pressure Dificit [kPa]
  return(vpd)

'''
if( len(sys.argv) < 2 ):
  print("usage: "+sys.argv[0]+" <INPUT_CSV>")
  sys.exit()
'''

data = []
file_list = sorted(glob.glob('./data/*.csv'))
for filename in file_list:
  print(filename)
  with codecs.open( filename, 'r', 'Shift-JIS' ) as f:
    for line in f:
      csv = line.strip().replace(" ", "").split(',')
      if(csv[0].isnumeric()):
        data.append(csv)

upload = []
prev = datetime.datetime(1900,1,1)
fiap = pyfiap.fiap.APP("http://iot.info.nara-k.ac.jp/axis2/services/FIAPStorage?wsdl")
for c in data:
  y = int(c[0][0:4])
  m = int(c[0][4:6])
  d = int(c[0][6:8])
  hh = int(c[1][0:2])
  mm = int(c[1][2:4])
  now = datetime.datetime(y,m,d,hh,mm)
  if(now>prev):
    bat = c[2] # バッテリー
    lat = c[3] # 緯度
    lon = c[4] # 経度
    alt = c[5] # 高度
    temp =c[6] # 温度
    humi =c[7] # 湿度
    pre = c[8] # 気圧
    co2 = c[9] # CO2濃度
    soil =c[10] # 土壌水分センサの生データ
    vpd = round(calc_vpd(float(temp),float(humi)),2)
    if( float(temp)>0 and float(humi)>0 and float(co2)>0 and float(pre)>0 and float(soil)>0 ):
      upload.append([url_prefix+'temp', temp, now])
      upload.append([url_prefix+'humi', humi, now])
      upload.append([url_prefix+'vpd',  vpd,  now])
      upload.append([url_prefix+'co2',  co2,  now])
      upload.append([url_prefix+'pre',  pre,  now])
      upload.append([url_prefix+'soil', soil, now])
  prev = now
'''
      fiap.write([[url_prefix+'temp', temp, now],
                  [url_prefix+'humi', humi, now],
                  [url_prefix+'vpd', vpd, now],
                  [url_prefix+'co2', co2, now],
                  [url_prefix+'pre', pre, now],
                  [url_prefix+'soil', soil, now],
                  ])
'''
#fiap.write(upload)
print(upload)
#today = datetime.datetime.now()
#today = datetime.datetime(2019,4,12,16,0,4)


