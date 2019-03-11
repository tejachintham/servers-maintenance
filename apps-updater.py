import requests
import mysql.connector
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument( '-s',"--server",type=str)
args = parser.parse_args()
def functiondata(url,headers,auth,parameters,tablename):
    try:
        data=[]
        respons = requests.get(url, headers=headers,auth=auth)
        #print(respons.text)
        j=json.loads(respons.text)
        val=j['data']
        d={}
        for v in val:
            d={}
            for p,k in parameters:
                try:
                    #print(v[k]) 
                    d[p]=v[k]
                except:
                    d[p]="0"      
            if(tablename=="servers"):
                    if(k=="serverProvider"):
                        try:
                            if("accounts" in v[k]):
                                data.append(d)
                        except Exception as e:
                            print(str(e))
            if(tablename=="applications"):
                try:
                    try:
                       response=requests.get("https://manage.runcloud.io/base-api/servers/"+d['server_id']+"/webapps/"+d['app_id']+"/installer", headers=headers,auth=auth)
                       d['installer']=response.text
                    except:
                       pass
                    data.append(d)
                except Exception as e:
                    print(str(e))           
        sqlwrite(data,tablename)
        return data
    except Exception as e:
        print(str(e))
     
def sqlwrite(data,tablename):
    try: 
        for ll in data:
            keys=[]
            value=[]
            values=ll.items()
            for v,x in values:
                if(x==None):
                    x="0"    
                keys.append(str(v))
                value.append(str(x).replace("'",'"'))
            mydb = mysql.connector.connect(
               host="35.238.96.143",
               user="serverman",
               passwd="",
               database="orgway_serverman"
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
            mycursor.execute(sql,val)
            mydb.commit()
            mydb.close()
    except Exception as e:
        print(str(e))

serverid=args.server
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



