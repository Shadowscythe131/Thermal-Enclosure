import csv
import numpy as np
from sklearn.linear_model import LinearRegression

class Channel:
    def __init__(self,channel_number: int):
        self.NUMBER=channel_number
        #assume ideal channel
        self.M=12/65535
        self.C=-4
        self.FAULTY=False
    def define(self, codes_sent: list[int], voltages_out: list[float]):
        self.FAULTY=True
        formatted_x=np.array(codes_sent).reshape(-1,1)
        model=LinearRegression()
        model.fit(formatted_x,voltages_out)
        self.M = float(model.coef_[0])
        self.C = float(model.intercept_)
    def get_code(self, needed_voltage: float):
        decimal_code = round((needed_voltage - self.C) / self.M)
        if decimal_code<0 or decimal_code>65535: raise ValueError("Voltage specified cannot be provided using the range of codes from 0000 - FFFF.")
        return hex(decimal_code)[2:]

class DAC:
    def __init__(self,channels: list[Channel] = []):
        self.channels=channels
    def add_channel(self,channel_number: int):
        self.channels.append(Channel(channel_number))

data={
    "8": [
        [21844,27305,32767],
        [1.081,2.02,2.958]
    ],
    "9": [
        [21844,27305,32767],
        [0.623,1.56,2.49]
    ],
    "10": [
        [21844,27305,32767],
        [2.57,3.511,4.45]
    ],
    "11": [
        [21844,27305,32767],
        [2.92,3.86,4.8]
    ],
    "12": [
        [21844,27305,32767],
        [-0.252,0.684,1.624]
    ],
    "13": [
        [21844,27305,32767],
        [3.2,4.14,5.08]
    ],
    "14": [
        [21844,27305,32767],
        [3.128,4.07,5.01]
    ],
    "15": [
        [21844,27305,32767],
        [0.203,1.139,2.079]
    ],
    "37": [
        [21844,27305,32767],
        [-0.141,0.86,1.863]
    ],
    "38": [
        [21844,27305,32767],
        [0.378,1.381,2.384]
    ],
    "39": [
        [21844,27305,32767],
        [1.03,2.033,3.036]
    ]
}

dac=DAC()
headers=[]
desired_voltages=[0,0.1,0.5,1,2]
rows = [[] for i in range(len(desired_voltages))]
for i in range(40):
    dac.add_channel(i)
    if str(i) in data:
        dac.channels[i].define(data[str(i)][0],data[str(i)][1])
        headers.append(f"Ch.{i}")
for i in dac.channels:
    if i.FAULTY:
        for j in range(len(desired_voltages)):
            rows[j].append(i.get_code(desired_voltages[j]))
with open("codes.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(headers)
    w.writerows(rows)


