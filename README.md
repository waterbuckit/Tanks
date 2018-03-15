# Tanks
---
## Tasks:
#### Player character control
	- Base of the tank
		- Can only rotate left and right on its axes, drive forwards and backwards (Divide the velocity to give the sense of inertia??) 
	- Turret of the tank
		- Must stay centred on the body of the tank
		- Must rotate relative to the mouse position on screen
	- Have some kind of health?
#### Ubiquitous Particle class 
	- For handling shots being fired and colliding (taking a vector for position, velocity etc)
#### Enemy tanks
	- Base of the enemy tank
	- Turret of the enemy tank
		- Must have an accuracy offset, for instance, first round should mean that their shots are slow, or innacurate etc
	- Maybe have some states for patrolling, attacking?
	- Have some kind of health too
#### Map generation
	- Must be able to place enemies around the map
	- Map could potentially be a randomly generated maze? (use recursive backtracking algorithm for generating it)
	- Or split the map up into a grid and place predesigned map elements that are randomly selected from a pool
		of other map elements.

#### Clerical things
	- Score system
	- Menu ???

