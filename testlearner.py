""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
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
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import math  		  	   		     		  		  		    	 		 		   		 		  
import sys  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.genfromtxt(inf, delimiter=",")

    data = data[1:, 1:]

  		  	   		     		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		  	   		     		  		  		    	 		 		   		 		  
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # separate out training and testing data  		  	   		     		  		  		    	 		 		   		 		  
    train_x = data[:train_rows, 0:-1]  		  	   		     		  		  		    	 		 		   		 		  
    train_y = data[:train_rows, -1]  		  	   		     		  		  		    	 		 		   		 		  
    test_x = data[train_rows:, 0:-1]  		  	   		     		  		  		    	 		 		   		 		  
    test_y = data[train_rows:, -1]

    # get index of data frame (this case is leaf size ascending)
    idx = np.arange(test_x.shape[0])

    ############################################################
    #### Experiment 1 testing overfit for one decision tree ####
    #### by using in sample error and out of sample error ######
    ############################################################

    # train for each leaf size
    rmse_trend_in = []
    rmse_trend_out = []
    overfit = 0
    prev_in = 0
    prev_out = 0
    for leaf in idx[1:]:
        # create a decision tree learner and train it
        learner = dt.DTLearner(leaf_size=leaf)
        learner.add_evidence(train_x, train_y)  # train it

        # evaluate in sample
        pred_y = learner.query(train_x)  # get the predictions
        rmse_in = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        rmse_trend_in.append(rmse_in)

        # evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        rmse_out = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        rmse_trend_out.append(rmse_out)

        # check for overfit
        if prev_in < rmse_in and prev_out > rmse_out and rmse_in < rmse_out:
            intersect = leaf
        else:
            prev_in = rmse_in
            prev_out = rmse_out

    # create png file of graph displaying results
    df_in = pd.DataFrame(data=rmse_trend_in, columns=["In Sample Results"], index=idx[1:])
    df_out = pd.DataFrame(data=rmse_trend_out, columns=["Out of Sample Results"], index=idx[1:])
    df_temp = pd.concat(
        [df_in, df_out],  axis=1)
    title = "Exp 1: Overfitting in Decision Tree Learner"
    xlabel = "Leaf size"
    ylabel = "RMSE"
    ax = df_temp.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.xlim(1, 100)
    plt.axvline(x=intersect, color='r', linestyle='--')
    plt.savefig("ex1.png")
    plt.clf()

    ##################################################################
    #### Experiment 2 testing overfit for multiple decision trees ####
    #### by using in sample error and out of sample error ############
    ##################################################################

    # train for each leaf size
    rmse_trend_in = []
    rmse_trend_out = []
    overfit = 0
    prev_in = 0
    prev_out = 0
    for leaf in idx[1:]:
        # create a bag learner and train it
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size": leaf}, bags=20, boost=False, verbose=False)
        learner.add_evidence(train_x, train_y)  # train it

        # evaluate in sample
        pred_y = learner.query(train_x)  # get the predictions
        rmse_in = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        rmse_trend_in.append(rmse_in)

        # evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        rmse_out = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        rmse_trend_out.append(rmse_out)

        # check for overfit
        if prev_in < rmse_in and prev_out > rmse_out and rmse_in < rmse_out:
            intersect = leaf
        else:
            prev_in = rmse_in
            prev_out = rmse_out

    # create visual displaying the results and saving it in png file
    df_in = pd.DataFrame(data=rmse_trend_in, columns=["In Sample Results"], index=idx[1:])
    df_out = pd.DataFrame(data=rmse_trend_out, columns=["Out of Sample Results"], index=idx[1:])
    df_temp = pd.concat(
        [df_in, df_out], axis=1)
    title = "Exp 2: Overfitting in Decision Tree Learner with 20 Bags"
    xlabel = "Leaf size"
    ylabel = "RMSE"
    ax = df_temp.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.xlim(1, 100)
    plt.axvline(x=intersect, color='r', linestyle='--')
    plt.savefig("ex2.png")
    plt.clf()

    ##################################################################
    #### Experiment 3 testing time to train and time to query ########
    #### between decision tree learner and random tree learner #######
    ##################################################################

    # Calculate and plot the time it takes to train and query DTLearner and RTLearner
    # create a learner and train it
    train_time = []
    query_time = []
    for leaf in idx[1:]:
        learner = dt.DTLearner(leaf_size=leaf)
        tt0 = time.clock()  # timestamp to track train time
        learner.add_evidence(train_x, train_y)  # train it
        tt1 = time.clock() - tt0  # train time total
        train_time.append(tt1)

        # evaluate in sample
        qt0 = time.clock()  # timestamp to track query time
        pred_y = learner.query(train_x)  # get the predictions
        qt1 = time.clock() - qt0  # query time total
        query_time.append(qt1)

    # Input results into dataframe
    train_time_DT = pd.DataFrame(data=train_time, columns=["Decision Tree"], index=idx[1:])
    query_time_DT = pd.DataFrame(data=query_time, columns=["Decision Tree"], index=idx[1:])

    # Repeat for random tree learner
    # create a learner and train it
    train_time = []
    query_time = []
    for leaf in idx[1:]:
        learner = rt.RTLearner(leaf_size=leaf)
        tt0 = time.clock()
        learner.add_evidence(train_x, train_y)  # train it
        tt1 = time.clock() - tt0
        train_time.append(tt1)

        # evaluate in sample
        qt0 = time.clock()
        pred_y = learner.query(train_x)  # get the predictions
        qt1 = time.clock() - qt0
        query_time.append(qt1)

    # Input results into dataframe
    train_time_RT = pd.DataFrame(data=train_time, columns=["Random Tree"], index=idx[1:])
    query_time_RT = pd.DataFrame(data=query_time, columns=["Random Tree"], index=idx[1:])

    # Graph the results
    df_temp = pd.concat(
        [train_time_DT, train_time_RT], axis=1)
    title = "Exp 3: Time to Train Over Leaf Sizes"
    xlabel = "Leaf size"
    ylabel = "Time in seconds"
    ax = df_temp.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.xlim(1, 100)
    plt.savefig("ex3-traintime.png")
    plt.clf()

    df_temp = pd.concat(
        [query_time_DT, query_time_RT], axis=1)
    title = "Exp 3: Time to Query Over Leaf Sizes"
    xlabel = "Leaf size"
    ylabel = "Time in seconds"
    ax = df_temp.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.xlim(1, 100)
    plt.savefig("ex3-querytime.png")
    plt.clf()
