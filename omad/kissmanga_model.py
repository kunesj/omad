#!/usr/bin/python2
# coding: utf-8
"""
This file is part of OMAD.

OMAD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

OMAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OMAD.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
logger = logging.getLogger(__name__)
import traceback

import requests
try:
    from BeautifulSoup import BeautifulSoup
except:
    # windows fix
    from bs4 import BeautifulSoup 

from archive_controller import ArchiveController

class KissmangaModel():    
    def __init__(self, series_url, gui_info_fcn):
        # default is download_controller.defaultInfoFcn
        self.gui_info_fcn = gui_info_fcn
        self.series_url = series_url
        
        self.cookies = {}
    
    def getRealPage(self, html, url):
        import js2py
        
        html = unicode(html)
        soup = BeautifulSoup(html)
        
        hidden_form = soup.body.find('form', attrs={'id':"challenge-form"})
        if hidden_form is None:
            return html
        
        get_params = {"jschl_vc":None, "pass":None, "jschl_answer":None}
        inputs = hidden_form.findAll('input')
        for i in inputs:
            get_params[i.get('name')] = i.get('value')
        
        # get important parts of script
        script = soup.head.find('script').text
        script_setTimeout_fcn = script.split("setTimeout(function(){")[-1].split("}")[0]+"}"
        script_fcn_end = script.split("setTimeout(function(){")[-1].split("}")[1]
        #print script_setTimeout_fcn
        #print script_fcn_end 
        
        # get script lines
        script_lines = []
        script_lines += [script_setTimeout_fcn.split(';')[0].strip()]
        for l in script_fcn_end.split('\n'):
            l_split = l.split(';')
            #filter and modify lines
            l_filtered = []
            for ls in l_split:
                ls = ls.strip()
                if ls.startswith('a.value ='):
                    ls = ls.replace('a.value =', 'a =')
                elif ls.startswith("t = t.firstChild.href"):
                    ls = "t = 'http://kissmanga.com/'"
                
                if ls == '' or ls.startswith('f.submit') or ls.startswith('f = ') or ls.startswith('a = document.get')\
                    or ls.startswith('t = document.') or ls.startswith('t.innerHTML'):
                    continue
                else:
                    l_filtered.append(ls)
            script_lines += l_filtered
        script_edited = ";\n".join(script_lines)+";"
        #print script_edited
        
        result = js2py.eval_js('function fcn() {\n'+script_edited+'\nreturn a;};')()
        get_params["jschl_answer"] = result
        #print result
        
        custom_headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
                    'referer': url, 'host':"kissmanga.com"}
        
        r = requests.get("http://kissmanga.com/cdn-cgi/l/chk_jschl", timeout=30, params=get_params, headers=custom_headers, cookies=self.cookies)
        self.cookies.update(r.cookies)
        html = unicode(r.text)
        
        #print html
        #print get_params
        
        print "Not finished!!!"
        exit(1) # TODO
        
    def getChaptersList(self):
        r = requests.get(self.series_url, timeout=30, cookies=self.cookies)
        self.cookies.update(r.cookies)
        html = unicode(r.text)
        #html = self.getRealPage(html, self.series_url)
        soup = BeautifulSoup(html)

        table_ch = soup.body.find('table', attrs={'class':'listing'})
        en_chs = table_ch.findAll('a')

        processed_chapters = []
        for ch in en_chs:
            name = ch.get('title').strip()
            name = BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).text
            href = ch.get('href')
            if not 'kissmanga.com' in href:
                href = 'http://kissmanga.com/'+href
            processed_chapters.append([name, href])
            
        processed_chapters.reverse()
        
        return processed_chapters
        
    def downloadChapter(self, chapter, downloadPath):
        """
        chapter = [name, url]
        """
        full_gallery_url = chapter[1]
        
        try:
            r = requests.get(full_gallery_url, timeout=30, cookies=self.cookies)
            self.cookies.update(r.cookies)
            html = unicode(r.text)
            #html = self.getRealPage(html, full_gallery_url)
            soup = BeautifulSoup(html)
            
            # parse html
            series_name = full_gallery_url.split('/Manga/')[-1].split('/')[0]
            ch_name = series_name+' - '+full_gallery_url.split('/')[-1].split('?')[0]
            ch_name = BeautifulSoup(ch_name, convertEntities=BeautifulSoup.HTML_ENTITIES).text
            grp_name = ''
            
            pages = []
            scripts = soup.body.findAll('script', attrs={'type':'text/javascript'})
            for script in scripts:
                if script.text.strip().startswith('var lstImages = new Array();'):
                    lines = script.text.split('\n')
                    for l in lines:
                        if l.strip().startswith('lstImages.push('):
                            pages.append(l.strip().split('lstImages.push("')[-1].split('");')[0])
            
            if len(pages)==0:
                raise Exception("No pages in chapter! Wrong URL?")
            
            galery_size = len(pages)
            galeryurl = full_gallery_url
        except Exception, e:
            logger.exception('Failed to parse chapter page for: '+full_gallery_url)
            self.gui_info_fcn("Error downloading/parsing chapter html")
            return False # failed download            

        logger.info('Downloading: '+ch_name)
        logger.info('Pages: '+str(galery_size))
        logger.info('Images url: '+galeryurl)

        # create temp folder for downloads
        ac = ArchiveController(downloadPath)
        ac.mkdir()

        errors = 0
        for i in range(len(pages)):
            self.gui_info_fcn("Downloading page "+str(i+1)+"/"+str(len(pages)))
                
            img_url = pages[i]
            img_ext = img_url.split('.')[-1].split('?')[0]                
            
            logger.info(img_url)
            
            if i<10:
                num = '000'+str(i)
            elif i<100:
                num = '00'+str(i)
            elif i<1000:
                num = '0'+str(i)
            else:
                num = str(i)
            
            img_filename = num+'.'+img_ext
            
            try:
                ac.download(img_url, img_filename)
            except Exception, e:
                logger.exception('BAD download for: '+img_url)
                self.gui_info_fcn("Error downloading page image")
                errors+=1
            else:
                logger.debug('OK download')

        logger.info("Download finished, Failed downloads = "+str(errors))
        
        if grp_name != '':
            grp_name = ' ['+grp_name+']'
        archive_name = ac.sanitize_filename(ch_name+grp_name+'.zip')
        
        self.gui_info_fcn('Compressing to: '+archive_name)
        ac.zipdir(archive_name)
        
        ac.rmdir()
        
        if errors>0:
            return False
        else:
            return True
