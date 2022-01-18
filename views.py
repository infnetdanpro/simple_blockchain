from uuid import uuid4

from flask import jsonify, request
from pydantic.error_wrappers import ValidationError

from inputs import NewTransaction, NewNodes
from lib.blockchain import Blockchain
from app import app

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block: dict = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1
    )

    previous_hash: str = blockchain.hash(last_block)
    block: dict = blockchain.new_block(proof=str(proof), previous_hash=previous_hash)

    return jsonify({
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    })


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    params = request.get_json()
    try:
        values = NewTransaction(**params)
    except ValidationError as e:
        return jsonify({
            'error': e
        }), 422
    index = blockchain.new_transaction(
        sender=values.sender,
        recipient=values.recipient,
        amount=values.amount
    )

    return jsonify({
        'message': f'New transaction in block: {index}'
    }), 201


@app.route('/chain', methods=['GET'])
def get_full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    params = request.get_json()
    try:
        nodes = NewNodes(**params)
    except ValidationError as e:
        return jsonify({
            'error': e
        }), 422

    for node in nodes.nodes:
        blockchain.register_node(node)

    return jsonify({
        'message': 'New nodes have been added',
        'total_nodes': len(blockchain.nodes)
    }), 201


@app.route('/nodes/resolve', methods=['GET'])
def resolve_nodes():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        return jsonify({
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        })
    return jsonify({
        'message': 'Our chain is authoritative',
        'chain': blockchain.chain
    })
