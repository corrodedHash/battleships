# Battleships
[![Build Status](https://travis-ci.org/corrodedHash/battleships.svg?branch=master)](https://travis-ci.org/corrodedHash/battleships)

Suite containing a variable size battleship field, bots that only shoot and
bots that only defend

## Code tour

**[management](management/)** contains necessary classes to represent the
board, and utilities that work on this board, like finding ships from hit
cells, and computing all surrounding cells of such a ship

**[bot](bot/)** contains tools to play the game automatically, _randombot_ that
only gets hit, and _marginbot_ or _checkerbot_ that only shoot.

**[util](util/)** contains random classes that are needed for this project

**battleshell.py** is a shell for playing manually

## Bots
**[marginbot](bot/marginbot.py)** shoots cells with the statistically highest
chance of a ship being there, which basically is the amount of free space of
this cells 4 sides.  
**[checkerbot](bot/checkerbot.py)** is marginbot, but only shoots 'at the white
fields in a chess board', e.g. only at A1, A3, B2, B4...

## Benchmarks
Shots needed to win in 20 games played with randomly placed ships
([Data](bench.txt)):  

| bot | mean | median | stdev |
|---|---|---|---|
| marginbot | 51.95 | 52.5 | 4.347 |
| checkerbot | 52.5 | 52.0 | 4.223 |
