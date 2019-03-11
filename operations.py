''' for all operations
    python operations.py --function updateapps --server serverid
    python operations.py --function createwebapp --server serverid --domain eexample.com
    python operations.py --function setdefault --server serverid --app wepappid
    python operations.py --function removedefault --server serverid --app wepappid
    python operations.py --function installer --server serverid --app wepappid
    python operations.py --function domainAdd --server serverid --app wepappid --domain www.example.com
    python operations.py --function domainDelete --server serverid --app wepappid --domain www.example.com
    python operations.py --function installSSL --server serverid --app wepappid
    python operations.py --function updateSSL --server serverid --app wepappid --ssl sslid --type hsts
    python operations.py --function addserver --name $NAME --region $REGION  --size $SIZE --backups $BACKUPS --server_provider digitalocean
    python operations.py --function installSSL --server serverid --name $name
'''
import requests
import sys
import json
import time
import time
import paramiko, StringIO
import os
import datetime
import datetime
import subprocess
import mysql.connector
import argparse
from requests_toolbelt.utils import dump
parser = argparse.ArgumentParser()
parser.add_argument( '-f',"--function",type=str)
parser.add_argument( '-n',"--name",type=str)
parser.add_argument( '-r',"--region",type=str)
parser.add_argument( '-sz',"--size",type=str)
parser.add_argument( '-b',"--backups",type=str)
parser.add_argument( '-p',"--server_provider",type=str)
parser.add_argument( '-d',"--domain",type=str)
parser.add_argument( '-s',"--server",type=str)
parser.add_argument( '-w',"--app",type=str)
parser.add_argument( '-sid',"--ssl",type=str)
parser.add_argument( '-t',"--type",type=str)
args = parser.parse_args()



f=open('config.txt','r')
data=f.read()

data=json.loads(data)
dbhost=data['DB_HOST']
dbuser=data['DB_USERNAME']
dbpass=data['DB_PASSWORD']
database=data['DB_DATABASE']
port=data['DB_PORT']
DO_API_KEY=data['DO_API_KEY']
VULTR_API_KEY=data['VULTR_API_KEY']
runcloud_apikey=data['RUNCLOUD_API_KEY']
runcloud_secretkey=data['RUNCLOUD_API_SECRET']

auth=(runcloud_apikey, runcloud_secretkey)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
params = (
         ('page', '1'),
           )


def functiondata(url,headers,auth,parameters,tablename):
    try:        
        data=[]
        respons = requests.get(url, headers=headers,auth=auth)
        #print(respons.text)
        dataaa = dump.dump_all(respons)
        g=open("logs.txt","a+")
        g.write(str(headers))
        g.write('\n')
        g.write('\n')
        g.write(dataaa)
        g.write('\n')
        g.write('\n')
        g.close()
        j=json.loads(respons.text)
        print(j)
        val=j['data']
        print("here2")
        d={}
        for v in val:
            d={}
            for p,k in parameters:
                d[p]=v[k]
            data.append(d)
        sqlwrite(data,tablename)     
        return data
    except:
        pass
     
def sqlwrite(data,tablename):
    for ll in data:
        print("here2")
        f=open('config.txt','r')
        data=f.read()
        data=json.loads(data)
        dbhost=data['DB_HOST']
        dbuser=data['DB_USERNAME']
        dbpass=data['DB_PASSWORD']
        database=data['DB_DATABASE']
        port=data['DB_PORT']
        keys=[]
        value=[]
        values=ll.items()
        for v,x in values:
            if(x==None):
                x="0"
            keys.append(str(v))
            value.append(str(x))
        mydb = mysql.connector.connect(
               host=dbhost,
               user=dbuser,
               passwd=dbpass,
               database=database,
               port=port,
                )
        mycursor = mydb.cursor()
        string=""
        vvv=""
        for k in keys:
            string=string+k+","
        for i in range(len(keys)):
            vvv=vvv+"%s,"
        vvv=vvv[:-1]    
        string=string[:-1]   
        sql = "INSERT INTO "+tablename+" ("+string+") VALUES ("+str(vvv)+")"
        #val = (id_val,user_id,serverid,sername,ipadrress,serverprovider)
        val=value
        print(val)
        mycursor.execute(sql,val)
        mydb.commit()
        mydb.close()

def createwebapp(serverid,headers,data,auth):    
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps', headers=headers, params=data, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def setasdefault(serverid,webapid,headers,auth):    
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/default', headers=headers, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def removeasdefault(serverid,webapid,headers,auth):   
    response = requests.delete('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/default', headers=headers, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def scriptinstaller(serverid,webapid,data,headers,auth):    
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/installer', headers=headers, data=data, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def domainnameadd(serverid,webapid,data,headers,auth):
    '''print headers
    print auth
    print data'''    
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/domainname', headers=headers,params =data, auth=auth)

    '''print "response"
    print response
    print response.text'''
    print('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/domainname')
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def domainnamedelete(serverid,webapid,domain,headers,auth): 
    response = requests.delete('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/domainname/'+domain, headers=headers, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def installssl(serverid,webapid,data,headers,auth):    
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/ssl', headers=headers, params=data, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def updatessl(serverid,webapid,data,sslid,headers,auth):    
    response = response = requests.patch('https://manage.runcloud.io/base-api/servers/'+serverid+'/webapps/'+webapid+'/ssl/'+sslid+'', headers=headers, params=data, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    return response

def updateapps(serverid):    
    f=open('config.txt','r')
    data=f.read()
    data=json.loads(data)
    dbhost=data['DB_HOST']
    dbuser=data['DB_USERNAME']
    dbpass=data['DB_PASSWORD']
    database=data['DB_DATABASE']
    port=data['DB_PORT']
    mydb = mysql.connector.connect(
               host=dbhost,
               user=dbuser,
               passwd=dbpass,
               database=database,
               port=port,
                )
    mycursor = mydb.cursor()
    sql = "DELETE FROM applications WHERE server_id='"+str(serverid)+"';"
    mycursor.execute(sql)
    mydb.commit()
    runcloud_apikey=data['RUNCLOUD_API_KEY']
    runcloud_secretkey=data['RUNCLOUD_API_SECRET']
    auth=(runcloud_apikey, runcloud_secretkey)
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
     }
    parameters=[('app_id','id'),('server_user_id','server_user_id'),('server_user_username','server_user_username'),('server_id','server_id'),('name','name'),('defaultServer','defaultServer'),('domains','domains'),('sslinfo','ssl')]
    tablename="applications"    
    res = functiondata("https://manage.runcloud.io/base-api/servers/"+serverid+"/webapps?page=1",headers,auth,parameters,tablename)

def dbcreate(name,serverid):
    name=name.replace(".","_")
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
     }
    f=open('config.txt','r')
    data=f.read()
    data=json.loads(data)
    runcloud_apikey=data['RUNCLOUD_API_KEY']
    runcloud_secretkey=data['RUNCLOUD_API_SECRET']
    auth=(runcloud_apikey, runcloud_secretkey)
    data='{"databaseName":"'+name+'","databaseCollation": "dec8_swedish_ci"}'
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/databases', headers=headers, params=data, auth=auth)
    time.sleep(1)
    data = '{"databaseUser": "'+name+'","password":"'+name+'","verifyPassword": "'+name+'"}'
    response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/databaseusers', headers=headers, params=data, auth=auth)
    time.sleep(1)
    response = requests.get('https://manage.runcloud.io/base-api/servers/'+serverid+'/databases?page=1', headers=headers, auth=auth)
    time.sleep(1)
    j=json.loads(response.text)
    val=j['data']
    for v in val:
        if(v["name"]==name):
            data = '{"databaseUser": "dbuser"}'
            response = requests.post('https://manage.runcloud.io/base-api/servers/'+serverid+'/databases/'+v["id"]+'/attachuser', headers=headers, params=data,auth=auth)
            
def addserver(name,region,size,backups,server_provider):   
    if(server_provider=="digitalocean"):
        f=open('config.txt','r')
        data=f.read()
        f.close()
        data=json.loads(data)
        DO_API_KEY=data['DO_API_KEY']
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+str(DO_API_KEY)}
        data = '{"name": "'+name+'","region": "'+region+'","size": "'+size+'","image": "ubuntu-16-04-x64","ssh_keys": ["23605276"] ,"backups": '+backups+'}'
        response = requests.post('https://api.digitalocean.com/v2/droplets', headers=headers, data=str(data))
        dataaa = dump.dump_all(response)
        g=open("logs.txt","a+")
        g.write("......................................................................")
        g.write('\n')
        g.write("......................................................................")
        g.write('\n')
        now = datetime.datetime.now()
        g.write(str(now))
        g.write('\n')
        g.write('\n')
        g.write(str(headers))
        g.write('\n')
        g.write('\n')
        g.write(str(dataaa))
        g.write('\n')
        g.write('\n')
        g.close()
        j=str(response.text)
        print(j,type(j))
        droplet_id=((((j.split('{"droplet":{"id":'))[1]).split(","))[0])
        print(droplet_id)
        time.sleep(5)
        response = requests.get('https://api.digitalocean.com/v2/droplets/'+str(droplet_id), headers=headers)
        dataaa = dump.dump_all(response)
        g=open("logs.txt","a+")
        g.write("......................................................................")
        g.write('\n')
        g.write("......................................................................")
        g.write('\n')
        now = datetime.datetime.now()
        g.write(str(now))
        g.write('\n')
        g.write('\n')
        g.write(str(headers))
        g.write('\n')
        g.write('\n')
        g.write(dataaa)
        g.write('\n')
        g.write('\n')
        g.close()
        #j=json.dumps(str(response.text).encode("utf-8"))
        j=str(response.text)
        print(j,type(j))
        droplet_id=((((j.split('{"droplet":{"id":'))[1]).split(","))[0])  
        ip=((((j.split('{"ip_address":"'))[1]).split('"'))[0])
        docreateserver(name,ip,droplet_id,server_provider)
    if(server_provider=="vultr"):
        f=open('config.txt','r')
        data=f.read()
        f.close()
        data=json.loads(data)
        VULTR_API_KEY=data['VULTR_API_KEY']
        headers = {
          'API-Key': VULTR_API_KEY,
           }
        data = {
           'DCID':region,
           'VPSPLANID': size,
           'OSID': '215',
           "label" : name,
           "SSHKEYID": "5bfd28f50442b",
           "auto_backups":backups,
           }
        response = requests.post('https://api.vultr.com/v1/server/create', headers=headers,data=data)
        dataaa = dump.dump_all(response)
        g=open("logs.txt","a+")
        g.write("......................................................................")
        g.write('\n')
        g.write("......................................................................")
        g.write('\n')
        now = datetime.datetime.now()
        g.write(str(now))
        g.write('\n')
        g.write('\n')
        g.write(str(headers))
        g.write('\n')
        g.write('\n')
        g.write(dataaa)
        g.write('\n')
        g.write('\n')
        g.close()
        dat=str(response.text)
        val=((dat.split(':'))[1]).strip()
        val=(val.split('}'))[0]
        droplet_id = val[1:-1]
        time.sleep(30)
        response = requests.get('https://api.vultr.com/v1/server/list_ipv4?SUBID='+str(droplet_id), headers=headers)
        dataaa = dump.dump_all(response)
        g=open("logs.txt","a+")
        g.write("......................................................................")
        g.write('\n')
        g.write("......................................................................")
        g.write('\n')
        now = datetime.datetime.now()
        g.write(str(now))
        g.write('\n')
        g.write('\n')
        g.write(str(headers))
        g.write('\n')
        g.write('\n')
        g.write(dataaa)
        g.write('\n')
        g.write('\n')
        g.close()
        j=str(response.text)
        ip=((j.split(':[{"ip":"'))[1]).strip()
        ip=(ip.split('","netmask":"'))[0]
        print(ip)
        docreateserver(name,ip,droplet_id,server_provider)
        
        
def docreateserver(name,ip,droplet_id,server_provider):
    print(name,ip,droplet_id,server_provider)
    f=open('config.txt','r')
    data=f.read()
    f.close()
    data=json.loads(data)
    runcloud_apikey=data['RUNCLOUD_API_KEY']
    runcloud_secretkey=data['RUNCLOUD_API_SECRET']
    auth=(runcloud_apikey, runcloud_secretkey)
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
      }
    name=name.replace(".","_")
    data = '{"serverName": "'+name+'","ipAddress": "'+ip+'","serverProvider": "'+server_provider+'"}'
    response = requests.post('https://manage.runcloud.io/base-api/servers', headers=headers, data=data, auth=auth)
    dataaa = dump.dump_all(response)
    g=open("logs.txt","a+")
    g.write("......................................................................")
    g.write('\n')
    g.write("......................................................................")
    g.write('\n')
    now = datetime.datetime.now()
    g.write(str(now))
    g.write('\n')
    g.write('\n')
    g.write(str(headers))
    g.write('\n')
    g.write('\n')
    g.write(dataaa)
    g.write('\n')
    g.write('\n')
    g.close()
    resp=str(response.text)
    print(resp)
    j=(((resp.split('installationURL":{"method":"get","link":"'))[1]).split('"},"delete":{"method":"delete",'))[0]
    print(j)
    cmd='''export DEBIAN_FRONTEND=noninteractive; echo 'Acquire::ForceIPv4 "true";' | tee /etc/apt/apt.conf.d/99force-ipv4; apt-get update; apt-get install curl netcat-openbsd -y; apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade -y; curl --silent --location {'''+j+'''} | bash -; export DEBIAN_FRONTEND=newt'''
    print("here1")
    time.sleep(30)
    try:
        f=open("key.txt")
        key_string=str(f.read())
        not_really_a_file = StringIO.StringIO(key_string)
        private_key = paramiko.RSAKey.from_private_key(not_really_a_file)
        not_really_a_file.close()
        ssh=paramiko.SSHClient()
        print("here2")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("trying to connect to paramiko")
        ssh.connect(ip,port="22", username='root', password='111111', pkey=private_key)
    except Exception as e:
        print(str(e))
        g=open("logs.txt","a+")
        g.write("......................................................................")
        g.write('\n')
        g.write("......................................................................")
        g.write('\n')
        now = datetime.datetime.now()
        g.write(str(now))
        g.write('\n')
        g.write(str(e))
        g.write("paramiko failed with following details")
        g.write(name,ip,droplet_id,server_provider)
        g.write('\n')
        g.write('\n')
        g.close()
    print("here4")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("here6")
    f=open("output2.txt","w")
    g=stdout.read()
    print("g")
    f.write(g)
    f.close()
    ssh.close()
    f=open("output2.txt","r")
    lines=f.readlines()
    for line in lines:
        if("MySQL ROOT PASSWORD:" in line):
            mysql_root=((line.split(":"))[1]).strip()
        if("User:" in line):
            user=((line.split(":"))[1]).strip()
        if("Password:" in line):
            runcloud_pass=((line.split(":"))[1]).strip()
    t=[]
    d={}
    d['droplet_id']=droplet_id
    d['name']=name
    d['ip']=ip
    d['mysql_root']=mysql_root
    d['runcloud_pass']=runcloud_pass
    d['server_provider']=server_provider
    t.append(d)
    sqlwrite(t,"server_details")
    try:
        path="runcloud_logs"    
        if not os.path.exists(path):
            os.makedirs(path)
        now = datetime.datetime.now()
        now=str(now)
        filename=path+"/"+ip+"_"+now+".txt"
        f=open(filename,"w")
        f.write(t)
        f.close()
    except:
        pass
    cmd="python3 /var/www/html/servermanagment/server.py"
    subprocess.call(cmd, shell=True)

#def vultrServerCreate():
    
   
if(args.function=="addserver"):
    try:
        name=args.name
        region=args.region
        size=args.size
        backups=args.backups
        server_provider=args.server_provider
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function addServer --name "+name+" --region "+region+"  --size "+size+" --backups "+backups+" --server_provider "+server_provider)
        f.close()
        addserver(name,region,size,backups,server_provider)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()
 

if(args.function=="createwebapp"):
    try:
        serverid=args.server
        domiain=args.domain
        name=domiain.replace(".","_")
        data = {"webApplicationName": name,
            "domainName": domiain,
            "user": "runcloud",
            "publicPath": "/public",
            "phpVersion": "php72rc",
            "stack": "nativenginx",
            "stackMode": "production",
            "clickjackingProtection": 1,
            "xssProtection": 1,
            "mimeSniffingProtection": 1,
            "processManager": "ondemand",
            "processManagerMaxChildren": 50,
            "processManagerMaxRequests": 500,
            "openBasedir": "/home/runcloud/webapps/"+name+":/var/lib/php/session:/tmp",
            "timezone": "Asia/Kuala_Lumpur",
            "disableFunctions": "getmyuid,passthru,leak,listen,diskfreespace,tmpfile,link,ignore_user_abord,shell_exec,dl,set_time_limit,exec,system,highlight_file,source,show_source,fpassthru,virtual,posix_ctermid,posix_getcwd,posix_getegid,posix_geteuid,posix_getgid,posix_getgrgid,posix_getgrnam,posix_getgroups,posix_getlogin,posix_getpgid,posix_getpgrp,posix_getpid,posix,_getppid,posix_getpwuid,posix_getrlimit,posix_getsid,posix_getuid,posix_isatty,posix_kill,posix_mkfifo,posix_setegid,posix_seteuid,posix_setgid,posix_setpgid,posix_setsid,posix_setuid,posix_times,posix_ttyname,posix_uname,proc_open,proc_close,proc_nice,proc_terminate,escapeshellcmd,ini_alter,popen,pcntl_exec,socket_accept,socket_bind,socket_clear_error,socket_close,socket_connect,symlink,posix_geteuid,ini_alter,socket_listen,socket_create_listen,socket_read,socket_create_pair,stream_socket_server",
            "maxExecutionTime": 30,
            "maxInputTime": 60,\
            "maxInputVars": 1000,
            "memoryLimit": 256,
            "postMaxSize": 256,
            "uploadMaxFilesize": 256,
            "sessionGcMaxlifetime": 1440,
            "allowUrlFopen": 1}
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function createwebapp --server "+serverid+" --domain "+domiain)
        f.close()
        createwebapp(serverid,headers,data,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()      
    
if(args.function=="setdefault"):
    try:
        serverid=args.server
        webapid=args.app
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function setdefault --server "+serverid+" --app "+webapid)
        f.close()
        setasdefault(serverid,webapid,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()      
    
if(args.function=="removedefault"):
    try:
        serverid=args.server
        webapid=args.app
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function removedefault --server "+serverid+" --app "+webapid)
        f.close()
        removeasdefault(serverid,webapid,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()
    
if(args.function=="installer"):
    try:
        serverid=args.server
        webapid=args.app
        data = '{"scriptName": "wordpress"}'
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function installer --server "+serverid+" --app "+webapid)
        f.close()
        scriptinstaller(serverid,webapid,data,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()    
if(args.function=="domainAdd"):
    try:
        serverid=args.server
        webapid=args.app
        domainname=args.domain
        data = {"domainName": domainname}
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function domainAdd --server "+serverid+" --app "+webapid+" --domain "+domainname)
        f.close()
        domainnameadd(serverid,webapid,data,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()     
if(args.function=="domainDelete"):
    try:
        serverid=args.server
        webapid=args.app
        domainname=args.domain
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function domainDelete --server "+serverid+" --app "+webapid+" --domain "+domainname)
        f.close()
        domainnamedelete(serverid,webapid,domainname,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()     
if(args.function=="installSSL"):
    try:
        serverid=args.server
        webapid=args.app
        data = {"provider": "letsencrypt",
                "enableHttp": 0,
                "enableHsts": 1,
                "http2":0,
                "brotli":1,
                "authorizationMethod":"http-01",
                "environment" : "live" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function installSSL --server "+serverid+" --app "+webapid)
        f.close()
        installssl(serverid,webapid,data,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()     
if(args.function=="updateSSL"):
    try:
        serverid=args.server
        webapid=args.app
        sslid=args.ssl
        if(args.type=="hsts"):
            data = {"enableHttp": false,
            "enableHsts": true
             }
        if(args.type=="http"):
            data = {"enableHttp": true,
            "enableHsts": false
              }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write("python operations.py --function updateSSL --server "+serverid+" --app "+wepappid+" --ssl "+sslid+" --type "+args.type)
        f.close()
        updatessl(serverid,webapid,sslid,data,headers,auth)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit()         
if(args.function=="updateapps"):
    try:
        serverid=args.server
        parameters=[('app_id','id'),('server_user_id','server_user_id'),('server_user_username','server_user_username'),('server_id','server_id'),('name','name'),('defaultServer','defaultServer'),('domains','domains'),('sslinfo','ssl')]
        tablename="applications"
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        now = datetime.datetime.now()
        f.write(str(now))
        f.write('\n')
        f.write('\n')
        f.write("python operations.py --function updateapps --server "+serverid)
        f.write('\n')
        f.write('\n')
        f.close()
        updateapps(serverid)
    except:
        data={ "status": "fail" }
        f=open("logs.txt","a")
        f.write("......................................................................")
        f.write('\n')
        f.write("......................................................................")
        f.write('\n')
        f.write(str(data))
        f.close()
        print(data)
        sys.exit() 	
	
if(args.function=="dbcreate"):
    serverid=args.server
    name=args.name
    dbcreate(name,serverid)
    
