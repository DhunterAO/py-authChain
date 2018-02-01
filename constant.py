from block import Block
from authorization import Authorization
from limit import Limit
from address import Address
from output import Output
from dataURL import DataURL
from duration import Duration

MAX_DATA_RANGE = 1000000

'''
{
  "blockchain": [
    {
      "authorizations": {}, 
      "hash_root": "", 
      "nonce": 52811, 
      "now_hash": "0000208efadb6caff4e351c6fd1bf059677bb3f64fb63e0e1aec9a7ffffca265", 
      "prev_hash": 0, 
      "timestamp": 1516156465.836211
    }
  ], 
  "difficulty": "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 
  "height": 1
}
'''

"""
    server pubkey: 59be9bbd5224fb4d69a861c3cd934ca07e2e56de148e988fcff7df8f47b98bcac15c0e3427433004e0a650cde005f4d5
    private_key: ae4d632b868f04b9fc9b69898f4a8a555f10c64e35cf7692
    or b'\xaeMc+\x86\x8f\x04\xb9\xfc\x9bi\x89\x8fJ\x8aU_\x10\xc6N5\xcfv\x92'
"""
SERVER_ADDRESS = Address("ae4d632b868f04b9fc9b69898f4a8a555f10c64e35cf7692")

out = Output(recipient='59be9bbd5224fb4d69a861c3cd934ca07e2e56de148e988fcff7df8f47b98bcac15c0e3427433004e0a650cde005f4d5',
             data_url=DataURL(0, MAX_DATA_RANGE), limit=Limit(7))
auth = Authorization(inputs=[], outputs=[out], duration=Duration(0), timestamp=1516156465.8362110)

"""
"genesis block":
{
    'prev_hash': 0,
    'now_hash': '0000cdba04652df1bf82edc180aa7ccedd9a5aa9881ef13fc40f2481122099a7',
    'timestamp': 1516156465.836211,
    'hash_root': '0c41debab6af9066e687e4df07a212174e112c727922a27c27cfe64c94c547af',
    'nonce': 51071,
    'authorizations':
    [{
        'inputs': [],
        'outputs': [{
            'recipient': '59be9bbd5224fb4d69a861c3cd934ca07e2e56de148e988fcff7df8f47b98bcac15c0e3427433004e0a650cde005f4d5',
            'dataURL': {
                'start': 0,
                'end': 1000000
            },
            'limit': 7
        }],
        'duration': {
            'start_time': 0,
            'end_time': 0
        },
        'timestamp': 1516156465.836211
    }]
}
"""
GENESIS_BLOCK = Block(prev_hash=0,
                      authorizations=[auth],
                      hash_root="0c41debab6af9066e687e4df07a212174e112c727922a27c27cfe64c94c547af",
                      timestamp=1516156465.8362110,
                      now_hash="0000cdba04652df1bf82edc180aa7ccedd9a5aa9881ef13fc40f2481122099a7",
                      nonce=51071)

server_address = '127.0.0.1:9000'
