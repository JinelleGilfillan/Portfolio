""""""  		  	   		     		  		  		    	 		 		   		 		  
"""MC1-P2: Optimize a portfolio.  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		     		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
Template code for CS 4646/7646  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		     		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		     		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		     		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		     		  		  		    	 		 		   		 		  
or edited.  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
We do grant permission to share solutions privately with non-students such  		  	   		     		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		     		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
Student Name: Tucker Balch (replace with your name)  		  	   		     		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		     		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  


import datetime as dt  		  	   		     		  		  		    	 		 		   		 		  

import numpy as np  		  	   		     		  		  		    	 		 		   		 		  

import matplotlib.pyplot as plt  		  	   		     		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import scipy.optimize as spo


# This is the function that will be tested by the autograder  		  	   		     		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality

def optimize_portfolio(  		  	   		     		  		  		    	 		 		   		 		  
    sd=dt.datetime(2008, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
    ed=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		     		  		  		    	 		 		   		 		  
    gen_plot=False,  		  	   		     		  		  		    	 		 		   		 		  
):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		     		  		  		    	 		 		   		 		  
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		     		  		  		    	 		 		   		 		  
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		     		  		  		    	 		 		   		 		  
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		     		  		  		    	 		 		   		 		  
    statistics.  		  	   		     		  		  		    	 		 		   		 		  
                                                                                          
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		     		  		  		    	 		 		   		 		  
    :type sd: datetime  		  	   		     		  		  		    	 		 		   		 		  
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		     		  		  		    	 		 		   		 		  
    :type ed: datetime  		  	   		     		  		  		    	 		 		   		 		  
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		     		  		  		    	 		 		   		 		  
        symbol in the data directory)  		  	   		     		  		  		    	 		 		   		 		  
    :type syms: list  		  	   		     		  		  		    	 		 		   		 		  
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		     		  		  		    	 		 		   		 		  
        code with gen_plot = False.  		  	   		     		  		  		    	 		 		   		 		  
    :type gen_plot: bool  		  	   		     		  		  		    	 		 		   		 		  
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		     		  		  		    	 		 		   		 		  
        standard deviation of daily returns, and Sharpe ratio  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: tuple  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  

    # Read in adjusted closing prices for given symbols, date range  		  	   		     		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		  	   		     		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		  	   		     		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		  	   		     		  		  		    	 		 		   		 		  
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later


    # find the allocations for the optimal portfolio  		  	   		     		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case
    for every in range(len(syms)):
        if every == 0:
            allocs = np.asarray(1/len(syms))
        else:
            allocs = np.append(allocs, 1/len(syms))
    # add code here to find the allocations

    ##################### Calculate variables ######################
    cr_list = calculate_variables(prices, syms)


    for each in range(len(syms)):
        if each == 0 or each == 1:
            bnds = ((0, 1), (0, 1))
        else:
            bnds = ((0, 1),) + bnds
    cnsts = ({'type': 'eq', 'fun': lambda allocs: 1-np.sum(allocs)})

    result = spo.minimize(calculate_sharpe, allocs, args=(syms, prices), method='SLSQP',
                          bounds=bnds, constraints=cnsts)

    allocs = result.x

    ##################### Calculate sharpe ratio ######################
    for i in range(len(syms)):
        if i == 0:
            test_list = np.array([prices[syms[i]].pct_change()]) * allocs[i]
        else:
            temp = np.array([prices[syms[i]].pct_change()]) * allocs[i]
            test_list = np.concatenate((test_list, temp), axis=0)

    test_val = np.nansum(test_list, axis=0)

    cr_total = np.sum(np.multiply(allocs, cr_list))
    adr_total = np.mean(test_val)
    sddr_total = np.std(test_val)
    sharpe = adr_total / sddr_total

    cr, adr, sddr, sr = [
        cr_total,
        adr_total,
        sddr_total,
        sharpe,
    ]  # add code here to compute stats

    # Get daily portfolio value
    for j in range(len(syms)):
        if j == 0:
            normed = np.array([prices[syms[j]][1:]]) / np.array([prices[syms[j]][:-1]])
            normed = np.array([np.insert(normed, 0, 1)])
            alloced = normed * allocs[j]
            port = alloced * np.array([prices[syms[j]]])
        else:
            normed = np.array([prices[syms[j]][1:]]) / np.array([prices[syms[j]][:-1]])
            normed = np.array([np.insert(normed, 0, 1)])
            alloced = normed * allocs[j]
            temp = alloced * np.array([prices[syms[j]]])
            port = np.concatenate((port, temp), axis=0)
    port_val = np.sum(port, axis=0)
    norm_port = (port_val - np.min(port_val)) / (np.max(port_val) - np.min(port_val))
    norm_spy = (prices_SPY - np.min(prices_SPY)) / (np.max(prices_SPY) - np.min(prices_SPY))
    # add code here to compute daily portfolio values
    # Compare daily portfolio value with SPY using a normalized plot  		  	   		     		  		  		    	 		 		   		 		  
    if gen_plot:  		  	   		     		  		  		    	 		 		   		 		  
        # add code to plot here
        prices_total = pd.DataFrame(data=norm_port, index=prices.index)
        df_temp = pd.concat(  		  	   		     		  		  		    	 		 		   		 		  
            [prices_total, norm_spy], keys=["Portfolio", "SPY"], axis=1
        )
        title = "Daily Portfolio Value and SPY"
        xlabel = "Date"
        ylabel = "Price"
        ax = df_temp.plot(title=title, fontsize=12)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.legend()
        plt.savefig("plot.png")
        plt.clf()
    pass

    return allocs, cr, adr, sddr, sr


def calculate_variables(prices, syms):
    ##################### Calculate Cumulative Return ######################

    for a in range(len(syms)):
        num_start = prices[syms[a]].iloc[1]
        num_end = prices[syms[a]].iloc[len(prices)-1]
        if a == 0:
            cr_list = np.array((num_end - num_start) / num_start)
        else:
            cr_list = np.append(cr_list, (num_end - num_start) / num_start)

    return cr_list


def calculate_sharpe(allocs, syms, prices):

    for i in range(len(syms)):
        if i == 0:
            test_list = np.array([prices[syms[i]].pct_change()]) * allocs[i]
        else:
            temp = np.array([prices[syms[i]].pct_change()]) * allocs[i]
            test_list = np.concatenate((test_list, temp), axis=0)

    test_val = np.nansum(test_list, axis=0)

    sharpe = np.mean(test_val) / np.std(test_val)
    return -sharpe

def test_code():  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    This function WILL NOT be called by the auto grader.  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  

    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]

    # Assess the portfolio  		  	   		     		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		     		  		  		    	 		 		   		 		  
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )  		  	   		     		  		  		    	 		 		   		 		  

    # Print statistics
    print(f"Start Date: {start_date}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"End Date: {end_date}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Symbols: {symbols}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Allocations:{allocations}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio: {sr}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Average Daily Return: {adr}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Cumulative Return: {cr}")  		  	   		     		  		  		    	 		 		   		 		  


if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		  	   		     		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		  	   		     		  		  		    	 		 		   		 		  
    test_code()  		  	   		     		  		  		    	 		 		   		 		  
