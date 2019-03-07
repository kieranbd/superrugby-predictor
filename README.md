# superrugby-predictor

This is a Python Jupyter notebook which uses a random forest model to predict the scores for upcoming Super Rugby games.

Data is from the website www.aussportsbetting.com, which provides historic match and betting odds data for Super Rugby matches since 2009.

*To-Do*

- Develop web scraper notebook to pull the odds data from oddsportal.com. This would need to spit out a csv file which contains all the games, including the upcoming ones. Scores for upcoming games can be set to zero (not blank), as these rows are dropped when training the model.
