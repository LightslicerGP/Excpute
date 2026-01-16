# Excpute

A 16 bit cpu VM that was meant to be made in minecraft, but it was too tough so now im making it here lol

V2.2 is meant to fix things and have a clean start, NOT using a string of binary, but using the ACTUAL instruction sheet itself, should prevent a bunch of conversions and whatnot (thank you mr_nano on discord for pointing this out)

V2.3 is v2.2 but rewritten to run faster, focusing on speed before features, so at the start there wont be any ram or register .bin files, but instead arrays created by the code itself. BUT this will still use the same ISA as v2.2

V2.4 is v2.3 but optimized even more, and also slightly changing the SPD Instruction to be able to push a buffer (so you only push when you need to, and not every time you set or fill the screen), and read from the display (not the buffer, couldnt figure that out), also got rid of number display as it would be difficult to implement anyway. Completely new ISA

[Documentation](https://docs.google.com/spreadsheets/d/1jg-Fbts24ksjgkxZRkGntg0EJQws3mo0vg7sR-p3xGc/edit?usp=sharing)

## Specs

### Cpu

- 8 bit registers/memory
- 8 registers
- support for up to 256 bytes of ram
- stack starts at byte 249 and goes down the more that is pushed

### Display

- up to 256x256 pixels (or more with some engineering)
- support for full 8 bit rgb
- uses memory addresses 250 to 255: Red, Green, Blue, X, Y, Operation

### IO propriatary slots

#### Keyboard

- uses ports 0-7
- keyboard charecter set, follows Keyboard Oriented Charecter Set (K. O. C. S.) system

#### Mouse

- uses ports 8-10
- port 8 is for mouse buttons
- ports 9 and 10 are for x and y coordinate of the mouse
