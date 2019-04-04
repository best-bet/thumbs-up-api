guidelines for contributing:

before submitting a pr:
  * run `make test`
  * run `make format`

==============
 Contributing
==============

Welcome!

If you're reporting a bug you should read the Reporting bugs section
below to ensure that your bug report contains enough information
to successfully diagnose the issue, and if you're contributing code
you should try to mimic the conventions you see surrounding the code
you're working on, but in the end all patches will be cleaned up by
the person merging the changes so don't worry too much.

.. contents::
    :local:

.. _community-code-of-conduct:

When you're unsure, ask for help
--------------------------------

Nobody knows everything, and nobody is expected to be perfect. Asking
questions avoids many problems down the road, and so questions are
encouraged. Those who are asked questions should be responsive and helpful.
However, when asking a question, care must be taken to do so appropriately.

.. _reporting-bugs:

Reporting Bugs
==============

The best way to report an issue and to ensure a timely response is to use the
issue tracker.

1) **Create a GitHub account**.

You need to `create a GitHub account`_ to be able to create new issues
and participate in the discussion.

.. _`create a GitHub account`: https://github.com/signup/free

2) **Determine if your bug is really a bug**.

You shouldn't file a bug if you're requesting support. Label your issue as
a ``Question``.

3) **Make sure your bug hasn't already been reported**.

Search through the appropriate Issue tracker. If a bug like yours was found,
check if you have new information that could be reported to help
the developers fix the bug.

4) **Collect information about the bug**.

To have the best chance of having a bug fixed, we need to be able to easily
reproduce the condost of the titions that caused it. Mime this information
will be from a Python traceback message, though some bugs might be in design,
spelling or other errors on the website/docs/code. If the error is from a
Python traceback, include it in the bug report.

5) **Submit the bug**.

By default `GitHub`_ will email you to let you know when new comments have
been made on your bug. In the event you've turned this feature off, you
should check back on occasion to ensure you don't miss any questions a
developer trying to fix the bug might ask.

.. _`GitHub`: https://github.com

.. _contributing-changes:

Working on Features & Patches
=============================

.. note::

    Contributing to thumbs up should be as simple as possible,
    so none of these steps should be considered mandatory.

    However following these steps may make maintainers life easier,
    and may mean that your changes will be accepted sooner.

Forking and setting up the repository
-------------------------------------

First you need to fork the thumbs-up-api repository, a good introduction to this
is in the GitHub Guide: `Fork a Repo`_.

After you have cloned the repository you should checkout your copy
to a directory on your machine:

::

    $ git clone git@github.com:username/thumbs-up-api.git

When the repository is cloned enter the directory to set up easy access
to upstream changes:

::

    $ cd thumbs-up-api
    $ git remote add upstream git://github.com/best-bet/thumbs-up-api.git
    $ git fetch upstream

If you need to pull in new changes from upstream you should
always use the ``--rebase`` option to ``git pull``:

::

    git pull --rebase upstream master

With this option you don't clutter the history with merging
commit notes. See `Rebasing merge commits in git`_.
If you want to learn more about rebasing see the `Rebase`_
section in the GitHub guides.

If you need to work on a different branch than the one git calls ``master``,
you can fetch and checkout a remote branch like this::

    git checkout --track -b 3.0-devel origin/3.0-devel

.. _`Fork a Repo`: http://help.github.com/fork-a-repo/
.. _`Rebasing merge commits in git`:
    http://notes.envato.com/developers/rebasing-merge-commits-in-git/
.. _`Rebase`: http://help.github.com/rebase/

.. _contributing-testing:

Running the unit test suite
---------------------------

To run the thumbs-up test suite you need to install a few dependencies.
A complete list of the dependencies needed are located in
``requirements.txt``.

::

    $ make init

After installing the dependencies required, you can now execute
the test suite by calling ``py.test <pytest``:

::

    $ py.test

Some useful options to ``py.test`` are:

* ``-x``

    Stop running the tests at the first test that fails.

* ``-s``

    Don't capture output

* ``-v``

    Run with verbose output.

If you want to run the tests for a single test file only
you can do so like this:

::

    $ py.test tests/unit/some_test_file.py

.. _contributing-pull-requests:

Creating pull requests
----------------------

When your feature/bugfix is complete you may want to submit
a pull request so that it can be reviewed by the maintainers.

Creating pull requests is easy, and also let you track the progress
of your contribution. Read the `Pull Requests`_ section in the GitHub
Guide to learn how this is done.

.. _`Pull Requests`: http://help.github.com/send-pull-requests/

.. _contributing-coverage:

Calculating test coverage
~~~~~~~~~~~~~~~~~~~~~~~~~

To calculate test coverage you must first install the ``pytest-cov`` module.

Installing the ``pytest-cov`` module:

::

    $ pip install -U pytest-cov

Code coverage in HTML format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Run ``py.test`` with the ``--cov-report=html`` argument enabled:

    ::

        $ py.test --cov=thumbs-up-api --cov-report=html

#. The coverage output will then be located in the ``htmlcov/`` directory:

    ::

        $ open htmlcov/index.html

Code coverage in XML (Cobertura-style)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Run ``py.test`` with the ``--cov-report=xml`` argument enabled:

::

    $ py.test --cov=thumbs-up-api --cov-report=xml

#. The coverage XML output will then be located in the ``coverage.xml`` file.

.. _contributing-verify:

Verifying your contribution
---------------------------

To use these tools you need to install a few dependencies. These dependencies
can be found in ``requirements/pkgutils.txt``.

Installing the dependencies:

::

    $ pip install -U -r requirements/pkgutils.txt

pyflakes & PEP-8
~~~~~~~~~~~~~~~~

To ensure that your changes conform to ``8`` and to run pyflakes
execute:

::

    $ make flakecheck

To not return a negative exit code when this command fails use
the ``flakes`` target instead:

::

    $ make flakes§

.. _coding-style:

Coding Style
============

You should probably be able to pick up the coding style
from surrounding code, but it is a good idea to be aware of the
following conventions.

* All Python code must follow the ``8`` guidelines.

``pep8`` is a utility you can use to verify that your code
is following the conventions.

* Docstrings must follow the ``257`` conventions, and use the following
  style.

    Do this:

    ::

        def method(self, arg):
            """Short description.

            More details.

            """

    or:

    ::

        def method(self, arg):
            """Short description."""


    but not this:

    ::

        def method(self, arg):
            """
            Short description.
            """

* Lines shouldn't exceed 120 columns.

  You can enforce this in ``vim`` by setting the ``textwidth`` option:

  ::

        set textwidth=120

* Import order

    * Python standard library (`import xxx`)
    * Python standard library ('from xxx import`)
    * Third-party packages.
    * Other modules from the current package.

    Within these sections the imports should be sorted by module name.

    Example:

    ::

        import threading
        import time

        from collections import deque
        from Queue import Empty, Queue

        from .platforms import Pidfile
        from .five import items, range, zip_longest
        from .utils.time import maybe_timedelta

* Wild-card imports must not be used (`from xxx import *`).

.. _contact_information:

Contacts
========

This is a list of people that can be contacted for questions
regarding the official git repositories, PyPI packages
Read the Docs pages.

If the issue isn't an emergency then it's better
to `report an issue`_.


Committers
----------

You!
~~~~

:github: https://github.com/you
:website: http://you.com

Maintainers
-----------

thumbs up is run and maintained by

Kyle Uehlein
~~~~~~~~~~~

:github: https://github.com/kuehlein
:twitter: http://kyleuehlein.com

.. _release-procedure:


Release Procedure
=================

Updating the version number
---------------------------

The version number must be updated two places:

    * ``thumbs-up-api/__init__.py``
    * ``docs/include/introduction.txt``

After you have changed these files you must render
the ``README`` files. There's a script to convert sphinx syntax
to generic reStructured Text syntax, and the make target `readme`
does this for you:

::

    $ make readme

Now commit the changes:

::

    $ git commit -a -m "Bumps version to X.Y.Z"

and make a new version tag:

::

    $ git tag vX.Y.Z
    $ git push --tags

Releasing
---------

Commands to make a new public stable release:

::

    $ make distcheck  # checks pep8, autodoc index, runs tests and more
    $ make dist  # NOTE: Runs git clean -xdf and removes files not in the repo.
    $ python setup.py sdist upload --sign --identity='Celery Security Team'
    $ python setup.py bdist_wheel upload --sign --identity='Celery Security Team'
