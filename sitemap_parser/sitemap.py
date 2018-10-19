# -*- coding: utf8 -*-
from __future__ import unicode_literals

import gzip
import urllib
from cStringIO import StringIO

import requests
from lxml import etree as ET


class SitemapError(Exception):
    pass


class SitemapParsingError(SitemapError):
    pass


class SitemapDownloadError(SitemapError):
    pass


class SitemapDecodingError(SitemapError):
    pass


class Sitemap(object):
    Error = SitemapError
    ParsingError = SitemapParsingError
    DownloadError = SitemapDownloadError
    DecodingError = SitemapDecodingError

    def __init__(self, sitemap_tree=None, sitemap_url=None):
        self._sitemap_tree = sitemap_tree
        self._sitemap_url = None
        if sitemap_url:
            self._sitemap_url = sitemap_url.strip()

    def __unicode__(self):
        return self._sitemap_url

    def __repr__(self):
        return "<Sitemap: {}>".format(self._sitemap_url)

    @property
    def url(self):
        return self._sitemap_url

    @property
    def _sitemap(self):
        if self._sitemap_tree is not None:
            return self._sitemap_tree

        if self._sitemap_url:
            try:
                self._sitemap_tree = ET.fromstring(self.download_sitemap(self._sitemap_url))
            except ET.XMLSyntaxError as e:
                raise self.ParsingError("Sitemap {} parsing error: {}".format(self._sitemap_url, e))
            return self._sitemap_tree

    @classmethod
    def download_sitemap(cls, sitemap_url):
        try:
            r = requests.get(sitemap_url, timeout=30)
            r.raise_for_status()
        except requests.HTTPError as e:
            raise cls.DownloadError("Sitemap {} return {} status code".format(sitemap_url, e.response.status_code))

        if r.headers.get("Content-Type") == "application/x-gzip" or sitemap_url.endswith('.gz'):
            try:
                return gzip.GzipFile(fileobj=StringIO(r.content)).read()
            except IOError as e:
                raise cls.DecodingError("Sitemap {} decoding error: {}".format(sitemap_url, e))
        else:
            return r.content

    @property
    def _ns(self):
        return self._sitemap.getroottree().getroot().nsmap[None]

    @classmethod
    def from_url(cls, sitemap_url):
        return cls(sitemap_url=sitemap_url)

    @classmethod
    def from_path(cls, sitemap_file_path):
        with open(sitemap_file_path) as f:
            return cls.from_file(f)

    @classmethod
    def from_file(cls, sitemap_file):
        return cls.from_string(sitemap_file.read())

    @classmethod
    def from_string(cls, sitemap_string):
        try:
            return cls(ET.fromstring(sitemap_string))
        except ET.XMLSyntaxError as e:
            raise cls.ParsingError("Sitemap parsing error: {}".format(e))

    @property
    def links(self):
        res = set()
        for url in self._sitemap.xpath("/s:urlset/s:url/s:loc/text()", namespaces={'s': self._ns}):
            res.add(url)
        return list(res)

    @property
    def sitemaps(self):
        sitemaps = set([sitemap.strip() for sitemap in self._sitemap.xpath("/s:sitemapindex/s:sitemap/s:loc/text()", namespaces={'s': self._ns})])

        return [self.__class__(sitemap_url=url) for url in sitemaps]
