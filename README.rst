Introduction
============

matem.elections aims to be an electronic voting system based on `KOA
<http://secure.ucd.ie/products/opensource/KOA/>`_ (*Kiezen op Afstand*), an
Open Source Electronic/Remote/Internet Voting System developed for the Dutch
government in 2003. *Kiezen op Afstand* is literally translated from Dutch as
"Remote Voting." A version of the KOA system was used in the European
Parliamentary election of June 2004 and was subsequently released under the
`GNU General Public License <http://www.gnu.org/copyleft/gpl.html>`_.

The first version of this system, `ATVotaciones
<http://proyectos.matem.unam.mx:8080/pm/p/infomatem/browser/Products.ATVotaciones>`_,
was developed in 2007 by Alexander Zapata under supervision of Sergio
Rajsbaum, a member of the `Institute of Mathematics
<https://info.matem.unam.mx/>`_ at `National Autonomous University of Mexico
<http://unam.mx>`_, and was later updated by Iván Cervantes to be Plone 3 compatible.

matem.elections is a new implementation of the system for Plone 4.1 and above
using `Dexterity <http://pypi.python.org/pypi/plone.app.dexterity>`_ and a
custom workflow.

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

Overview of the original system
===============================

The original system was developed using Archetypes and did not used Plone's
workflow machinery at all. The system was heavily attached to
`FacultyStaffDirectory
<http://pypi.python.org/pypi/Products.FacultyStaffDirectory>`_, a personnel
directory, and to `ATSelectUsers
<http://proyectos.matem.unam.mx:8080/pm/p/infomatem/browser/Products.ATSelectUsers>`_,
a product developed by the Institute of Mathematics in order to create subsets
of members of a Plone portal.

User types
----------

 - Election Administrator (EA): a member of the portal Administrators group
   that creates the election and the rolls of nominees and voters.
 - Election Officials (EO): members of the portal that will guarantee all the
   election call is fulfilled; they will also sign documents produced through
   the election process.
 - General Users (GU): nominees and voters.

The election process in a nutshell
----------------------------------

The EA adds a new election object and fills all the parameters in the general
configuration screen. These parameters include the title, description, the
username of the user that will act as the Chief Electoral Officer (CEO) and
the dates of the process (date to accept nomination, to start voting, to stop
voting, to publish results, and so on…). The EA will also include her GPG
public key that is going to be used later to sign and encrypt information as
the process moves on.

The CEO enters information for other fields like the usernames of the other
EO, and the PGP public key used by them. He will also generate a
human-readable PDF file with all the information relative to the general
configuration and will sign it with their own GPG private key. This
information will be available at any time of the process.

The EA creates the nominees roll and the voters roll using ATSelectUsers. This
product allows to create a subset of members of the portal that fulfill
certain requirements (like "being females over 40 years with at least 5 years
of experience").

Human readable PDF files with the list of nominees and voters are created and
these files are also signed by anyone of the EO. After this, nobody can change
these rolls without detection and everybody can check to see if all, nominees
and voters, really fulfill the requirements published in the call for the
election.
