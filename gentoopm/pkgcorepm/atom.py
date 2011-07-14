#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

from pkgcore.ebuild.atom import atom
from pkgcore.util.parserestrict import parse_match, ParseError

from gentoopm.basepm.atom import PMAtom
from gentoopm.exceptions import InvalidAtomStringError

class PkgCoreAtom(PMAtom):
	def __init__(self, s, pkg = None):
		if isinstance(s, atom):
			self._r = s
		else:
			try:
				self._r = parse_match(s)
			except ParseError:
				raise InvalidAtomStringError('Incorrect atom: %s' % s)

		self._pkg = pkg

	def __contains__(self, pkg):
		return self._r.match(pkg._pkg)

	def __str__(self):
		if self.complete:
			return str(self._r)
		else:
			raise ValueError('Unable to stringify incomplete atom')

	@property
	def complete(self):
		return isinstance(self._r, atom)

	@property
	def associated(self):
		return self._pkg is not None

	@property
	def slotted(self):
		assert(self.associated)
		return PkgCoreAtom(self._pkg._pkg.slotted_atom, self._pkg)

	@property
	def unversioned(self):
		assert(self.associated)
		return PkgCoreAtom(self._pkg._pkg.unversioned_atom, self._pkg)
