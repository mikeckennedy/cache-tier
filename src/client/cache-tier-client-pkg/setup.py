# from distutils.core import setup
#
# setup(
#     name='cache_tier_client',
#     version='1.0.0',
#     packages=['cache_tier_client'],
#     url='https://github.com/mikeckennedy/cache-tier',
#     license='MIT License',
#     author='Michael Kennedy - @mkennedy',
#     author_email='mikeckennedy+pypi@gmail.com',
#     description=''
# )

from setuptools import setup

setup(
    name='cache-tier-client',
    version='1.0.0',
    packages=['cache_tier_client'],
    url='https://github.com/mikeckennedy/cache-tier',
    license='MIT License',
    author='Michael Kennedy - @mkennedy',
    author_email='mikeckennedy+pypi@gmail.com',
    description='',

    install_requires=['requests'],
)
