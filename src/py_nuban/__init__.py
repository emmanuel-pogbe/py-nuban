"""
py-nuban: Nigerian bank account number validator and bank detector.
"""

from importlib.metadata import PackageNotFoundError, version

from .main import get_possible_banks, get_set_of_possible_codes

try:
	# Prefer setuptools_scm-generated module during editable/source usage.
	from ._version import version as __version__
except Exception:
	# Fallback for installed distributions where package metadata is available.
	try:
		__version__ = version("py-nuban")
	except PackageNotFoundError:
		__version__ = "0.0.0"

__all__ = ["get_possible_banks", "get_set_of_possible_codes", "__version__"]