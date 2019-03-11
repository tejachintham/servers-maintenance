#python3
this scripts are used for creating,managing new applications
commands to run the apps:
apps-updater.py(to update the apps in a particular server)
python3 apps-updater.py -s 7kfhsbdyw
--------------------
operations.py
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
------------------
server.py(to update all the servers data)
 python server.py
