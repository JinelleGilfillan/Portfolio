""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
    This learner was developed by Jinelle, the student. Random Tree Learner model built following 
    the template guidelines from class. Sharing of this file publicly so that other students can 
    have access will be considered a violation of Georgia Tech's honor code. Student is allowed to 
    share to potential employers. 	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np
import random as random
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class RTLearner(object):
    """
    This is a Random Tree Learner.

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
         # move along, these aren't the drones you're looking for

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
        # Follow random tree logic to train data
        # combine data x and data y together to not lose answers to train on
        data = np.ones([data_x.shape[0], data_x.shape[1] + 1])
        data[:, 0:data_x.shape[1]] = data_x
        data[:, -1] = data_y
        # if leaf size has reached the limit, return the leaf and the mean of the data
        if data.shape[0] <= self.leaf_size:
            return np.array([["Leaf", np.mean(data_y), "NA", "NA"]])
        # if all elements in a list are the same, return the leaf and the value
        elif all(elem == data_y[0] for elem in data_y):
            return np.array([["Leaf", np.mean(data_y), "NA", "NA"]])
        else:
            # determine feature i to split on as the feature (Xi) randomly
            result_i = random.randrange(0, data.shape[1]-1)
            SplitVal = np.median(data[:, result_i])
            # split the data into the left tree branch and the right tree branch
            left_tree = np.array(data[data[:, result_i] <= SplitVal])
            right_tree = np.array(data[data[:, result_i] > SplitVal])

            if len(left_tree) != 0 and len(right_tree) !=0:
                # recursively run the left tree and right tree results
                lefttree= self.add_evidence(left_tree[:, 0:len(data_x[0])], left_tree[:, -1])
                righttree = self.add_evidence(right_tree[:, 0:len(data_x[0])], right_tree[:, -1])
            elif len(right_tree) !=0:
                # if the right tree is empty, return 0 as the leaf
                lefttree = np.array([["Leaf", SplitVal, "NA", "NA"]])
                righttree = np.array([["Leaf", 0, "NA", "NA"]])
            else:
                # if the left tree is empty, return 0 as the leaf
                lefttree = np.array([["Leaf", 0, "NA", "NA"]])
                righttree = np.array([["Leaf", SplitVal, "NA", "NA"]])

            # combine the factor that was split on, the numeric value of the split, and how many
            # rows down the left tree is and how many rows down the right tree is
            root = np.array([[result_i, SplitVal, 1, lefttree.shape[0]+1]])
            # add the data to the "data_table" variable of the object
            self.data_table = np.concatenate((root, lefttree, righttree), axis=0)
            # return statement for recursion
            return np.concatenate((root, lefttree, righttree), axis=0)

    def query(self, points):
        """  		  	   		     		  		  		    	 		 		   		 		  
        Estimate the leaf that the data input would be located in.
  		  	   		     		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		     		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        """
        answers = []  # list to store answers
        for point in points:
            skip = 0  # variable to store the number of rows that it needs to go down to reach the appropiate tree
            for node in self.data_table:
                if skip == 0:
                    index = node[0]
                    value = node[1].astype(np.float)
                    if index == "Leaf":
                        # we have reached a leaf and we need to store it as the answer
                        answers.append(value)
                        break
                    # otherwise determine the # of rows to skip to reach appropiate tree
                    elif point[index.astype(np.float).astype(np.int)] <= value:
                        skip = node[2].astype(np.float).astype(int)-1
                    else:
                        skip = node[3].astype(np.float).astype(int)-1
                else:
                    skip -= 1
        return np.array(answers)  # return the list of answers

  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  		  	   		     		  		  		    	 		 		   		 		  
