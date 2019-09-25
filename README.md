# NFL Survivor Pool Picker 🏈

Found yourself in an NFL Survivor Pool but don't know anything about football? Don't worry, we've got you covered.

NFL Survivor Picker is a command line application to help you make picks in NFL Survivor Pools. Features include
* Scraper to fetch probabilities for all games in NFL season from fivethirtyeight.com
* Read in user specified NFL season and game probabilities
* Make picks using greedy algorithm or globally optimal linear programming algorithm

![](demos/make_picks.gif)

## Installation

## Usage


## Background

NFL Survivor is a fantasy sports game where participants pick one NFL team per week to win their matchup. If the picked team wins then the participant stays in the pool but if they lose then they are out of the game. The tricky bit is that a participant cannot pick the same team more than once. The last participant standing is crowned the winner of the pool (subject to tiebreakers if multiple participants have no losses at the end of the 17 week season).

## Algorithms

For the sake of our analysis we will assume that the probabilities that teams win their matchups in each week of the NFL season is given to us. Our problem is how to optimally pick one team for each week of the season without picking the same team twice. Optimality means that the probability of making it through the entire season is the highest.

### Greedy Algorithm

An intuitive approach is to make our picks greedily. That is, in week one we select the team with the highest win probability. This team is now labeled "picked" for the sake of selecting future teams. In each subsequent week we select the team with the highest win probability across all teams that we have not yet "picked" and add it to our set of "picked" teams. In this way, we pick a unique team per week for each week of the season.

For example, we may have the season

| Week 1  | Probability | Week 2  | Probability |
|---------------------|-------------|---------------------|-------------|
| NY Giants | 0.75  | NY Giants | 0.99  |
| NY Jets | 0.25  | Dallas Cowboys  | 0.1 |
| | | | |
| Dallas Cowboys  | 0.45  | NY Jets | 0.55  |
| Philadelphia Eagles | 0.55  | Philadelphia Eagles | 0.45  |

In the first week we pick the NY Giants since they have the highest win probability in that week. In the second week, the NY Giants again have the highest win probability but we have unfortunately picked them already. In week 2, we settle for the highest win probability across all teams we haven't picked yet which is the NY Jets.

This example illustrates that the greedy algorithm may not produce a set of picks that has the optimal probability of making it through the entire season. With the picks determined by the greedy algorithm we have a probability of  ![equation](https://latex.codecogs.com/gif.latex?0.75%20*%200.55%20%5Capprox%200.41) of making it through the season. However, the optimal set of picks are taking the Philadelphia Eagles in week 1 followed by the NY Giants in week 2 which has a probability of ![equation](https://latex.codecogs.com/gif.latex?0.55%20*%200.99%20%5Capprox%200.54) of making it through the season. Our greediness forced us to into picking the NY Giants in week 1 and then forbid us from selecting them again in their blowout matchup in week 2. We were better off picking a lower probability team in week 1 to save the NY Giants for our week 2.

Further, the greedy approach may not even successfully determine a team to pick for every week of the season. If our greediness forces us to pick a set of teams in the first ![equation](https://latex.codecogs.com/gif.latex?n) weeks and then in week ![equation](https://latex.codecogs.com/gif.latex?n&plus;1) the only teams playing are the ones we picked in weeks ![equation](https://latex.codecogs.com/gif.latex?1)  through ![equation](https://latex.codecogs.com/gif.latex?n) then we will not be able to select a team in week ![equation](https://latex.codecogs.com/gif.latex?n&plus;1). The schedule below shows such an example

| Week 1  | Probability | Week 2 | Probability | Week 3 | Probability |
|-----------|-------------|----------------|-------------|----------------|-------------|
| NY Giants | 0.9 | NY Jets  | 0.2 | NY Giants  | 0.7 |
| NY Jets | 0.1 | Dallas Cowboys | 0.8 | Dallas Cowboys | 0.3 |

In week 1 we pick the NY Giants and then in week 2 we pick the Dallas Cowboys. However, this leaves us without a team to pick in the third week's matchup between the NY Giants and the Dallas Cowboys. However, in practice this will likely not be an issue for the algorithm since real life NFL schedules are not this pathological.  There are 32 NFL teams playing across 17 weeks with generally only two teams having a bye per week which always leaves enough teams to be picked even at the end of the season.

### Linear Programming Formulation

The problem of picking a team for every week of the season can be solved in a globally optimal way by formulating it as a linear program. Let us define a few variables
* ![equation](https://latex.codecogs.com/gif.latex?W) is the number of weeks in the season. Weeks will be indexed by the numbers ![equation](https://latex.codecogs.com/gif.latex?1) through ![equation](https://latex.codecogs.com/gif.latex?W)
* ![equation](https://latex.codecogs.com/gif.latex?T) is the number of teams in the league. Teams will be indexed by the numbers ![equation](https://latex.codecogs.com/gif.latex?1) through ![equation](https://latex.codecogs.com/gif.latex?T)
* ![equation](https://latex.codecogs.com/gif.latex?p_%7Bw%2C%20t%7D) is the probability that in week ![equation](https://latex.codecogs.com/gif.latex?w) team ![equation](https://latex.codecogs.com/gif.latex?t) wins where ![equation](https://latex.codecogs.com/gif.latex?w%20%5Cin%20%5C%7B1%2C%202%2C%20%5Cldots%2C%20W%5C%7D) and ![equation](https://latex.codecogs.com/gif.latex?t%20%5Cin%20%5C%7B1%2C%202%2C%20%5Cldots%2C%20T%5C%7D)
* ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D) is an indicator variable which is ![equation](https://latex.codecogs.com/gif.latex?1) if we pick team ![equation](https://latex.codecogs.com/gif.latex?t)  in week ![equation](https://latex.codecogs.com/gif.latex?w) and ![equation](https://latex.codecogs.com/gif.latex?0) if not

The ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D) are the variables we would like to figure out and will indicate which team we pick for each week.

To formulate the problem as a linear program we must specify linear equations or inequalities capturing the constraints and a linear expression that represents the objective. The two constraints we need to impose are picking exactly one team per week and not picking the same team twice. The objective to be maximized is the probability of winning every week in the season.

#### Pick Exactly One Team Per Week

The constraint to pick exactly one team per week can be written in terms of our indicator variables as

![equation](https://latex.codecogs.com/gif.latex?%5Csum_%7Bt%3D1%7D%5ET%20s_%7Bw%2C%20t%7D%20%3D%201%20%5Chspace%7B20%7D%20%5Cforall%20w%20%5Cin%20%5C%7B1%2C%202%2C%20%5Cldots%2C%20W%5C%7D)

Since the ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D) are either zero or one this constraint says that exactly one of the ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D) is one per week or in other words that we pick exactly one team per week.

#### Don't Pick Same Team Twice

The constraint to not pick the same team twice can be written in terms of our indicator variables as

![equation](https://latex.codecogs.com/gif.latex?%5Csum_%7Bw%3D1%7D%5EW%20s_%7Bw%2C%20t%7D%20%5Cleq%201%20%5Chspace%7B20%7D%20%5Cforall%20t%20%5Cin%20%5C%7B1%2C%202%2C%20%5Cldots%2C%20T%5C%7D)

Since the ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D) are either zero or one this constraint says that at most one of the ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D) can be one for each team or in other words the same team cannot be picked more than once
#### Maximize Win Probability

The simplest expression equal to the probability of winning every week in the season is

![equation](https://latex.codecogs.com/gif.latex?%5Cleft%28%5Csum_%7Bt%3D1%7D%5ET%20s_%7B1%2C%20t%7D%20p_%7B1%2C%20t%7D%5Cright%29%5Cleft%28%5Csum_%7Bt%3D1%7D%5ET%20s_%7B2%2C%20t%7D%20p_%7B2%2C%20t%7D%5Cright%29%20%5Ccdots%20%5Cleft%28%5Csum_%7Bt%3D1%7D%5ET%20s_%7BW%2C%20t%7D%20p_%7B1%2C%20W%7D%5Cright%29)

The expression in the first set of parentheses is the probability that we win with our picks in week 1 since the only nonzero ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7B1%2C%20t%7D) is for the team that we have picked in week 1. Similarly, the expression in the ![equation](https://latex.codecogs.com/gif.latex?i)th set of parentheses is the probability that we win in the ![equation](https://latex.codecogs.com/gif.latex?i)th week. Multiplying across all the weeks of the season gives the probability that we win every week of the season.

Unfortunately, this expression is not linear and therefore cannot be used as an objective expression in a linear program. Luckily, we can write the probability of winning every week in the season in a different way that allows for a transformation into a linear expression. The following expression is also equal to the probability of winning every week of the season

![equation](https://latex.codecogs.com/gif.latex?%5Cleft%28%5Cprod_%7Bt%3D1%7D%5ET%20p_%7B1%2C%20t%7D%5E%7Bs_%7B1%2C%20t%7D%7D%20%5Cright%20%29%5Cleft%28%5Cprod_%7Bt%3D1%7D%5ET%20p_%7B2%2C%20t%7D%5E%7Bs_%7B2%2C%20t%7D%7D%20%5Cright%20%29%20%5Ccdots%20%5Cleft%28%5Cprod_%7Bt%3D1%7D%5ET%20p_%7BW%2C%20t%7D%5E%7Bs_%7BW%2C%20t%7D%7D%20%5Cright%20%29%20%3D%20%5Cprod_%7Bt%3D1%7D%5ET%20%5Cprod_%7Bw%3D1%7D%5EW%20p_%7Bw%2C%20t%7D%5E%7Bs_%7Bw%2C%20t%7D%7D)

The expression in the ![equation](https://latex.codecogs.com/gif.latex?i)th set of parentheses is the probability that we win in the ![equation](https://latex.codecogs.com/gif.latex?i)th week and multiplying across all the weeks gives the probability that we win every week of the season.

At first glance this doesn't seem to help us very much since this expression is also nonlinear in the ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bw%2C%20t%7D). However, we can just as well maximize the logarithm of this expression since logarithm is a strictly increasing function. The arguments which maximize a function ![equation](https://latex.codecogs.com/gif.latex?f) will also maximize a strictly increasing function applied to ![equation](https://latex.codecogs.com/gif.latex?f). Thankfully for us the logarithm of the above expression will be linear

![equation](https://latex.codecogs.com/gif.latex?%5Csum_%7Bt%3D1%7D%5ET%20%5Csum_%7Bw%3D1%7D%5EW%20s_%7Bw%2C%20t%7D%20%5Clog%20p_%7Bw%2C%20t%7D)

and this expression can be used as the objective in our linear program.
