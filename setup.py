from setuptools import setup


PLUGIN_ENTRY_POINT = 'ovos-coref-plugin-pronomial=pronomial.opm:PronomialCoreferenceSolver'

setup(
    name='pronomial',
    version='0.1.0',
    packages=['pronomial', 'pronomial.lang'],
    url='https://github.com/OpenJarbas/pronomial',
    license='apache-2.0',
    author='jarbasAi',
    install_requires=["nltk", "pytest", "quebra_frases"],
    include_package_data=True,
    author_email='jarbasai@mailfence.com',
    description='pronomial postag/word_gender based coreference solver',
    entry_points={'intentbox.coreference': PLUGIN_ENTRY_POINT}
)
