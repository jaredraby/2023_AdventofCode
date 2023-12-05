import re

# Total number of cubes in play
maxRedCount = 12
maxGreenCount = 13
maxBlueCount = 14
gameIndex = 1
validGameSum = 0

def handCheck(hands, indexCount):
    # Break down the hands into the distinct key/value pairs for red / green / blue
    for colorPair in hands.split(','):
        colorPair = colorPair.strip()
        pattern = re.compile(r'\w*[^\s]')
        colorPair = pattern.findall(colorPair)
        cubeHands[colorPair[1]] = int(colorPair[0])
        
    if cubeHands["blue"]<=maxBlueCount and cubeHands["red"]<=maxRedCount and cubeHands["green"]<=maxGreenCount:
        return True
    else:
        return False

# Open the file and read in the puzzle data
with open('puzzle-input.txt') as file:
    # Read in the content for the puzzle game results
    puzzleResults = file.read().splitlines()      
    
for line in puzzleResults:
    # print(f"Game {gameIndex}")
          
    # Split all the hands out coming from each game
    cubeCounts = line.split(":")[1].split(";")
    # Set up the dictionary to perform the tracking of the color sums for each game
    cubeHands = {"red" : 0, "blue" : 0, "green" : 0}
    handIndex=1
    gameValidation = True
    # After breaking down the line for each game, go through the hands in each game
    for hands in cubeCounts:
        gameValidation = handCheck(hands,handIndex) & gameValidation
        handIndex += 1
        
    print(f"Game {gameIndex} Validation: {gameValidation}")
    if gameValidation:
        validGameSum += gameIndex
        
    gameIndex += 1

print(f"Total Game Sum : {validGameSum}")    
