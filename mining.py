from hashlib import sha256
MAX_NONCE = 100000000000

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine(item, difficulty):
    prefix_str = '0'*difficulty
    for nonce in range(MAX_NONCE):
        text = str(item.prev_hash) + str(item.sender_id) + str(item.reciver_id) + str(item.transaction_amt) + str(nonce)
        new_hash = SHA256(text)
        print(new_hash)
        if new_hash.startswith(prefix_str):
            return new_hash

    raise BaseException(f"Couldn't find correct has after trying {MAX_NONCE} times")


def set_mine(item):
    difficulty = 5
    new_hash = mine(item, difficulty)
    mine_rewarded = 50
    return item, new_hash, mine_rewarded