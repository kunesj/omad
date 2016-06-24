#!/usr/bin/env python3
# encoding: utf-8

import unittest
from nose.plugins.attrib import attr

from omad.fixed_requests import FixedRequests

class FixedRequestsTest(unittest.TestCase):

    def getsetupdate_test(self):
        # test values
        headers1 = {'user-agent':'Firefox', 'referer': '127.0.0.1'}
        headers2 = {'user-agent':'Chrome'}
        headers_updated = dict(headers1); headers_updated.update(headers2)
        cookies1 = {'CAKE':'IS A', 'LIE':'!'}
        cookies2 = {'CAKE':'IS NOT A'}
        cookies_updated = dict(cookies1); cookies_updated.update(cookies2)
        timeout1 = 666

        fr = FixedRequests()

        # test headers
        fr.setHeaders(headers1)
        get = fr.getHeaders()
        self.assertEqual(get['user-agent'], headers1['user-agent'])
        self.assertEqual(get['referer'], headers1['referer'])
        self.assertEqual(len(get), 2)

        fr.updateHeaders(headers2)
        get = fr.getHeaders()
        self.assertEqual(get['user-agent'], headers_updated['user-agent'])
        self.assertEqual(get['referer'], headers_updated['referer'])
        self.assertEqual(len(get), 2)

        # test cookies
        fr.setCookies(cookies1)
        get = fr.getCookies()
        self.assertEqual(get['CAKE'], cookies1['CAKE'])
        self.assertEqual(get['LIE'], cookies1['LIE'])
        self.assertEqual(len(get), 2)

        fr.updateCookies(cookies2)
        get = fr.getCookies()
        self.assertEqual(get['CAKE'], cookies_updated['CAKE'])
        self.assertEqual(get['LIE'], cookies_updated['LIE'])
        self.assertEqual(len(get), 2)

        # test timeout
        fr.setTimeout(timeout1)
        get = fr.getTimeout()
        self.assertEqual(get, timeout1)
