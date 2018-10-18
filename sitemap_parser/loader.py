# -*- coding: utf8 -*-
from __future__ import unicode_literals

import re

import requests

from sitemap import Sitemap


class SitemapLoaderError(Exception):
    pass


class SitemapLoaderRobotsLoadError(SitemapLoaderError):
    pass


class SitemapLoaderRobotsParseError(SitemapLoaderError):
    pass


class SitemapLoader(object):
    Error = SitemapLoaderError
    RobotsLoadError = SitemapLoaderRobotsLoadError
    RobotsParseError = SitemapLoaderRobotsParseError

    ROBOTS_SITEMAP_RE = re.compile(r'^\s*sitemap:\s?(https?://.*)\s*$', re.I | re.U | re.M)

    @classmethod
    def from_url(cls, url):
        return Sitemap.from_url(url)

    @classmethod
    def from_robots(cls, robots_url):
        try:
            response = requests.get(robots_url, timeout=30)
        except requests.HTTPError as e:
            raise cls.RobotsLoadError("robots.txt from {} return {} status code".format(robots_url, e.response.status_code))

        robots_txt = response.content
        sitemaps = cls.ROBOTS_SITEMAP_RE.findall(robots_txt)
        if not sitemaps:
            raise cls.RobotsParseError("robots.txt from {} sitemaps not found".format(robots_url))

        sitemaps = set([s.strip() for s in sitemaps])

        return [Sitemap.from_url(url) for url in sitemaps]
