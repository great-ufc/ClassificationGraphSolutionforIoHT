import ServerProcessApi as SPA
import time

count = 1
while True:
    print("Request "+ str(count))
    if (count > 1440): #depois de um dia força reprocessamento do grafo
        SPA.execute(2) #RequestGraphProcess
        count = 0
    SPA.execute(0) #RequestGraphProcess Execute
    time.sleep(5) #Request a cada 1 min
    count+=1	