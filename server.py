import requests
import mysql.connector
import json
auth=('xxxxxxxxxxxx', 'xxxxxxxxxxxxxx')

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
                   except Exception as e:
                       print(str(e))                                       
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







parameters=[('server_id','id'),('user_id','user_id'),('name','serverName'),('ip','ipAddress'),('provider','serverProvider')]
tablename="servers"
mydb = mysql.connector.connect(
               host="35.238.96.143",
               user="serverman",
               passwd="",
               database="orgway_serverman"
                )
mycursor = mydb.cursor() 
mycursor.execute("TRUNCATE TABLE "+tablename)
mydb.commit()
mydb.close()
response = functiondata('https://manage.runcloud.io/base-api/servers',headers,auth,parameters,tablename)

parameters=[('app_id','id'),('server_user_id','server_user_id'),('server_user_username','server_user_username'),('server_id','server_id'),('name','name'),('defaultServer','defaultServer'),('domains','domains'),('sslinfo','ssl')]
tablename="applications"
try:
    mydb = mysql.connector.connect(
               host="35.238.96.143",
               user="serverman",
               passwd="",
               database="orgway_serverman"
                )
    mycursor = mydb.cursor() 
    mycursor.execute("TRUNCATE TABLE "+tablename)
    mydb.commit()
    mydb.close()
    for r in response:
        server=r['server_id']
        res = functiondata("https://manage.runcloud.io/base-api/servers/"+server+"/webapps?page=1",headers,auth,parameters,tablename)
except Exception as e:
    print(str(e))


