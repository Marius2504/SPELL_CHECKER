# :calendar: SPELL_CHECKER

## :memo: Description
A spell checker application built to analyze words based on their morphological attributes. Emphasising the structure of an Finite State Automata, it can predict the correct word/words with a regularization parameter given by user.

## :robot: Dataset
### Romanian + English
The dataset consists of 456 Romanian texts with a total number of 180.000 unique words, and 333,333 most commonly-used single words on the English language web, as derived from the Google Web Trillion Word Corpus.

### Rules
There are some grammerly rules implemented:
- e-deletion:
   * Stems that end in a silent e drop the e with certain suffixes (ing and ed in our case): <b>make → making</b>
- e-insertion:
  * Whenever a stem ends in a sibilant and is followed by the plural morpheme s: <b>watch → watches</b>
- y-replacement:
  * The y-replacement rule which acts when verb ends in y and is followed by morpheme boundary s: <b>try → tries</b>
- k-insertion:
  * Verbs that end in a c (corresponding to a phonological k), add a k before the morpheme boundary if followed by an affix beginning with a vowel: <b>panic → panicking</b>
- Consonant doubling:
  * Like k-insertion, double final consonants in the stem in certain environments: <b>beg → begging</b>

## HPF
Hierarchical Poisson Factorization is a probabilistic approach used for collaborative filtering and matrix factorization tasks. It assumes a Poisson distribution for the observed data.
The implementation consists of 4 gamma-distributed variables that include user activity, preferences, popularity, and song attributes. The observed data, ratings, represent a Poisson distributed variable that combines the user’s preferences with the song’s attributes.

## Hyperparameters 
Starting value: 0.3. Adjusted based on the MSE score.
MCMC steps based on Metropolis. The Metropolis algorithm is a basic form of the more general Metropolis-Hastings algorithm. 

## :camera: Picture
<p align="left">
 <img src="https://github.com/Marius2504/Music-Recommendation/blob/master/predicted_sgs.png" width="600">
</p>

