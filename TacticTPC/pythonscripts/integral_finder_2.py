import os
import timeit

os.chdir('/home/grids/wavedump-3.8.2/Setup/') #changes directory

def peak_info(n): 
#finds amplitudes for all events in file_name, (waven.txt)   
    
    f  = open("/home/grids/wavedump-3.8.2/Setup/analysis/wave"+str(n)+".txt", 'r') 
    f1 = f.readlines()     
    
    g = open("/home/grids/wavedump-3.8.2/Setup/analysis/channel" + str(n) + ".txt", "w+")    
    event=0
    list_of_values = [] 
    
    for line in f1: 
        try: 
            list_of_values.append(int(line))

        except ValueError:                         
            if line.startswith("Record") and len(list_of_values) > 0:
                event=event+1
                if event%1000==0:
                    print("Processed "+str(event)+" events from waveform "+str(n))
               # print("Event:",event)
               # print("length of event is",len(list_of_values))
                starting_val = 4095 
		starting_val = sum(list_of_values[1:30])/29.
                int_window = 400                
                
                minval = min(list_of_values) 
                minval_index = list_of_values.index(minval)
               # print("minimum value is",minval)
               # print("index of min", minval_index)
                amplitude = starting_val - minval                
               # print("amplitude",amplitude)
                #initial test
                if amplitude <= 150: 
                    g.write("0 0" + '\n')
                    list_of_values=[]

                #proceed with calculations if test passed                
                else: 
                    int_sum = 0
                    threshold = starting_val - 0.15 * amplitude 
                    time_status = False                
                   
                    #going through values backwards starting at minval
                    i = minval_index
                    while i >= 0 and i >= minval_index - int_window: 
                        int_sum += (starting_val - list_of_values[i])
                        
                        #finds time 
                        if time_status == False: 
                            if list_of_values[i] > threshold: 
                                time = i #assigns time 
                                time_status = True
                        i -= 1 
                        
                    #going through values forwards starting at minval
                    j = minval_index                    
                    while j <= len(list_of_values) - 1 and i <= minval_index + int_window:
                        int_sum += (starting_val - list_of_values[j] )
                        j += 1
                    
                    g.write(str(time) + " " + str(int_sum) + '\n')
                    
                    list_of_values = []


start = timeit.default_timer()



peak_info(4)
peak_info(5)
peak_info(6)
peak_info(7)


stop = timeit.default_timer()
print stop - start 
            

#old run method      
"""
def run():
#for all events, prints (amp, time) pairs for all txt files      
        
    storage = []     
    for file_name in os.listdir('/home/grids/wavedump-3.8.2/Setup/tactic_waveforms'):       
        storage.append(peak_info(file_name)) 
    #puts all (amplitude, time) in storage
    #storage is indexed by file number 
        
    number_of_events = len(storage[0]) #determining how many events are in one file  
    
    for event_number in range(number_of_events): 
        event_indexed_amp_time = ["Event " + str(event_number + 1)]
        for _list in storage: 
            event_indexed_amp_time.append(_list[event_number])
        
        print(event_indexed_amp_time)
        
"""        
        
        
        







    
