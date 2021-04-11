from hashlib import sha256
import random
import time

blockNumber = 0
previousHash = '0'*64
difficulty = 6
numZeros = '0'*difficulty

# Generates a sha256 hash for the given block
def SHA256(block):
    return sha256(block.encode("ascii")).hexdigest()

# Mines the current block of bitcoin
# Takes the block number, list of transactions for the block,
# and the previous hash and tries to compute a valid hash
# for the block based on the difficulty and leading 
# zero's requirement 
def mine(blockNumber, transactions, previousHash):
    nonce = 0
    while True:
        block = str(blockNumber) + transactions + previousHash + str(nonce)
        hashVal = SHA256(block)
        if(hashVal.startswith(numZeros)):
            print("Bitcoin successfully mined with a nonce of: "+ str(nonce))
            return hashVal
        nonce += 1

# Randomly generates a list of transactions for the block
def generateTransactions():
    transactions = ''
    users = ["Bob", "Alice", "Steve", "Jeremy", "Rebecca"]
    transactionsInBlock = random.randint(5,10)
    for x in range(transactionsInBlock):
        user1 = random.randint(0,len(users)-1)
        fromUser = users[user1]
        user2 = 0
        sameUser = True
        while sameUser:
            user2 = random.randint(0,len(users)-1)
            if(user2!=user1):
                sameUser = False
        toUser = users[user2]
        bitcoin = random.random()*25
        if(x!=transactionsInBlock-1):
            transactions += fromUser +"->"+toUser+"->" + str(bitcoin) +",\n"
        else:
            transactions += fromUser +"->"+toUser+"->" + str(bitcoin)
    return transactions


if __name__=='__main__':
    try:
        print("Mining started...")
        while(True):
            start = time.time()
            print("Mining Block "+str(blockNumber))

            transactions = generateTransactions()
            print("New Transactions: \n"+transactions)

            hashVal = mine(blockNumber, transactions, previousHash)
            print("Mining completed in: "+ str(time.time()-start) +"seconds")
            print("Block hash: "+hashVal)

            blockNumber += 1
            previousHash = hashVal
            print()

    except KeyboardInterrupt:
        print("\nShuting down miner...")
