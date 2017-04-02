import BeautifulSoup
import urllib
import csv
import time
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# BSNL Usage Page
page = urllib.urlopen("http://172.30.3.130:9090/SSSS_Servlet?key1=usage&exceed=usage").read()

soup=BeautifulSoup.BeautifulSoup(page)
a = soup.find("div", {"id":"usageTable"})
b = a.find("tr", {"class" : "odd"})
c = b.findAll("td")

usage = str(float(c[1].text)/(1024**3))
date = time.strftime("%#d/%#m/%Y")

print "Plan : ",c[0].text
print "Usage: ",usage,"GB"
print "Date : ",date

flag_add=0

# If CSV is present, read it
if os.path.isfile("usage.csv"):
	with open("usage.csv","r") as f:
		reader = csv.reader(f)
		lastrow = None
		for lastrow in reader: pass
		
		# If today's usage already noted, don't append but overwrite
		if date == lastrow[0]:
			flag_add=0
		else:
			flag_add=1
else:
	flag_add=1

# Append new usage for new date, or else overwrite last line
if flag_add:
	with open("usage.csv","a") as f:
		writer = csv.writer(f,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
		writer.writerow([date,usage])
else:
	with open("usage.csv","r") as f:
		reader = csv.reader(f)
		lines = [l for l in reader]
		for i in lines:
			if i[0]==date:
				i[1]=usage
	with open("usage.csv","wb") as f:
		writer = csv.writer(f,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
		writer.writerows(lines)
		
# Plot graph
with open("usage.csv","r") as f:
	reader = csv.reader(f)
	x = [dt.datetime.strptime(d[0],'%d/%m/%Y').date() for d in reader]
	f.seek(0)
	y = [d[1] for d in reader]

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.plot(x,y)
	plt.gcf().autofmt_xdate()
	plt.show()






