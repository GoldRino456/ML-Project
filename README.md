# ML Project
 
A machine learning project using sklearn's libraries. Originally created for my university capstone project.

This program uses linear regression to train a model on video game data collected in a csv file. Using the command line, users can input Steam game tags to get a user score in return, estimating the likely user score of a new game introduced to the marketplace. The user can also view a few different visual aids created from the csv file data.

Data used for this project was collected from the following Kaggle dataset and tested up to 7k entries: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset?select=games.csv

Estimations provided by the program are NOT accurate. This program focused on a hypothetical business application of machine learning and demonstrates how one could implement linear regression. To more accurately estimate the user score of a game on Steam with a given set of tags it is recommended to use a different learning model, take more information into consideration (such as hardware requirements, ESRB rating, price, sale frequency, etc), and process a much larger amount of entries.
