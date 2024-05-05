# Rocket-game
Should be a fun game.
## Controls
Use <kbd>w</kbd><kbd>a</kbd><kbd>s</kbd><kbd>d</kbd> or <kbd>↑</kbd><kbd>←</kbd><kbd>↓</kbd><kbd>→</kbd> to steer the rocket.  
Use <kbd>r</kbd> to reset the rocket's location, speed, acceleration and background scale.  
Use <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> <kbd>4</kbd> to change the fps (30, 60, 120, ∞)  
Use <kbd>F1</kbd> to turn on or off debug features  
Use the console to get information about your money and fuel  
`PS. you change the amount of powerups in the CONSTANTS.py file`
## About the game (Current state)
### Movement
Movement is good to go, maybe will be refined later (eg. rotation speed)
### Collisions
Collision with gorund is quite good, might be able to improve if all gameobject positions would be `float` instead of `int`  
Collision with powerups (money and fuel) is done
### Powerups
- Now implemented powerups and collision detection and everything else that is needed for collecting and tracking the powerup (creation on first game frame, drawing them efficiently on the screen, moving powerups that are too far away from the rocket and not making it obvious to the player that it has been done). Of course there are some performance issues (at least for my 14 year old Intel i7 m620 CPU. Basically the game stutters a bit when "unloading" powerups and moving them to their new position)
- Powerups come in two variations: money and fuel. Both of them have levels: 1, 2 and 3. Level 1 money is worth 1, level 2 money is worth 10 and level 3 money is worth 50. The same applies to fuel (at the moment).
- Powerups use pixel-based collisions with the rocket.
- The player's amount of money and fuel is being monitored (in console and on-screen). However at the moment there is no fuel consumption.


## TODO
- Fuel consumption when flying
- Adding obstacles
- Making sprites for all gameobjects (including creating `CollisionPoints` for the rocket)
- Main menu, options, upgrades (__Kevin's part at the moment__)
- Some kind of particle system for rocket's thrust or just an animation
- Boost


## Things that _**MIGHT**_ be implemented in the future
### Objective
To fly as high as possible until the game ends (game end is going to be probably some max height, going to the moon? / carrying stuff to ISS? / getting a satellite to orbit?)
### Upgrades
You can upgrade your rocket to make it accelerate faster, make the maximum velocity bigger, have more boost, have a bigger magnet to catch more money (make the radar radius bigger?, ~~make the durability better?~~ **Nope, too much math and too hard**).  
~~You can also buy new rockets, which go faster and further?~~ **Not doing that**
### Obstacles
To make the game more interesting, the rocket launch site has planes, helicopters and clouds (+ birds?), which make the rocket ~~vulnarable~~ **Nope, you will just die if you hit anything (+ you'll have a radar that helps you)**. Furthermore, the higher you get the wilder the flying objects get (weather balloons?, very fast fighter jets?, UFOs?, satellites?~~, GOD?~~ **NO**). There will also be wind, that will push you around for a short period of time. Thunder clouds make your flight computer glitch out (maybe it will happen also when you get higher aka due to radiation?).

## Some useful commands, if you get stuck with git
- Download git here: [git-scm.com](https://git-scm.com/downloads)
- To make this repository available in your computer run the following command    
  - `git clone https://github.com/HOR-163/Rocket-Game`  
- To update the repo that is in GitHub go inside the local repo folder, right click and select "open git GUI here". Then put your message (what you added, changed etc.) under "Commit Message". If that is done, be sure that nobody else has changed any other files. Then you'll have to press the buttons "Stage Changed", "Sign Off", "Commit" and lastly "Push". After pressing "Push" a new window will appear. Under that make sure you selected have selected "main" and then press "Push"- Now it will tell you if the push was successful or not.
