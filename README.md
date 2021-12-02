# Advent Of Code 2021

These are my solutions for
2021's [advent of code](https://adventofcode.com/2021). My plan this year is to
use this to get my python as idiomatic as possible, but I may deviate depending
on the size of my timebox for a given day, a whim, impatience, or specific
characteristics of a puzzle that make some other tool on my belt seem better.

Any original code here is licensed under the [MIT License](LICENSE.md). I
probably won't take the time to vet any dependencies' licenses unless I copy
them into this tree. In the unlikely event something from here is worth copying,
the burden is on the copying party to check the suitability of the licenses for
code that isn't mine.

## Usage

After spending some time with rust this year, I finally decided to learn to
use poetry for my python projects. It behaves a lot like cargo in a good way.

This project uses `poetry` to manage its virtual environments. Either
install it from system repositories or give it its own venv and install it
with `pip`, then put it on your path. Once that's done, from the top level
of this repository, run:

```bash
poetry install
```

to create a virtual environment with all the necessary libraries.

If you want to try my solution with your data, the easiest way is to grab
your `session` cookie from a visit to [adventofcode.com]
(https://adventofcode.com/) using the inspector in your browser and save it
into a top-level file called `.env` containing the cookie and your preferred
data storage location:

```dotenv
AOC_SESSION=GetYourOwnSessionCookie
AOCD_DIR=data
```

and run using poetry:

```bash
poetry run aoc run -y $YEAR -d $DAY
```

to have the script fetch your input and use it. If you've already got your
input saved, you can use

```bash
poetry run aoc run -y $YEAR -d $DAY /path/to/saved/input.txt
```
