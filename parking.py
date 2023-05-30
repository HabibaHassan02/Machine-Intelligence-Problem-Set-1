from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        st=list(state)
        size=len(st)
        x=0
        for i,car in enumerate(st):  #loop over the atate and the slot, if very car is in its slot then the goal has been achived
            for key,val in self.slots.items():
                if val==i:
                    if car==key:
                        x=x+1
        if x==size:
            return True
        else:
            return False



    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        li=[]
        for car,pos in enumerate(state):
            right=Point(1,0)
            up=Point(0,-1)
            left=Point(-1,0)
            down=Point(0,1)
            temp=pos.__add__(right) #the action is right on the current state
            if temp in self.passages and not temp in state:
                tup=(car,'R')
                li.append(tup)
            temp=pos.__add__(up)  #the action is up on the current state
            if temp in self.passages and not temp in state:
                tup=(car,'U')
                li.append(tup)
            temp=pos.__add__(left) #the action is left on the current state
            if temp in self.passages and not temp in state:
                tup=(car,'L')
                li.append(tup)
            temp=pos.__add__(down)  #the action is down on the current state
            if temp in self.passages and not temp in state:
                tup=(car,'D')
                li.append(tup)
        return li
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        mod_state=state[action[0]] #get the state of the car i== action[0] where action=(i,act)// state[i]=point this point is the position of car i
        mod_state=mod_state+action[1].to_vector() #add the action to it
        stli=list(state)  #cast the state from tuple to list
        stli[action[0]]=mod_state #modify the state list with the new state added
        rettup=tuple(stli) #return the state to tuple
        return rettup

    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        ac=list(action)
        temp=state[ac[0]]
        temp=temp.__add__(ac[1].to_vector())  #change the state to the given action
        car=ac[0]
        point=temp
        cost=0
        if point not in self.slots.keys():  #if the point of the new state id not one of those in slots then the cost is normally 1 
            cost=1
            return cost
        for pos,carslot in self.slots.items(): 
            if pos==point: #if the point is found in slots
                if car==carslot:  #and this point is the correct slot for this car
                    cost=1  #then teh cost is 1
                else:
                    cost=101  #if it is a slot of another car then the cost is 101, 100 for wrong slot and 1 for action
        return cost
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
