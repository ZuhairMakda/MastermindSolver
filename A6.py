
#Mastermind Solver in Python
import random
Colors = ['red', 'green', 'blue', 'yellow', 'purple', 'white']
allPossiblePegs = [[0,0], [0,1], [0,2], [0,3], [0,4], [1,0], [1,1], [1,2], [1,3], [2,0], [2,1], [2,2], [3,0], [3,1], [4,0]]


#Author: Dr. Emil Sekerinski - Mcmaster Professor for 3bb4 Concurrent systems
#Codemaker was given to us in an assignment, our task was to solve it (Codebreaker given below)
class Codemaker:
    def __init__(self):
        self.secret, self.attempts = {}, 0
    def newGame(self):
        self.attempts = 0 
        self.secret = [random.choice(Colors) for _ in range(4)]
    def guessCode(self, guess):
        if type(guess) != list or len(guess) != 4 or not (set(guess) <= set(Colors)):
            return "invalid guess"
        black = sum(s == g for s, g in zip(self.secret, guess))
        white = sum(min(guess.count(c), self.secret.count(c)) for c in Colors) - black
        self.attempts += 1
        if black == 4:
            del self.secret; return "win"
        if self.attempts == 12:
            del self.secret[username]; return "lose"
        return (black, white)
    def score(self):
        score = self.attempts
        return score

#To defeat the codemaker, the best algorithm to implement is Donald Knuth's five Guess Algorithm
#The best explanation to help me understand this algorithm was given by Nathan Duran in the following link:
# https://github.com/NathanDuran/Mastermind-Five-Guess-Algorithm/blob/master/README.md 
#PLEASE NOTE, I ONLY REFERRED TO THE README DOC FOR AN EXPLANATION OF ALGORITHM
#I also referred to the following link for a stackexchange forum
#https://cs.stackexchange.com/questions/18749/mastermind-board-game-five-guess-algorithm

#Author Zuhair Makda
def codebreaker():
    
    code = Codemaker()
    code.newGame()
    
    pegs = [0,0]
    guess = ['red','red','green','green'] #by Knuth's logic of first guess to be 0011
    
    S = [] #list of all 1296 possible codes
    nextOp = [] #next options
    for codePart1 in Colors:
        for codePart2 in Colors:
            for codePart3 in Colors:
                for codePart4 in Colors:
                    #print([codePart1,codePart2,codePart3,codePart4])
                    S.append([codePart1,codePart2,codePart3,codePart4])
                    nextOp.append([codePart1,codePart2,codePart3,codePart4])                
    while (len(nextOp) >= 1): #pegs != [4,0] and pegs != "win" and pegs != "lose":
        #loop until win or loose
        #print(guess)
        pegs = code.guessCode(guess)
        #print(pegs)
        
        #this list keeps track of what potential codes I can use to solve the hidden code
        potCode = []
        
        #check each option and compare Black/White peg score to eliminate unecessary options
        for option in S:
            optionPegs = codeEvaluator(guess,option)
            
            if optionPegs[0] == pegs[0] and optionPegs[1] == pegs[1]:
                # print(optionPegs)
                potCode.append(option)
        #This list essentially is the updated version for each iteration of my potential candidates to be a solution
        codeList = [code for code in nextOp if code in potCode]
        nextOp = codeList #updates next options
        optionMax = 0 #used to find out which guess to make next, Donald Knuth 5 guess algorithm:
        # find guess "with the smallest max score (hence minmax)." - Nathan Duran (link available above)
        for op1 in nextOp:
            pegList = []
            for op2 in S:
                pegList.append(codeEvaluator(op1,op2))
                
            pegAppear = [0]*15 #keeps track of how many times a possible Black/White count shows up
            #The number of times a certain combination appears helps "Rank" each next guess to figure out the best guess
            #The index of allPossiblePegs corresponds to pegAppear (at the same index keeps track of that particular
            #combo's appearence number)
            
            for item in pegList:
                pos = 0
                for i in range(len(allPossiblePegs)):
                    if allPossiblePegs[i] == item:
                        pos = i
                pegAppear[pos] = pegAppear[pos]+1
            
            minimax = len(S) - max(pegAppear) #scoring system to see how many options it can eliminate
            #used to determine next guess to make (min val with max score. hence minimax)
           # minimax = max(pegAppear)+1
            #once the smallest max score from all options is found, this option is the best next guess
            if minimax > optionMax:
                optionMax = minimax
                guess = op1
    #I know this is not good form for coding, but Knuth's Algorithm will
    #ALWAYS win :)
    print("Codemaker Defeated in " + str(code.score()) + " guesses!")
    print("The code was:" + str(guess))            
    print("You " + pegs + "!")

#the following function returns black/white peg score with assumption "option" is the solution and "guess" is the attempt
#Used in the 5 guess algorithm by Knuth to eliminate certain options from all possible options
#copied from codemaker above
def codeEvaluator(guess, option):
    black = sum(s == g for s, g in zip(option, guess))
    white = sum(min(guess.count(c), option.count(c)) for c in Colors) - black
    return [black,white]




codebreaker()

