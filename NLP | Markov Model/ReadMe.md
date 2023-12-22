# Markov Model Text Generator

**I built a Markov model text generator!** This project involved creating a data type called `MarkovModel` that represents a Markov model of order `k` from a given text string. It can generate realistic text that mimics the style and patterns of the original text.

## Key Features

* Creates a Markov model of order k
* Calculates frequencies
* Generates random characters
* Generates pseudo-random text
* Circular text handling
* Randomness with probabilities
* Client programs

### Circular Text Handling

I treated the input text as circular, meaning the last character comes after the first. This avoids dead ends in the Markov chain and allows for smoother text generation.

### Randomness with Probabilities

When generating characters or text, I used the calculated probabilities from the Markov model to ensure the generated output reflects the patterns of the original text.

## Experimentation and Results

1. I tested the model on different inputs, varying sizes and orders. Increasing the order generally led to more complex and realistic text generation.
2. I tried it on various texts, including ones I wrote, and the results were often surprisingly entertaining and coherent.

## Bonus: :sparkles:

I've included two of the most entertaining language-modeling fragments I discovered in the deliverables. You'll have to check them out to see what they are!

**Overall, this project was a fascinating exploration of Markov models and their potential for text generation. I learned a lot about data structures, probabilities, and how to build algorithms for analyzing and manipulating text data. I'm excited to see how this technology can be further developed and applied to generate even more creative and engaging text formats.**

