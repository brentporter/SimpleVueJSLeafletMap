import re

min_val_C = 10000000
max_val_C = 0
sum_val_C = 0
min_val_F = 10000000
max_val_F = 0
sum_val_F = 0
num_val = 0

def kc(k):
    if(k==-9999): return -9999 
    val = k - 273.15
    return val

def kf(k):
    if(k==-9999): return -9999
    i_val = kc(k)
    val = 1.8*i_val + 32
    global min_val_F
    min_val_F = min(min_val_F, val)
    global max_val_F
    max_val_F = max(max_val_F, val)
    global sum_val_F
    sum_val_F += val
    global num_val
    num_val += 1
    global min_val_C
    min_val_C = min(min_val_C, i_val)
    global max_val_C
    max_val_C = max(max_val_C, i_val)
    global sum_val_C
    sum_val_C += i_val
    return val

def form(line, regex, flag):
    sep = " "
    temp = []
    ind = re.findall(regex, line)
    
    for i in ind:
        if(flag):
            temp.append(str(round(kc(float(i)),1)))
        else:
            temp.append(str(round(kf(float(i)),1)))

    string = sep.join(temp)
    return string + '\n'

name = "paradiseca_l8_tirs_k_20181108.txt"
subst = name.index("_k_")+1

f = open(name, "r")
g1 = open(name[:subst]+"c"+name[subst+1:], "w")
g2 = open(name[:subst]+"f"+name[subst+1:], "w")

regex = re.compile(r"[0-9.]+")

for line in f:
    if(line[0] >= 'A'):
        g1.write(line)
        g2.write(line)
    else:
        g1.write(form(line, regex, True))
        g2.write(form(line, regex, False))

print("")
print("MIN_CELSIUS: " + str(round(min_val_C,1)))
print("MAX_CELSIUS: " + str(round(max_val_C,1)))
print("AVG_CELSIUS: " + str(round(sum_val_C/num_val,1)))
print("MIN_FAHRENHEIT: " + str(round(min_val_F,1)))
print("MAX_FAHRENHEIT: " + str(round(max_val_F,1)))
print("AVG_FAHRENHEIT: " + str(round(sum_val_F/num_val,1))) 

f.close()
g1.close()
g2.close()

