# Let it Ride [![Build Status](https://travis-ci.com/DamourYouKnow/LetItRide.svg?token=rfuE5AprBEX3cX7ehdRp&branch=master)](https://travis-ci.com/DamourYouKnow/LetItRide)
Final project for MATH 3808.

This version of Let it Ride will follow the rules outlined here: https://en.wikipedia.org/wiki/Let_It_Ride_(card_game)

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
python setup.py
```
To create an MSI installer:
```
python setup.py bdist_msi
```
