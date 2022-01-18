import hashlib
import json

from dataclasses import dataclass, asdict
from time import time
from urllib.parse import urlparse, urlunparse

import requests


@dataclass
class BaseData:
    def dict(self):
        return asdict(self)


@dataclass
class BlockData(BaseData):
    index: int
    timestamp: float
    transactions: list
    proof: str
    previous_hash: str


@dataclass
class Transaction(BaseData):
    sender: str
    recipient: str
    amount: int


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.new_block(previous_hash='1', proof='100')

    def new_block(self, proof: str, previous_hash: str) -> dict:
        block: BlockData = BlockData(
            index=len(self.chain),
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash
        )
        block: dict = block.dict()
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        self.current_transactions.append(transaction.dict())
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: dict) -> str:
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        block_str: str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
            - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
            - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof: int = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def register_node(self, address: str):
        """
        Adding new node into sets for unique nodes
        :param address: https://some-address.com/
        :return: None
        """
        url = urlparse(address)
        self.nodes.add(url.netloc)

    def valid_chain(self, chain: list) -> bool:
        """Validate given blockchain"""
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True
        # last_block = chain[0]
        #
        # for index, block in enumerate(chain):
        #     if block['previous_hash'] != self.hash(last_block):
        #         return False
        #
        #     if not self.valid_proof(last_proof=last_block['proof'], proof=block['proof']):
        #         return False
        #
        #     last_block = block
        # return True

    def resolve_conflicts(self) -> bool:
        """
        Simple Consensus Algorithm for resolve
        conflicts by replacing our chain with the longest one in the network
        """

        neighbours = self.nodes
        print(neighbours)
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            node_url = urlunparse(('http', node, 'chain', '', '', ''))
            resp = requests.get(node_url)

            if not resp.status_code == 200:
                continue

            result = resp.json()
            length, chain = result['length'], result['chain']

            valid = self.valid_chain(chain)
            ifff = length > max_length

            print(valid)
            print(ifff)

            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False

