#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from urlparse import urlparse
import datetime
import pytz

from twisted.web.client import getPage
from twisted.python.util import println
from BeautifulSoup import BeautifulSoup
from twisted.python import log
from twisted.internet import defer, task, reactor
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from apps.websites.models import Website
from apps.content.models import Content
from apps.common import helpers


def sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d


def parallel(iterable, count, callable, *args, **named):
    coop = task.Cooperator()
    work = (callable(elem, *args, **named) for elem in iterable)
    return defer.DeferredList([coop.coiterate(work) for i in xrange(count)])
 
 
def union(p, q):
    for url in p:
        parsed = urlparse(str(url))
        if parsed.netloc and parsed.netloc != 'www.webhostingtalk.com':
            url = 'http://%s/' % parsed.netloc
        if parsed.netloc and url not in q:
            print url
            if parsed.netloc != 'www.webhostingtalk.com':
                # Insert into Site
                try:
                    Website.objects.create(
                        url=url,
                        name=parsed.netloc,
                        last_crawled_at=datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                    )
                except IntegrityError:
                    println('%s - already existed in Site' % url)
            else:
                # We want to deep crawl webhosting talk
                q.append(url)


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def extract_context(html, url):
    soup = BeautifulSoup(html)
    # Insert into Content (under this domain)
    texts = soup.findAll(text=True)
    try:
        Content.objects.create(
            url=url,
            title=soup.title.string,
            summary=helpers.strip_tags(" \n".join(filter(visible, texts)))[:4000],
            last_crawled_at=datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        )
    except IntegrityError:
        println('%s - already existed in Content' % url)
    soup.prettify()
    return [str(anchor['href'])
            for anchor in soup.findAll('a', attrs={'href': re.compile("^http://")}) if anchor['href']]


def crawl_page(url, urlList):
    sleep(10)
    d = getPage(url)
    d.addCallback(extract_context, url)
    d.addCallback(union, urlList)
    d.addErrback(log.err)
    return d

 
def main(reactor, *args):
    urls = list(args)
    return parallel(urls, len(urls), crawl_page, urls)
 

class Command(BaseCommand):
    def handle(self, *args, **options):
        for site in Website.objects.filter(is_deep_crawl=True):
            site.last_crawled_at = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
            site.save()
            task.react(main, [str(site.url)]) # Can pass a list of urls