class CategoryTool:
    CATEGORY_DICT = {
        'politics': 'Politics',
        'cross-strait': 'Cross-Strait',
        'business': 'Business',
        'society': 'Society',
        'sports': 'Sports',
        'sci-tech': 'Science & Tech',
        'culture': 'Culture',
        'ad': 'AD'
    }

    TAG_DICT = {
        'Politics': 'politics',
        'Cross-Strait': 'cross-strait',
        'Business': 'business',
        'Society': 'society',
        'Sports': 'sports',
        'Science & Tech': 'sci-tech',
        'Culture': 'culture',
        'AD': 'ad'
    }

    @classmethod
    def category_to_tag(cls, category):
        tag = cls.TAG_DICT[category]
        return tag
