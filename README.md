A Monte Carlo simulation portfolio is a computational method used to estimate the potential outcomes of a portfolio’s performance by generating a large number of random scenarios.
Quite helpful to understand where you might potentially end up given your chosen portfolio.

This uses
* Time-Weighted Returns (TWR): Calculation of TWR for each simulation allows for a fair comparison that neutralizes the effects of periodic cash inflows (deposits).
* Use of TWR in Plot: TWR is used as a measure to better reflect the performance of the portfolio under recurring investment conditions.

Doing this in colab.google.com works really well. No need to setup anything on your machine
The time series used in the example can be found in the repo
If you want more timeseries, this is a good place to get some https://curvo.eu/backtest/en
They will also let you backtest and run monte carlo simulations on your ideas 

A note: 
If you're looking at doing some planning, and you'd rather use something ready-made and much more complete, you can look at this https://www.portfoliovisualizer.com/monte-carlo-simulation?s=y&sl=6oLYsxBBfI5FP17w0KIRdX and the above mentionned Curvo https://curvo.eu/backtest/en

But you'll likely better understand what you're doing if you try by yourself first, and ...it's more fun to DYI :) 
