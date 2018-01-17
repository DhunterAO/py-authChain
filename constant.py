from block import Block


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
genesis_block = Block(0, [], "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9", 1516156465.836211,
                      "00002758d1b4dd20111165f398e0cdf649af643176d5f77c5ab9cd1b39141ef9", 126745)
#print(genesis_block.to_json())