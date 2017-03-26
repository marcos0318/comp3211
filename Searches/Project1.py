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
    self.start=textArray[2].split(":")[1].split(",")
    self.goal= textArray[3].split(":")[1].split(",")
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









graph1=Graph("graph1.txt")
graph2=Graph("graph2.txt")
graph3=Graph("graph3.txt")
graph4=Graph("graph4.txt")
graph5=Graph("graph5.txt")














