import paramiko, os, time, datetime

def process(command):
    time.sleep(3)
    buffer=""
    buffer=shell.recv(8000)
    print ("Output:",buffer) 
    print ("Input:",command)
    shell.send(command)
timer=10    
#ssh=paramiko.SSHClient()
print (os.getcwd())
os.chdir('C:\\Users\\mramas004c\\Documents')
print (os.getcwd())
filelist=os.listdir()
for prikey in filelist:
    if prikey == 'Openssh':
        key=paramiko.RSAKey.from_private_key_file(prikey)
        print ('Successfully logged in')
        break
current_time=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
current_file='dump'+current_time+'.pcap'
host='x.x.x.x'
port=22
ssh=paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host,username='username',key_filename=prikey,port=port)
shell=ssh.invoke_shell()
process ('cd dump\n')
time.sleep(2)
process('sudo tcpdump port 5060 -w '+current_file+'\n')
time.sleep(timer)
process('\x03\n')
time.sleep(2)
buffer=shell.recv(8000)
buff=str(buffer)
print ('Final result:',buff)
ssh.close()
time.sleep(5)
# Trigger the SFTP connection
transport=paramiko.Transport((host,port))
transport.connect(username='username',pkey=key)
sftp=paramiko.SFTPClient.from_transport(transport)
sftp.chdir('/home/username/dump')
print ("Current Linux path:",sftp.getcwd())
filelist=sftp.listdir()
for files in filelist:
    if files==current_file:
        break
filepath='/home/username/dump/'+files
os.chdir('C:\\Users\\mramas004c\\Desktop\\Traces')
localpath=os.getcwd()+'/dump'+current_time+'.pcap'
sftp.get(filepath,localpath)
print ("File transfer successfull")
sftp.close()
transport.close()
