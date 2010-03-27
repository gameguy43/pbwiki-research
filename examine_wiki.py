#!/usr/bin/env python
from pbwiki import *
from store_wikis import *

## Collection of json parsers
# Takes data from pbworks, makes db insertable dicts
def parse_page(json):
    #print json
    page_dict = {
        'page_checked_at' : json['_valid_as_of'], # somewhat obsoleted by page_url which has rev timestamp
        'page_url' : json['revurl'], # persistant url of checked page
        'page_name' : json['name'], # often 'FrontPage' in current implementattion
        'page_revision' : json['revcount'], # int
        'page_char_size' : json['size'], # int character count
        'page_html' : json['html'] # html for analysis, tokenize/strip-formating somewhere else
    }
    return page_dict

def parse_files(json):
    #print json
    files_dict = {
        'files_checked_at' : json['_valid_as_of'], # handy to capture when this was checked for rolling updates
        'files_count' : json['_total_count'],
        'files_list' : json['files'],
    }
    # cast list as string, remove this when needed
    files_dict['files_list'] = str(files_dict['files_list'])
    return files_dict

def parse_times(json):
    times_dict = {
        'times_checked_at' : json['_valid_as_of'],
        'time_comment' : json['commenttime'], # timestamp of last comment
        'time_file' : json['filetime'], # timestamp of last uploaded(?) file
        'time_pageedit' : json['pagetime'], # last edit/move/create page
        'time_permission' : json['permtime'], # last permission edit
        'time_tag' : json['tagtime'] # last tag added/edited/removed
    }
    return times_dict

def parse_pages(json):
    # Take json from get_pages, turn into nice dict
    pages = json['pages']
    pages_list = []
    for i in pages:
        #print i['name']
        pages_list.append(i['name'])
    pages_dict = { 
        'pages_count': json['_total_count'], # number of pages in wiki
        'pages_list': pages_list # make sure list is not problematic
    }
    # cast list as string, remove this when needed
    pages_dict['pages_list'] = str(pages_dict['pages_list'])
    return pages_dict

def examine_wiki(url):
    # Controller for PBWiki class
    # Makes several api calls about wiki
    # Passes joined dict to be stored
    myswiki = PBWiki(url)
    try:
        files_json = myswiki.get_files(url)
        files_dict = parse_files(files_json)
        #print "files_dict stored"
        pages_json = myswiki.get_pages(url)
        pages_dict = parse_pages(pages_json)
        #print "page_dict stored"
        times_json = myswiki.get_times(url)
        times_dict = parse_times(times_json)
        #print "times_dict"
        page_json = myswiki.get_page(url)
        page_dict = parse_page(page_json)
        #print "page_dict"
        #name_dict = {"url" : url, "works" : 1}
        data_dict = dict(pages_dict.items() + files_dict.items() + times_dict.items() + page_dict.items() )
        data_dict['url'] = url
        data_dict['works'] = 1
        print url + " seems good"
    except KeyboardInterrupt:
        sys.exit(0)
        self.queue.task_done()
    except:
        print "Oops, that url doesn't work: " + url
        data_dict = {'url' : url, 'works' : '0'}
    return data_dict

def get_wikilist():
    # Read the semi-private list of wikis from file
    l = open('./list', 'r')
    ll = []
    for row in l:
        ll.append(row)    
    return ll

def traverse_wikis():
    # ?? Iterate over wikis and call other bits of api ?
    return wikipages

def store_wiki_dict(dict):
    i = wikis_table.insert()
    i.execute(dict)
    return 

def glue():
    test_url = 'http://testapi.pbworks.com'
    wiki_list = get_wikilist()
    for wikiplus in wiki_list:
        wiki = wikiplus[:-1]
        wiki_data = examine_wiki(wiki)
        store_wiki_dict(wiki_data)
        print wiki + " stored"
    return wiki_list
    
if __name__ == '__main__':
    wd = glue()
