import re

lineCount = 1
parsedCalValues = []
Total = 0



# Input will be alpha numeric string with numbers written out in text
# Function substitutes out the written out numeric value with equivilant
# digit then strips out non-numeric characters and returns the string
# of only numbers.
def replaceSubstrings(line, numberDic):
    regExp = "|".join(numberDic.keys())
    regExp = r"(?=(" + regExp + "))"
    pattern = re.compile(regExp)
    matchesFindAll = pattern.findall(line)
    matchesReIter = pattern.finditer(line)
    
    currentSpan = (0,0)
    currentStart = 0
    currentEnd = 0
    currentMatch = ""
    priorSpan = (0,0)
    priorStart = 0
    priorEnd = 0
    priorMatch = "N/A"
    overlapString = ""
    overlapStart = 0
    overlapEnd = 0
    overlapCount = 0
    
    # print(f"Line {lineCount} | {line}")
    for each in matchesReIter:
        currentSpan = each.span(1)
        currentStart = currentSpan[0]
        currentEnd = currentSpan[1]
        currentMatch = each[1]
        # print(f"Current match {currentMatch} [{currentStart},{currentEnd}] | Prior match {priorMatch} [{priorStart},{priorEnd}]")
        if currentStart < priorEnd:
            overlapCount += 1
            if overlapCount == 1:
                overlapString = priorMatch + currentMatch
                overlapStart = priorStart
                overlapEnd = currentEnd
            else:
                overlapString = overlapString + currentMatch
                overlapEnd = currentEnd
                
        priorSpan = currentSpan
        priorStart = currentStart
        priorEnd = currentEnd
        priorMatch = currentMatch
    
    print(f"Line {str(lineCount)} | {line} | Original")
     
    if overlapCount >= 1:
        # print(f"Line {str(lineCount)} | {line} | Overlap Count {overlapCount} | Overlap String: {overlapString}, {overlapStart},{overlapEnd}")
        line = line[:overlapStart] + overlapString + line[overlapEnd:]
        # print(f"Line {str(lineCount)} | Single Overlaps")
        
        # if overlapCount > 1:
            #print(f"Line {str(lineCount)} | Multiple Overlaps")
    
    print(f"Line {str(lineCount)} | {line} | Compensated if req")
    
    regExp = "|".join(numberDic.keys())
    regExp = r"((" + regExp + "))"
    pattern = re.compile(regExp)
    
    if len(matchesFindAll) > 0:
        line = pattern.sub(lambda m: numberDic[m.group(0)], line)
    else:         
        line = line
        
    if len(pattern.findall(line)) > 0:
        print(f"Line {lineCount} : Missed a number word!")
        
    print(f"Line {str(lineCount)} | {line} | Final")
   
    return line
    # return re.sub("[^0-9]", "", line)
    
# Function to return a two digit string from the input.
# For strings =>2 in length, it take the first and last and return it
# For strigs <2 in length, it puts that digit into the first and last places
def digitStrip(line):
    line = re.sub("[^0-9]", "", line)
    if len(line) < 2:
        line = line[0] + line[0]
        return line
    else:
        line = line[0] + line[len(line)-1]
        return line


# Open the file in read mode
with open('cal-values.txt', 'r') as file:
    # Read all the unparsed calibration values in
    unparsed_file = file.read()

# Split the file into series of lines for parsing
unparsed_lines = unparsed_file.split('\n')

# Perform replacement of all the numbers which are written out and replace with
# the numeric equivilant
for line in unparsed_lines:
    # Dictionary with the regex match | replacement pairs used for parsing
    # Numbers with zero included
    # numbers = {"zero" : "0", "one" : "1", "two" : "2", "three" : "3", "four" : "4", "five" : "5", "six" : "6", "seven" : "7", "eight" : "8", "nine" : "9"}
    # Number without zero included
    numbers = {"one" : "1", "two" : "2", "three" : "3", "four" : "4", "five" : "5", "six" : "6", "seven" : "7", "eight" : "8", "nine" : "9"}
    
    # Calls function to replace all words with number
    numberString = replaceSubstrings(line, numbers)
    twoDigit = int(digitStrip(numberString))
    
    # Calls function to strip non-digits out and return first and last number
    # twoDigit = int(digitStrip(line))
    
    
    # print(f"Line {str(lineCount)}  Final: {str(twoDigit)} | Original : {line}")
    parsedCalValues.append(twoDigit)
    lineCount += 1

totalCalibrationSum = sum(parsedCalValues)
print("Total : " + str(totalCalibrationSum))
 