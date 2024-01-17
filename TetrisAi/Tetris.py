from graphics import *
import time
import random

#600w by 800h
win = GraphWin('Tetris',600,800)
totalBlocks = 0
orientation = 0
maxOrientation = 0
allCurrentRotations = []
currentBlock = []
blocksMakeAPiece = 0
gameOver = False
timeNow = time.time()
timeLast = time.time()
timeStart = time.time()
pace = 1
totalLines = 0
score = 0
level = 1
scoreText = Text(Point(500,260),"Score: " + str(score))
levelText = Text(Point(500,280),"Level: " + str(level))
controlType = "LowestDropAi"
blockFilled = []
blockBoard = []
lowestDropAiInfo = ['x','o','block#','y']


def makeBoard():
    global score

    for x in range(20):
        temp = []
        for x in range(10):
            temp.append(False)
        blockFilled.append(temp)

    for x in range(20):
        temp = []
        for x in range(10):
            temp.append('')
        blockBoard.append(temp)


    gameBorder = Rectangle(Point(400,0),Point(401,800))
    gameBorder.draw(win)
    gameBorder.setOutline('white')
    gameBorder.setFill('white')

    scoreText.draw(win)
    scoreText.setFill('white')

    levelText.draw(win)
    levelText.setFill('white')

    nextBlockBorder = Rectangle(Point(400,200),Point(600,200))
    nextBlockBorder.draw(win)
    nextBlockBorder.setOutline('white')
    nextBlockBorder.setFill('white')

    for x in range(10):
        line = Rectangle(Point(0 + x*40,0),Point(1 + x*40,800))
        line.draw(win)
        line.setOutline('white')
        line.setFill('white')

    for x in range(20):
        line = Rectangle(Point(0,0 + x*40),Point(400,0 + x*40))
        line.draw(win)
        line.setOutline('white')
        line.setFill('white')

    win.setBackground('black')
    makeRandomShape()

def runGame():
    global score,timeNow,timeLast,pace,controlType
    while not gameOver:
        levelUp()
        scoreText.setText("Score: " + str(score))
        win.update()
        controlHandeler(controlType)
        timeNow = time.time()
        if(timeNow-timeLast>pace):
            moveBlock(0,40,"s")
            timeLast = time.time()
    recordData()
    gameOverScreen()    

def gameOverScreen():
    win.close()
    over = GraphWin('Game Over',300,300)
    over.setBackground('black')
    overText = Text(Point(150,50),"Game Over!")
    overText.setFill('white')
    overText.draw(over)
    overText = Text(Point(150,75),"You Got a Score of " + str(score))
    overText.setFill('white')
    overText.draw(over)
    if(controlType == 'Human'):
        over.getMouse()
    over.close()

def controlHandeler(ct):
    if ct == 'Human':
        pressed = win.checkKey()
    elif ct == 'RandomAi':
        pressed = randomAi()
    elif ct == 'LowestDropAi':
        pressed = lowestDropAi()
    if(pressed == "d" and not blockAtRight()):
        moveBlock(40,0,pressed)
    if(pressed == "a" and not blockAtLeft()):
        moveBlock(-40,0,pressed)
    if(pressed == "s"):
        moveBlock(0,40,pressed)
    if(pressed == "r" and maxOrientation != 1 and not invalidRotate()):
        clockwiseRotate()
    if(pressed == "space"):
        drop()

def randomAi():
    global pace
    pace = 0
    x = random.randint(1,5)
    if x == 1:
        return 'd'
    if x == 2:
        return 'a'
    if x == 3:
        return 'r'
    if x == 4:
        return 's'
    if x == 5:
        return 'space'

def moveBlock(x,y,d):
    if(blockAtBottom(1) and d == 's'):
        setNewHeight()
        completedRow()
        gameLost()
        allCurrentRotations.clear()
        currentBlock.clear()
        makeRandomShape()
    else: 
        for piece in allCurrentRotations:
            for block in piece:
                block.move(x,y)
        win.redraw()

def clockwiseRotate():
    global orientation, maxOrientation, currentBlock

    if orientation == maxOrientation:
        orientation = 0
    for block in currentBlock:
        block.undraw()
    currentBlock = allCurrentRotations[orientation]
    orientation+=1
    for block in currentBlock:
        block.draw(win)

def makeStraight():
    global maxOrientation, orientation, currentBlock

    orientationOne = []
    for i in range(4):
        B1pt1 = Point(120 + i*40,0)
        B1pt2 = Point(120 + (i+1)*40,40)
        block1 = Rectangle(B1pt1,B1pt2)
        block1.setOutline('white')
        block1.setFill('red')
        orientationOne.append(block1)
        block1.draw(win)

    orientationTwo = []
    for i in range(4):
        B1pt1 = Point(200,0 + i*40)
        B1pt2 = Point(240,40 + i *40)
        block1 = Rectangle(B1pt1,B1pt2)
        block1.setOutline('white')
        block1.setFill('red')
        orientationTwo.append(block1)

    maxOrientation = 2
    orientation = 1
    allCurrentRotations.clear()
    currentBlock = orientationOne
    allCurrentRotations.append(orientationOne)
    allCurrentRotations.append(orientationTwo)

def makeSquare():
    global maxOrientation, orientation, currentBlock

    orientationOne = []
    for i in range(4):
        if i > 1:
            pt1 = Point(120+i%2*40,0)
            pt2 = Point(120+(i%2+1)*40,40)
        else:
            pt1 = Point(120+i*40,40)
            pt2 = Point(120+(i+1)*40,80)
        block = Rectangle(pt1,pt2)
        block.draw(win)
        block.setOutline('white')
        block.setFill('blue')
        orientationOne.append(block)

    maxOrientation = 1
    orientation = 1
    allCurrentRotations.clear()
    allCurrentRotations.append(orientationOne)
    currentBlock = orientationOne

def makeLeft():
    global maxOrientation, orientation, blocksMakeAPiece, currentBlock

    maxOrientation = 4
    orientation = 1
    blocksMakeAPiece = 2

    orientationOne = []
    for i in range(4):
        if i == 3:
            pt1 = Point(120,0)
            pt2 = Point(160,40)
        else:
            pt1 = Point(120+i*40,40)
            pt2 = Point(120+(i+1)*40,80)
        block = Rectangle(pt1,pt2)
        block.draw(win)
        block.setOutline('white')
        block.setFill('blue')
        orientationOne.append(block)

    orientationTwo = []
    for i in range(4):
        if i == 3:
            pt1 = Point(160,0)
            pt2 = Point(200,40)
        else:
            pt1 = Point(120,i*40)
            pt2 = Point(160,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationTwo.append(block)

    orientationThree = []
    for i in range(4):
        if i == 3:
            pt1 = Point(200,40)
            pt2 = Point(240,80)
        else:
            pt1 = Point(120+i*40,0)
            pt2 = Point(120+(i+1)*40,40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationThree.append(block)

    orientationFour = []
    for i in range(4):
        if i == 3:
            pt1 = Point(120,80)
            pt2 = Point(160,120)
        else:
            pt1 = Point(160,i*40)
            pt2 = Point(200,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationFour.append(block)
        
    currentBlock.clear()
    currentBlock = orientationOne
    allCurrentRotations.append(orientationOne)
    allCurrentRotations.append(orientationTwo)
    allCurrentRotations.append(orientationThree)
    allCurrentRotations.append(orientationFour)

def makeRight():
    global maxOrientation, orientation, blocksMakeAPiece, currentBlock

    maxOrientation = 4
    orientation = 1
    blocksMakeAPiece = 2

    orientationOne = []
    for i in range(4):
        if i == 3:
            pt1 = Point(200,0)
            pt2 = Point(240,40)
        else:
            pt1 = Point(120+i*40,40)
            pt2 = Point(120+(i+1)*40,80)
        block = Rectangle(pt1,pt2)
        block.draw(win)
        block.setOutline('white')
        block.setFill('blue')
        orientationOne.append(block)

    orientationTwo = []
    for i in range(4):
        if i == 3:
            pt1 = Point(160,40)
            pt2 = Point(200,80)
        else:
            pt1 = Point(120,i*40)
            pt2 = Point(160,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationTwo.append(block)

    orientationTwo = []
    for i in range(4):
        if i == 3:
            pt1 = Point(160,80)
            pt2 = Point(200,120)
        else:
            pt1 = Point(120,i*40)
            pt2 = Point(160,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationTwo.append(block)

    orientationThree = []
    for i in range(4):
        if i == 3:
            pt1 = Point(120,40)
            pt2 = Point(160,80)
        else:
            pt1 = Point(120+i*40,0)
            pt2 = Point(120+(i+1)*40,40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationThree.append(block)

    orientationFour = []
    for i in range(4):
        if i == 3:
            pt1 = Point(120,0)
            pt2 = Point(160,40)
        else:
            pt1 = Point(160,i*40)
            pt2 = Point(200,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationFour.append(block)
        

    currentBlock.clear()
    currentBlock = orientationOne
    allCurrentRotations.append(orientationOne)
    allCurrentRotations.append(orientationTwo)
    allCurrentRotations.append(orientationThree)
    allCurrentRotations.append(orientationFour)

def makeLeftZ():
    global maxOrientation, orientation, blocksMakeAPiece, currentBlock

    maxOrientation = 2
    orientation = 1
    blocksMakeAPiece = 2

    orientationOne = []
    for i in range(4):
        if i > 1:
            pt1 = Point(120+i%2*40,0)
            pt2 = Point(120+(i%2+1)*40,40)
        else:
            pt1 = Point(160+i*40,40)
            pt2 = Point(160+(i+1)*40,80)
        block = Rectangle(pt1,pt2)
        block.draw(win)
        block.setOutline('white')
        block.setFill('blue')
        orientationOne.append(block)

    orientationTwo = []
    for i in range(4):
        if i > 1:
            pt1 = Point(120,40+(i%2)*40)
            pt2 = Point(160,40+(i%2+1)*40)
        else:
            pt1 = Point(160,(i%2)*40)
            pt2 = Point(200,(i%2+1)*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationTwo.append(block)

    currentBlock.clear()
    allCurrentRotations.append(orientationOne)
    allCurrentRotations.append(orientationTwo)
    currentBlock = orientationOne

def makeRightZ():
    global maxOrientation, orientation, blocksMakeAPiece, currentBlock

    maxOrientation = 2
    orientation = 1
    blocksMakeAPiece = 2

    orientationOne = []
    for i in range(4):
        if i > 1:
            pt1 = Point(160+i%2*40,0)
            pt2 = Point(160+(i%2+1)*40,40)
        else:
            pt1 = Point(120+i*40,40)
            pt2 = Point(120+(i+1)*40,80)
        block = Rectangle(pt1,pt2)
        block.draw(win)
        block.setOutline('white')
        block.setFill('blue')
        orientationOne.append(block)

    orientationTwo = []
    for i in range(4):
        if i > 1:
            pt1 = Point(120,(i%2)*40)
            pt2 = Point(160,(i%2+1)*40)
        else:
            pt1 = Point(160,40+(i%2)*40)
            pt2 = Point(200,40+(i%2+1)*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationTwo.append(block)

    currentBlock.clear()
    allCurrentRotations.append(orientationOne)
    allCurrentRotations.append(orientationTwo)
    currentBlock = orientationOne

def makeT():
    global maxOrientation, orientation, blocksMakeAPiece, currentBlock

    maxOrientation = 4
    orientation = 1
    blocksMakeAPiece = 2

    orientationOne = []
    for i in range(4):
        if i == 3:
            pt1 = Point(160,0)
            pt2 = Point(200,40)
        else:
            pt1 = Point(120+i*40,40)
            pt2 = Point(120+(i+1)*40,80)
        block = Rectangle(pt1,pt2)
        block.draw(win)
        block.setOutline('white')
        block.setFill('blue')
        orientationOne.append(block)

    orientationTwo = []
    for i in range(4):
        if i == 3:
            pt1 = Point(160,40)
            pt2 = Point(200,80)
        else:
            pt1 = Point(120,i*40)
            pt2 = Point(160,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationTwo.append(block)

    orientationThree = []
    for i in range(4):
        if i == 3:
            pt1 = Point(160,40)
            pt2 = Point(200,80)
        else:
            pt1 = Point(120+i*40,0)
            pt2 = Point(120+(i+1)*40,40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationThree.append(block)

    orientationFour = []
    for i in range(4):
        if i == 3:
            pt1 = Point(120,40)
            pt2 = Point(160,80)
        else:
            pt1 = Point(160,i*40)
            pt2 = Point(200,40+i*40)
        block = Rectangle(pt1,pt2)
        block.setOutline('white')
        block.setFill('blue')
        orientationFour.append(block)
        
    currentBlock.clear()
    currentBlock = orientationOne
    allCurrentRotations.append(orientationOne)
    allCurrentRotations.append(orientationTwo)
    allCurrentRotations.append(orientationThree)
    allCurrentRotations.append(orientationFour)
    
def makeRandomShape():
    global totalBlocks

    totalBlocks+=1
    x = random.randint(1,7)
    if x == 1:
        makeStraight()
    elif x == 2:
        makeSquare()
    elif x == 3:
        makeLeft()
    elif x == 4:
        makeRight()
    elif x == 5:
        makeLeftZ()
    elif x == 6:
        makeRightZ()
    elif x == 7:
        makeT()
    setLowestTarget()

def blockAtBottom(c):
    for block in currentBlock:
        x = int(block.getP1().getX()/40)
        y = int(block.getP1().getY()/40)
        if(y == 19 or blockFilled[y+c][x]):
            return True
    return False

def blockAtLeft():
    for block in currentBlock:
        x = int(block.getP1().getX()/40)
        y = int(block.getP1().getY()/40)
        if(x == 0 or blockFilled[y][x-1]):
            return True
    return False

def blockAtRight():
    for block in currentBlock:
        x = int(block.getP1().getX()/40)
        y = int(block.getP1().getY()/40)
        if(x==9 or blockFilled[y][x+1]):
            return True
    return False

def invalidRotate():
    global orientation, maxOrientation, currentBlock
    tempOR = orientation - 1

    if tempOR + 1 == maxOrientation:
        tempOR = 0
    else:
        tempOR += 1

    for block in allCurrentRotations[tempOR]:
        x = int(block.getP1().getX()/40)
        y = int(block.getP1().getY()/40)
        if(x>9 or y > 19 or blockFilled[y][x]):
            return True
    return False

def drop():
    while not blockAtBottom(1):
        for piece in allCurrentRotations:
            for block in piece:
                block.move(0,40)
    win.redraw()
    setNewHeight()
    completedRow()
    gameLost()
    allCurrentRotations.clear()
    currentBlock.clear()
    makeRandomShape()

def gameLost():
    global gameOver
    for block in currentBlock:
        y = int(block.getP1().getY()/40)
        if y == 0:
            gameOver = True

def setNewHeight():
    for block in currentBlock:
        x = int(block.getP1().getX()/40)
        y = int(block.getP1().getY()/40)
        blockFilled[y][x] = True
        blockBoard[y][x] = block

def completedRow():
    global score, totalLines

    count = -1
    firstCompleted = -10
    numCompleted = 0

    for row in blockBoard:
        count+=1
        isCompleted = True
        for block in row:
            if block == '':
                isCompleted = False
        if isCompleted:
            if(firstCompleted == -10):
                firstCompleted = count
            numCompleted+=1
            temp = []
            temp2 = []
            for block in row:
                temp.append('')
                temp2.append(False)
                block.undraw()
            blockFilled[count] = temp2
            blockBoard[count] = temp
    if numCompleted>0:
        totalLines += numCompleted
        lowerAllAbove(numCompleted,firstCompleted)
        if numCompleted == 1:
            score += 40
        elif numCompleted == 2:
            score += 100
        elif numCompleted == 3:
            score += 300
        elif numCompleted == 4:
            score += 1200

def lowerAllAbove(numCompleted,row):
    print(row)
    for i in reversed(range(row)):
        for z in range(10):
            if blockBoard[i][z] != '':
                if(19-i<numCompleted):
                    numCompleted = 19-i
                temp = blockBoard[i][z]
                blockBoard[i][z].move(0,40*numCompleted)
                blockBoard[i][z] = ''
                blockFilled[i][z] = False
                blockFilled[i+numCompleted][z] = True
                blockBoard[i+numCompleted][z] = temp

def levelUp():
    global totalLines,pace,level
    if(totalLines >= 10):
        totalLines = 0
        level+=1
        levelText.setText("Level: " + str(level))
        pace = pace/1.1

def lowestDropAi():
    global pace
    pace = 1

    if(orientation-1 != lowestDropAiInfo[1]):
        return 'r'
    if(int(currentBlock[lowestDropAiInfo[2]].getP1().getX()/40)>lowestDropAiInfo[0]):
        return 'a'
    if(int(currentBlock[lowestDropAiInfo[2]].getP1().getX()/40)<lowestDropAiInfo[0]):
        return 'd'
    return 'space'

def setLowestTarget():
    global lowestDropAiInfo
    dropInfo = [100,100,100,-10000000]
    count = 0

    for orentaion in allCurrentRotations:
        listOfX = []
        lowestOfCurrentOrentaionBlocks = []
        lowestOfAllX = []
        for x in range(0,10):
            b1y = orentaion[0].getP1().getY()
            b2y = orentaion[1].getP1().getY()
            b3y = orentaion[2].getP1().getY()
            b4y = orentaion[3].getP1().getY()
            b2XDiff = int((orentaion[1].getP1().getX() - orentaion[0].getP1().getX())/40)
            b3XDiff = int((orentaion[2].getP1().getX() - orentaion[0].getP1().getX())/40)
            b4XDiff = int((orentaion[3].getP1().getX() - orentaion[0].getP1().getX())/40)

            while b1y < 800 and b2y < 800 and b3y < 800 and b4y < 800 \
            and x + b2XDiff <= 9 and x + b3XDiff <= 9 and x + b4XDiff <= 9 \
            and not blockFilled[int(b1y/40)][x]\
            and not blockFilled[int(b2y/40)][x + b2XDiff]\
            and not blockFilled[int(b3y/40)][x + b3XDiff]\
            and not blockFilled[int(b4y/40)][x + b4XDiff]:
                b1y+=40
                b2y+=40
                b3y+=40
                b4y+=40
            lowestOfAllX.append(max(b1y,b2y,b3y,b4y))
        lowestOfCurrentOrentaionBlocks.append(max(lowestOfAllX))
        listOfX.append(lowestOfAllX.index(max(lowestOfAllX)))

        if dropInfo[3] < max(lowestOfCurrentOrentaionBlocks):
            dropInfo[0] = listOfX[lowestOfCurrentOrentaionBlocks.index(max(lowestOfCurrentOrentaionBlocks))]
            dropInfo[1] = count
            dropInfo[2] = 0
            dropInfo[3] = max(lowestOfCurrentOrentaionBlocks)
        count+=1
    lowestDropAiInfo = dropInfo

def recordData():
    global controlType,score,timeNow,timeStart,totalLines
    print('*****************************************************************')
    f = open("runData.txt", "a")
    f.write("\n" + str(controlType) + " " + str(score) + " " + str(timeNow-timeStart) + " " + str(totalLines) + " " + str(totalBlocks))
    f.close()

playAgain = True
while playAgain:
    makeBoard()
    runGame()
    gameOver = False
    totalBlocks = 0
    win = GraphWin('Tetris',600,800)
    orientation = 0
    maxOrientation = 0
    allCurrentRotations = []
    currentBlock = []
    blocksMakeAPiece = 0
    gameOver = False
    timeNow = time.time()
    timeLast = time.time()
    pace = 1
    totalLines = 0
    score = 0
    level = 1
    scoreText = Text(Point(500,260),"Score: " + str(score))
    levelText = Text(Point(500,280),"Level: " + str(level))
    controlType = "RandomAi"
    blockFilled = []
    blockBoard = []