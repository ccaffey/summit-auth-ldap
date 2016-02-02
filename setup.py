#!/usr/bin/env python

import summit_auth_ldap

long_description = open('README').read()

setup_args = dict(
    name='summit-auth-ldap',
    version=summit_auth_ldap.__version__,
    description='Extensions for django-auth-ldap to handle our snowflake of an LDAP',
    long_description=long_description,
    author='Jeremy Satterfield',
    author_email='jsatterfield@summitesp.com',
    license='MIT License',
    packages=['summit_auth_ldap'],
    install_requires=[
        'django-auth-ldap>=1.2.7',
    ],
    classifers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
    ],
)

if __name__ == '__main__':
    from distutils.core import setup

    setup(**setup_args)
