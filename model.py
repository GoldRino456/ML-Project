from os import system, name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, metrics, model_selection

#####################################################
#
# Helper Functions
#
#####################################################

def clear(): #Used to keep the User Interface from getting overcrowded with Text.
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def buildScatterplot(userScores, estimatedOwners):
    plt.scatter(userScores, estimatedOwners, c="red")
    plt.xlabel("User Score Percentage (Calculated based on Positive and Negative User Feedback)")
    plt.ylabel("# of Estimated Owners")
    plt.title("Estimated Owners vs User Score")
    plt.show()

def getRangeOfScores(userScores):
    #Function assumes range is as follows: <50%, 50% - 60%, 60% - 70%, 70% - 80%, 80% - 90%, >90%
    gamesInScoreRange = [0, 0, 0, 0, 0, 0]

    for game in userScores:
        if game < 0.5:
            gamesInScoreRange[0] += 1
        elif game <= 0.6:
            gamesInScoreRange[1] += 1
        elif game <= 0.7:
            gamesInScoreRange[2] += 1
        elif game <= 0.8:
            gamesInScoreRange[3] += 1
        elif game <= 0.9:
            gamesInScoreRange[4] += 1
        elif game >= 0.9:
            gamesInScoreRange[5] += 1

    return gamesInScoreRange

def buildPieChart(userScores):

    scoreRangeLabels = ["<50%", "50% - 60%", "60% - 70%", "70% - 80%", "80% - 90%", ">90%"]
    gamesInScoreRange = getRangeOfScores(userScores)

    plt.pie(gamesInScoreRange, labels = scoreRangeLabels)
    plt.title("Average User Score of All Games")
    plt.show()

def buildBarChart(listOfTags):
    listOfTags.sort()
    countedTags = dict()

    for tag in listOfTags: 
        if countedTags.keys() == None or countedTags.get(tag, -1) < 0:
            countedTags.update({tag : 1})
        else:
            count = countedTags.get(tag) + 1
            countedTags.update({tag : count})
        

    sortedCountedTags = sorted(countedTags, key= countedTags.get, reverse= True)
    sortedCountedTags = sortedCountedTags
    sortedCountedTagsValue = list()

    for tag in sortedCountedTags:
        sortedCountedTagsValue.append(countedTags.get(tag))

    plt.bar(sortedCountedTags[:10], sortedCountedTagsValue[:10])
    plt.title("Top 10 Most Common Tags")
    plt.show()  

#####################################################
#
# Import CSV Data as Dataframe
#
#####################################################

#Create DataFrame from CSV file
print("Reading in game data... ")
gamedata = pd.read_csv('data.csv')

#####################################################
#
# Get Tags from Data
#
#####################################################
gameTagList = list()

#Get a full list of Tags
for row in gamedata.index:
    tags = gamedata.loc[row, "Tags"].split(",") #Split tags into individual strings
     #add tags to gameTags list
    for tag in tags:
        gameTagList.append(tag)

gameTagList = np.unique(gameTagList)
gameTagList = gameTagList.tolist()

#####################################################
#
# Construct Model's Dataframe
#
#####################################################
#(Row - Games, Column - Individual Tags, Final Column - User Score (Positive / (Positive + Negative)))
columnList = gameTagList.copy()
columnList.insert(0, "AppID")

rowValues = list()

for row in gamedata.index:
    toInsert = [0] * (len(columnList)) #Create a list of 0s for all possible tags
    toInsert[0] = gamedata.loc[row, "AppID"]

    for tag in gamedata.loc[row, "Tags"].split(","):
        toInsert[columnList.index(tag)] = 1 #Mark tags the game does have as 1

    rowValues.append(toInsert) #append AppID value and tag values to rowValues

modelDF = pd.DataFrame(columns= columnList, data= rowValues)

#Add User Score Value to the end of Dataframe
modelDF["User score"] = gamedata["Positive"] / (gamedata["Positive"] + gamedata["Negative"])

#####################################################
#
# Train Model on Data
#
#####################################################

linearRegModel = linear_model.LinearRegression()
x = modelDF.loc[:, modelDF.columns[1] : modelDF.columns[len(modelDF.columns) - 2]] #Tags Present (All columns exclusing first and last)
y = modelDF.loc[:, "User score"] #AVG User Score (final column)
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state= 50)

linearRegModel.fit(x_train, y_train)
y_pred = linearRegModel.predict(x_test)

clear()
print("************************************************")
print("Model successfully trained on data, MSE Result: ")
print(metrics.mean_squared_error(y_test, y_pred))
print("************************************************")

#####################################################
#
# Loop to Allow User to Input Tags / View Visualizations
#
#####################################################

isExiting = False

while(not isExiting):
    print("\n\n************************************************")
    print("\nPlease enter a combinations of Tags to recieve a user score prediction. Tags must be separated by a \",\".")
    print("\nExample Input: Zombies,World War II,Action,Puzzle\n")
    print("\n************************************************")
    print("\nTo see a list of all tags, please enter \"1\" below.")
    print("To view visualizations of the collected data, please enter \"2\" below.")
    print("To exit the program, please enter \"3\" below.\n")
    print("\nAll input is CASE-SENSITIVE.\n")
    print("************************************************")
    userInput = input("\n\nPlease enter a combination of tags: ")

    if userInput == "1":
        clear()
        print("\nList of Steam Tags:\n")
        print(gameTagList)
        print("\n\n")
        continue
    if userInput == "2":

        chartSelection = "0"
        while chartSelection != "4":
            clear()
            print("\nPlease enter the number of th diagram you wish to view:\n")
            print("1 - User Score to Estimated Owners of a Game (Scatterplot)")
            print("2 - User Score Range of All Games (Pie Chart)")
            print("3 - Top 10 Most Common Tags (Bar Chart)")
            print("4 - Go Back to Main Menu")
            print("\n\n")

            chartSelection = input("Selection: ")

            if chartSelection == "1":
                buildScatterplot(modelDF["User score"].to_list(), gamedata["Estimated owners"].to_list())
            if chartSelection == "2":
                buildPieChart(modelDF["User score"].to_list())
            if chartSelection == "3":
                allGameTags = list()

                for row in gamedata.index:
                    for tag in gamedata.loc[row, "Tags"].split(","):
                        allGameTags.append(tag)

                buildBarChart(allGameTags)
        continue
    if userInput == "3":
        clear()
        print("\nExiting Program...")
        isExiting = 1
        continue

    #Check if inputted tags exist
    validInput = True
    splitStrings = list()

    for string in userInput.split(","):
        if gameTagList.count(string) < 1:
            clear()
            print("\nTag \"" + string + "\" not found. Please check spelling and capitialization and try again.")
            validInput = False
            break
        else:
            print("\nValid Tag: " + string + ".")
            splitStrings.append(string)
    
    if validInput:
        clear()
        print("Prediction For a Game with the Following Tags: " + userInput)

        #Set tags up for prediction
        predictionData = [0] * len(columnList)

        for tag in splitStrings:
            predictionData[columnList.index(tag)] = 1 #Set Tag to 1 to indicate present on game

        df = pd.DataFrame([predictionData], columns= columnList)
        print("Estimated User Score: ")
        print(linearRegModel.predict(df.loc[:, df.columns[1] : df.columns[len(df.columns) - 1]]))


