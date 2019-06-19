
#
# Haley Sanchez
# MAGIC - Flood Response
#

all_Temps = [] #added
avg = 0.0 #added
o = open("paradiseca_l8_tirs_k_20181007.txt", "r")
c = open("paradiseca_l8_tirs_c_20181007.txt", "w")
f = open("paradiseca_l8_tirs_f_20181007.txt", "w")
c.write(o.readline())
l = o.readline()
r = l.split(" ")
rows = r[9].split("\n")
c.write(l)
for i in range(4):
    c.write(o.readline())
for x in range(int(rows[0])):
    temps = o.readline().split(" ")
    temps.pop()
    all_Temps += temps #added
    for kelvin in temps:
        cel = float(kelvin) - 273.15
        c.write("%.1f " %(cel))
    c.write("\n")
o.close()
c.close()
all_Temps.sort() #added
for t in all_Temps: #added
    avg += float(t) #added
avg = avg/len(all_Temps) #added
avgC = avg - 273.15 #
avgF = (round(avgC, 1) * (9/5)) + 32 #
minN = float(all_Temps[0]) #
maxN = float(all_Temps[len(all_Temps)-1]) #
minC = minN - 273.15 #
maxC = maxN - 273.15 #
minF = ((9/5) * round(minC, 1)) + 32 #
maxF = ((9/5) * round(maxC, 1)) + 32 # 
print("For 'paradiseca_l8_tirs_k_20181007.txt':") #
print("The min Celsius temperature: %.1f Celsius\nThe max Celsius temperature: %.1f Celsius" %(minC, maxC)) #added
print("The average Celsius temperature: %.1f Celsius" %(avgC)) #
print("The min Fahrenheit temperature: %.1f Fahrenheit\nThe max Fahrenheit temperature: %.1f Fahrenheit" %(minF, maxF)) #added
print("The average Fahrenheit temperature: %.1f Fahrenheit" %(avgF)) #added
o = open("paradiseca_l8_tirs_k_20181007.txt", "r")
f.write(o.readline())
f.write(o.readline())
for i in range(4):
    f.write(o.readline())
for x in range(int(rows[0])):
    temps = o.readline().split(" ")
    temps.pop()
    for kelvin in temps:
        fah = ((float(kelvin) - 273.15) * (9/5)) + 32
        f.write("%.1f " %(fah))
    f.write("\n")
o.close()
f.close()


all_Temps = [] #added
avg = 0.0 #added
o = open("paradiseca_l8_tirs_k_20190127.txt", "r")
c = open("paradiseca_l8_tirs_c_20190127.txt", "w")
f = open("paradiseca_l8_tirs_f_20190127.txt", "w")
c.write(o.readline())
l = o.readline()
r = l.split(" ")
rows = r[9].split("\n")
c.write(l)
for i in range(4):
    c.write(o.readline())
for x in range(int(rows[0])):
    temps = o.readline().split(" ")
    temps.pop()
    all_Temps += temps #added
    for kelvin in temps:
        cel = float(kelvin) - 273.15
        c.write("%.1f " %(cel))
    c.write("\n")
o.close()
c.close()
all_Temps.sort() #added
for t in all_Temps: #added
    avg += float(t) #added
avg = avg/len(all_Temps) #added
avgC = avg - 273.15 #
avgF = (round(avgC, 1) * (9/5)) + 32 #
minN = float(all_Temps[0]) #
maxN = float(all_Temps[len(all_Temps)-1]) #
minC = minN - 273.15 #
maxC = maxN - 273.15 #
minF = ((9/5) * round(minC, 1)) + 32 #
maxF = ((9/5) * round(maxC, 1)) + 32 #
print("\nFor 'paradiseca_l8_tirs_k_20190127.txt':") #
print("The min Celsius temperature: %.1f Celsius\nThe max Celsius temperature: %.1f Celsius" %(minC, maxC)) #added
print("The average Celsius temperature: %.1f Celsius" %(avgC)) #
print("The min Fahrenheit temperature: %.1f Fahrenheit\nThe max Fahrenheit temperature: %.1f Fahrenheit" %(minF, maxF)) #added
print("The average Fahrenheit temperature: %.1f Fahrenheit" %(avgF)) #added
o = open("paradiseca_l8_tirs_k_20190127.txt", "r")
f.write(o.readline())
f.write(o.readline())
for i in range(4):
    f.write(o.readline())
for x in range(int(rows[0])):
    temps = o.readline().split(" ")
    temps.pop()
    for kelvin in temps:
        fah = ((float(kelvin) - 273.15) * (9/5)) + 32
        f.write("%.1f " %(fah))
    f.write("\n")
o.close()
f.close()


all_Temps = [] #added
avg = 0.0 #added
o = open("paradiseca_l8_tirs_k_20181108.txt", "r")
c = open("paradiseca_l8_tirs_c_20181108.txt", "w")
f = open("paradiseca_l8_tirs_f_20181108.txt", "w")
c.write(o.readline())
l = o.readline()
r = l.split(" ")
rows = r[9].split("\n")
c.write(l)
for i in range(4):
    c.write(o.readline())
for x in range(int(rows[0])):
    temps = o.readline().split(" ")
    temps.pop()
    all_Temps += temps #added
    for kelvin in temps:
        cel = float(kelvin) - 273.15
        c.write("%.1f " %(cel))
    c.write("\n")
o.close()
c.close()
all_Temps.sort() #added
for t in all_Temps: #added
    avg += float(t) #added
avg = avg/len(all_Temps) #added
avgC = avg - 273.15 #
avgF = (round(avgC, 1) * (9/5)) + 32 #
minN = float(all_Temps[0]) #
maxN = float(all_Temps[len(all_Temps)-1]) #
minC = minN - 273.15 #
maxC = maxN - 273.15 #
minF = ((9/5) * round(minC, 1)) + 32 #
maxF = ((9/5) * round(maxC, 1)) + 32 #
print("\nFor 'paradiseca_l8_tirs_k_20181108.txt':") #
print("The min Celsius temperature: %.1f Celsius\nThe max Celsius temperature: %.1f Celsius" %(minC, maxC)) #added
print("The average Celsius temperature: %.1f Celsius" %(avgC)) #
print("The min Fahrenheit temperature: %.1f Fahrenheit\nThe max Fahrenheit temperature: %.1f Fahrenheit" %(minF, maxF)) #added
print("The average Fahrenheit temperature: %.1f Fahrenheit" %(avgF)) #added
o = open("paradiseca_l8_tirs_k_20181108.txt", "r")
f.write(o.readline())
f.write(o.readline())
for i in range(4):
    f.write(o.readline())
for x in range(int(rows[0])):
    temps = o.readline().split(" ")
    temps.pop()
    for kelvin in temps:
        fah = ((float(kelvin) - 273.15) * (9/5)) + 32
        f.write("%.1f " %(fah))
    f.write("\n")
o.close()
f.close()
