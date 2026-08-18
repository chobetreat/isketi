import random, time




class bit:
    def __init__(self, weight=0, connectionValues=[1]):
        self.weight = weight
        self.conectedTo=connectionValues
        self.value=0
    def tick(self, rowWeights):
        if len(self.conectedTo)==0:
            self.value=0
            return 0
        self.value = 1
        for conection in self.conectedTo:
            self.value += (rowWeights[conection]*self.weight)
        self.value/=len(self.conectedTo)
        return self.value
    def change(self, value):
        buffer=value+self.weight
        if buffer > 1:
            self.weight=1
        elif buffer<0:
            self.weight=0
        else:
            self.weight=buffer
    def add_connection(self, highest_possible_amount):
        self.conectedTo.append(random.randint(0, highest_possible_amount))
    def remove_connection(self):
        if len(self.conectedTo)>0:

            self.conectedTo.remove(self.conectedTo[random.randint(0, len(self.conectedTo)-1)])
class row:
    def __init__(self, bitcount, bitweight=0, previousBitCount=-1):
        if previousBitCount==-1:
            previousBitCount=bitcount
        self.bits = []
        self.bitCount=bitcount
        connectionBit=0
        for i in range(bitcount):
            self.bits.append(bit(bitweight, [connectionBit]))
            connectionBit+=1
            if connectionBit>=previousBitCount-1:
                connectionBit=0
        self.value=0
    def display(self):
        for b in self.bits:
            print(f" {b.weight} ", end="")

    def tick(self, rowWeights):
        self.value=[]
        for bit in self.bits:
            self.value.append(bit.tick(rowWeights))
        return self.value
    def change(self, value):
        self.bits[random.randint(0, len(self.bits)-1)].change(value)
    def add_connection(self, highest_possible_amount):
        self.bits[random.randint(0, len(self.bits)-1)].add_connection(highest_possible_amount)
    def remove_connection(self):
        self.bits[random.randint(0, len(self.bits) - 1)].remove_connection()
class network:
    def __init__(self, rowCount, bitCount, bitWeight=0, maxBitWeight=10, outputValues=2, inputValues=4):
        self.rowCount = rowCount
        self.satisfaction=0
        self.bitCount = bitCount
        self.maxBitWeight = maxBitWeight
        self.rows=[]
        self.output=row(outputValues, bitWeight, bitCount)
        self.value=[]
        self.inputValues=inputValues
        for i in range(outputValues):
            self.value.append(0)
        for i in range(rowCount):
            if i==0:
                self.rows.append(row(bitCount, bitWeight,  inputValues))
            else:
                self.rows.append(row(bitCount, bitWeight,  bitCount))
    def execute(self, inputList):
        weights=inputList
        for row in self.rows:
            weights=row.tick(weights)
        self.output.tick(weights)
        for b, i in enumerate(self.output.bits):

            self.value[b]=i.value
    def display(self):
        for row in self.rows:
            print()
            row.display()
            print()
        print()
        self.output.display()
        print()


    def change(self, value):
        r = random.randint(0, self.rowCount)
        if r==self.rowCount:
            self.output.change(value)
        else:
            self.rows[r].change(value)
    def add_connection(self):
        rNumber=random.randint(-1, self.rowCount-1)
        if rNumber==-1:
            self.output.add_connection(self.bitCount-1)
        elif rNumber==0:
            self.output.add_connection(self.inputValues-1)
        else:
            self.rows[rNumber].add_connection(self.bitCount-1)
    def remove_connection(self):
        rNumber = random.randint(-1, self.rowCount - 1)
        if rNumber == -1:
            self.output.remove_connection()
        else:
            self.rows[rNumber].remove_connection()
ai = network(2, 4, 0, 20, 2, 4)

training_data = [
    [[0,0,0,0],[0,0]],
    [[0,0,0,1],[0,0]],
    [[0,0,1,0],[0,0]],
    [[0,0,1,1],[0,0]],
    [[0,1,0,0],[0,0]],
    [[0,1,0,1],[0,0]],
    [[0,1,1,0],[0,0]],
    [[0,1,1,1],[1,1]],
    [[1,0,0,0],[0,0]],
    [[1,0,0,1],[0,0]],
    [[1,0,1,0],[0,0]],
    [[1,0,1,1],[1,1]],
    [[1,1,0,0],[0,0]],
    [[1,1,0,1],[1,1]],
    [[1,1,1,0],[1,1]],
    [[1,1,1,1],[1,1]]
]
index=0
loops=0
startTime=time.time()
while ai.satisfaction<1:
    loops+=1
    #time.sleep(0.2)
    index+=1
    if index>len(training_data)-1:
        index=0
        #ai.display()
    ai.execute(training_data[index][0])
    if [round(ai.value[0]), round(ai.value[1])]==training_data[index][1]:
        ai.satisfaction+=0.01
    else:
        ai.satisfaction-=0.02
        for i in range(10):
            if random.randint(1, 3)!=1:
                ai.change(random.randint(-10, 25)/100)
            elif random.randint(1, 5)!=1:
                ai.add_connection()
            else:
                ai.remove_connection()
    print(f"Executed AI with input:{training_data[index][0]}, and recived output:{[round(ai.value[0]), round(ai.value[1])]}, expected output:{training_data[index][1]}, curent network satisfaction: {ai.satisfaction}")
ai.display()
print(f"Completed Ai Training in {time.time()-startTime} seconds. with {loops} loops.")
while True:
    inn = eval(input("Ai Input:"))
    ai.execute(inn)
    print(
        f"Executed AI with input:{inn}, and recived output:{[(ai.value[0]), (ai.value[1])]}")
