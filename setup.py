import setuptools

try:
    from pbr import util
except ImportError:
    setuptools.setup(
        setup_requires=['pbr'],
        pbr=True)
else:
    setuptools.setup(
        **util.cfg_to_args())
