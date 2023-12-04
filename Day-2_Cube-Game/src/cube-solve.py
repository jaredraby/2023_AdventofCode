# Total number of cubes in play
maxRedCount = 12
maxGreenCount = 13
maxBlueCount = 14
redSum = 0
greenSum = 0
blueSum = 0



# 
gameIndex = 1
validGameSum = 0

cubeCounts = 0

# Open the file and read in the puzzle data
with open('puzzle-input.txt') as file:
    # Read in the content for the puzzle game results
    puzzleResults = file.read().splitlines()
    
    
for line in puzzleResults:
    cubeCounts = line.split(":")[1].split(";")
    print(f'Game {gameIndex} : {cubeCounts}')
    handIndex = 1
    cubeHands = {"red" : 0, "blue" : 0, "green" : 0}
    for game in cubeCounts:
        print(f"Hand {handIndex} : {game}")
        for
        
        handIndex += 1
        
        
        
        
    

    
    gameIndex += 1


    
