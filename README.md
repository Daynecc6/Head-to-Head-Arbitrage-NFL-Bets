# Head-to-Head-Arbitrage-NFL-Bets
## Overview
I was listening to my friends talk about sports betting and their "strategies" behind making winning bets. While listening to this conversation I began to think about
bets and if there was a way in which a better was guarenteed not to lose. I then realized that there is a way to do this and that it only takes simplistic
statistics to figure this out. 

The statistics to find this "arbitrage" bet are as follows. 

The probability of any given event should always be equal to one P(Event) = 1 or rewritten with two inputs P(A) + P(B) = 1. 
For example, a coin flip:
  - P(Heads = .5) + P(Tails = .5) = 1

What I realized is that when betmakers decide odds for games they are smart and will make the P(Event) > 1 so they make money. The exact amount they make can be calculated
by taking P(Event) - 1 and the difference is the amount they would make. A good bookmaker knows to never set the P(Event) < 1 as they would lose money themselves, but
they can't control what other bookmakers do. Therefore, it is possible that the combination of two different bookmakers for the P(Event) < 1 whilst both still have the
P(Event) > 1 for themselves. For example:
 - P(A1= .45) + P(B2= .5) = .95
 - Where A is one bookmaker and B is a different bookmaker and 1 is one team and 2 is the opposite team
 - We can see that the P(Event) < 1
 - If an individual were to take bet A and B at the same time and allocate their money right they would make .05

After discovering this I decided to see if I could make a program that scrapes all NFL head to head match up odds for different bookmakers to find a scenario in
which P(Event) < 1. The information below goes into more depth about how I did this.

## Method
I needed a way in which to get all of the different betmakers and their odds for the different matchups and teams. I first tried to scrape the data off the web
but I was unable to do this as they had security features to block this that I did not know how to work aroud. So, I instead reasearched and found an API that 
provides this information for free (as long as requests are under 500 per month).

Next, I pulled the information from the API and was greeted with a very complex nested json object in which I was able to teach myself how to pick out the exact
data I needed and disregard the rest. I stored all of this information inside of a list.

Then I took this information from the list and changed it into a dictionary in which each key was the betmaker and the values were the matchups with the different teams
along with their odds. I did this because it made it easier to create a pandas dataframe with the dictionary than the list.
  - {Bookmaker : matchup1 { Team1 : Odds , Team2 : Odds} }

I then went through and found the absolute highest value odds for each team inside of each matchup as this will lead to the most likely P(Event) < 1. Then, I calculated
the odds for each team and added them together to get the P(Event) all while keeping the bookmaker and team attached as if this information were not there then the
results would be useless.

I then had the information be displayed on an html page as I found it was easier to view and understand for the user.
## Skills Utilized
- Python
- Pandas
- JSON
- HTML
- Statistics
- Data Manipulation
## Screenshots

