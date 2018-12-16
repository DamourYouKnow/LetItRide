# Let it Ride [![Build Status](https://travis-ci.com/DamourYouKnow/LetItRide.svg?token=rfuE5AprBEX3cX7ehdRp&branch=master)](https://travis-ci.com/DamourYouKnow/LetItRide)
Final project for MATH 3808 by 
Bailey D'Amour, Joseph Miller, and Michael Cardy.
This project addresses question 5.f from the final
topics document. It implements the game of Let it
Ride using python's [pygame](https://www.pygame.org/news) module.

This version of Let it Ride follows the rules outlined here: https://en.wikipedia.org/wiki/Let_It_Ride_(card_game)

Latest release can be downloaded here: https://github.com/DamourYouKnow/LetItRide/releases/   
Download the zip
or installer and launch "Let it Ride.exe".

# Features
In addition to the basic features of Let it Ride poker, this version
also features
* Optional Side Bet
* Configurable deck count
* Statistics Engine
* Card selector

Side bets can be placed using the button next to the side bet
amount and are 
reset with the Reset Bet button. Deck count as well as other
settings can be
configured in the Settings screen.
To get the most out of this program, the user can select cards using the
card selector screen and then view the probabilities related to that hand
using the statistics engine. The statistics engine allows for a user
to see the expected value of a hand by clicking the Show Statistics button.
The user can also see the number of resultant hands
and their relative probabilities
with the Probability Distribution button.


# Running instructions
Download the required packages:
```
pip install -r requirements.txt
```
To run the game:
```
python main.py
```
To run the unit tests:
```
python -m unittest tests
```

# Build instructions
This software can be built only for the Windows platform.  
  
To install the required packages for building:
```
pip install cx_Freeze
```
```
pip install idna
```
To create a package with an executable file:
```
python setup.py build
```
To create an MSI installer:
```
python setup.py bdist_msi
```
