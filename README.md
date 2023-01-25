# WordleSolver 

WordleSolver is a Python library prov(iding an algorithm to solve the poppular game Wordle.  
The WordleSolver class takes a word corpus as input and a word and based on a computation
of the most common syllables tries to guess the word from the corpus.  
The current default corpus generated contains approx 31,000 5-letter words 
(fetched from different NLTK corpora). 
The average size of a person's vocabulary is 20,000 - 35,000 words in total [(source)](https://www.economist.com/johnson/2013/05/29/lexical-facts#:~:text=Most%20adult%20native%20test%2Dtakers,a%20day%20until%20middle%20age).  
Of those, about 2,500 are 5-letter words [(source)](https://www.theledger.com/story/business/columns/2022/01/28/gadget-daddy-wordle-word-game-captivating-audiences-simplicity/9253440002/#:~:text=The%20the%20Official%20Scrabble%20Dictionary,list%20will%20be%20around%202%2C500.),
meaning WordleSolver's number of potential words to guess from is about x10 times more than the average person. 


## Installation
Install requirements.txt 
```bash
pip install -r requirements.txt
```

## Usage

Usage example given in main.py

## Todos
- Make faster
- Add corpus choice functionaility
- Improve popular words fetch functionality
- Increase accuracy