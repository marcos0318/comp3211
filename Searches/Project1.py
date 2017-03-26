#codind:UTF_8


class Vertex:
  #name, nextVertices=["name1:distance1","name2:distance2"]
  def __init__(self,name,nextVertices=[]):
    self.name=name
    self.nextVerticesNames=map(lambda x:x.split(",")[0],nextVertices)
    self.distanceDic={}
    #print "name: "+self.name      
    #print "nextVertices: "
    #print self.nextVerticesNames
    for line in nextVertices:
      name=line.split(",")[0]
      distance=(int)(line.split(",")[1])
      self.distanceDic[name]=distance
    self.heuristic=0

  #def Print(self):
    #print "dic: "
    #print self.distanceDic



class Graph:
  def __init__(self,path):
    #From the path of the file open the graph and store it
    self.path = path
    fh=open(path)
    try:
      allText=fh.read()
    finally:
      fh.close()

    textArray=allText.split("\n")
    self.verticesNumber=(int)(textArray[0])
    self.verticesNames=textArray[1].split(" ")
    self.start=textArray[2].split(":")[1]
    self.goals= textArray[3].split(":")[1].split(",")
    self.verticesDic={}
    for i in range(self.verticesNumber):
      name=textArray[4+i].split(":")[0]
      nextVertices=textArray[4+i].split(":")[1].split(";")
      if nextVertices[0] == "":
        nextVertices=[]
      self.verticesDic[name]=Vertex(name,nextVertices)
      #print self.verticesDic[name]
    if self.verticesNumber*2+4 == len(textArray):
      for i in range(self.verticesNumber):
        name=textArray[4+self.verticesNumber+i].split(":")[0]
        self.verticesDic[name].heuristic=(int)(textArray[4+self.verticesNumber+i].split(":")[1])




#The function that run searches on a graph
def runSearch(graph,algo):
  algo(graph)


def noLoop(n,alist):
  counter=0
  for i in alist:
    if n ==i:
      counter=counter+1
  if counter<4: return True
  else: return False



#These are the algos that are required
#A1, BreadFirstSearch
def BFS(graph):
  fringeCollector=[]
  fringe=[]
  state=graph.start
  fringe.append(state)
  while state not in graph.goals and fringe != []:
    state = fringe[0]
    fringe= fringe[1:]
    nextVertices = sorted(graph.verticesDic[state].nextVerticesNames)
    fringe.extend(nextVertices)
    fringeCollector.append(state)
  print fringeCollector



#A2, Depth Frist Search
def DFS(graph):
  fringeCollector=[]
  fringe=[]
  state=graph.start
  fringe.append(state)
  while state not in graph.goals and fringe != [] and noLoop(state,fringeCollector):
    if not noLoop(state,fringeCollector): break
    state=fringe[0]
    fringe=fringe[1:]
    nextVertices = sorted(graph.verticesDic[state].nextVerticesNames)
    array = nextVertices+fringe
    fringe = array
    fringeCollector.append(state)
  print fringeCollector

#A3, Uniformed Cost search
def UCS(graph):
  fringeCollector=[]
  fringe=[]
  state=[graph.start,0]
  fringe.append(state)
  while state[0] not in graph.goals and fringe != []:
    fringe=sorted(fringe,key=lambda state: state[1])
    state = fringe[0]
    fringe=fringe[1:]
    #pop out
    nextVertices = graph.verticesDic[state[0]].nextVerticesNames
    array=[]
    for name in nextVertices:
      distance=graph.verticesDic[state[0]].distanceDic[name]
      array.append([name, state[1]+distance])
    fringe.extend(array)
    #pop in new items
    fringeCollector.append(state)
    #collect from fringe
  print fringeCollector

#A4, A* tree search 
def AStarTree(graph):
  fringeCollector=[]
  fringe=[]
  state=[graph.start,0,0]
  fringe.append(state)
  while state[0] not in graph.goals and fringe != []:
    fringe=sorted(fringe,key=lambda state: state[2])
    state = fringe[0]
    fringe=fringe[1:]
    #pop out
    nextVertices = graph.verticesDic[state[0]].nextVerticesNames
    array=[]
    for name in nextVertices:
      distance=graph.verticesDic[state[0]].distanceDic[name]
      heuristic=graph.verticesDic[name].heuristic
      array.append([name, state[1]+distance,state[1]+distance+heuristic])
    fringe.extend(array)
    #pop in new items
    fringeCollector.append(state)
    #collect from fringe
  print fringeCollector

#A5, A* graph search 
def AStarGraph(graph):
  fringeCollector=[]
  fringe=[]
  state=[graph.start,0,0]
  fringe.append(state)
  while state[0] not in graph.goals and fringe != []:
    fringe=sorted(fringe,key=lambda state: state[2])
    state = fringe[0]
    fringe=fringe[1:]
    #pop out
    nextVertices = graph.verticesDic[state[0]].nextVerticesNames
    array=[]
    for name in nextVertices:
      distance=graph.verticesDic[state[0]].distanceDic[name]
      heuristic=graph.verticesDic[name].heuristic
      notPopped = 1
      for item in fringeCollector:
        if name == item[0]:
          notPopped = 0
      if notPopped:
        array.append([name, state[1]+distance,state[1]+distance+heuristic])
    fringe.extend(array)
    #pop in new items
    fringeCollector.append(state)
    #collect from fringe
  print fringeCollector





#Load the graphs
graph1=Graph("graph1.txt")
graph2=Graph("graph2.txt")
graph3=Graph("graph3.txt")
graph4=Graph("graph4.txt")
graph5=Graph("graph5.txt")



#dispatches

print "==============================================="
print "BFS"
runSearch(graph1,BFS)
runSearch(graph2,BFS)
runSearch(graph3,BFS)
runSearch(graph4,BFS)
runSearch(graph5,BFS)


print "==============================================="

print "DFS"
runSearch(graph1,DFS)
runSearch(graph2,DFS)
runSearch(graph3,DFS)
runSearch(graph4,DFS)
runSearch(graph5,DFS)


print "==============================================="
print "UCS"
runSearch(graph4,UCS)
runSearch(graph5,UCS)


print "==============================================="
print "A* Tree search"
runSearch(graph4,AStarTree)
runSearch(graph5,AStarTree)
print "==============================================="
print "A* Graph search"
runSearch(graph4,AStarGraph)
runSearch(graph5,AStarGraph)
