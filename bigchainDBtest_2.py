import logging
import bigchaindb_driver
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver.exceptions import NotFoundError

def defineAsset():
	#asset defination
	bicycle = { 'data': {'bicycle': {'serial_number': 'abcd1234','manufacturer': 'bkfab',},},}
	#metadata to tgransaction
	metadata = {'name':'vivek'}
	return bicycle, metadata

def prepareTransferAsset(operation, asset, signers="", metadata={}, inputs="", recipients=""): 
	prepare_tx=bigDB.transactions.prepare(operation=operation,asset=asset, recipients=recipients, inputs=inputs,signers=signers)
	return prepare_tx

def prepareCreateAsset(operation, asset, signers="", metadata={}, inputs="", recipients=""): 
	prepare_tx=bigDB.transactions.prepare(operation=operation,signers=signers,asset=asset,metadata=metadata)
	return prepare_tx

def fulfillAsset(prepare_tx, private_keys):
	fulfilled_tx=bigDB.transactions.fulfill(prepare_tx,private_keys=private_keys)
	return fulfilled_tx

def sentAsset(fulfilled_tx):
	sent_tx=bigDB.transactions.send(fulfilled_tx)
	sent_tx=fulfilled_tx
	return sent_tx

def getTransStatus(id):
	try:
	    status = bigDB.transactions.status(id)
	except NotFoundError as e:
	    logger.error('Transaction "%s" was not found.',id,extra={'status': e.status_code})


def main():
	global logger
	logger=logging.getLogger(__name__)
	logging.basicConfig(format='%(asctime)-15s %(status)-3s %(message)s')
	#logging.basicConfig(filename='/home/vivek/blockchainPractice/BIgchainDB_Practice/file.log', filemode='w', level=logging.INFO)

	logger.debug("Getting started")
	#create bigchain db object
	root_url='http://127.0.0.1:9984/'
	global bigDB
	bigDB=BigchainDB(root_url)

	bicycle, metadata = defineAsset()

	vivek,tom = generate_keypair(), generate_keypair()

	prepareCreateTx=prepareCreateAsset(operation='CREATE',signers=vivek.public_key,asset=bicycle,metadata=metadata)
	fulfillCreateTx=fulfillAsset(prepareCreateTx, vivek.private_key)
	sentCreateTx=sentAsset(fulfillCreateTx)

	id=fulfillCreateTx['id']

	#logger.debug(getTransStatus(123))

	logger.debug(getTransStatus(id))
	trials = 0
	while trials < 100:
		try:
			if bigDB.transactions.status(id).get('status') == 'valid':
				break
		except bigchaindb_driver.exceptions.NotFoundError:
			trials += 1
	logger.debug(getTransStatus(id))

	create_tx=bigDB.transactions.retrieve(id)
	asset_id=create_tx['id']
	transfer_asset={'id':asset_id,}

	out_index=0
	output = create_tx['outputs'][out_index]
	transfer_input = {'fulfillment': output['condition']['details'],'fulfills': {'output_index': out_index,'transaction_id': create_tx['id'],},'owners_before': output['public_keys']}

	preparedTransferdTx = prepareTransferAsset(operation='TRANSFER',asset=transfer_asset,inputs=transfer_input,recipients=tom.public_key)
	fulfilledTransferTx = fulfillAsset(preparedTransferdTx, vivek.private_key)
	sentTransferTx = sentAsset(fulfilledTransferTx)

	logger.debug(fulfilledTransferTx)

	#divisible assets

	bicycle_token = {
        'data': {
            'token_for': {
                'bicycle': {
                    'serial_number': 'abcd1234',
                    'manufacturer': 'bkfab'
                }
            },
            'description': 'Time share token. Each token equals one hour of riding.',
        },
    }

	bob, carly = generate_keypair(), generate_keypair()

	prepared_token_tx = prepareTransferAsset(operation='CREATE',signers=bob.public_key,recipients=[([carly.public_key], 10)],asset=bicycle_token,)
	fulfilled_token_tx = fulfillAsset(prepared_token_tx, private_keys=bob.private_key)
	sent_token_tx = sentAsset(fulfilled_token_tx)
	sent_token_tx = fulfilled_token_tx

	#print(sent_token_tx)

	print(bigDB.assets.get(search='bigchaindb', limit=2))

if __name__ == '__main__':
	main()