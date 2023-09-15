from typing import Any, List
from datetime import datetime
from dataclasses import dataclass
import hashlib
import streamlit as st
import pandas as pd

# class Block: 
#     def __init__(self, data: Any, creator_id: int, prev_hash: str = "0", timestamp: str = None):
#         self.data = data
#         self.creator_id = creator_id
#         self.prev_hash = prev_hash
#         self.timestamp = timestamp if timestamp is not None else datetime.utcnow().strftime("%H:%M:%S")
    
#     def __repr__(self):
#         return "Block(data={}, creator_id={}, prev_hash={}, timestamp={})".format(
#             repr(self.data),
#             repr(self.creator_id),
#             repr(self.prev_hash),
#             repr(self.timestamp)

#         )
    
#     def __eq__(self, other):
#         return (self.data == other.data and self.creator_id == other.creator_id and
#                 self.prev_hash == other.prev_hash and self.timestamp == other.timestamp)

@dataclass #decorator
class Block:
    data: Any
    creator_id :int
    prev_hash :str = "0"
    timestamp: str = datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0 

    def hash_block(self):
        sha = hashlib.sha256()
        data = str(self.data).encode()
        sha.update(data)
        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)
        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)
        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)
        nonce = str(self.nonce).encode()
        sha.update(nonce)
        return sha.hexdigest()

@dataclass 
class PyChain:
    chain: List[Block]
    difficulty: int = 5 

    def proof_of_work(self, block):
        calculated_hash = block.hash_block()
        num_of_zeros = "0" * self.difficulty #"0000"
        while not calculated_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()
        
        print("Winning hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]


# streamlit run blockchain-plain.py


def setup():
    cached_data = st.session_state.get("pychain")
    if cached_data is None:
        st.session_state['pychain'] = PyChain([Block(data="Genesis", creator_id=0)])
        return st.session_state['pychain']
    return cached_data

pychain = setup()

st.title("PyChain")
st.markdown('## Add a new block')

input_data = st.text_input("Block Data")

# add button

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()
    new_block = Block(data = input_data, creator_id=42, prev_hash = prev_block_hash)
    pychain.add_block(new_block)


st.markdown('## PyChain Ledger')
pychain_df = pd.DataFrame(pychain.chain)
st.write(pychain_df)

