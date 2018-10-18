# -*- coding: utf8 -*-
from __future__ import unicode_literals
from sitemap import Sitemap


class SitemapLoader(object):

    @staticmethod
    def load_from_url(url):
        return Sitemap.from_url(url)

    @staticmethod
    def load_from_robots(robots_url):
        pass
