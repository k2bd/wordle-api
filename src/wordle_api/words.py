from functools import lru_cache
from string import ascii_lowercase

from english_words import english_words_lower_alpha_set


@lru_cache(maxsize=None)
def candidate_words(size: int):
    """
    Get English words of a particular size
    """
    possible_words = {
        word
        for word in english_words_lower_alpha_set
        if all(letter in ascii_lowercase for letter in word)
    }
    return sorted(word for word in possible_words if len(word) == size)
