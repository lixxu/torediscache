#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class ToredisTool(object):
    def __init__(self, cache=None, **kwargs):
        if cache:
            self.init_cache(cache)
        else:
            self._cache = None

        self.prefix = kwargs.get('redis_prefix', 'toredistool')
        ip = kwargs.get('ip')
        if ip:
            self.init_key_prefix(ip)
        else:
            self._key_prefix = None

    def init_cache(self, cache):
        self._cache = cache

    @property
    def cache(self):
        return self._cache

    @property
    def key_prefix(self):
        return self._key_prefix

    def init_key_prefix(self, remote_ip):
        if isinstance(remote_ip, basestring):
            ip = remote_ip
        else:
            if hasattr(remote_ip, 'request'):  # handler instance
                request = remote_ip.request
            else:
                request = remote_ip

            x_real_ip = request.headers.get("X-Real-IP")
            ip = x_real_ip or request.remote_ip

        self._key_prefix = self.prefix + ip

    def set_cache(self, key, value, timeout=300):
        self.cache.setex(self.get_cache_key(key), value, timeout)

    def get_cache(self, key, remove=False):
        k = self.get_cache_key(key)
        value = self.cache.get(k)
        if remove:
            self.cache.delete(k)

        return value

    def delete_cache(self, key):
        self.cache.delete(self.get_cache_key(key))

    def flash(self, msg, category='info', timeout=2):
        self.set_cache('flash-cat', category, timeout=timeout)
        if not isinstance(msg, basestring):
            msg = '{}'.format(msg)

        self.set_cache('flash-msg', msg, timeout=timeout)

    def get_cache_key(self, key):
        return self.key_prefix + key

    def get_flashed_messages(self, remove=True):
        category = self.get_cache('flash-cat', remove=remove)
        msg = self.get_cache('flash-msg', remove=remove)
        return category, msg
