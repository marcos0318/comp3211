This is the first project of COMP3211. The implementattion of several searches on graphes.
The inputs are graphs, represented as adjacency lists, including the weighted ones and not weighted.

The project is writen in python currently

The input format: adjacency list

4 			       //The number total vertices
A B C D        //The names of the lines
start:A
goal:D
A:A,3;C,1     //The ajacency vertices lists and their weights of the edges,if there is no weight, then that means by default it is 1 
B:A,3;B,1
C:D,1
D:
A:3 		       //The heuristic function value of those verices
B:2
C:1
D:0  		
