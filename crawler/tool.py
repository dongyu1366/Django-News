import re

CATEGORY_TAG = {
    'Politics': 'politics',
    'Cross-Strait': 'cross-strait',
    'Business': 'business',
    'Society': 'society',
    'Sports': 'sports',
    'Science & Tech': 'sci-tech',
    'Culture': 'culture',
    'AD': 'ad'
}


REMOVE_AUTHOR = re.compile(r'<div class="author">.+<\\div>')
REMOVE_P_TAG = re.compile(r'(<p>)|(<\/p>)')
