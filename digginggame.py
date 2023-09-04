#Imports
import random
from threading import Thread
import time
import pygame
import math

#Generates the map
mining = []
for i in range(101):
    for n in range(1000):
        randomn = random.randint(1, 200)
        if 1 <= randomn <= 5:
            mining.extend(["Energy_Crystal"]) #energy crystal
        elif 6 <= randomn <= 20:
            mining.extend(["Iron_Ore"]) #iron
            
        elif 21 <= randomn <= 30:
            mining.extend(["Gold_Ore"]) #gold
            
        elif 31 <= randomn <= 40:
            mining.extend(["Copper_Ore"]) #copper
            
        elif 41 <= randomn <= 45:
            mining.extend(["Diamond_Ore"]) #diamond
                
        elif 46 <= randomn <= 50:
            mining.extend(["Emerald_Ore"]) #emerald
        else:
            mining.extend(["Stone_Block"])
for i in range(2000):
    mining.insert(0, "Air") #lava
for i in range(3000):
    mining.insert(0, "Lava") #lava
for i in range(1000):
    mining.insert(0, "Obsidian") #obsidian
for i in range(10000):
    mining.insert(0, "Stone_Block") #obsidian
        
#Inits important variables
middletilenr = 0
realx = 50000
realy = 50000
tiley = -50000
cameramovementx = 0
mousehower = 0
startupp = True
clickdistance = "Long"
facing = "Right"
idle = 1
idlestage = 1
miningstage = 0
lastblockhit = 0
walkingstage = 1
lavastage = 1
inventorystate = False
hotbarslot = 1
climbing = False
climbingdown = False
chestopened = False
tempchest = "Chest"

def wrenchfunction(placement):
    global turnableblocks
    global mining
    if mining[placement] in turnableblocks:
        if mining[placement] == "Piston_Right":
            return "Piston_Down"
        elif mining[placement] == "Piston_Down":
            return "Piston_Left"
        elif mining[placement] == "Piston_Left":
            return "Piston_Up"
        elif mining[placement] == "Piston_Up":
            return "Piston_Right"
        if mining[placement] == "Hopper_Right":
            return "Hopper_Down"
        elif mining[placement] == "Hopper_Down":
            return "Hopper_Left"
        elif mining[placement] == "Hopper_Left":
            return "Hopper_Up"
        elif mining[placement] == "Hopper_Up":
            return "Hopper_Right"

hopperlist = []
def hopperloop():
    global hopperlist
    global mining
    while True:
        for i in range(len(hopperlist)):
            while chestopened:
                time.sleep(0.5)
            if mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Right" or mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Left" or mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Down" or mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Up":
                if mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Right":
                    variable = -1
                elif mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Left":
                    variable = 1
                elif mining[int((hopperlist[i].split(" "))[0])] == "Hopper_Up":
                    variable = -1000
                else:
                    variable = 1000
                if (hopperlist[i].split(" "))[1] == "0": 
                    if "Chest" in mining[int((hopperlist[i].split(" "))[0]) + variable]:
                        temphoppervariable = mining[int((hopperlist[i].split(" "))[0]) + variable].split(",")
                        if len(temphoppervariable) > 10:
                            for l in range(0, 18):
                                if temphoppervariable[l + 1] != " ":
                                    hopperlist[i] = (hopperlist[i].split(" "))[0] + " " + (temphoppervariable[l + 1].split(" "))[0]
                                
                                    
                                    if (int((temphoppervariable[l + 1].split(" "))[1]) - 1) != 0:
                                        temphoppervariable[l + 1] = (temphoppervariable[l + 1].split(" "))[0] + " " + str(int((temphoppervariable[l + 1].split(" "))[1]) - 1)
                                    else:
                                        temphoppervariable[l + 1] = " "
                                        
                                    mining[int((hopperlist[i].split(" "))[0]) + variable] = ",".join(temphoppervariable)
                                    
                                    if mining[int((hopperlist[i].split(" "))[0]) + variable] == "Chest, , , , , , , , , , , , , , , , , , ":
                                        mining[int((hopperlist[i].split(" "))[0]) + variable] = "Chest"
                                        
                                    break
                                
                    elif "Hopper" in ((mining[int((hopperlist[i].split(" "))[0]) + variable]).split(","))[0]:
                        for l in range(len(hopperlist)):
                            if str(int((hopperlist[i].split(" "))[0]) + variable) in hopperlist[l]:
                                hopperlist[i] = (hopperlist[i].split(" "))[0] + " " + (hopperlist[l].split(" "))[1]
                                hopperlist[l] = (hopperlist[l].split(" "))[0] + " 0"
                                break
                
                elif "Chest" in mining[int((hopperlist[i].split(" "))[0]) - variable]:
                    if mining[int((hopperlist[i].split(" "))[0]) - variable] == "Chest":
                        mining[int((hopperlist[i].split(" "))[0]) - variable] = "Chest, , , , , , , , , , , , , , , , , , "
                    temphoppervariable = mining[int((hopperlist[i].split(" "))[0]) - variable].split(",")
                    
                    newspot = True
                    for l in range(0, 18):
                        if (hopperlist[i].split(" "))[1] in temphoppervariable[l + 1]:
                            newspot = False
                            temphoppervariable[l + 1] = (temphoppervariable[l + 1].split(" "))[0] + " " + str(int((temphoppervariable[l + 1].split(" "))[1]) + 1)
                            hopperlist[i] = (hopperlist[i].split(" "))[0] + " 0"
                            break
                    if newspot == True:
                        for l in range(0, 18):
                            if " " == temphoppervariable[l + 1]:
                                temphoppervariable[l + 1] = (hopperlist[i].split(" "))[1] + " 1"
                                hopperlist[i] = (hopperlist[i].split(" "))[0] + " 0"
                                break
                    mining[int((hopperlist[i].split(" "))[0]) - variable] = ",".join(temphoppervariable)
                    

            else:
                del hopperlist[i]
                break

        time.sleep(0.1)

def pistonupdate(placement):
    global mining
    global powerblocks
    for n in range(1, 5):
        if n == 1:
            pistonvariablelist = ["Piston_Up", "Piston_Up_Extended", "Pistonhead_Up"]
            variable2 = 1000
        elif n == 2:
            pistonvariablelist = ["Piston_Down", "Piston_Down_Extended", "Pistonhead_Down"]
            variable2 = -1000
        elif n == 3:
            pistonvariablelist = ["Piston_Left", "Piston_Left_Extended", "Pistonhead_Left"]
            variable2 = -1
        elif n == 4:
            pistonvariablelist = ["Piston_Right", "Piston_Right_Extended", "Pistonhead_Right"]
            variable2 = 1
        for i in range(1, 5):
            variable = round(-667.33*i**3+4505.5*i**2-8847.17*i+5010)
            if mining[placement + variable] == pistonvariablelist[0]:
                if mining[placement + variable - 1] in powerblocks or mining[placement + variable + 1] in powerblocks or mining[placement + variable + 1000] in powerblocks or mining[placement - 1000 + variable] in powerblocks:
                    if mining[placement + 2*variable2 + variable] == "Air" or mining[placement + variable2 + variable] == "Air":
                        mining[placement + variable] = pistonvariablelist[1]
                        if mining[placement + variable2 + variable] != "Air":
                            mining[placement + 2*variable2 + variable] = mining[placement + variable2 + variable]
                        mining[placement + variable2 + variable] = pistonvariablelist[2]

            elif mining[placement + variable] == pistonvariablelist[1]:
                if mining[placement + variable - 1] not in powerblocks and mining[placement + variable + 1] not in powerblocks and mining[placement + 1000 +  variable] not in powerblocks and mining[placement - 1000 + variable] not in powerblocks:
                    mining[placement + variable]  = pistonvariablelist[0]
                    if "Extended" not in mining[placement + 2*variable2 + variable] and "Pistonhead" not in mining[placement + 2*variable2 + variable]:
                        mining[placement + variable2 + variable] = mining[placement + 2*variable2 + variable]
                        mining[placement + 2*variable2 + variable] = "Air"
                    else:
                        mining[placement + variable2 + variable] = "Air"


redstonelist = []
def redstoneloop():
    global redstonelist
    global mining
    while True:
        for i in range(len(redstonelist)):
            if mining[int(redstonelist[i])] == "Redstone" or mining[int(redstonelist[i])] == "Redstone_On":
                power = False
                y = 4
                for n in range(9):
                    x = -4
                    for n in range(9):
                        if mining[int(redstonelist[i]) + y*1000 + x] == "Lever_Down":
                            if int(redstonelist[i]) in redlist:
                                if (int(redstonelist[i]) + y*1000 + x) in redlist:
                                    power = True
                                    break
                            elif int(redstonelist[i]) in bluelist:
                                if (int(redstonelist[i]) + y*1000 + x) in bluelist:
                                    power = True
                                    break
                            elif int(redstonelist[i]) in greenlist:
                                if (int(redstonelist[i]) + y*1000 + x) in greenlist:
                                    power = True
                                    break
                            elif (int(redstonelist[i]) + y*1000 + x) not in greenlist and (int(redstonelist[i]) + y*1000 + x) not in redlist and (int(redstonelist[i]) + y*1000 + x) not in bluelist:
                                power = True
                                break
                        x += 1
                    y -= 1
                if power == False:
                    mining[int(redstonelist[i])] = "Redstone"
                    pistonupdate(int(redstonelist[i]))
                else:
                    mining[int(redstonelist[i])] = "Redstone_On"
                    pistonupdate(int(redstonelist[i]))
            else:
                pistonupdate(int(redstonelist[i]))
                del redstonelist[i]
                break
        time.sleep(0.1)

Thread(target = hopperloop).start()
Thread(target = redstoneloop).start()


inventory = []
for i in range(54):
    inventory.extend([" "])

#Temp colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
inventorycolour = (255, 197, 140)

#Important for game window
pygame.init()
gamedisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Mining game')
gamedisplay.fill(white)
clock = pygame.time.Clock()

airtile = pygame.image.load('blocks/air.png')
stonetile = pygame.image.load('blocks/stonetile.png')
obsidiantile = pygame.image.load('blocks/obsidian.png')
goldore = pygame.image.load('blocks/goldore.png')
diamondore = pygame.image.load('blocks/diamondore.png')
ironore = pygame.image.load('blocks/ironore.png')
energyore = pygame.image.load('blocks/energyore.png')
emeraldore = pygame.image.load('blocks/emeraldore.png')
copperore = pygame.image.load('blocks/copperore.png')


lavas = [pygame.image.load('blocks/lava1.png'), pygame.image.load('blocks/lava2.png'), pygame.image.load('blocks/lava3.png')]
lava = lavas[0]

ladder = pygame.image.load('blocks/ladder.png')
planks = pygame.image.load('blocks/planks.png')
stonebricks = pygame.image.load('blocks/stonebricks.png')
redstonebricks = pygame.image.load('blocks/redstonebricks.png')

character = pygame.image.load('character/walking1.png')

shadow = pygame.image.load('misc/shadow.png')
shadow2 = pygame.image.load('misc/shadow2.png')
mousebox = pygame.image.load('misc/mousebox.png')
mouseboxred = pygame.image.load('misc/redmousebox.png')
hotbar = pygame.image.load('misc/hotbar.png')
inventorye = pygame.image.load('misc/inventory.png')
inventorybox = pygame.image.load('misc/inventorybox.png')
inventorybox2 = pygame.image.load('misc/inventorybox2.png')
hotkeyicon = pygame.image.load('misc/hotkey.png')
chestgui = pygame.image.load('misc/chestgui.png')

chest = pygame.image.load('factoryblocks/chest.png')
hopper_left = pygame.image.load('factoryblocks/hopper_left.png')
hopper_right = pygame.image.load('factoryblocks/hopper_right.png')
hopper_up = pygame.image.load('factoryblocks/hopper_up.png')
hopper_down = pygame.image.load('factoryblocks/hopper_down.png')
lever_up = pygame.image.load('factoryblocks/lever1.png')
lever_down = pygame.image.load('factoryblocks/lever2.png')
redstone = pygame.image.load('factoryblocks/redstone.png')
redstone_on = pygame.image.load('factoryblocks/redstone_on.png')

piston_up = pygame.image.load('factoryblocks/piston/piston_up.png')
piston_up_extended = pygame.image.load('factoryblocks/piston/piston_up_extended.png')
pistonhead_up = pygame.image.load('factoryblocks/piston/pistonhead_up.png')

piston_down = pygame.image.load('factoryblocks/piston/piston_down.png')
piston_down_extended = pygame.image.load('factoryblocks/piston/piston_down_extended.png')
pistonhead_down = pygame.image.load('factoryblocks/piston/pistonhead_down.png')

piston_right = pygame.image.load('factoryblocks/piston/piston_right.png')
piston_right_extended = pygame.image.load('factoryblocks/piston/piston_right_extended.png')
pistonhead_right = pygame.image.load('factoryblocks/piston/pistonhead_right.png')

piston_left = pygame.image.load('factoryblocks/piston/piston_left.png')
piston_left_extended = pygame.image.load('factoryblocks/piston/piston_left_extended.png')
pistonhead_left = pygame.image.load('factoryblocks/piston/pistonhead_left.png')

reddye = pygame.image.load('items/reddye.png')
bluedye = pygame.image.load('items/bluedye.png')
greendye = pygame.image.load('items/greendye.png')
eraser = pygame.image.load('items/eraser.png')
wrench = pygame.image.load('items/wrench.png')




paintingmonster = pygame.image.load('painting/painting.png')

#When adding new blocks / items add them to items1 list and items2 list
items1 = [lava, stonetile, obsidiantile, goldore, diamondore, ironore, energyore, 
          emeraldore, copperore, stonebricks, ladder, planks, paintingmonster, 
          chest, hopper_right, hopper_left, hopper_up, hopper_down, lever_up, lever_down, 
          airtile, redstone, redstone_on, piston_up, piston_up_extended, pistonhead_up, 
          piston_down, piston_down_extended, pistonhead_down, piston_right, piston_right_extended, 
          pistonhead_right, piston_left, piston_left_extended, pistonhead_left, reddye, greendye, 
          bluedye, eraser, redstonebricks, wrench]

items2 = ["Lava", "Stone_Block", "Obsidian", "Gold_Ore", "Diamond_Ore", "Iron_Ore", 
          "Energy_Crystal", "Emerald_Ore", "Copper_Ore", "Stone_Bricks", 
          "Ladder", "Planks", "Painting_(Monster)", "Chest", "Hopper_Right", 
          "Hopper_Left", "Hopper_Up", "Hopper_Down", "Lever", "Lever_Down", 
          "Air", "Redstone", "Redstone_On", "Piston_Up", "Piston_Up_Extended", 
          "Pistonhead_Up", "Piston_Down", "Piston_Down_Extended", "Pistonhead_Down", 
          "Piston_Right", "Piston_Right_Extended", "Pistonhead_Right", "Piston_Left", 
          "Piston_Left_Extended", "Pistonhead_Left", "Red_Dye", "Green_Dye", "Blue_Dye", 
          "Eraser", "Red_Bricks", "Wrench"]

blocksthatcanbreak = ["Stone_Block", "Gold_Ore", "Diamond_Ore", "Iron_Ore", 
                      "Energy_Crystal", "Emerald_Ore", "Copper_Ore", "Stone_Bricks", 
                      "Ladder", "Planks", "Painting_(Monster)", "Chest", "Hopper_Right", 
                      "Hopper_Left", "Hopper_Up", "Hopper_Down", "Lever", "Redstone", 
                      "Piston_Up", "Piston_Down", "Piston_Right", "Piston_Left", 
                      "Red_Bricks"]

buildingblocks = ["Lava", "Stone_Block", "Obsidian", "Gold_Ore", "Diamond_Ore", 
                  "Iron_Ore", "Energy_Crystal", "Emerald_Ore", "Copper_Ore", 
                  "Stone_Bricks", "Ladder", "Planks", "Painting_(Monster)", 
                  "Chest", "Hopper_Right", "Hopper_Left", "Hopper_Up", 
                  "Hopper_Down", "Lever", "Lever_Down", "Redstone", "Redstone_On", 
                  "Piston_Up", "Piston_Down", "Piston_Right", "Piston_Left", 
                  "Red_Bricks"]

transparantblocks = ["Lava", "Air", "Ladder", "Painting_(Monster)", "Lever", "Lever_Down", 
                     "Redstone", "Redstone_On"]

lightblocks = ["Lava", "Air", "Ladder", "Painting_(Monster)", "Chest", "Hopper_Right", 
               "Hopper_Left", "Hopper_Up", "Hopper_Down", "Lever", "Lever_Down", "Redstone_On", 
               "Redstone", "Piston_Up", "Piston_Up_Extended", "Piston_Down", "Piston_Down_Extended", 
               "Piston_Left", "Piston_Left_Extended", "Piston_Right", "Piston_Right_Extended"]

transparantgravityblocks = ["Air", "Painting_(Monster)", "Lever", "Lever_Down", 
                            "Redstone", "Redstone_On"]
reducedGravityBlocks = ["Lava"]

climbingBlocks = ["Lava", "Ladder"]

factoryblocks = ["Chest", "Hopper_Right", "Hopper_Left", "Hopper", "Hopper_Down", 
                 "Lever", "Lever_Down", "Piston_Up", "Redstone", "Redstone_On", 
                 "Piston_Down", "Piston_Right", "Piston_Left"]

updatableblocks = ["Lever", "Lever_Down"]

blocksthatneedairbehindthem = ["Ladder", "Lever", "Lever_Down", "Redstone", 
                               "Redstone_On", "Piston_Up_Extended", "Pistonhead_Up", 
                               "Piston_Down_Extended", "Pistonhead_Down", "Pistonhead_Left", 
                               "Piston_Left_Extended", "Pistonhead_Left", "Pistonhead_Right", 
                               "Piston_Right_Extended", "Pistonhead_Right"]

powerblocks = ["Redstone_On", "Lever_Down"]

colorableblocks = ["Redstone_On", "Redstone", "Lever", "Lever_Down"]

turnableblocks = ["Piston_Left", "Piston_Right", "Piston_Up", "Piston_Down", "Hopper_Left", "Hopper_Right", "Hopper_Up", "Hopper_Down"]

greenlist = []
bluelist = []
redlist = []


font = pygame.font.SysFont('Arial', 15) 
titlefont = pygame.font.SysFont('Arial', 30)

pygame.display.set_icon(stonetile)

def givecommand(command):
    global inventory
    command = command.split(" ")
    if command[1] in items2:
        inInventory = False
        for i in range(len(inventory)):
            if command[1] in inventory[i]:
                inventoryitemsplit = inventory[i].split(" ")
                inventory[i] = command[1] + " " + str(int(inventoryitemsplit[1]) + int(command[2]))
                inInventory = True
                break
        if inInventory == False:
            for i in range(len(inventory)):
                if inventory[i] == " ":
                    inventory[i] = command[1] + " " + command[2]
                    break




def startup():
    global startupp
    global mining
    global middletilenr
    global xnumber
    global ynumber
    mining[middletilenr - 4 * 1000 + 4 - 998] = "Planks"
    mining[middletilenr - 4 * 1000 + 4 - 999] = "Planks"
    mining[middletilenr - 4 * 1000 + 4 - 1000] = "Chest,Planks 99,Red_Bricks 100,Stone_Bricks 68,Chest 56,Ladder 45, , ,Hopper_Up 99, ,Lever 15,Redstone 99,Piston_Up 99, ,Blue_Dye 10,Green_Dye 10,Wrench 1,Eraser 1,Lava 12" 
    mining[middletilenr - 4 * 1000 + 4 - 1001] = "Planks"
    mining[middletilenr - 4 * 1000 + 4 - 1002] = "Planks"
    mining[middletilenr - 4 * 1000 + 4] = "Air"
    mining[middletilenr - 4 * 1000 + 4 + 1] = "Air"
    mining[middletilenr - 4 * 1000 + 4 - 1] = "Air"
    mining[middletilenr - 4 * 1000 + 4 + 1001] = "Air"
    mining[middletilenr - 4 * 1000 + 4 + 1000] = "Air"
    mining[middletilenr - 4 * 1000 + 4 + 999] = "Air"
    startupp = False

jumpwait = False
def jump():
    global realy
    global tiley
    global mining
    global jumpwait   
    global climbing
    if (mining[(round((realx-16)/100) + (round((tiley)/1000))*1000) + 5 - 3000]) in climbingBlocks or (mining[(round((realx - 50)/100) + (round((tiley)/1000))*1000) + 5 - 3000]) in climbingBlocks or (mining[(round((realx-72)/100) + (round((tiley)/1000))*1000) + 5 - 3000]) in climbingBlocks:
        climbing = True
    elif (mining[(round((realx-16)/100) + (round((tiley - 4)/1000))*1000) + 5 - 3000]) not in transparantblocks or (mining[(round((realx - 50)/100) + (round((tiley - 4)/1000))*1000) + 5 - 3000]) not in transparantblocks or (mining[(round((realx-72)/100) + (round((tiley - 4)/1000))*1000) + 5 - 3000]) not in transparantblocks:
        climbing = False
        for i in range(10):
            if (mining[(round((realx - 50)/100) + (round((tiley + 1550)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 72)/100) + (round((tiley + 1550)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 16)/100) + (round((tiley + 1550)/1000))*1000) + 5 - 3000]) in transparantblocks:  
                realy -= 20
                tiley += 200
                jumpwait = True
                while jumpwait:
                    pass
            else:
                break
        for i in range(5):
            if (mining[(round((realx - 50)/100) + (round((tiley + 1450)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 72)/100) + (round((tiley + 1450)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 16)/100) + (round((tiley + 1450)/1000))*1000) + 5 - 3000]) in transparantblocks:  
                realy -= 10
                tiley += 100
                jumpwait = True
                while jumpwait:
                    pass
            else:
                break            

        if (mining[(round((realx - 50)/100) + (round((tiley + 1400)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 72)/100) + (round((tiley + 1400)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 16)/100) + (round((tiley + 1400)/1000))*1000) + 5 - 3000]) in transparantblocks:  
            realy -= 5
            tiley += 50

            jumpwait = True
            while jumpwait:
                pass
   
                
def blockloop():
    global ynumber
    global middletilenr
    global xnumber
    y = 1
    light = False
    for i in range(3):
        x = -1
        for i in range(3):
            if mining[middletilenr - ynumber * 1000 + xnumber + y*1000 + x] in lightblocks:
                light = True
                break
            x += 1
        if light == True:
            break
            
        y -= 1
    if light != True:
        y = 2
        for i in range(5):
            x = -2
            for i in range(5):
                if mining[middletilenr - ynumber * 1000 + xnumber + y*1000 + x] in lightblocks:
                    light = True
                    break
                x += 1
            y -= 1
            if light == True:
                break
        if light == True:
            gamedisplay.blit(shadow2, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))
        else:
            gamedisplay.blit(shadow, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))

def blockupdate():
    global mining
    global mousehower
    if mining[mousehower] == "Lever":
        mining[mousehower] = "Lever_Down"
        pistonupdate(mousehower)
    elif mining[mousehower] == "Lever_Down":
        mining[mousehower] = "Lever"
        pistonupdate(mousehower)

def inventoryloop():
    global inventorye
    global mousebox
    global QUIT
    global inventorystate
    global chestopened
    global chestgui
    global tempchest
    
    if tempchest == "Chest":
        tempchest = "Chest" + ", , , , , , , , , , , , , , , , , , "
    tempchestlist = tempchest.split(",")

    
    inventorystate = True
    firstslot = ["", "", ""]
    secondslot = ["", "", ""]
    while inventorystate:
        currentinventorybox = ""
        mousepos = pygame.mouse.get_pos()

        gamedisplay.fill(inventorycolour)
        
        for l in range(0, 6):
            for n in range(0, 9):
                for i in range(len(items2)):
                    if items2[i] in inventory[n + l*9]:
                        inventoryaddition = pygame.transform.scale(items1[i], (40, 40))
                        gamedisplay.blit(inventoryaddition, (278 + n*79, 475 - l*80))
                        break

        gamedisplay.blit(inventorye, (260, 60))
        
        for l in range(0, 6):
            for n in range(0, 9):
                text = font.render(((inventory[n + l*9]).split(" "))[1] , True, black) 
                gamedisplay.blit(text, (312 + n*79, 506 - l*79))    
                    
                if (250 + n*79) <= mousepos[0] <= (250 + n*79 + 79) and (475 - l*80-20) <= mousepos[1] <= (475 - (l-1)*80-20):
                    gamedisplay.blit(inventorybox, (278 + (n + 1)*79 - 96.5, 475 - (l-1) * 79 - 99))
                    currentinventorybox = [n + l*9, "Inventory"]
                if len(firstslot) != 0:
                    if (n + l*9) == firstslot[0] and "Inventory" == firstslot[1]:
                        gamedisplay.blit(inventorybox2, (278 + (n + 1)*79 - 96.5, 475 - (l-1) * 79 - 99))
                        
        text = titlefont.render("Inventory", True, black)
        gamedisplay.blit(text, (563, 23))
              
        if chestopened == True:
            text = titlefont.render("Chest", True, black)
            gamedisplay.blit(text, (87, 23))            
                        
            for l in range(0, 6):
                for n in range(0, 3):
                    for i in range(len(items2)):
                        if items2[i] in ((tempchest.split(","))[1 + n + l*3]):
                            inventoryaddition = pygame.transform.scale(items1[i], (40, 40))
                            gamedisplay.blit(inventoryaddition, (23 + n*79, 475 - l*80))
                        
                            break
                        
            gamedisplay.blit(chestgui, (5, 60))
            
            for l in range(0, 6):
                for n in range(0, 3):
                    text = font.render((((tempchest.split(","))[1 + n + l*3]).split(" "))[1] , True, black) 
                    gamedisplay.blit(text, (57 + n*79, 506 - l*79))    
                    
                    if (-5 + n*79) <= mousepos[0] <= (-5 + n*79 + 79) and (475 - l*80-20) <= mousepos[1] <= (475 - (l-1)*80-20):
                        gamedisplay.blit(inventorybox, (23 + (n + 1)*79 - 96.5, 475 - (l-1) * 79 - 99))
                        currentinventorybox = [n + l*3, "Chest"]
                    if len(firstslot) != 0:
                        if (n + l*3) == firstslot[0] and "Chest" == firstslot[1]:
                            gamedisplay.blit(inventorybox2, (23 + (n + 1)*79 - 96.5, 475 - (l-1) * 79 - 99))
                                           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inventorystate = False
                QUIT = False               
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    inventorystate = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if currentinventorybox != "":
                    if "" in firstslot:
                        if currentinventorybox[1] == "Inventory":
                            firstslot = [currentinventorybox[0], currentinventorybox[1], inventory[currentinventorybox[0]]]
                        else:
                            firstslot = [currentinventorybox[0], currentinventorybox[1], tempchestlist[currentinventorybox[0] + 1]]
                    else:
                        if currentinventorybox[1] == "Inventory":
                            secondslot = [currentinventorybox[0], currentinventorybox[1], inventory[currentinventorybox[0]]]
                        else:
                            secondslot = [currentinventorybox[0], currentinventorybox[1], tempchestlist[currentinventorybox[0] + 1]]
                        
                        if "Inventory" in firstslot:
                            inventory[firstslot[0]] = secondslot[2]
                            
                        else:
                            tempchestlist[firstslot[0] + 1] = secondslot[2]
                            tempchest = ",".join(tempchestlist)
                            
                        if "Inventory" in secondslot:
                            inventory[secondslot[0]] = firstslot[2]
                            
                        else:
                            tempchestlist[secondslot[0] + 1] = firstslot[2]
                            tempchest = ",".join(tempchestlist)
                        
                        firstslot = ""
                        secondslot = ""   
            
        pygame.display.update()
        
    if tempchest == "Chest, , , , , , , , , , , , , , , , , , ":
        tempchest = "Chest"
    chestopened = False
        
        
QUIT = True
while QUIT:  
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           QUIT = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                cameramovementx = 1
            elif event.key == pygame.K_d:
                cameramovementx = 2
            elif event.key == pygame.K_w:
                Thread(target = jump).start()
            elif event.key == pygame.K_s:
                climbingdown = True
                

            elif event.key == pygame.K_1:
                hotbarslot = 1
            elif event.key == pygame.K_2:
                hotbarslot = 2
            elif event.key == pygame.K_3:
                hotbarslot = 3
            elif event.key == pygame.K_4:
                hotbarslot = 4
            elif event.key == pygame.K_5:
                hotbarslot = 5
            elif event.key == pygame.K_6:
                hotbarslot = 6
            elif event.key == pygame.K_7:
                hotbarslot = 7
            elif event.key == pygame.K_8:
                hotbarslot = 8
            elif event.key == pygame.K_9:
                hotbarslot = 9

            elif event.key == pygame.K_e:
                inventoryloop()
                
            elif event.key == pygame.K_t:
                givecommand(input("\n\n\n\n\n\n\n\n\n/"))
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                cameramovementx = 0
            elif event.key == pygame.K_d:
                cameramovementx = 0
                
            elif event.key == pygame.K_s:
                climbingdown = False
                
            elif event.key == pygame.K_w:
                climbing = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if clickdistance == "Short":
                if mining[mousehower] in blocksthatcanbreak:
                    if mousehower == lastblockhit:
                        miningstage += 1
                        lastblockhit = mousehower
                        if miningstage == 4:
                            miningstage = 0
                            inInventory = False
                            for i in range(len(inventory)):
                                if mining[mousehower] in inventory[i]:
                                    inventoryitemsplit = inventory[i].split(" ")
                                    inventory[i] = mining[mousehower] + " " + str(int(inventoryitemsplit[1]) + 1)
                                    inInventory = True
                                    break
                            
                            if inInventory == False:
                                for i in range(len(inventory)):
                                    if inventory[i] == " ":
                                        inventory[i] = mining[mousehower] + " 1"
                                        break
                            mining[mousehower] = "Air"
                            if mousehower in redlist or mousehower in greenlist or mousehower in bluelist:
                                if mousehower in redlist:
                                    redlist.remove(mousehower)
                                elif mousehower in greenlist:
                                    greenlist.remove(mousehower)
                                elif mousehower in bluelist:
                                    bluelist.remove(mousehower)
                            
                        break1 = pygame.image.load('misc/break' + str(miningstage) + '.png')
                    else:
                        miningstage = 1
                        lastblockhit = mousehower
                        break1 = pygame.image.load('misc/break' + str(miningstage) + '.png')
                else:
                    miningstage = 0
                    break1 = pygame.image.load('misc/break' + str(miningstage) + '.png')
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            if hotbarslot == 1:
                hotbarslot = 9
            else:
                hotbarslot -= 1
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            if hotbarslot == 9:
                hotbarslot = 1
            else:
                hotbarslot += 1
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if clickdistance == "Short":
                if "Chest" in mining[mousehower]:
                    tempchest = mining[mousehower]
                    chestopened = True
                    inventoryloop()
                    mining[mousehower] = tempchest
                
                elif mining[mousehower] in turnableblocks and ((inventory[hotbarslot-1]).split(" "))[0] == "Wrench":
                    mining[mousehower] = wrenchfunction(mousehower)
                    
                elif "Green_Dye" in inventory[hotbarslot - 1] and mousehower not in redlist and mousehower not in bluelist and mousehower not in greenlist and mining[mousehower] in colorableblocks:
                    greenlist.extend([mousehower])
                    if (int(((inventory[hotbarslot-1]).split(" "))[1]) - 1) == 0:
                        inventory[hotbarslot-1] = " "    
                    else:
                        inventory[hotbarslot-1] = ((inventory[hotbarslot-1]).split(" "))[0] + " " + str(int(((inventory[hotbarslot-1]).split(" "))[1]) - 1)
                elif "Red_Dye" in inventory[hotbarslot - 1] and mousehower not in greenlist and mousehower not in bluelist and mousehower not in redlist and mining[mousehower] in colorableblocks:
                    redlist.extend([mousehower])
                    if (int(((inventory[hotbarslot-1]).split(" "))[1]) - 1) == 0:
                        inventory[hotbarslot-1] = " "    
                    else:
                        inventory[hotbarslot-1] = ((inventory[hotbarslot-1]).split(" "))[0] + " " + str(int(((inventory[hotbarslot-1]).split(" "))[1]) - 1)
                elif "Blue_Dye" in inventory[hotbarslot - 1] and mousehower not in redlist and mousehower not in greenlist and mousehower not in bluelist and mining[mousehower] in colorableblocks:
                    bluelist.extend([mousehower])
                    if (int(((inventory[hotbarslot-1]).split(" "))[1]) - 1) == 0:
                        inventory[hotbarslot-1] = " "    
                    else:
                        inventory[hotbarslot-1] = ((inventory[hotbarslot-1]).split(" "))[0] + " " + str(int(((inventory[hotbarslot-1]).split(" "))[1]) - 1)
                        
                elif "Eraser" in inventory[hotbarslot - 1]:
                    if mousehower in redlist:
                        redlist.remove(mousehower)
                    elif mousehower in greenlist:
                        greenlist.remove(mousehower)
                    elif mousehower in bluelist:
                        bluelist.remove(mousehower)
                    
                elif mining[mousehower] in updatableblocks:
                    blockupdate()
                
                elif round ((((realx - 74)/100) + (round((tiley + 100)/1000))*1000) + 5 - 3000) != mousehower and ((((realx - 74)/100) + (round((tiley + 900)/1000))*1000) + 5 - 3000) != mousehower and ((round((realx - 74)/100) + (round((tiley + 1500)/1000))*1000) + 5 - 3000) != mousehower and ((round((realx - 14)/100) + (round((tiley + 100)/1000))*1000) + 5 - 3000) != mousehower and ((round((realx - 14)/100) + (round((tiley + 1500)/1000))*1000) + 5 - 3000) != mousehower and ((round((realx - 14)/100) + (round((tiley + 900)/1000))*1000) + 5 - 3000) != mousehower:
                    if mining[mousehower] == "Air":
                        if ((inventory[hotbarslot-1]).split(" "))[0] in buildingblocks:
                            mining[mousehower] = ((inventory[hotbarslot-1]).split(" "))[0]
                            if "Hopper" in mining[mousehower]:
                                hopperlist.extend([str(mousehower) + " 0"])
                            elif "Redstone" in mining[mousehower]:
                                redstonelist.extend([str(mousehower)])
                                
                            if (int(((inventory[hotbarslot-1]).split(" "))[1]) - 1) == 0:
                                inventory[hotbarslot-1] = " "
                                
                            else:
                                inventory[hotbarslot-1] = ((inventory[hotbarslot-1]).split(" "))[0] + " " + str(int(((inventory[hotbarslot-1]).split(" "))[1]) - 1)
                                
                elif ((inventory[hotbarslot-1]).split(" "))[0] in transparantblocks:
                    if mining[mousehower] == "Air":    
                        if ((inventory[hotbarslot-1]).split(" "))[0] in buildingblocks:
                            mining[mousehower] = ((inventory[hotbarslot-1]).split(" "))[0]
                            if "Hopper" in mining[mousehower]:
                                hopperlist.extend([str(mousehower) + " 0"])
                            elif "Redstone" in mining[mousehower]:
                                redstonelist.extend([str(mousehower)])

                            if (int(((inventory[hotbarslot-1]).split(" "))[1]) - 1) == 0:
                                inventory[hotbarslot-1] = " "
                                
                            else:
                                inventory[hotbarslot-1] = ((inventory[hotbarslot-1]).split(" "))[0] + " " + str(int(((inventory[hotbarslot-1]).split(" "))[1]) - 1)
            
                
    
    if cameramovementx == 1:
        if (mining[(round((realx - 74)/100) + (round((tiley + 100)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 74)/100) + (round((tiley + 750)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 74)/100) + (round((tiley + 1500)/1000))*1000) + 5 - 3000]) in transparantblocks:
            walkingstage += 0.06
            if walkingstage > 5:
                walkingstage = 0.55
            character = pygame.image.load('character/walking' + str(round(walkingstage)) + '.png')
            character = pygame.transform.flip(character, True, False)
            realx -= 2
            facing = "Left"
            idle = 1

    elif cameramovementx == 2:
        if (mining[(round((realx - 14)/100) + (round((tiley + 100)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 14)/100) + (round((tiley + 750)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 14)/100) + (round((tiley + 1500)/1000))*1000) + 5 - 3000]) in transparantblocks:
            walkingstage += 0.06
            if walkingstage > 5:
                walkingstage = 0.55
            
            character = pygame.image.load('character/walking' + str(round(walkingstage)) + '.png')
            realx += 2
            facing = "Right"
            idle = 1
    idle -= 0.1
    
    if idle < 0.2:
        idlestage += 0.03
        if idlestage > 4.2:
            idlestage = 0.6
        
        character = pygame.image.load('character/idle' + str(round(idlestage)) + '.png')
        if facing == "Left":
            character = pygame.transform.flip(character, True, False)
            
            
    if climbing == True:
        if (mining[(round((realx-16)/100) + (round((tiley)/1000))*1000) + 5 - 3000]) in climbingBlocks or (mining[(round((realx - 50)/100) + (round((tiley)/1000))*1000) + 5 - 3000]) in climbingBlocks or (mining[(round((realx-72)/100) + (round((tiley)/1000))*1000) + 5 - 3000]) in climbingBlocks:
            if (mining[(round((realx - 50)/100) + (round((tiley + 1550)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 72)/100) + (round((tiley + 1550)/1000))*1000) + 5 - 3000]) in transparantblocks and (mining[(round((realx - 16)/100) + (round((tiley + 1550)/1000))*1000) + 5 - 3000]) in transparantblocks:
                realy -= 5
                tiley += 50
        else:
            climbing == False
        
            
    jumpwait = False
        
    gamedisplay.fill(white)


    middletilenr = round(realx/100) + (round(tiley/1000))*1000
    blockx = round(realx/100)*100+(450-realx)
    blocky = round(realy/100)*100+(450-realy)
    ynumber = 6

    lavastage = (lavastage + 0.01)%3
    items1[0] = lavas[math.floor(lavastage)]

    for i in range(10):
        if startupp:
            startup()
        xnumber = 10
        for i in range(12):
            for i in range(len(items2)):
                if mining[middletilenr - ynumber * 1000 + xnumber] == items2[i]:
                    if mining[middletilenr - ynumber * 1000 + xnumber] in blocksthatneedairbehindthem:
                        gamedisplay.blit(airtile, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))
                    if (middletilenr - ynumber * 1000 + xnumber) in redlist:
                        pygame.draw.rect(gamedisplay,red,[(blockx - (450 - xnumber*100) + 25), (blocky - (450 - ynumber*100) + 25),50,50])
                    elif (middletilenr - ynumber * 1000 + xnumber) in bluelist:
                        pygame.draw.rect(gamedisplay,blue,[(blockx - (450 - xnumber*100) + 25), (blocky - (450 - ynumber*100) + 25),50,50])
                    elif (middletilenr - ynumber * 1000 + xnumber) in greenlist:
                        pygame.draw.rect(gamedisplay,green,[(blockx - (450 - xnumber*100) + 25), (blocky - (450 - ynumber*100) + 25),50,50])
                    gamedisplay.blit(items1[i], ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))
                    break

                elif "Chest" in mining[middletilenr - ynumber * 1000 + xnumber]:
                    gamedisplay.blit(chest, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))
                    break
                    
                
            blockloop()
            
            if lastblockhit == (middletilenr - ynumber * 1000 + xnumber):
                gamedisplay.blit(break1, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))

            if (blockx - (450 - xnumber*100)) <= mousepos[0] <= (blockx - (450 - xnumber*100) + 100) and (blocky - (450 - ynumber*100)) <= mousepos[1] <= (blocky - (450 - ynumber*100) + 100):
                if 285 <= (mousepos[0] - 450) or -172 >= (mousepos[0] - 450) or -250 >= (mousepos[1] - 200) or 350 <= (mousepos[1] - 200):
                    gamedisplay.blit(mouseboxred, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))
                    clickdistance = "Long"
                else:
                    gamedisplay.blit(mousebox, ((blockx - (450 - xnumber*100)), (blocky - (450 - ynumber*100))))
                    clickdistance = "Short"
                mousehower = middletilenr - ynumber * 1000 + xnumber
            
                
            xnumber += -1
        ynumber += -1
    

        
    
    for i in range(50):
        if (mining[(round((realx - 16)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in transparantgravityblocks and (mining[(round((realx - 50)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in transparantgravityblocks and (mining[(round((realx - 72)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in transparantgravityblocks: 
            tiley -= (50-i)
            realy += (5-i/10)
            break
        elif (mining[(round((realx - 16)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in reducedGravityBlocks or (mining[(round((realx - 50)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in reducedGravityBlocks or (mining[(round((realx - 72)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in reducedGravityBlocks:
            if (mining[(round((realx - 16)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in transparantgravityblocks + reducedGravityBlocks and (mining[(round((realx - 50)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in transparantgravityblocks + reducedGravityBlocks and (mining[(round((realx - 72)/100) + (round((tiley - (50-i))/1000))*1000) + 5 - 3000]) in transparantgravityblocks + reducedGravityBlocks:
                tiley -= (25-i)
                realy += (2.5-i/10)
                break
    if climbingdown == True:
        if (mining[(round((realx - 16)/100) + (round((tiley - (50))/1000))*1000) + 5 - 3000]) in climbingBlocks or (mining[(round((realx - 50)/100) + (round((tiley - 50)/1000))*1000) + 5 - 3000]) in climbingBlocks or (mining[(round((realx - 72)/100) + (round((tiley - 50)/1000))*1000) + 5 - 3000]) in climbingBlocks: 
            if (mining[(round((realx - 16)/100) + (round((tiley - (50))/1000))*1000) + 5 - 3000]) in transparantblocks + climbingBlocks and (mining[(round((realx - 50)/100) + (round((tiley - 50)/1000))*1000) + 5 - 3000]) in transparantblocks + climbingBlocks and (mining[(round((realx - 72)/100) + (round((tiley - 50)/1000))*1000) + 5 - 3000]) in transparantblocks + climbingBlocks: 
                tiley -= 50
                realy += 5 
    gamedisplay.blit(character, (465, 196))

    for n in range(0, 9):
        for i in range(len(items2)):
            if items2[i] in inventory[n]:
                inventoryaddition = pygame.transform.scale(items1[i], (40, 40))
                gamedisplay.blit(inventoryaddition, (170 + n*79, 515))
                break
    gamedisplay.blit(hotbar, (150, 500))
    
    for n in range(0, 9):
        text = font.render(((inventory[n]).split(" "))[1] , True, black) 
        gamedisplay.blit(text, (203 + n*79, 549)) 
    
    gamedisplay.blit(hotkeyicon, (71 + hotbarslot*79, 500)) 
    
    
    text = font.render(" ".join((((inventory[hotbarslot-1]).split(" "))[0]).split("_")) , True, white)
    offset = len(list(inventory[hotbarslot-1]))
    gamedisplay.blit(text, (500 - offset * 2, 470))
    
    pygame.display.update()

pygame.quit()
print("Game quit")