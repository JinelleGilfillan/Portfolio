import sys

from numpy import zeros, float32
#from numpy.random import choice
#  pgmpy
import pgmpy
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from random import *

def make_power_plant_net():
    """Create a Bayes Net representation of the above power plant problem. 
    Use the following as the name attribute: "alarm","faulty alarm", "gauge","faulty gauge", "temperature". (for the tests to work.)
    """
    BayesNet = BayesianModel()   
    
    #Create BayesNet instances of name attributes
    BayesNet.add_node("alarm")
    BayesNet.add_node("faulty alarm")
    BayesNet.add_node("gauge")
    BayesNet.add_node("faulty gauge")
    BayesNet.add_node("temperature")
    
    #Create edges between name attributes with probabilities between each other
    BayesNet.add_edge("temperature", "faulty gauge")
    BayesNet.add_edge("temperature", "gauge")
    BayesNet.add_edge("faulty gauge", "gauge")
    BayesNet.add_edge("gauge", "alarm")
    BayesNet.add_edge("faulty alarm", "alarm")
    
    return BayesNet


def set_probability(bayes_net):
    """Set probability distribution for each node in the power plant system.
    Use the following as the name attribute: "alarm","faulty alarm", "gauge","faulty gauge", "temperature". (for the tests to work.)
    """
    cpd_alarm = TabularCPD('alarm', 2, values=[[0.9, 0.1, 0.55, 0.45], \
        [0.1, 0.9, 0.45, 0.55]], evidence=['faulty alarm', 'gauge'], evidence_card=[2, 2])
    cpd_faultyAlarm = TabularCPD('faulty alarm', 2, values=[[0.85], [0.15]])
    cpd_gauge = TabularCPD('gauge', 2, values=[[0.95, 0.05, 0.2, 0.8], \
        [0.05, 0.95, 0.8, 0.2]], evidence=['faulty gauge', 'temperature'], evidence_card=[2, 2])
    cpd_faultyGauge = TabularCPD('faulty gauge', 2, values=[[0.95, 0.2], [0.05, 0.8]], \
        evidence=['temperature'], evidence_card=[2])
    cpd_temperature = TabularCPD('temperature', 2, values=[[0.8], [0.2]])
    
    bayes_net.add_cpds(cpd_alarm)
    bayes_net.add_cpds(cpd_faultyAlarm)
    bayes_net.add_cpds(cpd_gauge)
    bayes_net.add_cpds(cpd_faultyGauge)
    bayes_net.add_cpds(cpd_temperature)
    
    return bayes_net


def get_alarm_prob(bayes_net):
    """Calculate the marginal 
    probability of the alarm 
    ringing in the 
    power plant system."""
    solver = VariableElimination(bayes_net)
    marginal_prob = solver.query(variables=['alarm'], joint=False)
    alarm_prob = marginal_prob['alarm'].values
    return alarm_prob[1]


def get_gauge_prob(bayes_net):
    """Calculate the marginal
    probability of the gauge 
    showing hot in the 
    power plant system."""
    solver = VariableElimination(bayes_net)
    marginal_prob = solver.query(variables=['gauge'], joint=False)
    gauge_prob = marginal_prob['gauge'].values
    return gauge_prob[1]


def get_temperature_prob(bayes_net):
    """Calculate the conditional probability 
    of the temperature being hot in the
    power plant system, given that the
    alarm sounds and neither the gauge
    nor alarm is faulty."""
    solver = VariableElimination(bayes_net)
    conditional_prob = solver.query(variables=['temperature'], evidence={'alarm':1, 'faulty alarm':0, 'faulty gauge':0}, joint=False)
    temp_prob = conditional_prob['temperature'].values
    return temp_prob[1]


def get_game_network():
    """Create a Bayes Net representation of the game problem.
    Name the nodes as "A","B","C","AvB","BvC" and "CvA".  """
    BayesNet = BayesianModel()
    #add bayes nodes
    BayesNet.add_node("A")
    BayesNet.add_node("B")
    BayesNet.add_node("C")
    BayesNet.add_node("AvB")
    BayesNet.add_node("BvC")
    BayesNet.add_node("CvA")
    
    #add edges between team and match
    BayesNet.add_edge("A", "AvB")
    BayesNet.add_edge("A", "CvA")
    BayesNet.add_edge("B", "AvB")
    BayesNet.add_edge("B", "BvC")
    BayesNet.add_edge("C", "BvC")
    BayesNet.add_edge("C", "CvA")
    
    #add probabilities (skills)
    cpd_A = TabularCPD('A', 4, values=[[0.15], [0.45], [0.3], [0.1]])
    cpd_B = TabularCPD('B', 4, values=[[0.15], [0.45], [0.3], [0.1]])
    cpd_C = TabularCPD('C', 4, values=[[0.15], [0.45], [0.3], [0.1]])
    cpd_AvB = TabularCPD('AvB', 3, values=[ \
        [0.1, 0.2, 0.15, 0.05, 0.6, 0.1, 0.2, 0.15, 0.75, 0.6, 0.1, 0.2, 0.9, 0.75, 0.6, 0.1], \
        [0.1, 0.6, 0.75, 0.9, 0.2, 0.1, 0.6, 0.75, 0.15, 0.2, 0.1, 0.6, 0.05, 0.15, 0.2, 0.1], \
        [0.8, 0.2, 0.1, 0.05, 0.2, 0.8, 0.2, 0.1, 0.1, 0.2, 0.8, 0.2, 0.05, 0.1, 0.2, 0.8]], \
        evidence=['A', 'B'], evidence_card=[4, 4])
    cpd_BvC = TabularCPD('BvC', 3, values=[ \
        [0.1, 0.2, 0.15, 0.05, 0.6, 0.1, 0.2, 0.15, 0.75, 0.6, 0.1, 0.2, 0.9, 0.75, 0.6, 0.1], \
        [0.1, 0.6, 0.75, 0.9, 0.2, 0.1, 0.6, 0.75, 0.15, 0.2, 0.1, 0.6, 0.05, 0.15, 0.2, 0.1], \
        [0.8, 0.2, 0.1, 0.05, 0.2, 0.8, 0.2, 0.1, 0.1, 0.2, 0.8, 0.2, 0.05, 0.1, 0.2, 0.8]], \
        evidence=['B', 'C'], evidence_card=[4, 4])
    cpd_CvA = TabularCPD('CvA', 3, values=[ \
        [0.1, 0.2, 0.15, 0.05, 0.6, 0.1, 0.2, 0.15, 0.75, 0.6, 0.1, 0.2, 0.9, 0.75, 0.6, 0.1], \
        [0.1, 0.6, 0.75, 0.9, 0.2, 0.1, 0.6, 0.75, 0.15, 0.2, 0.1, 0.6, 0.05, 0.15, 0.2, 0.1], \
        [0.8, 0.2, 0.1, 0.05, 0.2, 0.8, 0.2, 0.1, 0.1, 0.2, 0.8, 0.2, 0.05, 0.1, 0.2, 0.8]], \
        evidence=['C', 'A'], evidence_card=[4, 4])
    
    BayesNet.add_cpds(cpd_A)
    BayesNet.add_cpds(cpd_B)
    BayesNet.add_cpds(cpd_C)
    BayesNet.add_cpds(cpd_AvB)
    BayesNet.add_cpds(cpd_BvC)
    BayesNet.add_cpds(cpd_CvA)
    
    return BayesNet


def calculate_posterior(bayes_net):
    """Calculate the posterior distribution of the BvC match given that A won against B and tied C. 
    Return a list of probabilities corresponding to win, loss and tie likelihood."""
    posterior = [0,0,0] 
    solver = VariableElimination(bayes_net)
    conditional_prob = solver.query(variables=['BvC'], evidence={'AvB':0, 'CvA':2}, joint=False)
    posterior = conditional_prob['BvC'].values
    return posterior # list 


def Gibbs_sampler(bayes_net, initial_state):
    """Complete a single iteration of the Gibbs sampling algorithm 
    given a Bayesian network and an initial state value. 
    
    initial_state is a list of length 6 where: 
    index 0-2: represent skills of teams A,B,C (values lie in [0,3] inclusive)
    index 3-5: represent results of matches AvB, BvC, CvA (values lie in [0,2] inclusive)
    
    Returns the new state sampled from the probability distribution as a tuple of length 6.
    Return the sample as a tuple.    
    """
    sample = tuple(initial_state) 
    A_cpd = bayes_net.get_cpds("A")     
    AvB_cpd = bayes_net.get_cpds("AvB")
    match_table = AvB_cpd.values
    team_table = A_cpd.values

    if sample == ():
        a_random = choices([0,1,2,3],[(team_table[0]*match_table[0,0,0])+(team_table[0]*match_table[0,0,1])+ \
            (team_table[0]*match_table[0,0,2])+(team_table[0]*match_table[0,0,3])+ \
            (team_table[0]*match_table[2,0,0])+(team_table[0]*match_table[2,1,0])+ \
            (team_table[0]*match_table[2,2,0])+(team_table[0]*match_table[2,3,0]), \
            (team_table[1]*match_table[0,1,0])+(team_table[1]*match_table[0,1,1])+ \
            (team_table[1]*match_table[0,1,2])+(team_table[1]*match_table[0,1,3])+ \
            (team_table[1]*match_table[2,0,1])+(team_table[1]*match_table[2,1,1])+ \
            (team_table[1]*match_table[2,2,1])+(team_table[1]*match_table[2,3,1]), \
            (team_table[2]*match_table[0,2,0])+(team_table[2]*match_table[0,2,1])+ \
            (team_table[2]*match_table[0,2,2])+(team_table[2]*match_table[0,2,3])+ \
            (team_table[2]*match_table[2,0,2])+(team_table[2]*match_table[2,1,2])+ \
            (team_table[2]*match_table[2,2,2])+(team_table[2]*match_table[2,3,2]), \
            (team_table[3]*match_table[0,3,0])+(team_table[3]*match_table[0,3,1])+ \
            (team_table[3]*match_table[0,3,2])+(team_table[3]*match_table[0,3,3])+ \
            (team_table[3]*match_table[2,0,3])+(team_table[3]*match_table[2,1,3])+ \
            (team_table[3]*match_table[2,2,3])+(team_table[3]*match_table[2,3,3])])[0]
        b_random = choices([0,1,2,3],[(team_table[0]*match_table[1,0,0])+(team_table[0]*match_table[1,0,1])+ \
            (team_table[0]*match_table[1,0,2])+(team_table[0]*match_table[1,0,3]), \
            (team_table[1]*match_table[1,1,0])+(team_table[1]*match_table[1,1,1])+ \
            (team_table[1]*match_table[1,1,2])+(team_table[1]*match_table[1,1,3]), \
            (team_table[2]*match_table[1,2,0])+(team_table[2]*match_table[1,2,1])+ \
            (team_table[2]*match_table[1,2,2])+(team_table[2]*match_table[1,2,3]), \
            (team_table[3]*match_table[1,3,0])+(team_table[3]*match_table[1,3,1])+ \
            (team_table[3]*match_table[1,3,2])+(team_table[3]*match_table[1,3,3])])[0]
        c_random = choices([0,1,2,3],[(team_table[0]*match_table[2,0,0])+(team_table[0]*match_table[2,0,1])+ \
            (team_table[0]*match_table[2,0,2])+(team_table[0]*match_table[2,0,3]), \
            (team_table[1]*match_table[2,1,0])+(team_table[1]*match_table[2,1,1])+ \
            (team_table[1]*match_table[2,1,2])+(team_table[1]*match_table[2,1,3]), \
            (team_table[2]*match_table[2,2,0])+(team_table[2]*match_table[2,2,1])+ \
            (team_table[2]*match_table[2,2,2])+(team_table[2]*match_table[2,2,3]), \
            (team_table[3]*match_table[2,3,0])+(team_table[3]*match_table[2,3,1])+ \
            (team_table[3]*match_table[2,3,2])+(team_table[3]*match_table[2,3,3])])[0]
        
        b_win_prob = match_table[0, b_random, c_random]/(match_table[0, b_random, c_random]+match_table[1, b_random, c_random]+match_table[2, b_random, c_random])
        b_lose_prob = match_table[1, b_random, c_random]/(match_table[0, b_random, c_random]+match_table[1, b_random, c_random]+match_table[2, b_random, c_random])
        b_tie_prob = match_table[2, b_random, c_random]/(match_table[0, b_random, c_random]+match_table[1, b_random, c_random]+match_table[2, b_random, c_random])
        
        
        sample = (a_random, b_random, c_random, 0, choices([0,1,2], \
            [b_win_prob, b_lose_prob, b_tie_prob])[0], 2)
        
        
    
    
    #chose one node to change at random, not including the evidence (AvB and CvA)
    change_index = 3
    while change_index == 3:
        change_index = randint(0,4)
    
    #change tuple to list to edit
    sample_list = list(sample)
    
    #edit single node
    if change_index == 0:
        new_value = choices([0, 1, 2, 3], [(team_table[0]*match_table[0,0,0])+(team_table[0]*match_table[0,0,1])+ \
            (team_table[0]*match_table[0,0,2])+(team_table[0]*match_table[0,0,3])+ \
            (team_table[0]*match_table[2,0,0])+(team_table[0]*match_table[2,1,0])+ \
            (team_table[0]*match_table[2,2,0])+(team_table[0]*match_table[2,3,0]), \
            (team_table[1]*match_table[0,1,0])+(team_table[1]*match_table[0,1,1])+ \
            (team_table[1]*match_table[0,1,2])+(team_table[1]*match_table[0,1,3])+ \
            (team_table[1]*match_table[2,0,1])+(team_table[1]*match_table[2,1,1])+ \
            (team_table[1]*match_table[2,2,1])+(team_table[1]*match_table[2,3,1]), \
            (team_table[2]*match_table[0,2,0])+(team_table[2]*match_table[0,2,1])+ \
            (team_table[2]*match_table[0,2,2])+(team_table[2]*match_table[0,2,3])+ \
            (team_table[2]*match_table[2,0,2])+(team_table[2]*match_table[2,1,2])+ \
            (team_table[2]*match_table[2,2,2])+(team_table[2]*match_table[2,3,2]), \
            (team_table[3]*match_table[0,3,0])+(team_table[3]*match_table[0,3,1])+ \
            (team_table[3]*match_table[0,3,2])+(team_table[3]*match_table[0,3,3])+ \
            (team_table[3]*match_table[2,0,3])+(team_table[3]*match_table[2,1,3])])[0]
        
        sample_list[change_index] = new_value
        
    elif change_index == 1:
        new_value = choices([0, 1, 2, 3], [(team_table[0]*match_table[1,0,0])+(team_table[0]*match_table[1,0,1])+ \
            (team_table[0]*match_table[1,0,2])+(team_table[0]*match_table[1,0,3]), \
            (team_table[1]*match_table[1,1,0])+(team_table[1]*match_table[1,1,1])+ \
            (team_table[1]*match_table[1,1,2])+(team_table[1]*match_table[1,1,3]), \
            (team_table[2]*match_table[1,2,0])+(team_table[2]*match_table[1,2,1])+ \
            (team_table[2]*match_table[1,2,2])+(team_table[2]*match_table[1,2,3]), \
            (team_table[3]*match_table[1,3,0])+(team_table[3]*match_table[1,3,1])+ \
            (team_table[3]*match_table[1,3,2])+(team_table[3]*match_table[1,3,3])])[0]
        
        sample_list[change_index] = new_value
    
    elif change_index == 2:
        new_value = choices([0, 1, 2, 3], [(team_table[0]*match_table[2,0,0])+(team_table[0]*match_table[2,0,1])+ \
            (team_table[0]*match_table[2,0,2])+(team_table[0]*match_table[2,0,3]), \
            (team_table[1]*match_table[2,1,0])+(team_table[1]*match_table[2,1,1])+ \
            (team_table[1]*match_table[2,1,2])+(team_table[1]*match_table[2,1,3]), \
            (team_table[2]*match_table[2,2,0])+(team_table[2]*match_table[2,2,1])+ \
            (team_table[2]*match_table[2,2,2])+(team_table[2]*match_table[2,2,3]), \
            (team_table[3]*match_table[2,3,0])+(team_table[3]*match_table[2,3,1])+ \
            (team_table[3]*match_table[2,3,2])+(team_table[3]*match_table[2,3,3])])[0]
        
        sample_list[change_index] = new_value
         
    elif change_index >3:
        new_value = choices([0,1,2], [match_table[0,sample_list[1],sample_list[2]], \
            match_table[1,sample_list[1],sample_list[2]], match_table[2,sample_list[1],sample_list[2]]])[0]
    
            
        sample_list[change_index] = new_value
    
    #change list to tuple
    sample = tuple(sample_list)
    return sample


def MH_sampler(bayes_net, initial_state):
    """Complete a single iteration of the MH sampling algorithm given a Bayesian network and an initial state value. 
    initial_state is a list of length 6 where: 
    index 0-2: represent skills of teams A,B,C (values lie in [0,3] inclusive)
    index 3-5: represent results of matches AvB, BvC, CvA (values lie in [0,2] inclusive)    
    Returns the new state sampled from the probability distribution as a tuple of length 6. 
    """
    A_cpd = bayes_net.get_cpds("A")     
    AvB_cpd = bayes_net.get_cpds("AvB")
    match_table = AvB_cpd.values
    team_table = A_cpd.values
    sample = tuple(initial_state)
    if sample == ():
        sample = (randint(0, 3), randint(0, 3), randint(0, 3), 0, randint(0,2), 2)

    sample_prob = team_table[sample[0]] * team_table[sample[1]] * team_table[sample[2]] * \
        match_table[sample[3]][sample[0]][sample[1]] * match_table[sample[4]][sample[1]][sample[2]] * \
        match_table[sample[5]][sample[2]][sample[0]]
    
    new_sample = (randint(0, 3), randint(0, 3), randint(0, 3), 0, randint(0,2), 2)
    
    new_sample_prob = team_table[new_sample[0]] * team_table[new_sample[1]] * team_table[new_sample[2]] * \
        match_table[new_sample[3]][new_sample[0]][new_sample[1]] * match_table[new_sample[4]][new_sample[1]][new_sample[2]] * \
        match_table[new_sample[5]][new_sample[2]][new_sample[0]]
    
    r = new_sample_prob / sample_prob
    u = uniform(0,1)
    
    if u <= min(r, 1):
        sample = new_sample
    
    return sample


def compare_sampling(bayes_net, initial_state):
    """Compare Gibbs and Metropolis-Hastings sampling by calculating how long it takes for each method to converge."""    
    Gibbs_count = 0
    MH_count = 0
    MH_rejection_count = 0
    Gibbs_convergence = [0,0,0] # posterior distribution of the BvC match as produced by Gibbs 
    MH_convergence = [0,0,0] # posterior distribution of the BvC match as produced by MH
    delta = 0.00001
    n = 100
    delta_val = [0,0,0]
    avg = [1,1,1]
    BvC_Win = 0
    BvC_Lose = 0
    BvC_Tie = 0
    sample_state = initial_state
    
    #calculate Gibbs
    while Gibbs_count < n or delta_val > delta:
        Gibbs_count += 1
        sample = Gibbs_sampler(bayes_net, sample_state)
        sample_state = sample
        
        #add sample value win to counts
        if sample[4] == 0:
            BvC_Win += 1
        elif sample[4] == 1:
            BvC_Lose += 1
        elif sample[4] == 2:
            BvC_Tie += 1
        
        #calculate convergence
        previous_Gibbs = Gibbs_convergence
        Gibbs_convergence = [BvC_Win/Gibbs_count, BvC_Lose/Gibbs_count, BvC_Tie/Gibbs_count]
        #print (Gibbs_convergence)
        #print(Gibbs_count)
        delta_val = abs(previous_Gibbs[0]-Gibbs_convergence[0]) + abs(previous_Gibbs[1]-Gibbs_convergence[1]) + abs(previous_Gibbs[2]-Gibbs_convergence[2])
    
    #calculate MH
    delta_val = 0
    BvC_Win = 0
    BvC_Lose = 0
    BvC_Tie = 0
    while MH_count < n or delta_val > delta:
        MH_count += 1
        sample = MH_sampler(bayes_net, sample_state)
        sample_state = sample
        
        #add sample value win to counts
        if sample[4] == 0:
            BvC_Win += 1
        elif sample[4] == 1:
            BvC_Lose += 1
        elif sample[4] == 2:
            BvC_Tie += 1
        
        #calculate convergence
        previous_MH = MH_convergence
        MH_convergence = [BvC_Win/MH_count, BvC_Lose/MH_count, BvC_Tie/MH_count]
        #print (Gibbs_convergence)
        #print(Gibbs_count)
        delta_val = abs(previous_MH[0]-MH_convergence[0]) + abs(previous_MH[1]-MH_convergence[1]) + abs(previous_MH[2]-MH_convergence[2])
    
    #print("Gibbs_convergence: " + str(Gibbs_convergence))
    #print("MH_convergence: " + str(MH_convergence))
    #print("Gibbs_count: " + str(Gibbs_count))
    #print("MH_count: " + str(MH_count))
        
    return Gibbs_convergence, MH_convergence, Gibbs_count, MH_count, MH_rejection_count


def sampling_question():
    """Question about sampling performance."""
    choice = 2
    options = ['Gibbs','Metropolis-Hastings']
    factor = 1.09
    return options[choice], factor
