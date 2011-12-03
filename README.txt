Introduction
============

matem.elections aims to be an electronic voting system based on `KOA
<http://secure.ucd.ie/products/opensource/KOA/>`_ (*Kiezen op Afstand*), an
Open Source Electronic/Remote/Internet Voting System developed for the Dutch
government in 2003. *Kiezen op Afstand* is literally translated from Dutch as
"Remote Voting." A version of the KOA system was used in the European
Parliamentary election of June 2004 and was subsequently released under the
`GNU General Public License <http://www.gnu.org/copyleft/gpl.html>`_.

The first version of this system was developed by Alexander Zapata under
supervision of Sergio Rajsbaum, a member of the `Institute of Mathematics
<https://info.matem.unam.mx/>`_ at `National Autonomous University of Mexico
<http://unam.mx>`_.

matem.elections is a new implementation of the system for Plone 4.1 and above
using `Dexterity <http://pypi.python.org/pypi/plone.app.dexterity>`_.

Security requirements
---------------------

KOA protocol fulfills the following requirements:

 - Only authorized voter are able to vote
 - No voter can vote more than once
 - Votes are securely stored
 - Votes can not be modified/removed without detection
 - It is possible to verify that the votes were counted in the final election
 - Votes are not lost
 - It allows a greater level of confidence among voters
 - It is easy to use

matem.elections uses `GnuPG <http://www.gnupg.org/>`_ for all cryptographic
functions. GnuPG is a complete and free implementation of the OpenPGP standard
as defined by RFC4880. GnuPG allows to encrypt and sign data, features a
versatile key management system as well as access modules for all kinds of
public key directories.
