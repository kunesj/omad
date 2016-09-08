#!/usr/bin/env python3
# encoding: utf-8

import logging
logger = logging.getLogger(__name__)
import traceback

import sys, os, time
import requests

class FixedRequests(object):
    DEFAULT_HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'}

    def __init__(self, use_cookies=True, max_errors=5):
        self.max_errors = max_errors
        self.error_sleep_time = 1

        # cookies
        self.use_cookies = use_cookies
        self.cookies = {}

        # requests arguments
        self.args_timeout = 30
        self.args_headers = dict(self.DEFAULT_HEADERS)

        # request delay
        self.request_delay = 0 # min time delay between requests
        self.last_request_time = 0

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

    def setRequestDelay(self, delay):
        self.request_delay = delay

    ###
    # Methods from requests library
    ###

    def get(self, **kwargs):
        """ Only accepts keyword arguments """
        kwargs["req_type"] = "get"
        return self._request(**kwargs)

    def post(self, **kwargs):
        """ Only accepts keyword arguments """
        kwargs["req_type"] = "post"
        return self._request(**kwargs)

    ###
    # Private methods
    ###

    def _request(self, **kwargs):
        """
        * Generic request function
        * Only accepts keyword arguments
        * Needs to have "req_type": "get"/"post"
        """
        kwargs = self._fillKWARGS(**kwargs)

        if "req_type" not in kwargs:
            kwargs["req_type"] = "get"
        req_type = kwargs["req_type"]
        del(kwargs["req_type"])

        error_num = 0
        while True:
            if error_num >= self.max_errors:
                raise Exception("Request failed too many times ("+str(error_num)+" times).")

            response_ok = True
            try:
                self._delayRequests()
                if req_type == "get":
                    r = requests.get(**kwargs)
                elif req_type == "post":
                    r = requests.post(**kwargs)
                else:
                    raise Exception("Unknown request type!")
                if not self._testStatusCode(r.status_code):
                    response_ok = False
            except requests.exceptions.ConnectionError:
                logger.warning("Connection refused")
                response_ok = False

            if response_ok:
                break
            else:
                error_num += 1
                time.sleep(self.error_sleep_time)
                continue

        # update cookies
        if self.use_cookies:
            self.updateCookies(r.cookies.get_dict())

        return r

    def _delayRequests(self):
        """ makes sure that self.request_delay is obeyed """
        if self.request_delay == 0:
            return

        deltat = time.time() - self.last_request_time
        if deltat < self.request_delay:
            time.sleep(float(self.request_delay)-deltat)

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
