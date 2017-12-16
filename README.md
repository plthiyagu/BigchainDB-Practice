![Logo of the project](https://github.com/vivek-bombatkar/BIgchainDB_Practice/blob/master/bigchaindb_logo.JPG)

# Hands-on exercise on BigchainDB to getting conceptual familiarity on Blockchain 
https://www.bigchaindb.com/


Install MongoDB and bigchainDB python package from : https://docs.bigchaindb.com/projects/server/en/latest/quickstart.html

Issue while installation - 
vivek@ubuntu:~$ sudo apt-get install -y mongodb-org

E: Could not get lock /var/lib/dpkg/lock - open (11: Resource temporarily unavailable)

E: Unable to lock the administration directory (/var/lib/dpkg/), is another process using it?

Steps to resolve - 
vivek@ubuntu:~$ sudo rm /var/lib/apt/lists/lock


Sample code handson from : https://docs.bigchaindb.com/projects/py-driver/en/latest/usage.html

Code snippet look at : https://docs.bigchaindb.com/projects/py-driver/en/latest/usage.html



Once installation done, keep mongoDB running on one terminal and blockchainDB running on another terminal.

$ sudo mkdir -p /data/db

$ sudo chmod -R 700 /data/db

Drop and recreate /data/db if any issue with connection to mongoDB

$ sudo mongod --replSet=bigchain-rs

$ bigchaindb -y configure mongodb

$ bigchaindb start

http://127.0.0.1:9984/


Run with python3

$ python3 <>.py




