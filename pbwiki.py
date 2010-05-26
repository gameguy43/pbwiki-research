#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple python binding for PBWiki.  At this point it really only has a
specific method for returning page information grouped by date, but the api call
infrastructure may be useful.
"""
from urllib import urlopen, urlencode, quote as urlquote
from collections import defaultdict
from itertools import groupby
import operator
import time

__author__ = "Chris Murphy"
__email__ = "chrismurf@gmail.com"
__copyright__ = "Copyright 2009, Chris Murphy"
__version__ = "0.1"

# Constants for grouping level
YEAR, MONTH, DAY, HOUR, MINUTE, SECOND = range(1, 7)

class PBWiki(object):
    def __init__(self, url):
      """Create a PBWiki object, which can be used to later make API calls against
      a PBWiki site.
      url - the wiki base URL in (EXACTLY) the form 'https://site_name.pbwiki.com'
      """
      # TODO: this fails if the wiki has a trailing slash.  let's fix that programatically
      self.url = url
      self._authenticate()
  
    def _authenticate(self):
      """Authenticate against a pbwiki site so that API calls can be placed.
      """
      # Request front page so that we get a cookie, used later for authentication
      f = urlopen(self.url)
      f.read()
      f.close()
  
    # PB Wiki API is documented at https://some_wiki_name.pbwiki.com/api_v2/
    def _api_call(self, oper, **kwargs):
      """Make an API call against a pbwiki site.
      oper - the operation to perform
      ** any other keyword arguments are passed on to the API call
      """
      # Generate an appropriate API call URL
      kwargs['_type'] = 'jsontext'
      argstr = '/'.join(["%s/%s" % (k,v) for k, v in kwargs.iteritems()])
      call_url = '%s/api_v2/op/%s/%s' % (self.url, oper, argstr)
      #print call_url
      # Fetch text and strip off first and last lines, which are comment tags
      doc = urlopen(call_url)
      json = '\n'.join(doc.read().split('\n')[1:-2])
      doc.close()
  
      # Use eval to get a python dict (JSON looks a lot like python)
      # TODO: These next two lines are fragile - replace with a proper JSON parser
      json_translation_table = {'true': True, 'false': False, 'null': None}
      return eval(json, json_translation_table, {})  

    def api_call(self, oper, **kwargs):
      """Make an API call against a pbwiki site.
      oper - the operation to perform
      ** any other keyword arguments are passed on to the API call
      """
      # Generate an appropriate API call URL
      kwargs['_type'] = 'jsontext'
      argstr = '/'.join(["%s/%s" % (k,v) for k, v in kwargs.iteritems()])
      call_url = '%s/api_v2/op/%s/%s' % (self.url, oper, argstr)
      #print call_url
      # Fetch text and strip off first and last lines, which are comment tags
      doc = urlopen(call_url)
      json = '\n'.join(doc.read().split('\n')[1:-2])
      doc.close()
  
      # Use eval to get a python dict (JSON looks a lot like python)
      # TODO: These next two lines are fragile - replace with a proper JSON parser
      json_translation_table = {'true': True, 'false': False, 'null': None}
      return eval(json, json_translation_table, {})  
  
    def grouped_by_date(self, level=DAY):
      """Fetch all revisions of all pages for a site, grouped by revision dates.
      level - the level of grouping to perform (Day ? Month?) 
      """
      # First fetch all pages into a dictionary
      all_pages = self._api_call('GetPages')['pages']
      dates = defaultdict(list)
      for page in all_pages:
        pagerevs = self._api_call('GetPageRevisions', page=urlquote(page['name']))
        revnums = [int(pgrev) for pgrev in pagerevs['revisions']]
        allrevtimes = [ (time.gmtime(rev)[:level], rev) for rev in revnums ]
        allrevtimes.sort(key=operator.itemgetter(0))
  
        for group, revtimes in groupby(allrevtimes, key=operator.itemgetter(0)):
          onlytimes = tuple(map(operator.itemgetter(1), revtimes))
          dates[group].append( (page['name'], onlytimes) )
  
      # Now convert dictionary to a sorted list
      alldates = list(dates.iteritems())
      alldates.sort(key=operator.itemgetter(0))
      return alldates
  
    def get_files(self, url):
        wiki_files = self._api_call('GetFiles')
        return wiki_files

    def get_page(self, url):
        wiki_page = self._api_call('GetPage', page='FrontPage')
        return wiki_page

    def get_pages(self, url):
        wiki_pages = self._api_call('GetPages')
        return wiki_pages

    def get_times(self, url):
        wiki_times = self._api_call('GetTimes')
        return wiki_times
