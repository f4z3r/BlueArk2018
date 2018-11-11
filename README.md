# BlueArk2018 [![Build Status](https://travis-ci.com/jakobbeckmann/BlueArk2018.svg?token=6RwG9cGf5RW9JwThwdpc&branch=master)](https://travis-ci.com/jakobbeckmann/BlueArk2018)

BlueArk 2018 Hackathon Repo

## Project Description

Our challenge was to optimise the water distribution of arbitrary complex water networks. The optimisation aimed at minimising the water waster while maximising the energy production. Moreover, the problem was constrained by sanitation regulations.

An arbitrary network would consist of sources, both natural and with filtration systems, sinks, consumers, power turbines, tanks, and pipes. Natural sources would have uncontrolled flow into the network. Artificial sources with filtration systems would have controlled flow into the system with a maximal possible capacity. Pipes would allow a flow constrained by the maximum capacity of the pipe. Power turbines would have generation efficiencies and maximal water throughput capacities. Finally tank would allow to store water, but should be fully renewed every two days in order to guard against water stagnation and conform to sanitation guidelines.

Consumers in the network should obviously be provided with their required water demand while sinks allowed to evacuate surplus water from the network, should the demand drop too low and water sanitation become problematic.

The problem that was proposed to us was to provide an automated solution that would allow a user to either be provided with instruction on how to improve the water flow, or even fully automate it. This is relevant since at the current standing, only very few people understand the network and have the knowledge to properly configure it to meet consumer demands without wasting water in masses.

## Proposed Solution

Our solution aimed at translating a custom model into a constrained mathematical model of the network and leverage the power of existing optimisers to mathematically prove and provide an optimal network configuration for any instant in time.

The way this was achieved was by building a virtual model of the network, then building equations for each constraint in in the network using formal equations. In order to be able to provide such equations, the flow was once simulated by a form of symbolic execution of the model from sources to consumers. This would terminate eventually as the network could be modelled as a DAG. Once this was performed, the flow of the network was modelled, and each component knew from how many different _parents_ it could receive water, and to how many _children_ it would need to distribute it to. Moreover, it knew the symbolic representation of its parents and children.

Once all these components were modelled and initialised in this manner, consumers would propagate their demand to their parents, where equations would be generated to symbolically represent the required flow within each component. Moreover, during this stage, every component would produce a set of mathematical constraints based on its internal physical constraints within the network. Once all these constraints had been generated, they would be simplified in order to remove constraints that symbolically represented the same problem, and constant propagation would reduce the overall size of the constraint equations.

The reduced equations produced in the precedent stage would then be fed into high performance optimiser maximising the power generation equations while keeping water waste to a minimum. This would then provide a mathematically optimal solution to the network configuration problem.

### Advantages

The advantage of our solution compared to others, such as using machine learning to solve the problem was the following:

- Extremely fast computation of the optimum.
- No training required.
- Mathematically provable optimum.
- Full transparency in the decision making.
- Relatively extensible.

## Details

### Equation Generation and Reduction

All equations where encoded as (sort of) abstract syntax trees modelling the semantics of the equation. This allowed to reduce them very effectively by propagating constants. On top of that, it also allowed to easily compare the semantics between equations in order to verify that all the meaning of the equations passed to the optimiser has different semantic meanings.

### Model Description

Our approach to describing the model would have been to simply allow to define the model in some sort of configuration file and serialise it to generate a virtual model in our program. We did not implement any of this during the challenge as it would not be a challenging part of the issue.

## Issues Encountered

We had trouble connecting our produced model to the high performance optimiser due to unreliability of the python `subprocess` mechanisms. Moreover, expressing all the model's constraints purely mathematically turned out more of a challenge than we expected.

## Presentation

[Slides](https://docs.google.com/presentation/d/1MT_bg8ItWeix48uDccBgQQXffNL95mJuQ8Vkn-_Et6A/edit?usp=sharing).
