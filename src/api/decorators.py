#!/usr/bin/env python3
"""Contains all decorators for our API"""

import functools

import gevent
from flask import g, jsonify, request

# TODO: convert pseudo-code to working code

# email sending decorator
def email(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        envelope = f(*args, **kwargs)
        envelope.from_addr = api.config["SYSTEM_EMAIL"]

        def task():
            smtp().send(envelope)

        gevent.spawn(task)
        return jsonify({"status": "OK"})

    return wrapped


# rate limiting request decorator
def limit(requests=100, window=60, by="ip", group=None):
    if not callable(by):
        by = {"ip": lambda: request.headers.remote_addr}[by]

    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            group = group or request.endpoint
            key = ":".join(["rl", group, by()])

            try:
                remaining = requests - int(redis.get(key))
            except (ValueError, TypeError):
                remaining = requests
                redis.set(key, 0)

            ttl = redis.ttl(key)
            if not ttl:
                redis.expire(key, window)
                ttl = window

            g.view_limits = (requests, remaining - 1, time() + ttl)

            if remaining > 0:
                redis.incr(key, 1)
                return f(*args, **kwargs)
            else:
                return Response("Too Many Requests", 429)

        return wrapped

    return decorator


# background tasks --- use for MAB calculations???
def background(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        jobid = uuid4().hex
        key = "job-{0}".format(jobid)
        skey = "job-{0}-status".format(jobid)
        expire_time = 3600
        redis.set(skey, 202)
        redis.expire(skey, expire_time)

        @copy_current_request_context
        def task():
            try:
                data = f(*args, **kwargs)
            except:
                redis.set(skey, 500)
            else:
                redis.set(skey, 200)
                redis.set(key, data)
                redis.expire(key, expire_time)
            redis.expire(skey, expire_time)

        gevent.spawn(task)
        return jsonify({"job": jobid})

    return wrapper
