===============
 thumbs up API
===============
Public API for the  optimization of traffic using ML
----------------------------------------------------

.. image:: https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/198/thumbs-up-sign_1f44d.png

|build-status| |license|

:Version: 0.1.0
:Source: https://github.com/best-bet/thumbs-up-api
:Keywords: thumbnail, a/b_testing, multi_armed_bandit, python, api

----

.. _What is thumbs up?:

What is thumbs up?
==================

thumbs up is a tool that utilizes machine learning to help you A/B test
your thumbnails in production! This way you can find the best thumbnail
to attract the attention of your users to your products while minimizing
regret.

.. _How does it work?:

How does it work?
=================

Submit an id to the API of a piece of content that you wish to A/B test
and add some options to that content. Then add the `thumbs-up-js` npm
package to your project. You can use the Thumbnail component as a wrapper
on the content that you wish to A/B test. Whenever your users visit the
page with this content, a request will be made to the API to return one
of the options that you provided for this item. This option will be chosen
based on the decision of the Multi-Armed Bandit algorithm.

If the thumbnail that was provided attracted the attention of the user,
this information will be sent back to the API to refine the algorithm.

Over time, the algorithm will find which option is the most "clickable"
and cash in on that one to help you optimize your traffic to that product.

It is possible to use this API without using the React.js library, however
that will require you to build a custom solution, rather than the
out-of-the-box ready solution that is provided by `thumbs-up-js`.

.. _Why?:

Why?
=====

Thumbnails are often the first thing that a user will see on your page;
however a bad or bland thumbnail is easily overlooked. Choosing a good
thumbnail is one of the best ways to increase traffic to your products,
videos or blog posts. The virality of many videos on Youtube or content
on Instagram can be attributed to the ingenious marketing packaged into
the content's thumbnails.

thumbs up utilizes machine learning to help you find the most clickable
thumbnail out of a set that you provide based on real world interactions
with your users. This can significantly increase traffic to your products!

.. _What-is-the-Multi-Armed-Bandit-Algorithm?:

What is the Multi-Armed Bandit Algoritm?
========================================

In marketing terms, a multi-armed bandit solution is a ‘smarter’ or more
complex version of A/B testing that uses machine learning algorithms to
dynamically allocate traffic to variations that are performing well, while
allocating less traffic to variations that are underperforming. In theory,
multi-armed bandits should produce faster results since there is no need to
wait for a single winning variation.

The term "multi-armed bandit" comes from a hypothetical experiment where a
person must choose between multiple actions (i.e. slot machines, the
"one-armed bandits"), each with an unknown payout. The goal is to determine
the best or most profitable outcome through a series of choices. At the
beginning of the experiment, when odds and payouts are unknown, the gambler
must determine which machine to pull, in which order and how many times.
This is the “multi-armed bandit problem.”

More at: `Optimizely`_

Also: `Wikipedia`_

.. _`Optimizely`:
    https://www.optimizely.com/optimization-glossary/multi-armed-bandit/

.. _`Wikipedia`:
    https://en.wikipedia.org/wiki/Multi-armed_bandit

.. _`The Bayesian Multi-Armed Bandit`:

The Bayesian Multi-Armed Bandit
===============================

So now that we know what a multi-armed bandit solution is, which implementation
is used by thumbs up?

There are many variations on the multi-armed bandit (Epsilon-Greedy, Softmax,
UBC-1, etc.), but we have have chosen to use the **Bayesian Theorem**
(AKA Thompson Sampling or Randomized Probability Matching). *Why?*

The Bayesian Theorem will help us answer that question; it states the following:

`For two events **Y** and **Z**, the conditional probability of **Y** given **Z**
is the conditional probability of **Z** given **Y** scaled by the relative
probability of **Y** compared to **Z**: PZ=PY*P(Y)P(Z)`

This means that for every iteration of our trial, we scale the distribution of
thumbnails based on the set of previous distributions of clicks.

Basically, after every trial we recompute the probabilities of each thumbnail's
superiority, scaled by the number of trials in total. This approach will help us
get the results of the experiment in as little time as possible, with less data,
**AND** the same level of statistical validity as regular A/B testing.

If that isn't convincing enough, take Google's word for it. Google uses the Bayesian
multi-armed bandit for `Google Analytics`_!

For a detailed analysis of the Bayesian multi-armed bandit algoritm:
`A modern Bayesian look at the multi-armed bandit`_

.. _`Google Analytics`:
    https://support.google.com/analytics/answer/2844870?hl=en&ref_topic=1745207

.. _`A modern Bayesian look at the multi-armed bandit`:
    http://www.economics.uci.edu/~ivan/asmb.874.pdf

.. _getting-started:

Getting Started
===============

If you are new here, these are some resources that may be helpful:

- `Getting started with thumbs up`_

    A quick introduction to a simple setup with thumbs up.

- `API reference`_

    A comprehensive overview of the API and all of its functionality.

.. _`Getting started with thumbs up`:
    https://github.com/best-bet/thumbs-up-api/blob/master/docs/getting-started.rst

.. _`API reference`:
    https://github.com/best-bet/thumbs-up-api/blob/master/docs/api-reference.rst

.. _bug-tracker:

Bug tracker
===========

If you have any suggestions, bug reports, or annoyances please report them
to our issue tracker at https://github.com/best-bet/thumbs-up-api/issues/

.. _contributing:

Contributing
============

Development of `thumbs-up-api` happens at GitHub: https://github.com/best-bet/thumbs-up-api

Please feel free to participate in development, this project
is only made possible through open source contributions.

Be sure to also read the `Contributing to thumbs up`_ section in the
documentation.

.. _`Contributing to thumbs up`:
    https://github.com/best-bet/thumbs-up-api/blob/master/CONTRIBUTING.rst

.. _tracking-development:

Tracking Development
====================

If you are interested in tracking development, check out our `scrum board`_!

.. _`scrum board`:
    https://app.asana.com/0/1116794279727503/1116794279727503

.. _license:

License
=======

This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

.. |build-status| image:: https://secure.travis-ci.org/best-bet/thumbs-up-api.png?branch=master
    :alt: Build status
    :target: https://travis-ci.org/best-bet/thumbs-up-api

.. |license| image:: https://img.shields.io/github/license/best-bet/thumbs-up-api.svg
    :alt: MIT License
    :target: https://opensource.org/licenses/MIT
