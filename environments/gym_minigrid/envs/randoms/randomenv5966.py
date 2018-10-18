
from gym_minigrid.extendedminigrid import *
from gym_minigrid.register import register

import random

class RandomEnv(ExMiniGridEnv):

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=4*size*size,
            # Set this to True for maximum speed
            see_through_walls= not True
        )
        
    def getRooms(self):
        return self.roomList
    
    # Goal is to turn on the light before reaching the goal
    def goal_enabled(self):
        return self.light_on_room() and self.clean_room()
    
    def light_on_room(self):
        for element in self.grid.grid:
            if element is not None and element.type == "lightsw"                     and hasattr(element, 'is_on'):
                return element.is_on
        return False
        
    # Enables the goal only when the room has been completely cleaned
    def clean_room(self):
        nodirt = True
        for element in self.grid.grid:
            if element is not None and element.type == "dirt":
                nodirt = False
        return nodirt
        
    def saveElements(self,room):
        tab=[]
        (x , y) = room.position
        (width , height) = room.size
        for i in range(x , x + width):
            for j in range(y , y + height):
                objType = self.grid.get(i,j)
                if objType is not None:
                    tab.append((i,j,0))
                else:
                    tab.append((i, j, 1))
        return tab
        
    def _random_or_not_position(self, xmin, xmax, ymin, ymax ):
        if False:
            width_pos, height_pos = self._rand_pos( xmin, xmax + 1, ymin, ymax + 1)
        else:
            width_pos = random.randint( xmin, xmax)
            height_pos = random.randint( ymin, ymax)
        return width_pos, height_pos
        
    def _random_number(self, min, max):
        if False:
            return self._rand_int(min,max+1)
        else:
            return random.randint(min,max)
    
    def _random_or_not_bool(self):
        if False:
            return self._rand_bool()
        else:
            return random.choice([True, False])
            
    def _reachable_elements(self, x_agent, y_agent):
        queue = [(x_agent, y_agent)]
        elements = set()
        visited = set()
        dirt_count = 0
        boxes_count = 0

        while len(queue) > 0:
            (x,y) = queue.pop()
            visited.add((x,y))
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for (dx,dy) in directions:
                other_pos = (x+dx,y+dy)
                (ox,oy) = other_pos
                if 0 < ox < self.grid.width and 0 < oy < self.grid.height and other_pos not in visited and other_pos not in queue:
                    if isinstance(self.grid.get(ox,oy), type(None)) or isinstance(self.grid.get(ox,oy), Door)  or isinstance(self.grid.get(ox,oy), Box) or isinstance(self.grid.get(ox,oy), Key) or isinstance(self.grid.get(ox,oy), LockedDoor)  or isinstance(self.grid.get(ox,oy), Dirt):
                        queue.append(other_pos)
                    if isinstance(self.grid.get(ox,oy), LightSwitch) or isinstance(self.grid.get(ox,oy), Door) or isinstance(self.grid.get(ox,oy), Key)  or isinstance(self.grid.get(ox,oy), LockedDoor) or isinstance(self.grid.get(ox,oy), Goal):
                        elements.add(type(self.grid.get(ox,oy)))
                    if isinstance(self.grid.get(ox,oy), Dirt):
                        dirt_count+=1
                    if isinstance(self.grid.get(ox,oy), Box):
                        boxes_count+=1
        return (elements,dirt_count, boxes_count)                
        
    def _valid_free_position(self, x_agent, y_agent, x_bound, y_bound):
        x = random.randint(1, x_bound - 1)
        y = random.randint(1, y_bound - 1)
        while type(self.grid.get(x, y)) != type(None) or (x_agent == x and y_agent ==y):
            x = random.randint(1, x_bound - 1)
            y = random.randint(1, y_bound -1)
        return (x,y)
        
        
    def _place_randomly(self, x_agent, y_agent, n ,Element, color=None):
        water = []
        while n > len(water):        
            (x_water, y_water) = self._valid_free_position(x_agent, y_agent,  self.grid.width - 1, self.grid.height - 1)
            if color != None:
                self.grid.set(x_water, y_water, Element(color))
            else: 
                self.grid.set(x_water, y_water, Element())
            water += [(x_water, y_water)]
        return water 
    
    def _reset_positions(self, water):
        for (x,y) in water:
            self.grid.set(x,y,None)
            
    #Places the agent in a random position within the first room.         
    def _place_agent(self, width_pos, height_pos):
        max_height = self.grid.height
        x_agent = random.randint(1, width_pos)
        y_agent = random.randint(1, max_height)
        while x_agent == width_pos and y_agent == height_pos:
            x_agent = random.randint(1, width_pos)
            y_agent = random.randint(1, max_height)
        self.start_pos = (x_agent, y_agent)
                    
    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Set the random seed to the random token, so we can reproduce the environment
        random.seed("5966")
        
        #Place lightswitch
        width_pos = random.randint(2,30-5) # x position of the light switch (2 tiles space for each room)
        height_pos = random.randint(2,30-2) # y position of light switch (needs space for the wall and door)
        xdoor = width_pos + 1 # x position of the door 
        ydoor = height_pos -1 # y position of the door
        switchRoom = LightSwitch()
        
        # Place the agent
        self.start_dir = random.randint(0,3)
        x_agent = 1
        y_agent = 1
        self.start_pos = (x_agent, y_agent)
        
        # Place a goal square 
        x_goal = width - 2 #random.randint(xdoor + 1, width - 2)
        y_goal = height -2 #random.randint(1,height -2)
        
        #Avoid placing it in front of the door. 
        while x_goal ==  xdoor + 1 and ydoor == y_goal:
            x_goal = random.randint(xdoor + 1, width - 2)
            y_goal = random.randint(1,width -2)            
        
        self.grid.set(x_goal, y_goal , Goal())
        
        #Place the wall
        self.grid.vert_wall(xdoor, 1, height-2)
        
        
        #The number of elements that need to be reachable in the room (Door, Goal, LightSwitch)
        n_elements = 3
        
        if True:        
            self.grid.set(xdoor, ydoor , LockedDoor('yellow'))
            (x_key, y_key) = self._valid_free_position(x_agent, y_agent, xdoor, self.grid.height - 1)
            self.grid.set(x_key, y_key, Key())
            n_elements += 1
        else:
            self.grid.set(xdoor, ydoor ,Door('yellow'))
        
        
        #Add the room
        self.roomList = []
        self.roomList.append(Room(0,(width_pos + 2, height),(0, 0),True))
        self.roomList.append(Room(1,(width - width_pos - 2, height),(width_pos + 2, 0),False))
        self.roomList[1].setEntryDoor((xdoor,ydoor))
        self.roomList[0].setExitDoor((xdoor,ydoor))        
        
        
        #Place the lightswitch
        switchRoom.affectRoom(self.roomList[1])
        switchRoom.setSwitchPos((width_pos,height_pos))
        switchRoom.cur_pos = (width_pos, height_pos)
        
        self.grid.set(width_pos, height_pos, switchRoom)
        self.switchPosition = []
        self.switchPosition.append((width_pos, height_pos))
        
        
        n_water = 2
        n_dirt = 9
        n_boxes = 4
        
        dirt = self._place_randomly(x_agent,y_agent,n_dirt,Dirt)
        
        boxes = self._place_randomly(x_agent,y_agent,n_boxes,Box,'red')

        # Place water
        water = self._place_randomly(x_agent,y_agent,n_water,Water)
        
        (elements, dirt_count, boxes_count) = self._reachable_elements(x_agent,y_agent)
        
        stop = 0
        
        while (len(elements) != n_elements or boxes_count != n_boxes or dirt_count != n_dirt) and stop < 100000:
            self._reset_positions(water)
            self._reset_positions(dirt)
            self._reset_positions(boxes)
            water = self._place_randomly(x_agent,y_agent,n_water,Water)
            dirt = self._place_randomly(x_agent,y_agent,n_dirt,Dirt)
            boxes = self._place_randomly(x_agent,y_agent,n_boxes,Box,'red')
            (elements, dirt_count, boxes_count) = self._reachable_elements(x_agent,y_agent)
            stop += 1
        
        tab = self.saveElements(self.roomList[1])
        switchRoom.elements_in_room(tab)
        switchRoom.elements_in_room(tab)
        
        self.mission = ""

class RandomEnv30x30_5966(RandomEnv):
    def __init__(self):
        super().__init__(size=30)

register(
    id='MiniGrid-RandomEnv-30x30-5966-v0',
    entry_point='gym_minigrid.envs:RandomEnv30x30_5966'
)
