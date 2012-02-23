Introduction
============

collective.elections aims to be an electronic voting system based on `KOA
<http://secure.ucd.ie/products/opensource/KOA/>`_ (*Kiezen op Afstand*), an
Open Source Electronic/Remote/Internet Voting System developed for the Dutch
government in 2003. *Kiezen op Afstand* is literally translated from Dutch as
"Remote Voting." A version of the KOA system was used in the European
Parliamentary election of June 2004 and was subsequently released under the
`GNU General Public License <http://www.gnu.org/copyleft/gpl.html>`_.

The first version of this system, ATVotaciones, was developed in 2007 by
Alexander Zapata under supervision of Sergio Rajsbaum, a member of the
`Institute of Mathematics <https://info.matem.unam.mx/>`_ at `National
Autonomous University of Mexico <http://unam.mx>`_, and was later updated by
Iván Cervantes to be Plone 3 compatible.

collective.elections is a new implementation of the system for Plone 4.1 and
above using `Dexterity <http://pypi.python.org/pypi/plone.app.dexterity>`_ and
a custom workflow.

Security requirements
---------------------

KOA protocol fulfills the following requirements:

 - Only authorized voters are able to vote
 - No voter's vote can be counted more than once
 - Votes are securely stored
 - Votes can not be modified/removed without detection
 - It is possible to verify that all the votes were counted
 - Votes are not lost
 - It allows a greater level of confidence among voters
 - It is easy to use

collective.elections uses `GnuPG <http://www.gnupg.org/>`_ for all
cryptographic functions. GnuPG is a complete and free implementation of the
OpenPGP standard as defined by `RFC4880
<http://tools.ietf.org/html/rfc4880>`_. GnuPG allows to encrypt and sign data,
features a versatile key management system as well as access modules for all
kinds of public key directories.

Overview of the original system
===============================

The original system was developed using Archetypes and did not used Plone's
workflow machinery at all. The system was heavily attached to
`FacultyStaffDirectory
<http://pypi.python.org/pypi/Products.FacultyStaffDirectory>`_, a personnel
directory, and to ATSelectUsers, a product developed by the Institute of
Mathematics in order to create subsets of persons inside a staff directory.

User roles
----------

The original system defined three user roles:

 - **Election Administrator** (EA)
      A member of the portal Administrators group that creates the election
      and the rolls of nominees and voters.
 - **Election Officials** (EO)
      These are the members of the portal that will guarantee the election
      call is fulfilled; they will also sign documents produced through the
      election process.
 - **General Users** (GU)
      Nominees, candidates and voters.

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

(To be continued…)

Overview of the current effort
==============================

collective.elections will use Dexterity-based content types to describe an
election. The election object will move across an election workflow in which
different actions will be available to different users with different roles.
We want to keep this as simple as we can, so we will try not to implement more
roles or permissions unless necessary.

User roles
----------

We will maintain the three roles mentioned before:

 - EA (probably mapped as Manager or Site Administrator)
 - EO (probably mapped as Editor)
 - GU (probably mapped as Contributor)

Workflow states
---------------

We visualize a workflow with, more or less, the following states:

 #. **Private**
      Initial state of the election; the EA fills all the parameters.
 #. **Public**
      The CEO will add more information about EO and sign the file with the
      parameters of the election.
 #. **Draft**
      The EA will then proceed to create the rolls of nominees and voters.
 #. **Pending**
      Any EO can sign the rolls.
 #. **Nominating**
      Draft lists will be visible to everyone; in case of any issue with
      nominees or voters we must return to the Draft state. Nominees can
      accept or withdraw nominations; in case of acceptance, they will become
      candidates.
 #. **Voting**
      Election is open to voters as soon as the start date arrives; we leave
      this state automatically when end date arrives.
 #. **Counting**
      The votes are being counted.
 #. **Validating**
      The results of the election are being validated.
 #. **Published**
      Results of the election are available to everybody as soon as the
      publishing date arrives.
 #. **Closed**
      No one can make further changes to the election object.
