SimpleTronBot
==============

SimpleTronBot is a simple Tron Bot. It competed in the 2010 AI challenge
organised by the University of Waterloo and sponsored by Google.
Is is based on the classic MiniMax algorithm. A writeup of the
bot strategy is [available here](http://www.sifflez.org/misc/tronbot/).

##Usage

Make sure to install Java and Python.
To pit SimpleTronBot against one of the default bots run the following command:

```bash
$ java -jar uwaterloo-aichallenge-utils/engine/Tron.jar <map> <cmd_bot1> <cmd_bot2> [delay-between-turns] [max-move-time] 

# Here is an example between #1: WallHugger and #2: SimpleTronBot 

java -jar uwaterloo-aichallenge-utils/engine/Tron.jar \
          uwaterloo-aichallenge-utils/maps/toronto.txt \
          "java -jar uwaterloo-aichallenge-utils/example_bots/WallHugger.jar" \
          "./SimpleTronBot.py" \
          0

[...]

15 15
###############
#          ####
# # # # # #####
#  #       # ##
# ### # # #####
#  #       # ##
# ### # # #####
####       # ##
### # # # #####
######     # ##
# # ### # #####
#  ###  2# # ##
# ### # ###1###
#  ####### ####
###############
Player Two Wins!
```

##License

The files under `uwaterloo-aichallenge-utils` and `tron.py` were provided by
the University of Waterloo Computer Science Club as a starting package for the
competition. You should contact Waterloo Computer Science Club if you want to 
reuse them. 

The SimpleTronBot source code in `SimpleTronBot.py` is covered by the MIT License.

Copyright (C) 2010-2013 Pablo Oliveira 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.






