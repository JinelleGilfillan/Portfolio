""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
    This learner was developed by Jinelle, the student. Decision Tree Learner model built following 
    the template guidelines from class. Sharing of this file publicly so that other students can 
    have access will be considered a violation of Georgia Tech's honor code. Student is allowed to 
    share to potential employers.  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class DTLearner(object):
    """  		  	   		     		  		  		    	 		 		   		 		  
    This is a Decision Tree Learner.

    :param leaf_size: the number of leaves left when the tree stops branching. Once the list reaches the leaf_size,
                      it will return the mean result.
    :type leaf_size: int
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		     		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		     		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size=1, verbose=False):
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.leaf_size = leaf_size
        self.verbose = verbose
  		  	   		     		  		  		    	 		 		   		 		  
    def author(self):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        :return: The GT username of the student  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        return "jgilfillan6"  # replace tb34 with your Georgia Tech username
  		  	   		     		  		  		    	 		 		   		 		  
    def add_evidence(self, data_x, data_y):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param data_x: A set of feature values used to train the learner  		  	   		     		  		  		    	 		 		   		 		  
        :type data_x: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        :param data_y: The value we are attempting to predict given the X data  		  	   		     		  		  		    	 		 		   		 		  
        :type data_y: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  

  		# Follow decision tree logic to train data
        # combine data x and data y to not lose sight of ys related to xs
        data = np.ones([data_x.shape[0], data_x.shape[1] + 1])
        data[:, 0:data_x.shape[1]] = data_x
        data[:, -1] = data_y
        # if the data set has reached the leaf size, the return the mean of the data ys
        if data.shape[0] <= self.leaf_size:
            return np.array([["Leaf", np.mean(data_y), "NA", "NA"]])
        # if all the data ys are the same, return the leaf with the value of y
        elif all(elem == data_y[0] for elem in data_y):
            return np.array([["Leaf", np.mean(data_y), "NA", "NA"]])
        else:
            # determine best feature i to split on as the feature (Xi) that has the highest absolute value correlation with Y
            max_corr = 0
            for i in range(len(data_x[0])):
                corr = np.corrcoef(data_x[:, i], data_y)
                correlation = abs(corr[0, 1])
                if correlation > max_corr:
                    max_corr = correlation
                    result_i = i
            SplitVal = np.median(data[:, result_i])
            # split the data into the left tree and the right tree
            left_tree = data[data[:, result_i] <= SplitVal]
            right_tree = data[data[:, result_i] > SplitVal]

            if len(left_tree) != 0 and len(right_tree) !=0:
                # if both the left and right tree are not empty, recursively run the function again
                lefttree= self.add_evidence(left_tree[:, 0:len(data_x[0])], left_tree[:, -1])
                righttree = self.add_evidence(right_tree[:, 0:len(data_x[0])], right_tree[:, -1])
            elif len(right_tree) !=0:
                # if the right tree is empty, return the leaf and 0
                lefttree = np.array([["Leaf", SplitVal, "NA", "NA"]])
                righttree = np.array([["Leaf", 0, "NA", "NA"]])
            else:
                # if the left tree is empty, return the leaf and 0
                lefttree = np.array([["Leaf", 0, "NA", "NA"]])
                righttree = np.array([["Leaf", SplitVal, "NA", "NA"]])

            # if no leaf is returned, return the x value split on, the split value,
            # # of rows down the left tree is, and # of rows down the right tree is
            root = np.array([[result_i, SplitVal, 1, lefttree.shape[0]+1]])
            # store the data in the object variable data table
            self.data_table = np.concatenate((root, lefttree, righttree), axis=0)
            return np.concatenate((root, lefttree, righttree), axis=0)
  		  	   		     		  		  		    	 		 		   		 		  
    def query(self, points):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		     		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        """
        answers = []  # list for storing the answers that will be returned
        for point in points:
            skip = 0  # variable to store how many rows to move down in the tree
            for node in self.data_table:
                if skip == 0:
                    index = node[0]
                    value = node[1].astype(np.float)
                    if index == "Leaf":
                        answers.append(value)  # if leaf is reached, return the answer
                        break
                    elif point[index.astype(np.float).astype(np.int)] <= value:
                        skip = node[2].astype(np.float).astype(np.int)-1
                    else:
                        skip = node[3].astype(np.float).astype(np.int)-1
                else:
                    skip -= 1
        return np.array(answers)

  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  		  	   		     		  		  		    	 		 		   		 		  
