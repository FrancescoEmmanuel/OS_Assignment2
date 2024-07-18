import random
import os
import sys

def generateRandomRequests(filename, numRequests=1000, maxCylinder=4999):
    with open(filename, 'w') as file:
        for _ in range(numRequests):
            file.write(f"{random.randint(0, maxCylinder)}\n")

def readDiskRequests(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file]

def computeHeadMovements(requests, initialPosition):
    currentPos = initialPosition
    totalMovements = 0
    for req in requests:
        totalMovements += abs(req - currentPos)
        currentPos = req
    return totalMovements

def fcfsAlgorithm(requests, initialPosition):
    return computeHeadMovements(requests, initialPosition)

def scanAlgorithm(requests, initialPosition):
    sortedReqs = sorted(requests)
    leftReqs = [r for r in sortedReqs if r <= initialPosition]
    rightReqs = [r for r in sortedReqs if r > initialPosition]

    movements = computeHeadMovements(leftReqs[::-1], initialPosition)
    if rightReqs:
        movements += abs(leftReqs[0] - rightReqs[0])
        movements += computeHeadMovements(rightReqs, rightReqs[0])
    return movements

def cScanAlgorithm(requests, initialPosition, maxCylinder=4999):
    sortedReqs = sorted(requests)
    leftReqs = [r for r in sortedReqs if r <= initialPosition]
    rightReqs = [r for r in sortedReqs if r > initialPosition]

    movements = computeHeadMovements(leftReqs[::-1], initialPosition)
    if rightReqs:
        movements += abs(leftReqs[0] - 0) + abs(maxCylinder - 0)
        movements += computeHeadMovements(rightReqs, maxCylinder)
    return movements

def optimizedFcfsAlgorithm(requests, initialPosition):
    sortedReqs = sorted(requests)
    return computeHeadMovements(sortedReqs, initialPosition)

def optimizedScanAlgorithm(requests, initialPosition):
    lowerHalf = sorted([r for r in requests if r <= initialPosition], reverse=True)
    upperHalf = sorted([r for r in requests if r > initialPosition])

    movements = computeHeadMovements(lowerHalf, initialPosition)
    if upperHalf:
        movements += abs(lowerHalf[0] - upperHalf[0])
        movements += computeHeadMovements(upperHalf, upperHalf[0])
    return movements

def optimizedCScanAlgorithm(requests, initialPosition, maxCylinder=4999):
    sortedReqs = sorted(requests)
    leftReqs = [r for r in sortedReqs if r < initialPosition]
    rightReqs = [r for r in sortedReqs if r >= initialPosition]
    movements = 0

    if rightReqs:
        movements += computeHeadMovements(rightReqs, initialPosition)
        if leftReqs:
            optimalJump = min(leftReqs, key=lambda x: abs(maxCylinder - x))
            movements += abs(rightReqs[-1] - optimalJump)
            movements += computeHeadMovements(leftReqs, optimalJump)
    else:
        optimalJump = min(leftReqs, key=lambda x: abs(maxCylinder - x))
        movements += abs(initialPosition - optimalJump)
        movements += computeHeadMovements(leftReqs, optimalJump)
    return movements

def main():
    if len(sys.argv) != 3:
        print("Please type in the following into your cmd to run: python script.py <initialHeadPosition> <requestFile>")
        sys.exit(1)

    initialPosition = int(sys.argv[1])
    filename = sys.argv[2]

    if not os.path.exists(filename):
        print(f"{filename} not found. Generating a new file with 1000 random requests.")
        generateRandomRequests(filename)
    else:
        print(f"{filename} found")
    
    
    requests = readDiskRequests(filename)
    print("\nNot Optimized")
    print("====================================")
    print("FCFS Total Movements:", fcfsAlgorithm(requests, initialPosition))
    print("SCAN Total Movements:", scanAlgorithm(requests, initialPosition))
    print("C-SCAN Total Movements:", cScanAlgorithm(requests, initialPosition))


    # Print optimized results
    print("\nOptimized")
    print("====================================")
    print("FCFS Total Movements:", optimizedFcfsAlgorithm(requests, initialPosition))
    print("SCAN Total Movements:", optimizedScanAlgorithm(requests, initialPosition))
    print("C-SCAN Total Movements:", optimizedCScanAlgorithm(requests, initialPosition))

if __name__ == "__main__":
    main()
