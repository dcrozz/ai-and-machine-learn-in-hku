from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = successorGameState.getScore()

        WEIGHT_GHOST = 10.0
        WEIGHT_FOOD = 10.0

        disToFood = [manhattanDistance(newPos, x) for x in newFood.asList()]
        if len(disToFood):
            score += WEIGHT_FOOD / min(disToFood)

        disToGhost = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if disToGhost > 0:
            score -= WEIGHT_GHOST / disToGhost

        return score 

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

    def isTerminal(self, state, depth, agent):
        """check the terminal state"""

        return state.isWin() or state.isLose() or state.getLegalActions(agent) == [] or depth == self.depth

    def isPacman(self, state, agent):
        """check whether it is pacman"""

        return agent % state.getNumAgents() == 0

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
        def minimax(state, depth, agent):
            #when all the agent has moved, goto the next depth
            if agent == state.getNumAgents():
                return minimax(state, depth+1, 0)

            if self.isTerminal(state, depth, agent):
                return self.evaluationFunction(state)
            #the minimax value of the next agent
            successors = (
                minimax(state.generateSuccessor(agent, action), depth, agent + 1)
                for action in state.getLegalActions(agent)
            )
            return (max if self.isPacman(state, agent) else min)(successors)

        return max(gameState.getLegalActions(0),
                  key = lambda x: minimax(gameState.generateSuccessor(0, x), 0, 1)
                  )

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        alpha = float("-inf")
        beta = float("inf")
 
        def maxValue(state, depth, agent=0, alpha=float("-inf"), beta=float("inf")):
            if self.isTerminal(state, depth, 0):
                return self.evaluationFunction(state)
            v = float("-inf")
            for action in state.getLegalActions(0):
                v = max(v, minValue(state.generateSuccessor(0, action), 1, depth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v  

        def minValue(state, agent, depth, alpha=float("-inf"), beta=float("inf")):
            if self.isTerminal(state, depth, agent):
                return self.evaluationFunction(state)
            v = float("inf")
            if agent == gameState.getNumAgents() - 1:
                for action in state.getLegalActions(agent):
                    v = min(v, maxValue(state.generateSuccessor(agent, action), depth+1, agent,  alpha, beta))
                    if v < alpha: return v
                    beta = min(beta, v)
                return v
            else:
                for action in state.getLegalActions(agent):
                    v = min(v, minValue(state.generateSuccessor(agent, action), agent+1, depth, alpha, beta))
                    if v < alpha: return v
                    beta = min(beta, v)
                return v
        # Start with pacman: 
        v = float("-inf")
        for action in gameState.getLegalActions(0):
            nextValue = minValue(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if nextValue > v:
                v = nextValue
                nextAction = action
            alpha = max(alpha, v)
 
        return nextAction

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
        def expectimax(state, depth, agent):
            if agent == state.getNumAgents():
                return expectimax(state, depth+1, 0)

            if self.isTerminal(state, depth, agent):
                return self.evaluationFunction(state)
            #the expectimax value of the next agent
            successors = (
                expectimax(state.generateSuccessor(agent, action), depth, agent + 1)
                for action in state.getLegalActions(agent)
            )

            def avg(successors):
                """get the avg value of successors"""
                toList = list(successors)
                return sum(toList) / len(toList)

            return (max if self.isPacman(state, agent) else avg)(successors)

        return max(gameState.getLegalActions(0),
                   key = lambda x: expectimax(gameState.generateSuccessor(0, x), 0, 1)
                  )

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    curFood = currentGameState.getFood()
    curPos = currentGameState.getPacmanPosition()
    curGhostStates = currentGameState.getGhostStates()

    WEIGHT_GHOST = 10.0
    WEIGHT_FOOD = 10.0
    WEIGHT_SCAR = 100.0

    score = currentGameState.getScore()

    disToFood = [manhattanDistance(curPos, x) for x in curFood.asList()]
    if len(disToFood):
        score += WEIGHT_FOOD / min(disToFood)

    for ghost in curGhostStates:
        disToGhost = manhattanDistance(curPos, ghost.getPosition())
        if disToGhost > 0:
            if ghost.scaredTimer > 0:
                score += WEIGHT_SCAR / disToGhost
            else:
                score -= WEIGHT_GHOST / disToGhost

    return score

# Abbreviation
better = betterEvaluationFunction

