from setuptools import setup

setup(
    name='consulta_investimentos',
    version='0.0.1',
    packages=['consulta_investimentos'],
    entry_points={
        'console_scripts':['consulta_investimentos = consulta_investimentos.cli:cli']
    }

)