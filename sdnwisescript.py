import xlrd
import re
import matplotlib.pyplot as plt
from math import sqrt

loc = 'loglistnersdnwise.xlsx'
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

sheet.cell_value(0,0)

message = []
for i in range(1,sheet.nrows):
    ms = sheet.cell_value(i,2)
    mote = sheet.cell_value(i,1)
    message.append(ms)

power_msg = []
for m in message:
    if 'PW:' in m:
        power_msg.append(m)
energy_dict = {}
rtt_dict ={}
for line in power_msg:
    match = re.search('P (\d+)',line)
    match2 = re.search('en:(\d+)',line)
    match3 = re.search('rtt:(\d+)',line)
    match4 = re.search('sent:(\d+)',line)
    match5 = re.search('recv:(\d+)',line)
    if match and match2 and match3 and match4 and match5:
        mote = (match.group(1))
        energy = (match2.group(1))
        rtt = (match3.group(1))
        sent = (match4.group(1))
        recv = (match5.group(1))
        energy_dict[energy] = mote
        rtt_dict[rtt] = mote
        #print('mote: '+mote+' Energy: '+energy+'mJ '+' Round-trip time: '+rtt+'ms')

avg_energy = 0
avg_rtt = 0
avg_delay = 0
delay_dict = {10:112,9:117,7:594,8:250,3:480,4:572,5:219}
for en in energy_dict.keys():
    avg_energy = avg_energy + int(en)

avg_energy = avg_energy/(len(energy_dict))

for rt in rtt_dict.keys():
    avg_rtt = avg_rtt + int(rt)

for de in delay_dict.values():
    avg_delay = avg_delay + de

avg_rtt = avg_rtt/(len(rtt_dict))
avg_delay = avg_delay/len(delay_dict)
sd_energy = []
sd_rtt = []
sd_delay = []
for sd in energy_dict.keys():
    sd_energy.append(sqrt(((int(sd) - avg_energy) ** 2) / len(energy_dict)))

for sdr in rtt_dict:
    sd_rtt.append(sqrt(((int(sdr) - avg_rtt)**2)/len(energy_dict)))

for sdd in delay_dict.values():
    sd_delay.append(sqrt(((sdd - avg_delay)**2)/len(delay_dict)))

final_sd_energy = 0
final_sd_rtt = 0
final_sd_delay = 0

for pos in sd_energy:
    final_sd_energy = final_sd_energy + pos

for posr in sd_rtt:
    final_sd_rtt = final_sd_rtt + posr

for posd in sd_delay:
    final_sd_delay = final_sd_delay + posd

final_sd_rtt = final_sd_rtt/len(sd_rtt)
final_sd_energy = final_sd_energy/len(sd_energy)
final_sd_delay = final_sd_delay/len(sd_delay)

print("The average energy consumption is: "+ str(avg_energy)+ "mJ")
print("The standard deviation in energy consumption is: " + str(final_sd_energy) + "mJ")
print("The average Round-Trip time is: " +str(avg_rtt)+"ms")
print("The standard deviation in Round-Trip time: " +str(final_sd_rtt) + "ms")
print("The average delay is: " +str(avg_delay)+"ms")
print("The standard deviation in delay: " +str(final_sd_delay) + "ms")

e = plt.figure('Plot for Energy consumption SDN-WISE')
plt.bar(list(energy_dict.values()), list(energy_dict.keys()))
plt.xlabel('Motes')
plt.ylabel('Energy in (mJ)')
plt.show()

x = list(rtt_dict.values())
x.sort(reverse=True)
y = list(rtt_dict.keys())
y.sort(reverse=True)
r = plt.figure('Plot for RTT in SDN-WISE')
plt.plot(x, y)
plt.xlabel('Motes')
plt.ylabel('Round-trip time in (ms)')
plt.show()

d = plt.figure('Plot for delay in SDN-WISE')
plt.bar(list(delay_dict.keys()), list(delay_dict.values()))
plt.xlabel('Motes')
plt.ylabel('Delay in (ms)')
plt.show()




