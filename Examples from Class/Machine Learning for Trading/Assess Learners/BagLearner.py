""""""  		  	   		     		  		  		    	 		 		   		 		  
"""""""""	
     This learner was developed by Jinelle, the student. The format follow the template requirements
     for the program to run.
     Sharing of this file publicly so that other students can have access will be considered 
     a violation of Georgia Tech's honor code. Student is allowed to share to potential employers. 		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
"""
import numpy as np

class BagLearner(object):
    """  		  	   		     		  		  		    	 		 		   		 		  
    This is the Bag Learner, which intakes a type of learner, the arguments required, and n, the number of bags.
    It then creates n models of the learner (creating a forest of decision trees).

    :param learner: Learner selected to create multiple bags of.
    :type learner: object
    :param kwargs: Dict of variables that are the arguments required for the learner.
    :type kwargs: dict
    :param bags: number of bags that the learner will create.
    :type bags: int
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		     		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		     		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """
        self.learner = learner
        self.learners = []
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
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
        learners = [] # list to store the learner objects
        # unpack the arguments for each learner and append to learner list
        for i in range(self.bags):
            learners.append(self.learner(**self.kwargs))

        # combine data x and data y to be able to randomly select from data list without losing corresponding y
        data = np.ones([data_x.shape[0], data_x.shape[1] + 1])
        data[:, 0:data_x.shape[1]] = data_x
        data[:, -1] = data_y

        for i in range(len(learners)):
            # randomly select with replacement of data for training from the data set
            new_data = data[np.random.choice(data.shape[0], data.shape[0])]
            new_data_x = new_data[:, 0:-1]
            new_data_y = new_data[:, -1]

            # run the training
            learners[i].add_evidence(new_data_x, new_data_y)
            self.learners.append(learners[i])
  		  	   		     		  		  		    	 		 		   		 		  
    def query(self, points):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Estimate the learner result through regression method based on the bags built
        during the training phase  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		     		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  

        # get the list of results for each point in the data based on the bagging model
        result_list = np.empty([len(points), self.bags])
        for i in range(self.bags):
            result_list[:, i] = self.learners[i].query(points)
        # return the mean value (with regression) of each point
        return np.mean(result_list, axis=1)
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  		  	   		     		  		  		    	 		 		   		 		  
