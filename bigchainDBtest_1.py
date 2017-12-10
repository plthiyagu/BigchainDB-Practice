import bigchaindb_driver
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

###example of bike transfer
#https://docs.bigchaindb.com/projects/py-driver/en/latest/usage.html
#vivek --> tom


#create bigchain db object
root_url='http://127.0.0.1:9984/'
bigDB=BigchainDB(root_url)

#asset defination
bicycle = { 'data': {'bicycle': {'serial_number': 'abcd1234','manufacturer': 'bkfab',},},}

#metadata to tgransaction
metadata = {'name':'vivek'}

#cryptographic identities, key-pair
vivek,tom = generate_keypair(), generate_keypair()
#print(vivek,tom)


##asset creation
#1> create transaction
prepare_tx=bigDB.transactions.prepare(operation='CREATE',signers=vivek.public_key,asset=bicycle,metadata=metadata)
#print(prepare_tx)

#2> fultuiled transaction
fulfilled_tx=bigDB.transactions.fulfill(prepare_tx,private_keys=vivek.private_key)
#print(fulfilled_tx)

#3> send transaction to bigchain db
sent_tx=bigDB.transactions.send(fulfilled_tx)
sent_tx=fulfilled_tx
#print(sent_tx)
id=fulfilled_tx['id']
#print(id)

#loop till transaction get valid
print(bigDB.transactions.status(id))
trials = 0
while trials < 100:
	try:
		if bigDB.transactions.status(id).get('status') == 'valid':
			break
	except bigchaindb_driver.exceptions.NotFoundError:
		trials += 1
print(bigDB.transactions.status(id))


##asset transfer
#vivek --> tom
#1> create transaction
create_tx=bigDB.transactions.retrieve(id)
print(create_tx)

#In order to prepare the transfer transaction, we first need to know the id of the asset we’ll be transferring. Here, because Alice is consuming a CREATE transaction, we have a special case in that the asset id is NOT found on the asset itself, but is simply the CREATE transaction’s id:

asset_id=create_tx['id']
transfer_asset={'id':asset_id,}

#2> prepare transfer transaction
out_index=0
output = create_tx['outputs'][out_index]

transfer_input = {'fulfillment': output['condition']['details'],'fulfills': {'output_index': out_index,'transaction_id': create_tx['id'],},'owners_before': output['public_keys']}

prepared_transfer_tx = bigDB.transactions.prepare(operation='TRANSFER',asset=transfer_asset,inputs=transfer_input,recipients=tom.public_key,)

#3> fulfill transfer
fulfilled_transfer_tx = bigDB.transactions.fulfill(prepared_transfer_tx,private_keys=vivek.private_key,)

#4> sent to bigchain db
send_tx=bigDB.transactions.send(fulfilled_transfer_tx)
send_tx=fulfilled_transfer_tx
#print(fulfilled_transfer_tx)

fulfilled_transfer_tx['outputs'][0]['public_keys'][0] == tom.public_key
fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == vivek.public_key




