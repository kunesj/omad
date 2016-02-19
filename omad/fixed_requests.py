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

import sys, os, time
import requests


class FixedRequests(object):
    DEFAULT_HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'}

    def __init__(self, use_cookies=True, max_errors=5):
        self.max_errors = max_errors
        
        # cookies
        self.use_cookies = use_cookies
        self.cookies = {}
        
        # requests arguments
        self.args_timeout = 30
        self.args_headers = dict(self.DEFAULT_HEADERS)
    
    ###
    # Getters, Setters, Updaters
    ###
    
    def getHeaders(self):
        return self.args_headers
    
    def setHeaders(self, new_headers):
        self.args_headers = dict(new_headers)
    
    def updateHeaders(self, new_headers):
        self.args_headers.update(new_headers)
    
    def getCookies(self):
        return self.cookies
    
    def setCookies(self, new_cookies):
        self.cookies = dict(new_cookies)
    
    def updateCookies(self, new_cookies):
        self.cookies.update(new_cookies)
    
    def getTimeout(self):
        return self.args_timeout
    
    def setTimeout(self, new_timeout):
        self.args_timeout = new_timeout
    
    ###
    # Methods from requests library
    ###
    
    def get(self, **kwargs):
        """ Only accepts keyword arguments """
        kwargs = self._fillKWARGS(**kwargs)        
        
        error_num = 0
        while True:
            if error_num >= self.max_errors:
                raise Exception("Request failed too many times ("+str(error_num)+" times).")
            
            response_ok = True
            try:
                r = requests.get(**kwargs)
            except requests.exceptions.ConnectionError:
                logger.warning("Connection refused")
                response_ok = False
            if not self._testStatusCode(r.status_code):
                response_ok = False
            
            if response_ok:
                break
            else:
                error_num += 1
                time.sleep(1)
                continue
        
        # update cookies
        if self.use_cookies:
            self.updateCookies(r.cookies.get_dict())
        
        return r
    
    ###
    # Private methods
    ###
    
    def _fillKWARGS(self, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.args_timeout
        if "headers" not in kwargs:
            kwargs["headers"] = self.args_headers
        
        if self.use_cookies:
            kwargs["cookies"] = self.cookies
        
        return kwargs
    
    def _testStatusCode(self, status_code):
        """ Returns True if status code is OK """
        # status code is OK by default
        code_ok = True
        
        # specific status codes messages
        codes = {
                200: "OK",
                301: "Moved Permanently",
                404: "Not Found", 
                503: "Service Unavailable"
                }
        
        # detect status code type
        if status_code >= 100 and status_code < 200:
            code_type = "Informational"
        elif status_code >= 200 and status_code < 300:
            code_type = "Success"
        elif status_code >= 300 and status_code < 400:
            code_type = "Redirection"
        elif status_code >= 400 and status_code < 500:
            code_type = "Client Error"; code_ok = False
        elif status_code >= 500 and status_code < 600:
            code_type = "Server Error"; code_ok = False
        else:
            code_type = "Unknown"
        
        # get status code info
        if status_code in codes:
            code_info = codes[status_code]
        else:
            code_info = ""
        
        # log status code and return if it's OK
        logger.info( code_type+" - "+str(status_code)+" "+code_info+" [code_ok="+str(code_ok)+"]" )
        return code_ok
