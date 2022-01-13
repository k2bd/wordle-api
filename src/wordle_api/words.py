from functools import lru_cache

from english_words import english_words_lower_alpha_set


@lru_cache(maxsize=None)
def candidate_words(size: int):
    """
    Get English words of a particular size
    """
    return sorted(word for word in english_words_lower_alpha_set if len(word) == size)
