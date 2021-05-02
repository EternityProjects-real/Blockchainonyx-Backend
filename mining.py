from hashlib import sha256
MAX_NONCE = 100000000000

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine(item, difficulty):
    prefix_str = '0'*difficulty
    for nonce in range(MAX_NONCE):
        text = str(item.prev_hash) + str(item.sender_id) + str(item.reciver_id) + str(item.transaction_amt) + str(nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            print(f"Yay! Successfully mined bitcoins with nonce value:{nonce}")
            return new_hash

    raise BaseException(f"Couldn't find correct has after trying {MAX_NONCE} times")


def set_mine(item):
    difficulty = 4
    new_hash = mine(item, difficulty)
    return item, new_hash