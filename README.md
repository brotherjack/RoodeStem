# RoodeStem
**Current Version: 0.3.1 - {Nudey Monkey - Nude Again for the First Time}**

Voting simulator and ethereum group decision making engine.

### State:

* Ethereum group decision making engine is fully ethereal. Like not there at all. Not yet. Working on it. Will do, probably. Eventually. Maybe.
    * The current plan is to have a program which can generate contracts in Solidity which will implement the different voting conventions outlined in the simulator. 

* Voting simulator contains two EXCITING simulations. You can make more too. Can't install them yet. HAH!

### Install / Basic Use Guide:

Runs as a standard python program on the command-line. I won't explain how to install Python, you can go to python.org to do that. Install you some Python3 if you haven't already.

Dependencies can be installed via pip, specifically running `pip install -r requirements.txt`. If you want to install the development tools being used then run `pip install -r requirements/dev.txt`, in addition to the previous command.

Just run `python setup.py install`, as is customary.

##### Using the command line program

Currently the two simulations can be run by "`roodestem scenario run` \<ScenarioName/alias\>"

`roodestem scenario --list` shows scenario names with spaces, and their respective aliases. 



### Revision History: 
______________________________________
| Version Number | Release Name | Notes                                                        |
-----------------|--------------|--------------------------------------------------------------|
| 0.0.1            |              | Added test for detecting Condorcet Paradox |
| v0.1.0           |              | Basic BordaCount and CondorcetMethod available for simulation. |
| v0.1.1           |              | Profit?
| v0.1.2           |              | Improved Result class
| v0.1.3           |              | Added simulations package with Scenario and RadomCondorcet classes.
| v0.2.1           |              | New system for implementing scenarios as plugins.
| v0.2.2           |              | Fixed several bugs concerning results.
| v0.2.3           | Nudey Monkey - Alpha Business                | Added usable CardinalVote class |
| v0.2.4           | Nudey Monkey - Alpha Business  | Added RankedBallot              |
| v0.3.0           | Nudey Monkey - Nude Again for the First Time | Added Voters, VotingMetrics, and NolanCharts              |
| v0.3.1           | Nudey Monkey - Nude Again for the First Time | Added PluralityBallot              | 
| v0.3.2           | Nudey Monkey - Nude Again for the First Time | Added labels to the positions NolanChart |          

