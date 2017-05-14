#Example modifying





# myTeam.py
# ---------
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


#This team is produced by Mark Bai Jiaxin
#One part of the comp3211 project


from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensivePlanningAgent', second = 'OffensivePlanningAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########
#the Planning Cpature is from baseline team.
#the baseline team is not very good. And I am going to fix it
class PlanningCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    print "choice actions: "
    for i in range (0,len(actions)):
      print actions[i]
      print values[i]
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.getFood(gameState).asList())

    #if ((foodLeft == 5 and self.getScore(gameState) != 5 )or (foodLeft == 10 and self.getScore(gameState) != 10 )or (foodLeft == 15 and self.getScore(gameState) != 15) or foodLeft <= 2):
    if gameState.getAgentState(self.index).numCarrying > 3 or foodLeft <=2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def getSuccessorByIndex(self, gameState, index, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(index, action)
    pos = successor.getAgentState(index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(index, action)
    else:
      return successor

  def evaluate(self, gameState, action):

    successor = self.getSuccessor(gameState, action)


    """
    Computes a linear combination of features and feature weights
    """
    value = self.value(successor, 4, 0)

    return value

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

  #TODO:
  #first for the attacking agent
  def evaluateCurrentState(self, gameState):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getCurrentFeatures(gameState)
    weights = self.getCurrentWeights(gameState)
    return features * weights

  def getCurrentFeatures(self, gameState):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    features['successorScore'] = self.getScore(gameState)
    return features

  def getCurrentWeights(self, gameState):
    return {'successorScore': 1.0}

  def value(self, gameState, depth, isMax = 0, a = -999999, b = 999999):
    if depth == 0:
      return  self.evaluateCurrentState(gameState)

    if isMax:
      return self.max_value(gameState, depth-1, 1-isMax, a, b)
    else:
      return self.min_value(gameState, depth-1, 1-isMax, a, b)

  def max_value(self, gameState, depth, isMax, a , b):
    v = -99999999
    actions = gameState.getLegalActions(self.index)
    for action in actions:
      successor = self.getSuccessor(gameState, action)
      v = max(v, self.value(successor, depth, isMax, a, b))
      if v >= b:
        return v
        a = max(a,v)
    return v

  def min_value(self, gameState, depth, isMax, a, b):
    v = 99999999
    #get successors to the secondSuccessros
    opponentList = self.getOpponents(gameState)


    if gameState.getAgentPosition(opponentList[0]) != None and gameState.getAgentPosition(opponentList[1]) !=None:
      successors = []
      secondSuccessors = []
      actions = gameState.getLegalActions(opponentList[0])
      for action in actions:
        successors.append(self.getSuccessorByIndex(gameState, opponentList[0], action))
      for state in successors:
        actions = state.getLegalActions(opponentList[1])
        for action in actions:
          secondSuccessors.append(self.getSuccessorByIndex(state, opponentList[1], action))

      for successor in secondSuccessors:
        v = min(v, self.value(successor, depth, isMax, a, b))
        if v <= a:
          return v
          b = min(b, v)
      return v

    if gameState.getAgentPosition(opponentList[0]) != None:
      actions = gameState.getLegalActions(opponentList[0])
      for action in actions:
        successor = self.getSuccessorByIndex(gameState, opponentList[0] ,action)
        v = min(v, self.value(successor, depth, isMax, a, b))
        if v <= a:
          return v
          b = min(b, v)
      return v

    if gameState.getAgentPosition(opponentList[1]) != None:
      actions = gameState.getLegalActions(opponentList[1])
      for action in actions:
        successor = self.getSuccessorByIndex(gameState, opponentList[1] ,action)
        v = min(v, self.value(successor, depth, isMax,a ,b))
        if v <= a:
          return v
          b = min(b, v)
      return v




    v = min(v, self.value(gameState, depth, isMax))
    if v <= a:
      return v
      b = min(b, v)
    return v



class OffensivePlanningAgent(PlanningCaptureAgent):
  """
  This agent consider getting food and also be aware of other ememy
  that can eat him
  """


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}


  #def getWeights(self, gameState, action):
   # return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    foodList = self.getFoodYouAreDefending(gameState).asList()

    if len(foodList) > 17:
      successor = self.getSuccessor(gameState, action)
      value = self.value(successor, 4, 0)
      return value
    elif len(foodList) > 10:
      if self.index < 2:
        successor = self.getSuccessor(gameState, action)
        value = self.value(successor, 4, 0)
        return value
      else:
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights
    else:
      features = self.getFeatures(gameState, action)
      weights = self.getWeights(gameState, action)
      return features * weights

#methods may be used
  #getAgentState(self, index) return the agent state
  # gameState.getAgentPosition(index)
  #use gameState.getAgentState(index).isPacman to check
  #AgentState.scaredTimer <= 0: means the ghost is not scared

  #def getWeights(self, gameState, action):
  #  return {'successorScore': 100, 'distanceToFood': -1, 'isNearDangerGhost': -10000}


  def getCurrentFeatures(self, gameState):
    features = util.Counter()

    #sucessor is another gameState object of the next moment with a certain
    #action
    foodList = self.getFood(gameState).asList()
    foodList1 = []
    foodList2 = []
    for food in foodList:
      if food[1] <= 2:
        foodList1.append(food)
      elif food[1]>10:
        foodList2.append(food)

    features['gameStateScore'] = -len(foodList)#self.getScore(gameState)

    # Compute distance to the nearest food

    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = gameState.getAgentState(self.index).getPosition()
      if self.index < 2:
        if len(foodList1) > 0:
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList1])
        else:
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      else:
        if len(foodList2) > 0:
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList2])
        else:
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance


    opponentList = self.getOpponents(gameState)
    dangerGhostList = []
    #print opponentList
    for opponent in opponentList:
      #check whether the opponent is a pacman
      #print gameState.getAgentState(opponent).isPacman
      if gameState.getAgentState(opponent).isPacman:
        continue
      #check whether the ghost is scared
      #print gameState.getAgentState(opponent).scaredTimer > 0
      if gameState.getAgentState(opponent).scaredTimer > 0:
        continue
      #check the distance of the agents
      opponentPos = gameState.getAgentState(opponent).getPosition()
      myPos = gameState.getAgentState(self.index).getPosition()
      if opponentPos != None:
        if self.getMazeDistance(myPos, opponentPos) > 1:
          continue
      else:
        continue
      dangerGhostList.append(opponent)
    if len(dangerGhostList) > 0:
      features['isNearDangerGhost'] = 1
    else:
      features['isNearDangerGhost'] = 0

    return features




  def getCurrentWeights(self, gameState):
    return {'gameStateScore': 100, 'distanceToFood': -1, 'isNearDangerGhost': -1000}






class DefensivePlanningAgent(PlanningCaptureAgent):


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights
