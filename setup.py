from setuptools import find_packages, setup

setup(
    name='my_retail',
    version='0.5.0',
    description='Retailing for the common man',
    long_description='Retailing for the comman man and woman',
    author='Jacob Gregor',
    author_email='gregorj9974@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'my_retail=my_retail.main:main',
        ],
    },
    install_requires=['flask', 'mock', 'urlib', 'redis']
)