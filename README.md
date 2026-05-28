# Intro
Snowchuck is a game I wrote in Turbo Pascal in 1998. It was a simple side scrolling game
that ran in DOS in VGA (mode 13h). All graphics were created with a homemade drawing program
that I also had written in Turbo Pascal. 

I also have the game running in a vritual DOS machine on the web. Check out [http://chuck.dumais.io](http://chuck.dumais.io)

When I found out that it was possible to buy a Sega Genesis carthridge in which you could store homemade games
with an SD card, I decided to take a stab at porting my game to the Sega.

## Sega hardware
The fun challenge was to learn about the hardware. Learning about the instruction set of the Motorola 68000 and the z80.
One of the boring task I had to do was to convert my graphics to a format that would work on the Genesis, being tile based and all that stuff.
I used AI to help me create a converter and it worked well. I also needed to convert my "map" file that contains all information about
placement of stuff in each 33 levels of the game.

When writing a game for the Sega, you have full control over the hardware. The Sega does not provide any OS or any functions like the BIOS 
does on x86. You start executing at 0x00000000, you need to setup interupt handlers and have full ownership of RAM.

## The initial version
In the original game, I used a technique called "compiled sprites". This was something a friend of mine had showed me back then. The idea was to store images as executable functions in a binary file instead of a bitmap. So instead of getting the game to load each pixel information from memory and copy it to video memory, we would have a compiled binary that directly writes the right data in video memory. The speedup I gained from this was incredible. So I had to create a tool that converts my bitmaps to machine code. That's how I learned machine code programming. That was fun. By thinking about it now, I could have saved myself a lot of trouble if I had just generated assembly code and compiled it afterwards. 

So for this version, I had to rewrite the bitmaps to a different formats too. This is because the sega only understands 8x8 tiles and you build sprites with those tiles. So I wrote a tool (AI wrote most of that tool actually) to split into tiles and generate pallettes. I'm not using the tiles in the most efficient manner, but it's the only way to port the game without having to redo all the graphics.

## Sound
I had to compose all the music and sound FX myself. I used Furnace, a very good sound editor made specially for creating VGM files
that are easy to used within the game. I am no musician, so the music is as good as it gets :).
The sound engine is a completly different ROM. It's a separate "app" that runs on the z80 processor of the Sega. That meant
learning another architecture, and learning about the FM and PSG chips for sound processing.

# Gameplay
There are 33 levels in the game. The goal is just to get to the end of the level without touching any of the bad guys.
Chuck jumps using a jetpack. Chuck can die if he falls in an empty space, in water, on ice pics and a few other tiles. 
There are coins that chuck can collect but they don't really do anything. 
There are adrenaline shots that can make chuck go faster, H2 bottles to jump higher, and other surprises.
There are no weapons. Chuck cannot kill any bad guys, he can only avoid them.

In this version, there is a bug where if chuck is in front of a tree or another object, a bad guy will not kill him. I decided to keep this as a feature.
It's kinda like if chuck was able to hide in front of objects

# Demo
The game works flawlessly on a real Sega Genesis. But displaying a 320x200 resolution on a 55" TV doesn't look great.
Also, I think I would need some kind of fancy HDMI converter instead of connecting the console directly to the TV's coax connector.
The image looks terrible, and it looks even worse when filming it with my cellphone. So apologies for the bad demo

[![TV](https://img.youtube.com/vi/NAQdWAKoxGE/0.jpg)](https://youtu.be/NAQdWAKoxGE)

Here's what it looks like running on an emulator

[![EMU](https://img.youtube.com/vi/-V9ukKmz-T8/0.jpg)](https://youtu.be/-V9ukKmz-T8)


# Toolchain
## Build tools
I'm using vasm and vlink.
http://sun.hasenbraten.de/vasm/release/vasm.tar.gz
    make CPU=m68k SYNTAX=mot
    make CPU=z80 SYNTAX=mot
http://sun.hasenbraten.de/vlink/release/vlink.tar.gz
    make

# Map Editor
Automaticlaly loads ../../images/edited-map.json. Saves in the same file

select block in the bottom view when it shows 5 slots. use Del key to remove.
    use mouse scroll to adjst Y

to test edited map:
    run "make edit" in images
    run "make" in src

to run with original file:
    run "make" in images
    run "make" in src

to use changes officially:
    copy edited-map.json to map.json and build
    run "make" in images
    run "make" in src

## Emulator
I'm using blastem. The package is available on ubuntu


# TODO
    - Game loop enhancements
        - find a way to report vsync stats back when running on metal. Save in sram?

    - Level editor
        - change type on right click (type should include "empty")
            either we lock the choice to tiles that are already in level or we need to update the palettes if we add new blocks
      - move objects
        - add blocks (will affect palette if adding those that are not in map already
      - add/remove/change badguys (will affect palette if adding those that are not in map already

# Bugs
    - when checking if we can move left, I need to take 12 from X. Why? block collision for bad guys work without it.
    - on death animation, frame show hero facing left. It should face the same way it was facing when death occured   
    - dangerous tiles are only detected when falling on them. Not it we walk up to them when they are at the same level we already are on 
    - sometimes I die immediately after respawning for no reason

# Improvements
    - Use movem everywhere instead of PUSH/POP in function entry/exit
    - After ending the game, we just go back to level 0. There should be a nice ending
    - change font color. Would need to find a fixed slot in palette. And we dont wanna have to change the font file's numbers


