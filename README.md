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

### Asset Transfer - also in 3 steps
1. Let’s now prepare the transfer transaction
2. fulfill it
3. sent over to BigchainDB

### Create VS Transfer Asset
Create asset is a special case in that the asset id is NOT found on the asset itself, but is simply the CREATE transaction’s id VS If you instead wanted to consume TRANSFER transactions (for example, fulfilled_transfer_tx), you could obtain the asset id to transfer from the asset['id'] property

![Create VS Transfer Asset] (https://github.com/vivek-bombatkar/BIgchainDB_Practice/blob/master/Asset_CreateVsTransfer.JPG)


In order to prepare a transfer transaction, we needs to provide at least three things:
1. inputs – one or more fulfillments that fulfill a prior transaction’s output conditions.
2. asset['id'] – the id of the asset being transferred.
3. Recipient public_keys – one or more public keys representing the new recipients(s).

### Divisible Assets
All assets in BigchainDB become implicitly divisible if a transaction contains more than one of that asset. To create divisible assets, we need to specify an amount >1 together with the public keys. The way we do this is by passing a list of tuples in recipients where each tuple corresponds to an output.

### Querying for Assets
BigchainDB allows you to query for assets using simple text search. This search is applied to all the strings inside the asset payload and returns all the assets that match a given text search string. It’s also possible to limit the amount of returned results using the limit argument

### Double Spends
BigchainDB makes sure that a user can’t transfer the same digital asset two or more times (i.e. it prevents double spends). If we try to create another transaction with the same input as before, the transaction will be marked invalid and the validation will throw a double spend exception.

### Multiple Owners
To create a new digital asset with multiple owners, one can simply provide a list or tuple of recipients

### Crypto-Conditions 
Crypto-conditions provide a mechanism to describe a signed message such that multiple actors in a distributed system can all verify the same signed message and agree on whether it matches the description.
This provides a useful primitive for event-based systems that are distributed on the Internet since we can describe events in a standard deterministic manner (represented by signed messages) and therefore define generic authenticated event handlers.

### Threshold Conditions
Threshold conditions introduce multi-signatures, m-of-n signatures, or even more complex binary Merkle trees to BigchainDB.
Setting up a generic threshold condition is a bit more elaborate than regular transaction signing but allows for flexible signing between multiple parties or groups.
The basic workflow for creating a more complex cryptocondition is the following:
Create a transaction template that includes the public key of all (nested) parties (signers) in the output‘s public_keys
Set up the threshold condition using the cryptocondition library. Update the output’s condition and hash in the transaction template.

### Timeout Conditions
Timeout conditions allow assets to expire after a certain time. The primary use case of timeout conditions is to enable Escrow.
The condition can only be fulfilled before the expiry time. Once expired, the asset is lost and cannot be fulfilled by anyone

### Escrow
Escrow is a mechanism for conditional release of assets.
This means that the assets are locked up by a trusted party until an execute condition is presented. In order not to tie up the assets forever, the escrow foresees an abort condition, which is typically an expiry time.
BigchainDB and cryptoconditions provides escrow out-of-the-box, without the need of a trusted party.
A threshold condition is used to represent the escrow, since BigchainDB transactions cannot have a pending state



