#Temperature Conversions to celsius and fahrenheit
#Anavi Nayak
#Flood Response Team

#declaring variables:
cTemp = 0.0
fTemp = 0.0
lineNumber = 0
max = 0.0
min = 0.0
sum = 0.0
numEntries = 0

#reading the input file and creating output files
f = open("paradiseca_l8_tirs_k_20181108.txt", "r")
outC = open("celsius2.txt", "w")
outF = open("Fahrenheit2.txt", "w")

#Credits to PythonAstronomers for lines 21-24
#Reading every entry in every line after line 6
for line in f:
    lineNumber = lineNumber + 1
    line.strip()
    lineArr = line.split()
    
    if lineNumber > 6:
        if lineNumber == 7:
            min = float(lineArr[0]) - 273.15
            max = float(lineArr[0]) - 273.15
            
        for entry in lineArr:
            #Counting the entries, converting to celsius and fahrenheit, 
            numEntries += 1
            cTemp = float(entry) - 273.15
            fTemp = cTemp * 9/5 + 32.00
            outC.write(str(cTemp) + " ")
            outF.write(str(fTemp) + " ")
            
            #Also calculates sum, maximum, and minimum temperatures
            sum = sum + cTemp
            if(cTemp > max):
                max = cTemp
            elif cTemp<min:
                min = cTemp
        #and writing the new temperatures into the new files       
        outC.write("\n")
        outF.write("\n")
    elif lineNumber >=0:
        outC.write(line)
        outF.write(line)

#Calculating the average and printing calculations
#in celsius then fahrenheit
avg = sum/numEntries
outC.write("Maximum: %s\nMinimum: %s\nAverage: %s" % (max, min, avg))


avg = avg * 9/5 + 32
max = max * 9/5 + 32
min = min * 9/5 + 32
outF.write("Maximum: %s\nMinimum: %s\nAverage: %s" % (max, min, avg))

#closing files
f.close()
outC.close()
outF.close()

    
