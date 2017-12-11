import bigchaindb_driver
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair



def defineAsset():
	#asset defination
	bicycle = { 'data': {'bicycle': {'serial_number': 'abcd1234','manufacturer': 'bkfab',},},}
	#metadata to tgransaction
	metadata = {'name':'vivek'}
	return bicycle, metadata

def prepareAsset(operation, asset, signers="", metadata={}, inputs="", recipients=""): 
	prepare_tx=bigDB.transactions.prepare(operation=operation,signers=signers,asset=asset,metadata=metadata, inputs=inputs, recipients=recipients)
	return prepare_tx

def fulfillAsset(prepare_tx, private_keys):
	fulfilled_tx=bigDB.transactions.fulfill(prepare_tx,private_keys=private_keys)
	return fulfilled_tx

def sentAsset(fulfilled_tx):
	sent_tx=bigDB.transactions.send(fulfilled_tx)
	sent_tx=fulfilled_tx
	return sent_tx

def main():
	#create bigchain db object
	root_url='http://127.0.0.1:9984/'
	global bigDB
	bigDB=BigchainDB(root_url)

	bicycle, metadata = defineAsset()

	vivek,tom = generate_keypair(), generate_keypair()

	prepareCreateTx=prepareAsset(operation='CREATE',signers=vivek.public_key,asset=bicycle,metadata=metadata)
	fulfillCreateTx=fulfillAsset(prepareCreateTx, vivek.private_key)
	sentCreateTx=sentAsset(fulfillCreateTx)

	id=fulfillCreateTx['id']

	print(bigDB.transactions.status(id))
	trials = 0
	while trials < 100:
		try:
			if bigDB.transactions.status(id).get('status') == 'valid':
				break
		except bigchaindb_driver.exceptions.NotFoundError:
			trials += 1
	print(bigDB.transactions.status(id))

	create_tx=bigDB.transactions.retrieve(id)
	asset_id=create_tx['id']
	transfer_asset={'id':asset_id,}

	out_index=0
	output = create_tx['outputs'][out_index]
	transfer_input = {'fulfillment': output['condition']['details'],'fulfills': {'output_index': out_index,'transaction_id': create_tx['id'],},'owners_before': output['public_keys']}

	preparedTransferdTx = prepareAsset(operation='TRANSFER',asset=transfer_asset,inputs=transfer_input,recipients=tom.public_key)
	fulfilledTransferTx = fulfillAsset(preparedTransferdTx, vivek.private_key)
	sentTransferTx = sentAsset(fulfilledTransferTx)

	print(fulfilledTransferTx)


if __name__ == '__main__':
	main()