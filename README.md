# superrugby-predictor

Machine learning approach to predicting score margins for super rugby games, using historic results and bookmakers' odds.

Data is from the website www.aussportsbetting.com, which provides historic match and betting odds data for Super Rugby matches since 2009.

Mainly for fun, this is a collaborative effort between friends in their spare time.

*To-Do*

- Develop web scraper notebook to pull the odds data from oddsportal.com. This would need to spit out a csv file which contains all the games, including the upcoming ones. Scores for upcoming games can be set to zero (not blank), as these rows are dropped when training the model.
- Build out working version of dashboard to include the option for users to interact and generate predictions. Tabs/charts to include:
  - Results viewer: central view of historic results data with ability to sort and filter
  - Team viewer: view of a single team, displaying current form
  - Forecaster: view of model predictions and how they compare to bookmakers' odds


## Git  
![git logo](https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png)

Since we are pretty new to Git, here are some guidelines:

Avoid pushing directly to Master branch. Instead, checkout a new branch and work there.

**Switching branches**   
To create a new branch locally:
```console
git checkout -b <branchname>
```

To switch to a remote branch:
```console
git checkout --track origin/<branchname>
```

**Making changes**   
When you are ready to push changes from local to remote:
```console
$ git add <filename>

$ git commit -m 'write a useful commit message here'

$ git push
```
