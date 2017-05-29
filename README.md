# AboutTranslationClf

<b> about_translation.py</b>

Functions to classify whether a text is about the translation quality.

<b> make_wordlist.py </b>

Makes a wordlist used by about_translation.py.
Wordlist will contain words that are typical for texts about translation quality.
Wordlist is created on the basis of upvoted.tab (the annotated data)

<b> split_upvoted.py </b>
Splits upvoted in two random sets. One to make the wordlist and one to evaluate the classifier.

<b> evaluate_translation_extractor.py </b>
Evaluates the about_translation classifier.
