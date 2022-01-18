from django.contrib.sitemaps import Sitemap
from .models import Post


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.published_date
