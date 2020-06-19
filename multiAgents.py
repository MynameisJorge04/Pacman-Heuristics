# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from argparse import Action
from random import random
from test.support import temp_cwd

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

        distance_to_food = None
        distance_to_ghost = None

        #Make the successorGameState usable
        state_rows = str(successorGameState).split("\n")
        state_rows = state_rows[:-2]        #The last two elements are always the score and then a blank
        height = len(state_rows)
        width = len(state_rows[0])

        #Get all food and ghosts
        food = []
        ghosts = successorGameState.getGhostPositions()
        for i in reversed(range(0, height)):
            for j in reversed(range(0, width)):
                if(successorGameState.hasFood(j, i)):
                    food.append((j, i))


        #Find the closest food and closest ghost
        for pip in food:
            if(distance_to_food == None or manhattanDistance(pip, newPos) < distance_to_food):
                distance_to_food = manhattanDistance(pip, newPos)

        for ghost in ghosts:
            if(distance_to_ghost == None or manhattanDistance(ghost, newPos) < distance_to_ghost):
                distance_to_ghost = manhattanDistance(ghost, newPos)

        #Find if pacman is more safe with this choice
        more_safe = False
        for i in range(0, len(oldScaredTimes)):
            if(newScaredTimes[i] > oldScaredTimes[i]):
                more_safe = True

        #more_safe == true iff pacman could pick up a powerup, so he always should
        if(more_safe):
            return 1000

        #Find if pacman is invincible
        invincible = True
        for time in newScaredTimes:
            if(time == 0):
                invincible = False

        if(distance_to_food != None):
            if(distance_to_ghost != None and invincible):
                return successorGameState.getScore() - distance_to_food
            else:
                return successorGameState.getScore() - distance_to_food + distance_to_ghost * 1.1
        else:
            return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
          ## find the most valuable successor        
        choice = recursiveTree(self.evaluationFunction,self.depth,0,gameState)
        print(gameState,choice)
        return choice[1]
       
        
def recursiveTree (evaluationFunction, depth, agentNum, gameState):
    if(depth == 0 or gameState.isWin() or gameState.isLose()):
        return (evaluationFunction(gameState), Directions.STOP)
   
    
    
    newAgent = agentNum + 1
    if(newAgent >= gameState.getNumAgents()):
       newAgent = 0
       depth -= 1
       
    successors = []
    moves = gameState.getLegalActions(agentNum)
    for move in moves:
        # stores the game states of successors
        successors.append((gameState.generateSuccessor(agentNum, move), move))
    
    successorVals = []
    for successor in successors:
        successorState = successor[0]
        successorMove = successor[1]
        successorVals.append((recursiveTree (evaluationFunction, depth, newAgent, successorState), successorMove)) 
    
   
    
    if (agentNum == 0):
        # # then max
        max = None
        for val in successorVals:
            if (max == None or max < val[0][0]):
                max = val [0][0]
                direction = val [1]
                
        return (max, direction)
    else:
        min = None
        direction = None
        for val in successorVals:
            if (min == None or min > val[0][0]):
                min = val[0][0]
                direction = val[1]
        # #then min
        return (min, direction)

        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
       
        
        choice = ABTree(self.evaluationFunction,self.depth,0,gameState,-NEXT_TO_INF,NEXT_TO_INF)
        return choice[1]
    
NEXT_TO_INF = 9999999999

def ABTree(evaluationFunction, depth, agentNum, gameState, alpha, beta):
    #If we're as deep as we can go, get eval function
    if(depth == 0 or gameState.isWin() or gameState.isLose()):
        return (evaluationFunction(gameState), None)

    #Update the agentNum and depth for our successors
    new_agent_num = agentNum + 1
    if(new_agent_num >= gameState.getNumAgents()):
        new_agent_num = 0
        depth -= 1

    #Get list of lega moves
    legalMoves = gameState.getLegalActions(agentNum)

    #Return min or max of the child nodes and the direction we'll take to get there
    #Also, update alpha and beta
    if(agentNum == 0):      #We're pacman
        maximum = None
        max_direction = None
        for move in legalMoves:

            successor = gameState.generateSuccessor(agentNum, move)
            successor_value = ABTree(evaluationFunction, depth, new_agent_num, successor, alpha, beta)

            if(maximum == None or maximum < successor_value[0]):
                maximum = successor_value[0]
                max_direction = move

            if(maximum > beta):
                return (maximum, move, alpha, beta)

            alpha = max(alpha, maximum)

        return (maximum, max_direction, alpha, beta)
    else:                   #We're ghosts
        minimum = None
        min_direction = None
        for move in legalMoves:
            successor = gameState.generateSuccessor(agentNum, move)
            successor_value = ABTree(evaluationFunction, depth, new_agent_num, successor, alpha, beta)

            if(minimum == None or minimum > successor_value[0]):
                minimum = successor_value[0]
                min_direction = move

            if(minimum < alpha):
                return (minimum, move, alpha, beta)

            beta = min(beta, minimum)

        return (minimum, min_direction, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        choice = expectiTree(self.evaluationFunction,self.depth,0,gameState)
        return choice[1]
    
NEXT_TO_INF = 9999999999

def expectiTree(evaluationFunction, depth, agentNum, gameState):
    if(depth == 0 or gameState.isWin() or gameState.isLose()):
        return (evaluationFunction(gameState), Directions.STOP)
   
    
    
    newAgent = agentNum + 1
    if(newAgent >= gameState.getNumAgents()):
       newAgent = 0
       depth -= 1
       
    successors = []
    moves = gameState.getLegalActions(agentNum)
    for move in moves:
        # stores the game states of successors
        successors.append((gameState.generateSuccessor(agentNum, move), move))
    
    successorVals = []
    for successor in successors:
        successorState = successor[0]
        successorMove = successor[1]
        successorVals.append((expectiTree (evaluationFunction, depth, newAgent, successorState), successorMove)) 
    
    
    if (agentNum == 0):
        # # then max
        maximum = None
        direction = None
        for val in successorVals:
            if (maximum == None or maximum < val[0][0]):
                maximum = val [0][0]
                direction = val [1]
                
        return (maximum, direction)
    else:                   #We're ghosts
        maximum = None
        max_direction = None
        for val in successorVals:
            p= 1.0/float(len(successorVals))
            temp = p*val[0][0]
            
            if (maximum == None or maximum <temp):
                maximum = temp
                max_direction = val[1]

        return (maximum, max_direction)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction