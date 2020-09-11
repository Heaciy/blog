from haystack import indexes
from myblog.models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(null=True, model_attr='title')
    title_description = indexes.CharField(null=True, model_attr='title_description')
    content = indexes.CharField(null=True, model_attr='content')

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
