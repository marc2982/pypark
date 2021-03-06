# pypark

A 2d tile-based theme park simulator written in Python.

The idea of this project is to discover how 2D tile-based engines work and is mostly a testing ground for figuring out different (interesting) problems. It is unlikely this will become an actual game at any point, although it may resemble one eventually.

This was a project that I recently rediscovered after years of gathering dust. It required some love so I'm currently working on it in my (limited) spare time.

Problems I hope to gain insights into:
- how 2d tile-engines work
- object dependencies and how best to structure the data
- performance implications (of both Python and chosen data structures)
- understanding proper game loops
- discovering problems I haven't thought about

Couldn't this be done in Unity super quickly?

    Probably, but I'm enjoying learning the details of how an engine
    works (obviously Unity is orders of magnitude more complex).

# TODO
- always more cleanup!
- proper action handling / context menus
- fix odd circular dependency between world and pathfinder
- write a few more tests for the pathfinding
- decouple update logic from frame rate
- maybe switch to "isometric" view?
- shops target coordinates (x,y)
- more peep decision making
- more testing
- add fun at somepoint?
- so much more...
