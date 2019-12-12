# MP4---Classification Competition

# DUE: Sunday Nov 24 11:59pm

MP4 is an optional assignment and anyone passes the baseline would get a score that weighs extra 2% of total grade + Min (0, [TheirRank-BaselineRank]/[TopRank-BaselineRank] * 1%). For example, the student ranking 1st would get a total of 3% extra credit. The student just passed baseline would get 2% extra credit. 

In this assignment, we will use the MeTA toolkit to participate in a classification competition.
Our dataset comes from a real-word application: predicting the location of twitter users from their textual posts/tweets!
All twitter users are from the [Contiguous U.S.](https://en.wikipedia.org/wiki/Contiguous_United_States) and can be classified into *4 classes*, which represent the main four U.S. regions (Northeast, Midwest, South and West) as defined by the [Census Bureau](https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf)

All MPs are checked on [EWS machines](https://answers.uillinois.edu/illinois.engineering/page.php?id=81727).
While we cannot ensure that all operating systems and configurations are covered in the instructions, students can connect to these Linux-based workstations to complete assignments.

Also, you are free to edit all files **except**:
- .gitginore
- .gitlab-ci.yml
- timeout.py
- competition.py
- requirements.txt

**Your goal is to train a classifier that *beats* (i.e. being *better* than and not equal to) the baseline found on [the leaderboard](http://cs410-classify.centralus.cloudapp.azure.com/).**

## Setup
We'll use [metapy](https://github.com/meta-toolkit/metapy)---Python bindings for MeTA.
If you have not installed metapy so far, use the following commands to get started.

```bash
# Ensure your pip is up to date
pip install --upgrade pip

# install metapy!
pip install metapy pytoml
```

If you're on an EWS machine
```bash
module load python3
# install metapy on your local directory
pip install metapy pytoml --user
```

## Competition Setup
For this assignment, you will have to setup the `GITLAB_API_TOKEN` and the `COMPETITION_ALIAS`  the same way we did for MP2.

## Training a classifier
This repository contains what you need to begin participating in
the classification competition. You will want to change the code in the
`make_classifier()` function in the file `classify.py` to use a different
classifier. You might also want to try changing your feature
representation by modifying the `[[analyzers]]` table array in
`config.toml`.

Thus, the only files that you will have to update are `classify.py` and `config.toml`.
Please do not edit the rest of the files in the repository, as you might experience issues with submitting.

A nice tutorial about text classification with metapy, as well as some config.toml files
can be found [here](https://github.com/meta-toolkit/metapy/blob/master/tutorials/4-classification.ipynb).

## Submitting Results
With that all configured, you should be done! Now whenever you push code to
this repository (note that you need to commit locally first, and then push
to the repository here because we're using `git`), it should automatically
update the leaderboard. You can see the output of the job by looking in the
"Pipelines" section on your repository.

You can play with things locally by using the "train" dataset we provided.

```bash
python classify.py config.toml
```
Note that the datasets we are using for the leaderboard are different, so the accuracy running locally with  the "train" dataset will vary from the leaderboard score.


Good luck!
