# house-snake
﻿INTRODUCTION

This is House Snake, a HTTP Basic Authentication Brute Forcing tool that I created using
Python, frustration, and a lot of swearing. In Theory it will use a list of username and a list of
passwords to brute force past a HTTP Basic Authentication login. I named it house snake for
two reasons; It was programmed in Python, and much like a house snake, it isn’t very
threatening.

USAGE

House Snake is written in python 3, but two of its cosmetic modules are not compatible with
python 3. To avoid any unnecessary errors, it should be run using python 2, or made into an
executable via chmod.
When you run it, you need to provide it with some parameters. These are as follows:

* -u/-U: username list or a single username
* -t/-T: a list of targets(in csv format) or a single url
* -p/-P: password list or a single password
* -i: a single text file containing usernames and passwords

There are also some optional arguments that can be used:

* -h: will display the help
* -v: (verbose) will display all usernames and passwords attempted
* -o: will output the results to a specific output file in the json format
