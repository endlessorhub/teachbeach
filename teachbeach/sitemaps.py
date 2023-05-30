import json

from django.conf import settings
from django.contrib import sitemaps
from django.urls import reverse
from main.models import Class, Teacher, CompanyProfile


class ClassSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Class.objects.all().values_list('pk', flat=True)

    def location(self, item):
        return f'/class/{item}'


class TeacherSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Teacher.objects.all().values_list('pk', flat=True)

    def location(self, item):
        return f'/teacher_profile/{item}'


class CompanySitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return CompanyProfile.objects.all().values_list('pk', flat=True)

    def location(self, item):
        return f'/company_profile/{item}'


class StaticSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'


    def items(self):
        try:
            fn = settings.BASE_DIR + '/js/src/sitemap_template.json'
            with open(fn, 'r') as json_file:
                data = json.load(json_file)
                return [x['path'] for x in data['routes'] if ':' not in x['path'] and not x.get('meta', {}).get("requiresAuth", False)]
        except:
            return []

    def location(self, item):
        return item

