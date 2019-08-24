#coding: utf-8
from setuptools import setup, find_packages

packages = find_packages('blog')
print(packages)

setup(
    name='jummy-blog',
    version='0.0.1',
    decription='Blog',
    author='jummy',
    author_email='a929440925@game.com',
    url='https://www.jummy.top',
    packages=packages,
    package_dir={'': 'blog'},
    include_package_data=True,
    install_requires=[
        'Django==2.1.5',
        'django-cors-headers==2.4.0',
        'django-redis==4.10.0',
        'django-simditor==0.0.15',
        'djangorestframework==3.9.1',
        'djangorestframework-jwt==1.11.0',
        'djangorestframework-stubs==0.4.2',
        'hiredis==0.3.1',
        'idna==2.8',
        'Markdown==3.0.1',
        'mysqlclient==1.4.2.post1',
        'Pillow==5.4.1',
        'PyJWT==1.7.1',
        'redis==3.0.1',
        'python-decouple==3.1',
        'redis==3.0.1',
        'requests==2.21.0',
        'urllib3==1.24.1',
    ],
    script=[
        'blog/manage.py',
    ],
)
