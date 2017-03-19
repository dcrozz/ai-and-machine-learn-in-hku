import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        currentNumber = self.getNumberOfAttacks()
        betterBoard = copy.deepcopy(self)
        costBoard = betterBoard.getCostBoard()
        from functools import reduce
        minNumber = min(reduce(lambda x,y:x+y, costBoard.squareArray))
        newRow,newCol = random.choice([(y, x) for y in range(8) for x in range(8) if costBoard.squareArray[y][x] == minNumber])
        oldRow = min([y for y in range(8) if self.squareArray[y][newCol] == 1])
        betterBoard.squareArray[newRow][newCol] = 1
        betterBoard.squareArray[oldRow][newCol] = 0
        return (betterBoard, betterBoard.getNumberOfAttacks(), newRow, newCol)

        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        from itertools import permutations
        queenPosition=[]

        for x in range(0,8):
            for y in range(0,8):
                if self.squareArray[y][x]==1:
                    queenPosition.append(y)
                    break
        horzon_set = [ queenPosition.count(x) for x in set(queenPosition) ]
        queens = [ (x,y) for x,y in enumerate(queenPosition)]
        rcross = {}
        lcross = {}
        for q1, q2 in permutations(queens,2):
            if ( q1[0] -q2[0] == q1[1] - q2[1] ):
                if str(q1[0]-q2[0]) in rcross:
                    rcross[str(q1[0] -q2[0])] +=1
                else:
                    rcross[str(q1[0] -q2[0])] = 1
            if ( q1[0] + q1[1] == q2[0] + q2[1] ):
                if str(q1[0]+q2[0]) in lcross:
                    lcross[str(q1[0] +q2[0])] +=1
                else:
                    lcross[str(q1[0] +q2[0])] = 1
# mention that sum of coordinate will cause the value of same key count twice, the product of minus will cause keys with same absolute value
        cost = int(sum([ x*(x-1)/2 for x in horzon_set if x > 1 ]) + sum([x for x in rcross.values()])/2+ sum([x/2 for x in lcross.values()]))
        return cost
        util.raiseNotDefined()

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
