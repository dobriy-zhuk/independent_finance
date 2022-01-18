from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
import unidecode


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, max_length=200, editable=False)
    image = models.FileField(upload_to='blog/', default='blog/logo-rus.png')
    meta_title = models.CharField(max_length=80)
    meta_description = models.CharField(max_length=160)
    meta_keywords = models.CharField(max_length=1000, default='')
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Posts'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode.unidecode(self.title))
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=(self.slug,))

    def __str__(self):
        return self.title


