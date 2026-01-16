# Excpute

A 16 bit cpu VM that was meant to be made in minecraft, but it was too tough so now im making it here lol
[Documentation](https://docs.google.com/spreadsheets/d/1jg-Fbts24ksjgkxZRkGntg0EJQws3mo0vg7sR-p3xGc/edit?usp=sharing)

## Specs

### Cpu

- 8 bit registers
- 8 registers
- support for up to 256 bytes of ram
- -built in vram for r, g, b, x, and y values in 8 bits

### Display

- up to 256x256 pixels (or more with some engineering)
- support for full 8 bit rgm
- uses ports 1-6

## How some systems will work

### rendering a charecter

1. Read the right register/RAM that has the charecter
2. go to that charecter id's slot in storage
3. ???
4. profit

### IO propriatary slots

- Display

1. red color push
2. green color push
3. blue color push
4. x coordinate push
5. y coordinate push
6. Write pixel data push (1 = push)

- Storage

9. data storage register location push (push data with port 10)
10. data push (with port 9)
11. data storage register location push (pull data with port 12)
12. data pull (with port 11)
13. mouse x coordinate push
14. mouse y coordinate push
