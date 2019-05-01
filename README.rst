========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/2019sp-ap_project-jackeiel/badge/?style=flat
    :target: https://readthedocs.org/projects/2019sp-ap_project-jackeiel
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/jackeiel/2019sp-ap_project-jackeiel.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jackeiel/2019sp-ap_project-jackeiel

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/jackeiel/2019sp-ap_project-jackeiel?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/jackeiel/2019sp-ap_project-jackeiel

.. |version| image:: https://img.shields.io/pypi/v/ap-project.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/ap-project

.. |commits-since| image:: https://img.shields.io/github/commits-since/jackeiel/2019sp-ap_project-jackeiel/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jackeiel/2019sp-ap_project-jackeiel/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/ap-project.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/ap-project

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ap-project.svg
    :alt: Supported versions
    :target: https://pypi.org/project/ap-project

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ap-project.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/ap-project


.. end-badges

Final Project for CSCI-E29

* Free software: BSD 2-Clause License

Installation
============

::

    pip install ap-project

Documentation
=============


https://2019sp-ap_project-jackeiel.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
