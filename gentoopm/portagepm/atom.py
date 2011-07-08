#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

import portage.exception as pe
from portage.dbapi.dep_expand import dep_expand
from portage.dep import Atom, match_from_list
from portage.versions import catsplit

from gentoopm.basepm.atom import PMAtom

class PortageAtom(object):
	def __new__(self, s, pm):
		try:
			a = dep_expand(s, settings = pm._portdb.settings)
		except pe.InvalidAtom:
			raise ValueError('Incorrect atom: %s' % s)

		if catsplit(a.cp)[0] == 'null':
			return UnexpandedPortageAtom(a)
		else:
			return CompletePortageAtom(a)

class CompletePortageAtom(PMAtom):
	def __init__(self, a):
		self._atom = a

	def __contains__(self, pkg):
		# SLOT matching requires metadata so delay it.
		if not match_from_list(self._atom, [pkg.id]):
			return False
		return not self._atom.slot \
				or self._atom.slot == pkg.metadata.SLOT

class UncategorisedPackageWrapper(object):
	def __init__(self, pkg):
		self._pkg = pkg

	@property
	def id(self):
		cpv = self._pkg.id
		return 'null/%s' % catsplit(cpv)[1]
				
class UnexpandedPortageAtom(CompletePortageAtom):
	"""
	An atom without a category specified.
	"""

	def __contains__(self, pkg):
		return CompletePortageAtom.__contains__(self,
				UncategorisedPackageWrapper(pkg))