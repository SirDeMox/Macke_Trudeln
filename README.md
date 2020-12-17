# Macke Trudeln - Rules
A Repos to solve the German Dice Game "Macke Trudeln" or "Macke".


## Setup:
You play with 5 6-sided dice.

A round consists of:

- rolling all dice  
- put aside (take out) any dice which grant you points and 
- decide to either score those points and stop rolling, or keep rolling the _remaining dice_.
- continue this for as long as you want until you roll a _Macke_ or stop.

## How dice score points:
All 1s are worth 100 points.
All 5s are worth 50 points.
All three-of-a-kinds (toak) are worth their pips * 100 (toak of 2s is 200 points)
    - except for three 1s, they are worth 1000 points.

## Stopping
If you decide to stop rolling, you note down all the points you accumulated this round and it's the next players turn.

## Keep rolling
If you decide to keep rolling, you take all the remaining dice (those, which you rolled, but havn't scored points) and roll all of them again.

## Macke
If you roll dice, but none of the dice are scoring, you lose all the points accumulated this round and it's the next players turn. You just rolled (old German word: "Trudeln") a "Macke" (old German word for an inperfection).

## Forced Continue
If you successfully score all 5 of your dice, you have to roll all 5 dice again, following the same rules. I call those instances "resets". Resets are your way to really score highly in one round, as the score adds up.

## Winning
You usually play in a clockwise rotations and players play games and note down points until they reached 5000 points. First to reach 5000 points wins the session.

## Notes
If you score multiple dice, lets say you roll 1-1-5-2-4, you can choose which dice you want to score. You can take out 1-1-2 and decide how you want to handle the remaining two dice. Or you can choose to only take out a subset of 1-1-2. The only rule is: you have to take out at least one dice.
You can not take out 2s, 3s, 4s or 6s unless you roll a three-of-a-kind, if so, you must take out three of them, or none at all (you can't take out four of a kind for example).

# Code

There are 4 classes responsible for playing the game.

# DiceRolls

The class rolls n (1-5) dice, or takes in a list of predetermined rolls.
Afterwards it:
- evaluates macke,
- detect toaks,
- counts remaining dice and
- scores _pointsbefore_
- returning itself

# PlayGame

The class plays a game according to a _method_ and a _threshold_. These parameters determine when the game stops rolling. The class rolls until the contitions are met.
- rolls dice with **DiceRolls**
- check for macke
- score
- interpret methods and thresholds
- repeat

# RunSession

The class takes a _method_, a _threshold_, as well as a _special_ parameter. It uses the **PlayGame** to run games until it reaches 5000 points.

# CreateSummaryData

This class is a wrapper for **RunSession** which runs the session n times. It can check for a wide range of thresholds and outputs a pd.DataFrame