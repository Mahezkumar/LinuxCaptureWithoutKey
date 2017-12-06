# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 18:05:21 2017

@author: mramas004c
"""

import paramiko, time, os, datetime, shutil
hostname = 'x.x.x.x'
timer=20
# Process function to execute commands in CSCF box
def process(command):
    time.sleep(3)
    buffer=""
    buffer=shell.recv(8000)
    print ("Output:",buffer) 
    print ("Input:",command)
    shell.send(command)
#Initiate SSH Client instance to capture CSCF logs
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, username = 'username', password = 'password', port = 22)
#Invoke shell function to pass on the commands
shell=client.invoke_shell()
process('eprtsetup\n')
time.sleep(5)
process('eptsptcpdump -s0 -P /opt/tsp/storage0\n')
time.sleep(5)
process('yes\n')
time.sleep(timer)
process('\x03\n')
time.sleep(5)
buffer=shell.recv(8000)
#Convert the received bytes into string for processing
buff=str(buffer)
#print ("Result:",buff)
start=buff.find('axe/')+4
end=buff.find('.tgz',start)
filename=buff[start:end]+'.tgz'
#print ("Filename:",filename)
#print ("Present:",os.getcwd())
#Perform SFTP to copy the files to the local machine
sftp=client.open_sftp()
sftp.chdir('/opt/telorb/axe')
for linux in sorted(sftp.listdir()):
    if linux==filename:
        st=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        windows='C:\\Users\\mramas004c\\Desktop\\Traces\\Dump\\dump'+st+'.tgz'
        sftp.get(linux,windows)
        break
#print ("Telorb filename:",linux)   
#print ("Local Windows file:",windows)
start=windows.find('Dump')+5
end=windows.find('.tgz',start)
new_file=windows[start:end]+'.tgz'
#print ("New file name:",new_file)
#print ("Current windows path:",os.getcwd())
os.chdir('/Users/mramas004c/Desktop/Traces/Dump/')
#print ("After Change directory:",os.getcwd())
temp_file='dump'+st
os.mkdir('/Users/mramas004c/Desktop/Traces/dumpfiles/'+ temp_file)
os.system('python -m tarfile -e '+new_file+' /Users/mramas004c/Desktop/Traces/dumpfiles/'+temp_file)
os.chdir('/Users/mramas004c/Desktop/Traces/dumpfiles/'+temp_file+'/opt/telorb/axe/')
filelist=os.listdir()
file_str='.'.join(filelist)
os.chdir('/Users/mramas004c/Desktop/Traces/dumpfiles/'+temp_file+'/opt/telorb/axe/'+file_str)
#print ("Current:",os.getcwd())
shutil.copy('C:\\Users\\mramas004c\\Desktop\\Traces\\combine.bat', os.getcwd()+'\\combine.bat')
os.system('combine.bat')
shutil.copy('/Users/mramas004c/Desktop/Traces/dumpfiles/'+temp_file+'/opt/telorb/axe/'+file_str+'/temp.pcap','C:\\Users\\mramas004c\\Desktop\\Traces\\CSCF Traces'+'\\cscf'+st+'.pcap')
print ('CSCF Trace captured')
sftp.close()
client.close()
print ("Closing the connection")