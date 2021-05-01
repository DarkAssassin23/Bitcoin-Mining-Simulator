from hashlib import sha256
from multiprocessing import Process, Queue
import random
import time
import os
import sys


numCPUs = os.cpu_count()
processes = []
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
def mine(blockNumber, transactions, previousHash, nonce, queue):
    while True:
        block = str(blockNumber) + transactions + previousHash + str(nonce)
        hashVal = SHA256(block)
        if(hashVal.startswith(numZeros)):
            queue.put([hashVal, nonce])
            return
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

# Starts up as many miners, or processes, as cpu cores
# and runs until a valid hash is found. That value is returned
# and all processes are ended
def startMiners(blockNumber, transactions, previousHash):
    queue = Queue()
    
    segmentStart = 0
    for p in range(numCPUs):
        if(not(p==0)):
            segmentStart += segmentSize
        p = Process(target=mine, args=(blockNumber, transactions, previousHash, segmentStart, queue))
        processes.append(p)
        p.start()
    while queue.empty():
        pass
    result = queue.get()

    for p in processes:
        p.terminate()

    return result

# Prints out the hash that was found with the corresponding nonce
# as well as how long it took to find
def showResults(nonce, hashVal, time):
    print("Bitcoin successfully mined with a nonce of: "+ str(nonce))
    print("Block hash: "+hashVal)
    print("Mining completed in: "+ str(time) +" seconds")
    print()

if __name__=='__main__':
    runTimes = []
    segmentSize = sys.maxsize

    try:
        print("Mining started...")
        while(True):
            start = time.time()
            print("Mining Block "+str(blockNumber))

            transactions = generateTransactions()
            print("New Transactions: \n"+transactions)

            result = startMiners(blockNumber, transactions, previousHash)

            finalTime = time.time() - start

            hashVal = result[0]
            nonce = result[1]

            showResults(nonce, hashVal, finalTime)

            runTimes.append(finalTime)
            blockNumber += 1
            previousHash = hashVal

    except KeyboardInterrupt:
        print("\nShuting down miner...")
        for p in processes:
            p.terminate()
        print("Miner shutdown")

        total = 0
        for t in runTimes:
            total += t
        print("Average time per hash: "+str(total/len(runTimes))+" seconds")
