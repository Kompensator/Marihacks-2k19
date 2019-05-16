# Marihacks2k19
## Repository for Marihacks 2019

## To simulate a Hohmann transfer from Earth to another planet using realistic Keplerian physics
The Hohmann transfer is the most energy-efficient way to transfer between two planets.
However, the two planets have to be in a certain relative position to allow this transfer.
This project simulates such a transfer from Earth to one of the outter planets.
When the user presses `space`, the software holds the launch until the optimal position is obtained.
To implement Keplerian physics, Euler numerical integration is used to update each planet's position.


## To run:
1. Navigate to the folder
2. `python3 main.py` *args*
3. *args* indicate a particular planet to transfer (Mars, Jupiter or Saturn, with Mars being the default)
4. Once the animation starts, press `space` to prep the launch
5. Enjoy!


## Dependencies:
- Python 3 with Numpy and Pygame
- Anaconda Python 3 distro is recommanded 


## Authors:
- Ding Yi Z.
- Zachary V.
- Manuel M.


## References:
- https://www.jpl.nasa.gov/edu/teach/activity/lets-go-to-mars-calculating-launch-windows/


### Special thanks to MariHacks for organizing the hackathon where all this happened!