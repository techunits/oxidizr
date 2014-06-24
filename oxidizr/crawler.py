#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.web.client import getPage
from twisted.python.util import println
from BeautifulSoup import BeautifulSoup
from twisted.python import log
from twisted.internet import defer, task, reactor
import re
from urlparse import urlparse
# Needs : PyOpenSSL and Twisted 12.3+
 

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
        parsed = urlparse(url)
        if parsed.netloc and parsed.netloc != 'www.webhostingtalk.com':
            url = 'http://%s/' % parsed.netloc
        if url not in q:
            print url
            # q.append(url)


def extractLinks(html, url):
    print "URL in extractLinks: ", url
    soup = BeautifulSoup(html)
    soup.prettify()
    return [str(anchor['href'])
            for anchor in soup.findAll('a', attrs={'href': re.compile("^http://")}) if anchor['href']]
 

def crawlPage(url, urlList):
    sleep(10)
    d = getPage(url)
    d.addCallback(extractLinks, url)
    d.addCallback(union, urlList)
    d.addErrback(log.err)
    return d
 
 
# def crawler(urls):
#     urls = list(urls)

 
def main(reactor, *args):
    urls = list(args)
    return parallel(urls, len(urls), crawlPage, urls)
 
 
if __name__ == '__main__':
    import sys
    task.react(main, ["http://www.webhostingtalk.com"])  # Can pass a list of urls
