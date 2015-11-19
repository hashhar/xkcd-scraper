[![Stories in Help Wanted](https://badge.waffle.io/hashhar/xkcd-scraper.png?label=help%20wanted&title=help%20wanted)](https://waffle.io/hashhar/xkcd-scraper)
[![Stories in Ready](https://badge.waffle.io/hashhar/xkcd-scraper.png?label=ready&title=Ready)](https://waffle.io/hashhar/xkcd-scraper)
[![Stories in Progress](https://badge.waffle.io/hashhar/xkcd-scraper.png?label=in%20progress&title=In%20Progress)](https://waffle.io/hashhar/xkcd-scraper)
[![Stories in Under Review](https://badge.waffle.io/hashhar/xkcd-scraper.png?label=under%20review&title=Under%20Review)](https://waffle.io/hashhar/xkcd-scraper)
# XKCD Scraper

Let's download all the XKCD comics and their titles! Why not use a browser plugin? Because you are a geek (or just want to look cool among your friends :satisfied:)!!!

## Dependencies

**Requests Python Module**  
Get it by doing
```python
pip install requests
```

## Setup Instructions

Why are you even reading this (unless you are somebody new to Python)???  
Make sure you have all the dependencies resolved before proceeding.

```github
git clone https://github.com/hashhar/xkcd-scraper.git
python xkcd-scraper.py --your-arguments
```

## Command Line Options

Unfortunately, you will need to provide command line parameters everytime you run the script (because I am a bad, bad man :smiling_imp:)

- **`-o`** *`directory`*, **`--output-dir`** *`directory`*  
Changes the output directory to `directory`.  
The default output directory is the current working directory.

- *`N`*  
This will fetch the comic number `N` from xkcd where `N` is an **integer or a set of integers greater than or equal to 0**.  
Use 0 to fetch the latest comic.

- **`-r`** *`M N`*, **`--range`** *`M N`*  
Fetches comics within the range `M` to `N`.  
`-r 3 30`, `--range 3 30` will fetch the comics from 3 to 30.

- **`-a`**, **`--all`**  
Fetches all the comics from the first one to the latest.

- **`-x`** *`N`*, **`--random`** *`N`*  
Fetches `N` pseudo-random (because, well, <a href="#food-for-thought">the world is not fair</a>) comics. You can specify how many you want to fetch as -x 10, --random 30. This will fetch 30 random comics.

- **`-t`**, **`--title`**  
Appends the title of the comic to the filename of the downloaded comic

## Comments

I am still working on it so feel free to contribute code and file issues and feature requests.

## Food For Thought

[Is there anything that is totally random? - StackExchange](http://philosophy.stackexchange.com/questions/2439/is-there-anything-that-is-totally-random)  
[Randomness vs Unpredictability - Wikipedia](https://en.wikipedia.org/wiki/Randomness#Randomness_versus_unpredictability)  
[Can we sure that randomeness exists? - Quora](https://www.quora.com/Can-we-be-sure-that-true-randomness-exists-Can-it-be-proven-that-anything-is-truly-random)
