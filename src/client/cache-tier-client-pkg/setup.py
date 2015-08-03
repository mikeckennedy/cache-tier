from setuptools import setup

setup(
    name='cache_tier',
    packages=['cache_tier'],
    version='1.0.2',
    description='Imagine you have a set of static files you want to serve to '
                'the world. Cache-tier allows you to quickly spin up a Linux '
                'web server in a location with cheap, plentiful bandwidth and '
                'serve those files to your users.',
    author='Michael Kennedy - @mkennedy',
    author_email='mikeckennedy+pypi@gmail.com',
    url='https://github.com/mikeckennedy/cache-tier',
    download_url='https://github.com/mikeckennedy/cache-tier/tarball/1.0.2',
    license='MIT License',
    keywords=['caching', 'cache-tier', 'cache', 'tier'],
    classifiers=[],
    install_requires=['requests']
)
