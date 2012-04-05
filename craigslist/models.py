from django.db import models
from django.contrib.auth.models import User

class cl_Site(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __unicode__(self):
        return self.name

class cl_Site_subSite(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    cl_Site = models.ForeignKey(cl_Site)

class cl_Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

class cl_Category_subCat(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    cl_Category = models.ForeignKey(cl_Category)

    def __unicode__(self):
        return self.name

class cl_GleanQuery(models.Model):
    user = models.ManyToManyField(User)
    cl_Categories = models.ManyToManyField(cl_Category, blank=True)
    cl_Categories_subCat = models.ManyToManyField(cl_Category_subCat, blank=True)
    expiration_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now=True)
    search_term = models.CharField(max_length=255)
    cl_Sites = models.ManyToManyField(cl_Site)
    cl_Sites_subSites = models.ManyToManyField(cl_Site_subSite, blank=True)
    notification_frequency = models.IntegerField()
    execution_frequency = models.IntegerField()
    last_execution = models.DateTimeField(null=True, blank=True)
    min_price = models.IntegerField(blank=True, null=True)
    max_price = models.IntegerField(blank=True, null=True)
    has_image = models.BooleanField()
    only_search_titles = models.BooleanField()
    active = models.BooleanField()

    def __unicode__(self):
        return self.search_term
    def number_Of_Results(self):
        return cl_GleanResult.objects.filter(cl_GleanQuery=self).count()
class cl_GleanResult(models.Model):
    title = models.CharField(max_length=255)
    posted = models.DateTimeField(blank=True, null=True)
    url = models.URLField(unique=True)
    image_url = models.URLField()
    location = models.CharField(max_length=255)
    gleaned_time = models.DateTimeField()
    telephone_number = models.CharField(max_length=25)
    reply_to_address = models.EmailField()
    cl_GleanQuery = models.ForeignKey(cl_GleanQuery)
    description = models.TextField()

    def __unicode__(self):
        return self.title

