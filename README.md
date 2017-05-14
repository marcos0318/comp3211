COMP3211 Final Project

Project name: Pacman contest

Project group members: Bai Jiaxin, Yang Shaohui, Kyuhong Lee

Programming language: python 2.7

Configuration steps:

```
1\. install python 2.7 on your computer.
2\. unzip the file "FinalProject_pacman_contest.zip". Open command line tools such as terminal and cd to the directory of the files.
3\. Or alternatively, you can use the command "git clone https://github.com/syangav/COMP3211FinalProject.git" to a new directory and cd to that directory.
4\. run the command "python capture.py -r myteam -b baselineTeam". The game demo will automatically begin. Red team uses the agents we implemented and blue team uses agents the Berkeley team implemented.
```

Other statements:

```
1\. Our team's work are all stored in the file myTeam.py. Others all come from http://ai.berkeley.edu/contest.html.
2\. We create two classes derived from CaptureAgent class, PlanningCaptureAgent and FinalPlanningAgent. All functions are inside the class implementation.
```

Innovative points:

```
1\. Add 4-depth Adversarial search with pruning
2\. Distribute foods to offensive agents
3\. Flexible change of attitude according to game development, i.e. the agent can become offensive or defensive by judging the game situation
4\. Evaluate go-home condition
```
