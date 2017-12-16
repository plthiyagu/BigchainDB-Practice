![Logo of the project](https://github.com/vivek-bombatkar/BIgchainDB_Practice/blob/master/bigchaindb_logo.JPG)

# Hands-on exercise on BigchainDB to getting conceptual familiarity on Blockchain 
> https://www.bigchaindb.com/


## Install MongoDB and bigchainDB python package
> https://docs.bigchaindb.com/projects/server/en/latest/quickstart.html

Issue while installation - 
```shell
vivek@ubuntu:~$ sudo apt-get install -y mongodb-org
E: Could not get lock /var/lib/dpkg/lock - open (11: Resource temporarily unavailable)
E: Unable to lock the administration directory (/var/lib/dpkg/), is another process using it?
```
Steps to resolve - 
```shell
vivek@ubuntu:~$ sudo rm /var/lib/apt/lists/lock
```

## Starting up DBs
Once installation done, keep mongoDB running on one terminal and blockchainDB running on another terminal.

```shell
#Drop and recreate /data/db onlt if any issue with connection to mongoDB
$ sudo mkdir -p /data/db
$ sudo chmod -R 700 /data/db

$ sudo mongod --replSet=bigchain-rs
$ bigchaindb -y configure mongodb
$ bigchaindb start
```

Check running it on localhost
> http://127.0.0.1:9984/


## Code snippet run with python3
```Shell
$ python3 <>.py
```

## Code refrence from
> https://docs.bigchaindb.com/projects/py-driver/en/latest/usage.html

## My notes

### Cryptographic Identities Generation
Represented by public/private key pairs. The private key is used to sign transactions, meanwhile the public key is used to verify that a signed transaction was indeed signed by the one who claims to be the signee

### Asset Creation - in 3 steps
1. First, let’s prepare the transaction
2. The transaction now needs to be fulfilled by signing it with private key
3. sent over to a BigchainDB node
response from the node should be the same as that which was sent

### Asset Transfer
1. Let’s now prepare the transfer transaction
2. fulfill it
3. sent over to BigchainDB

