## Bayes Nets

In this project, I worked with probabilistic models known as Bayesian networks to efficiently calculate the answer to probability questions concerning discrete random variables.

## Part 1 Bayesian network:

First exercise was to build a basic probabilistic model for the following system:

There's a nuclear power plant in which an alarm is supposed to ring when the gauge reading exceeds a fixed threshold. The gauge reading is based on the actual temperature, and for simplicity, we assume that the temperature is represented as either high or normal. However, the alarm is sometimes faulty. The temperature gauge can also fail, with the chance of failing greater when the temperature is high.

Assume that the following statements about the system are true:
> 1. The temperature gauge reads the correct temperature with 95% probability when it is not faulty and 20% probability when it is faulty. For simplicity, say that the gauge's "true" value corresponds with its "hot" reading and "false" with its "normal" reading, so the gauge would have a 95% chance of returning "true" when the temperature is hot and it is not faulty.
> 2. The alarm is faulty 15% of the time.
> 3. The temperature is hot (call this "true") 20% of the time.
> 4. When the temperature is hot, the gauge is faulty 80% of the time. Otherwise, the gauge is faulty 5% of the time.
> 5. The alarm responds correctly to the gauge 55% of the time when the alarm is faulty, and it responds correctly to the gauge 90% of the time when the alarm is not faulty. For instance, when it is faulty, the alarm sounds 55% of the time that the gauge is "hot" and remains silent 55% of the time that the gauge is "normal."


Use the following name attributes:

>- "alarm"
>- "faulty alarm"
>- "gauge"                   (high = True, normal = False)
>- "faulty gauge"
>- "temperature"             (high = True, normal = False)  

### Casting the net

The following commands will create a BayesNet instance add node with name "alarm":

    BayesNet = BayesianModel()
    BayesNet.add_node("alarm")

### Setting the probabilities

The conditional probabilities for the necessary variables on the network that was just built is set using the function `set_probability()`.

### Probability calculations : Perform inference

Perform inference on the network to calculate the following probabilities:

> - the marginal probability that the alarm sounds
> - the marginal probability that the gauge shows "hot"
> - the probability that the temperature is actually hot, given that the alarm sounds and the alarm and gauge are both working

## Part 2: Sampling

Consider the following scenario:

There are three frisbee teams who play each other: the Airheads, the Buffoons, and the Clods (A, B and C for short). 
Each match is between two teams, and each team can either win, lose, or draw in a match. Each team has a fixed but 
unknown skill level, represented as an integer from 0 to 3. The outcome of each match is probabilistically proportional to the difference in skill level between the teams.

Sampling is a method for ESTIMATING a probability distribution when it is prohibitively expensive (even for inference!) to completely compute the distribution. 

Here, we want to estimate the outcome of the matches, given prior knowledge of previous matches. Rather than using inference, we will do so by sampling the network using two [Markov Chain Monte Carlo](http://www.statistics.com/papers/LESSON1_Notes_MCMC.pdf) models: Gibbs sampling (2c) and Metropolis-Hastings (2d).

### Build the network

Built a Bayes Net to represent the three teams and their influences on the match outcomes using the function `get_game_network()`.

### Calculate posterior distribution for the 3rd match

Suppose that it is known the following outcome of two of the three games: A beats B and A draws with C. Calculated the posterior distribution for the outcome of the **BvC** match in `calculate_posterior()` method. 

### Gibbs sampling

The Gibbs sampling algorithm is a special case of Metropolis-Hastings. This takes place in `Gibbs_sampler()`, which takes a Bayesian network and initial state value as a parameter and returns a sample state drawn from the network's distribution. In case of Gibbs, the returned state differs from the input state at at-most one variable (randomly chosen).

### Metropolis-Hastings sampling

The independent Metropolis-Hastings sampling algorithm is implemented in `MH_sampler()`, which is another method for estimating a probability distribution.
The general idea of MH is to build an approximation of a latent probability distribution by repeatedly generating a "candidate" value for each sample vector comprising of the random variables in the system, and then probabilistically accepting or rejecting the candidate value based on an underlying acceptance function. Unlike Gibbs, in case of MH, the returned state can differ from the initial state at more than one variable.

### Comparing sampling methods

I now estimated the likelihood of different outcomes for the third match by running Gibbs sampling until it converged to a stationary distribution. 

I used the functions to measure how many iterations it takes for Gibbs and MH to converge to a stationary distribution over the posterior. 

I then repeated it for Metropolis-Hastings sampling.

Check `compare_sampling()` and `sampling_question()` to view the results of the comparison.
 