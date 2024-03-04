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



