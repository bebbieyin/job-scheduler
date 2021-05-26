import sys
import os
from subprocess import Popen, PIPE
from multiprocessing import Process
import time
import random
import threading
import torch 

#NUM_GPU = 2
NUM_GPU = torch.cuda.device_count()
# convert the txt file content to list
def txt2list(input_file):
    env_list = []

    with open(input_file) as f:
        Content = f.read()
        line_counter = 0
        lines = Content.split("\n")
        for i in lines : 
            if i:
                line_counter+=1
            proc_list = lines[:line_counter]

        for l in proc_list:
            l  = l.strip('\n')
            e = l.split(",")
            env_list.append(e)

    return env_list[1:]

# sort the executed task into seperate folder
def sort_task(input_file,shared_list):

    current_proc = shared_list[0]
    output_file = 'done.txt'
                
    # add to output file
    str1 = ','.join(current_proc)
    d = open(output_file, 'a+')
    d.seek(0)
    data = d.read(10000)
    if len(data) > 0 :
        d.write("\n")
    d.write(str1)

    # delete first row from environment.txt
    with open(input_file, 'r') as fin:
        data1 = fin.read().splitlines(True)
        first_line = data1[0]
    with open(input_file, 'w') as fout:
        fout.writelines(first_line)
        fout.writelines(data1[2:])
    
    return current_proc

# activate environment and run python script
def process(input_file,shared_list,gpu_index):

    get_gpu = '-gpu {}'.format(gpu_index)
    current_proc = sort_task(input_file,shared_list)
    env_name, path, script = [current_proc[i] for i in (0, 1, 2)]
    os.chdir(path)
    proc = Popen("conda activate "+ env_name+ " && python "+script+" "+get_gpu,
                    shell=True,)
    
    # wait for subprocess to finish only will the multiprocess ends
    while proc.poll() is None: 
        time.sleep(5) # check if the subprocess is still running every 5 seconds


# initialize the available GPUs
def initialize_gpu(number_of_processes):
    list_gpu = []
        
    for i in range(number_of_processes):
        list_gpu.append(1) # 1 = available, 0 =not available
    return list_gpu
    
# check if there is any gpu available
def get_availability(list_gpu):
    
    if 1 in list_gpu:
        return True
    else:
        return False

def create_multiprocess(input_file,gpu_index):

    shared_list = txt2list(input_file)
    proc = Process(target=process,args=(input_file,shared_list,gpu_index))

    return proc

def start_process(proc):
    proc.start() 

    if proc.is_alive:
        print("\n")
        print(proc.name," has started\n")
 
# add process to a list and chg the gpu to unavailable
def allocate_gpu(proc,p_list,list_gpu):
    
    for i,process in enumerate(p_list):
        if process =='':
            p_list[i] = proc
            break
    process_index =p_list.index(proc)
    list_gpu[process_index] = 0 

# check if the process has ended
def check_status(p_list,list_gpu):

    for i,p in enumerate(p_list):
        if p.exitcode==0:
            list_gpu[i]=1   # change the gpu asssigned to the process to available 
            p_list[i]=''   # remove the process once it is finish
            print("\n",p.name," has ended")

def run(input_file):
    
    list_gpu = initialize_gpu(NUM_GPU)
    p_list = []

    # initialize to only n process in the list
    for i in range(NUM_GPU):
        p_list.append('')


    while os.stat(input_file).st_size != 0:
        x = random.randint(1,4)

        if get_availability(list_gpu) ==True:
            available_gpu = list_gpu.index(1)
            if txt2list(input_file):
                proc = create_multiprocess(input_file,available_gpu)
                allocate_gpu(proc,p_list,list_gpu)
                start_process(proc)
        else:
            check_status(p_list,list_gpu)
        time.sleep(x) # add delay so processes won't crash into each other
   
