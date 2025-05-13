#player comands I'd like to make. 
''' 
invintory, equipment, stats, north, east, south, west, look around. #conditional: insight.
'''

# map
''' 3x3
Foyer (number 8), Study, Ballroom, Conservatory, Billiard Room, Library, Lounge, Dining Room, and Kitchen. 
'''
position = 1
print("You wake up and compose yourself")

#Game
win = False
while win == False:
    "Commands: "
    "You are in an open "
    movment = input()
    movment = movment.lower()
    if movment == "north" or "n":
        if position > 3:
            position =- 3
        else:
            print("Thats Too far north, you will get lost.")
    if movment == "east" or "e":
        if position != 3 or 6 or 9:
            position += 1
        else:
            print("Thats too far east")
    if movment == "south" or "s":
        if position != 7 or 8 or 9:
            position += 3
        else:
            print("Thats too far south")
    if movment == "west" or "w":
        if position != 1 or 4 or 7:
            position -= 1
        else:
            print("Thats too far west")
