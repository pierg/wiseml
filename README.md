# wiseml


Tool for safe and efficient model-free reinforcement learning in unknown environments. 

This approach leverages runtime monitoring to prevent the agent from taking "wrong" actions and explores the environment intelligently. 

Monitors, defined by properties and context, are orchestrated by a meta-monitor that dynamically activates and deactivates them. 

Evaluation of the approach shows that it blocks the agent from performing unsafe actions in all tested environments, and helps the agent achieve its goal faster.


Check (paper on IEEE Xplore)[https://ieeexplore.ieee.org/document/8823721].
