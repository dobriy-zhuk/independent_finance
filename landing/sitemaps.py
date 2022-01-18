from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class MainSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['index', 'courses', 'camp', 'countrycamp', 'contact']

    def location(self, item):
        return reverse(item)
