# NFL Survivor Pool Picker 🏈

Found yourself in an NFL Survivor Pool but don't know anything about football? Don't worry, we've got you covered.

NFL Survivor Picker is a command line application to help you make picks in NFL Survivor Pools. Features include
* Scraper to fetch probabilities for all games in NFL season from fivethirtyeight.com
* Read in user specified NFL season and game probabilities
* Make picks using greedy algorithm or globally optimal linear programming algorithm

## Background

NFL Survivor is a fantasy sports game where participants pick one NFL team per week to win their matchup. If the picked team wins then the participant stays in the pool but if they lose then they are out of the game. The tricky bit is that a participant cannot pick the same team more than once. The last participant standing is crowned the winner of the pool (subject to tiebreakers if multiple participants have no losses at the end of the 17 week season).

## Algorithms

For the sake of our analysis we will assume that the probabilities that teams win their matchups in each week of the NFL season is given to us. Our problem is how to optimally pick one team for each week of the season without picking the same team twice.

### Greedy Algorithm

An intuitive approach is to make our picks greedily. That is, in week one we select the team with the highest win probability. This team is now labeled "picked" for the sake of selecting future teams. In each subsequent week we select the team with the highest win probability across all teams that we have not yet "picked" and add it to our set of "picked" teams. In this way, we pick a unique team per week for each week of the season.

For example, we may have the season

| Week 1              | Probability | Week 2              | Probability |
|---------------------|-------------|---------------------|-------------|
| NY Giants           | 0.75        | NY Giants           | 0.99        |
| NY Jets             | 0.25        | Dallas Cowboys      | 0.1         |
|                     |             |                     |             |
| Dallas Cowboys      | 0.45        | NY Jets             | 0.55        |
| Philadelphia Eagles | 0.55        | Philadelphia Eagles | 0.45        |

In the first week we pick the NY Giants since they have the highest win probability. In the second week, the NY Giants again have the highest win probability but we have unfortunately picked them already. In week 2, we settle for the highest win probability across all teams we haven't picked yet which is the NY Jets.

The first thing to notice about this approach is that it actually may not successfully determine a team to pick for every week of the season. If our greediness forces us to pick a set of teams in the first `n` weeks and then in week `n + 1` the only teams playing are the ones we picked in weeks `1` through `n` then we will not be able to select a team in week `n + 1`. The schedule below shows such an example

Further, this algorithm does not necessarily determine a schedule that has the highest probability of making it through the every week of the season. For example ...

### Linear Program Formulation
