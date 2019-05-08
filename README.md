# superrugby-predictor

Machine learning approach to predicting score margins for super rugby games, using historic results and bookmakers' odds.

Data is from the website www.aussportsbetting.com, which provides historic match and betting odds data for Super Rugby matches since 2009.

Mainly for fun, this is a collaborative effort between friends in their spare time.

*To-Do*

- Develop web scraper notebook to pull the odds data from oddsportal.com. This would need to spit out a csv file which contains all the games, including the upcoming ones. Scores for upcoming games can be set to zero (not blank), as these rows are dropped when training the model.
  - Kieran to package all of the web scraping code into a `.py` module that can be called in the main `app.py` script to keep the predictions up to date.
- Build out working version of dashboard to include the option for users to interact and generate predictions. Tabs/charts to include:
  - Results viewer: central view of historic results data with ability to sort and filter
  - Team viewer: view of a single team, displaying current form
  - Forecaster: view of model predictions and how they compare to bookmakers' odds


## Git  
![git logo](http://shijuvarghese.com/wp-content/uploads/2018/03/git-logo.png)

Since we are pretty new to Git, we will be creating our own guidelines as we go.   

> Avoid pushing directly to Master branch. Instead, checkout a new branch and work there.

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
When you are ready to push changes from local to remote, you can first do a precautionary check to see what your changes are:
```console
$ git status

$ git diff <filename>
```

Then push your changes:
```console
$ git add <filename>

$ git commit -m 'write a useful commit message here'

$ git push
```

**Staying up to date with remote**   
When you return to work on your computer, remember to fetch any changes which might have been added by others while you were away.   

The `fetch` command downloads data from the remote repository, but does **not** integrate any changes into your working files:
```console
$ git fetch
```

The `pull` command, on the other hand, tries to merge changes from the remote branch into your local files:
```console
$ git pull
```
This is essentially a pull request between remote and local version of the same branch.   

Assuming your local repository was completely up to date the last time you worked on it, you should be able to do a pull request without any conflicts.   

However, if you make some changes **before** pulling from the remote, you will then end up with merge conflicts when you try to push or pull to/from remote.   

This is why it is a good idea to pull from remote **before** making new changes locally.
