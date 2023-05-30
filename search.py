from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils
from queue import Queue
from queue import PriorityQueue
from heapq import *
from itertools import count

#TODO: Import any modules you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    sdic=dict() #the dictionary that I am going to save the pointers to parent node eg: 'child node':'parent node'
    dundic=dict()
    dung=0
    Solution=[] #list of last solution
    s=[] #stack used to save the final path in reverse, before poping it in the solution list
    if problem.is_goal(initial_state): #if the initial node is the goal, then add it to Solution and FINISH
        Solution.append(initial_state)
        return Solution
    frontier=[]
    frontier.append(initial_state)
    explored=[]
    while len(frontier)>0: #as long as the frontier contains elements then do the logic
        actions=[]
        node=frontier.pop(0)   #get the node that its turn to work on from the frontier
        explored.append(node)  #add the same node to explored list to prevent from visiting it again later
        actions=problem.get_actions(node) #get the node's children/actions
        for i in range(len(actions)):   #loop over these actions
            act=actions[i]            #get one action
            child=problem.get_successor(node,act)
            if not (child in explored or child in frontier): #if this child is not in the frontier or the explored list then work on it
                if act!=child:
                    tup=(act,node)
                    dundic[child]=tup
                    dung=1
                else:
                    sdic[child]=node #add to the dictionary 'child':'parent node'
                if problem.is_goal(child): #if the child is the goal then 
                    if dung==0:
                       s.append(list(sdic)[-1])  #add the goal (which is the last key added to the dictionary) to the stack
                       s.append(sdic[list(sdic)[-1]]) #add the item of the key (parent node of the goal) to the stack
                       nt=sdic[list(sdic)[-1]]  #get the item of the key(parent node of the goal) to work on and get all previous nodes 
                       while nt!=initial_state: #as long as the variable that holdes the parent node has not reached the root do:
                           s.append(sdic[nt])  #add to the stack the previous parent node
                           nt=sdic[nt]         #change the nt variable to hold the previous parent node
                       s.pop()                 #remove the initial state from the stack
                       for k in range(len(s)):
                          Solution.append(s.pop())   #add the path in its correct od=rder to the Solution
                       return Solution                #FINISH
                    else:
                       rettup=dundic[list(dundic)[-1]]
                       s.append(rettup[0])  #add the goal (which is the last key added to the dictionary) to the stack
                       nt=rettup[1]  #get the item of the key(parent node of the goal) to work on and get all previous nodes 
                       while nt!=initial_state: #as long as the variable that holdes the parent node has not reached the root do:
                           dum=dundic[nt]
                           s.append(dum[0])  #add to the stack the previous parent node
                           nt=dum[1]         #change the nt variable to hold the previous parent node
                       for k in range(len(s)):
                          Solution.append(s.pop())   #add the path in its correct od=rder to the Solution
                       return Solution                #FINISH
                else:
                    frontier.append(child)         #if it is not the goal add it to the frontier
    else:
         return None #if the frontier is empty then there is no answer so return Nne and FINISH


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    frontier=[]  #stack
    Solution=[]
    sdic=dict() 
    dungdic=dict()  #dict used to track the actions of the dungeon  child:(action,node)
    dung=0
    s=[]    #a stack that saves the solution in reverse
    explored=[]
    actions=[]
    frontier.append(initial_state)  #push the initial state
    while len(frontier)>0:   
        node=frontier.pop()     #pop the last state entered the frontier
        if not node in explored:  #if it is not explored before then check on it
         if problem.is_goal(node):  #is this node the goal?
            if node==initial_state:  #if it is the initial state then return this node only
                Solution.append(node)
                return Solution
            else:
              if dung==0:              #if it is not the initial state and it is not the dungeon
                  for key,val in sdic.items():
                      if key==node: #find the dict item that its key is the goal node
                         break
                  s.append(key)  #add the goal (which is the last key added to the dictionary) to the stack
                  s.append(sdic[key]) #add the item of the key (parent node of the goal) to the stack
                  nt=sdic[key]  #get the item of the key(parent node of the goal) to work on and get all previous nodes 
                  while nt!=initial_state: #as long as the variable that holdes the parent node has not reached the root do:
                     s.append(sdic[nt])  #add to the stack the previous parent node
                     nt=sdic[nt]         #change the nt variable to hold the previous parent node
                  s.pop()                 #remove the initial state from the stack
                  for k in range(len(s)):
                     Solution.append(s.pop())   #add the path in its correct od=rder to the Solution
                  return Solution                #FINISH
              else:             #if it is not the initial state and it is dungeon
                for key,val in dungdic.items():
                      if key==node:
                         break
                rettup=dungdic[key]  #return the tuple(action,node)
                s.append(rettup[0]) #save the last action taken 
                nt=rettup[1]        #save the node in a variable to keep track of it
                while nt!=initial_state:
                    dum=dungdic[nt]   #save a dummy tuple
                    s.append(dum[0])  #append the action in the tuple
                    nt=dum[1]
                for k in range(len(s)):
                    Solution.append(s.pop())  #pop the solution from s to Solution to be in its right sequence
                return Solution
         else:
            if not node in explored: #if the popped node is not the goal and it is not in the explored
                explored.append(node)  #append it in the explored set
                actions=problem.get_actions(node)  #get its list of actions
                for act in actions:   #loop over actions
                    child=problem.get_successor(node,act)  #get the successor 
                    if not child in explored:  #if this successor is not explored before
                        if act!=child:  #if the act is different from the child then it is dungeon 
                          t1=(act,node)
                          dungdic[child]=t1   #save these info in the dict
                          dung=1              #turn the flag true to know then that it is dungeon 
                        else:  #it is graph search
                          sdic[child]=node
                        frontier.append(child)  #either it is dungeon or graph, push the child in the fromtier
    else:
        return None  #if the frontier is empty return none
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    frontier=[]  #priority queue
    Solution=[]
    sdic=dict()
    dungdic=dict()
    dung=0
    s=[]
    unique=count()  #a count used to differentiate between nodes of the same count, to keep the priority queue stable,those of same priority the first entered is the first in the queue
    heappush(frontier,(0,next(unique),initial_state))  #enter the first tuple in the frontier, heappush makes the list priority queue
    explored=[]
    actions=[]
    while len(frontier)>0:
        node=heappop(frontier)  #get the node of the least priority in the queue. np: node=(cost,unique num,state)
        if problem.is_goal(node[2]):  #node[2] is the state
            if node[2]==initial_state:
                Solution.append(node[2])
            else:
             if dung==0:
                for key,val in sdic.items():
                    if key==node[2]:
                        break
                s.append(key)  #add the goal (which is the last key added to the dictionary) to the stack
                s.append(sdic[key]) #add the item of the key (parent node of the goal) to the stack
                nt=sdic[key]  #get the item of the key(parent node of the goal) to work on and get all previous nodes 
                while nt!=initial_state: #as long as the variable that holdes the parent node has not reached the root do:
                    s.append(sdic[nt])  #add to the stack the previous parent node
                    nt=sdic[nt]         #change the nt variable to hold the previous parent node
                s.pop()                 #remove the initial state from the stack
                for k in range(len(s)):
                    Solution.append(s.pop())   #add the path in its correct od=rder to the Solution
                return Solution
             else:
                for key,val in dungdic.items():
                      if key==node[2]:
                         break
                rettup=dungdic[key]
                s.append(rettup[0])
                nt=rettup[1]
                while nt!=initial_state:
                    dum=dungdic[nt]
                    s.append(dum[0])
                    nt=dum[1]
                for k in range(len(s)):
                    Solution.append(s.pop())
                return Solution
        else:
            explored.append(node)
            actions=problem.get_actions(node[2])
            for act in actions:
                child=problem.get_successor(node[2],act)
                x=0
                k=0
                for temp in frontier: #loop to check if the child in the frontier or not
                    if temp[2]==child:
                        x=1   #if in frontier -> change the flag
                        break
                for temp2 in explored:
                    if temp2[2]==child:
                        k=1
                        break
                if k==0 and x==0:  #if it is not the frontier nor in the explored
                    cost=problem.get_cost(node[2],act)  #get the cost of this action
                    tcost=node[0]+cost  #add it to the previous cost
                    tup=(tcost,next(unique),child)
                    heappush(frontier,tup)  
                    if act!=child:  #if it is dungeon
                        t1=(act,node[2])
                        dungdic[child]=t1
                        dung=1
                    else:
                        sdic[child]=node[2]
                elif x==1:  #if it is not explored but in the frontier check if its cost< the cost of the same node in the frontier or not
                    cost=problem.get_cost(node[2],act)
                    tcost=node[0]+cost
                    for data in frontier:
                        if data[2]==child and data[0]>tcost:
                            if act!=child:
                               t1=(act,node[2])
                               dungdic[child]=t1
                               dung=1
                            else:
                               sdic[child]=node[2]
                            tup=(tcost,data[1],child)
                            heappop(frontier)
                            heappush(frontier,tup)
    else:
        return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    frontier=[]
    Solution=[]
    sdic=dict()
    dungdic=dict()
    dung=0
    s=[]
    unique=count()
    heappush(frontier,(heuristic(problem,initial_state),next(unique),initial_state))  #like the uniform cost, the diff is that here is the heuristic instead of the cost
    explored=[]
    actions=[]
    while len(frontier)>0:
        node=heappop(frontier)
        if problem.is_goal(node[2]):
            if node[2]==initial_state:
                Solution.append(node[2])
            else:
             if dung==0:
                for key,val in sdic.items():
                    if key==node[2]:
                        break
                s.append(key)  #add the goal (which is the last key added to the dictionary) to the stack
                s.append(sdic[key]) #add the item of the key (parent node of the goal) to the stack
                nt=sdic[key]  #get the item of the key(parent node of the goal) to work on and get all previous nodes 
                while nt!=initial_state: #as long as the variable that holdes the parent node has not reached the root do:
                    s.append(sdic[nt])  #add to the stack the previous parent node
                    nt=sdic[nt]         #change the nt variable to hold the previous parent node
                s.pop()                 #remove the initial state from the stack
                for k in range(len(s)):
                    Solution.append(s.pop())   #add the path in its correct od=rder to the Solution
                return Solution
             else:
                for key,val in dungdic.items():
                      if key==node[2]:
                         break
                rettup=dungdic[key]
                s.append(rettup[0])
                nt=rettup[1]
                while nt!=initial_state:
                    dum=dungdic[nt]
                    s.append(dum[0])
                    nt=dum[1]
                for k in range(len(s)):
                    Solution.append(s.pop())
                return Solution
        else:
            explored.append(node)
            actions=problem.get_actions(node[2])
            for act in actions:
                child=problem.get_successor(node[2],act)
                x=0
                k=0
                for temp in frontier:
                    if temp[2]==child:
                        x=1
                        break
                for temp2 in explored:
                    if temp2[2]==child:
                        k=1
                        break
                if k==0 and x==0:
                    cost=problem.get_cost(node[2],act)
                    tcost=node[0]-heuristic(problem,node[2])+cost #remove from the previous g(n) the heuristic of the previous node to get the cummulative cost only and add the current cost to it 
                    gn=tcost+heuristic(problem,child) #add the heuristic to the cumulative cost to get the new g(n)
                    tup=(gn,next(unique),child)
                    heappush(frontier,tup)
                    if act!=child:
                        t1=(act,node[2])
                        dungdic[child]=t1
                        dung=1
                    else:
                        sdic[child]=node[2]
                elif x==1:
                    cost=problem.get_cost(node[2],act)
                    tcost=node[0]+cost
                    gn=tcost+heuristic(problem,child)
                    for data in frontier:
                        if data[2]==child and data[0]>gn:
                            if act!=child:
                               t1=(act,node[2])
                               dungdic[child]=t1
                               dung=1
                            else:
                               sdic[child]=node[2]
                            tup=(gn,data[1],child)
                            heappop(frontier)
                            heappush(frontier,tup)
    else:
        return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    frontier=[]
    Solution=[]
    sdic=dict()
    dungdic=dict()
    dung=0
    s=[]
    unique=count()
    heappush(frontier,(heuristic(problem,initial_state),next(unique),initial_state))
    explored=[]
    actions=[]
    while len(frontier)>0:
        node=heappop(frontier)
        if problem.is_goal(node[2]):
            if node[2]==initial_state:
                Solution.append(node[2])
            else:
             if dung==0:
                for key,val in sdic.items():
                    if key==node[2]:
                        break
                s.append(key)  #add the goal (which is the last key added to the dictionary) to the stack
                s.append(sdic[key]) #add the item of the key (parent node of the goal) to the stack
                nt=sdic[key]  #get the item of the key(parent node of the goal) to work on and get all previous nodes 
                while nt!=initial_state: #as long as the variable that holdes the parent node has not reached the root do:
                    s.append(sdic[nt])  #add to the stack the previous parent node
                    nt=sdic[nt]         #change the nt variable to hold the previous parent node
                s.pop()                 #remove the initial state from the stack
                for k in range(len(s)):
                    Solution.append(s.pop())   #add the path in its correct od=rder to the Solution
                return Solution
             else:
                for key,val in dungdic.items():
                      if key==node[2]:
                         break
                rettup=dungdic[key]
                s.append(rettup[0])
                nt=rettup[1]
                while nt!=initial_state:
                    dum=dungdic[nt]
                    s.append(dum[0])
                    nt=dum[1]
                for k in range(len(s)):
                    Solution.append(s.pop())
                return Solution
        else:
            explored.append(node)
            actions=problem.get_actions(node[2])
            for act in actions:
                child=problem.get_successor(node[2],act)
                x=0
                k=0
                for temp in frontier:
                    if temp[2]==child:
                        x=1
                        break
                for temp2 in explored:
                    if temp2[2]==child:
                        k=1
                        break
                if k==0 and x==0:
                    heur=heuristic(problem,child)
                    tup=(heur,next(unique),child)
                    heappush(frontier,tup)
                    if act!=child:
                        t1=(act,node[2])
                        dungdic[child]=t1
                        dung=1
                    else:
                        sdic[child]=node[2]
    else:
        return None