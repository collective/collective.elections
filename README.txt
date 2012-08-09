====================
collective.elections
====================

.. contents:: Table of Contents

Introduction
------------

.. image:: https://secure.travis-ci.org/collective/collective.elections.png
    :target: http://travis-ci.org/collective/collective.elections

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
^^^^^^^^^^^^^^^^^^^^^

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
-------------------------------

The original system was developed using Archetypes and did not used Plone's
workflow machinery at all. The system was heavily attached to
`FacultyStaffDirectory
<http://pypi.python.org/pypi/Products.FacultyStaffDirectory>`_, a personnel
directory, and to ATSelectUsers, a product developed by the Institute of
Mathematics in order to create subsets of persons inside a staff directory.

User roles
^^^^^^^^^^

The original system defined three user roles:

**Election Administrator** (EA)
  A member of the portal Administrators group that creates the election and
  the rolls of nominees and voters.

**Election Officials** (EO)
  These are the members of the portal that will guarantee the election call is
  fulfilled; they will also sign documents produced through the election
  process.

**General Users** (GU)
  Nominees, candidates and voters.

The election process in a nutshell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Users of the system can check their status as nominees and/or voters and they
can accept/reject/cancel their nomination to become candidates. Any claim must
be done to the EO.

Before the voting process starts, the system generates a set of random numbers
for each pair of voter/candidate (if we have 2 candidates and 10 voters the
system will generate 20 random numbers) to avoid duplicate votes. This set of
numbers is encrypted with the public key used by the EO, and is used to create
ballots for each voter:

.. csv-table::
   :header: Candidates, A, B
   :widths: 10, 10, 10

   "Voter 1", 9095, 7613
   "Voter 2", 9211, 8291
   "Voter 3", 522, 4640
   "Voter 4", 5988, 4415
   "Voter 5", 8489, 4730
   "Voter 6", 9416, 1940
   "Voter 7", 877, 8033
   "Voter 8", 3028, 487
   "Voter 9", 8875, 1164
   "Voter 10", 7854, 2642

Each ballot can only be accessed by the voter associated with it when she is
about to cast her vote.

After the voting has finished (the end date arrives), the vote counting
process starts. First, the EO has to decrypt the ballots, to check that no
vote has been modified, and then the counting is done automatically by the
system.

Now the results can be published. The EO creates and signs a PDF with the
results of the election and the information is made available to the public.

Overview of the current effort
------------------------------

collective.elections will use Dexterity-based content types to describe an
election. The election object will move across an election workflow in which
different actions will be available to different users with different roles.
We want to keep this as simple as we can, so we will try not to implement more
roles or permissions unless necessary.

User roles
^^^^^^^^^^

We will maintain the three roles mentioned before:

- EA (probably mapped as Manager or Site Administrator)
- EO (probably mapped as Editor)
- GU (probably mapped as Contributor)

Workflow states
^^^^^^^^^^^^^^^

We visualize a workflow with, more or less, the following states:

#. **Private**
    * Initial state of the election; the EA fills all the parameters and
      submit the election to be reviewed by the EO's (Trans. 1).

#. **Internal revision**
    * In this state the election configuration is reviewed by the CEO; if
      everything is correct, a PDF file with this information gets exported.
    * The CEO signs the file locally with his GPG private key and adds the
      signed PDF and signature to the election.
    * Only the PDF and signature fields are writable in this state.
    * The election can be sent back to the Private state (Trans. 2) or be
      submitted for public review (Trans. 3).
    * The CEO is the only role allowed to call Trans. 3.

#. **Public revision**
    * In this state, none of the fields of the election are writable by
      anybody.
    * It can be sent back to the Private state (Trans. 4) in case of some
      error.
    * Transition to the Nominees state is done automatically in a given date
      (Trans. 5).

#. **Nominees**
    * In this state, the electoral and nominations roll are filled by the EA.
    * Only these 2 fields are writable by anybody in this state.
    * This state cannot be sent back.
    * The EA can submit to the Nominee revision state (Trans. 6)

#. **Nominee revision**
    * In this state, the electoral and nominations roll are reviewed by the
      CEO; if everything is correct, then a second PDF file with the rolls
      gets exported.
    * The CEO signs it locally with his GPG private key and adds the signed
      PDF and signature to the election.
    * Only the PDF and signature fields are writable in this state. (2
      additional fields, separate from the 2 fields used in state Internal
      revision).
    * The election can be sent back to the Nominees state (Trans. 7) or be
      submitted for public review (Trans. 8).
    * The CEO is the only role allowed to call Trans. 8.

#. **Public**
    * In this state, none of the fields of the election are writable by
      anybody.
    * It can be sent back to the Nominees state (Trans. 9) in case of some
      error Transition to the Voting state is done automatically in a given
      date (Trans. 10).

#. **Voting**
    * Votes are allowed to be entered. No fields are writable by anybody.
    * This state cannot be sent back.
    * Voting will end in a previously given date automatically and the
      election be moved to the Vote Counting state (Trans. 11).

#. **Vote Counting**
    * Votes are counted.
    * In a previously given date, the election will automatically be moved to
      the Results state (Trans. 12).

#. **Results**
    * Results of the election are available to everybody.
    * In this state, the EO's can validate valid signatures and finally, the
      CEO can close the election (Trans. 13).

#. **Closed**
    * No one can make further changes to the election object.

Transitions
^^^^^^^^^^^

#. **Trans. 1**
    * Private -> Internal revision
    * Manually triggered transition. Only the EA is allowed to call it

#. **Trans. 2**
    * Internal revision -> Private
    * Manually triggered transition. EA and EO's are allowed to call it

#. **Trans. 3**
    * Internal revision -> Public revision
    * Manually triggered transition.
    * This transition cannot be triggered, unless the PDF and signature fields
      of the election are populated. Only the CEO is allowed to call it.

#. **Trans. 4**
    * Public revision -> Private
    * Manually triggered transition. EA and EO's are allowed to call it
    * When this transition is triggered, the PDF and signature fields are
      wiped out.

#. **Trans. 5**
    * Public revision -> Nominees
    * Automatically triggered transition when a specific date is reached

#. **Trans. 6**
    * Nominees -> Nominee revision
    * Manually triggered transition. Only the EA is allowed to call it

#. **Trans. 7**
    * Nominee revision -> Nominees
    * Manually triggered transition. EA and EO's are allowed to call it

#. **Trans. 8**
    * Nominee revision -> Public
    * Manually triggered transition.
    * This transition cannot be triggered, unless the second PDF and signature
      fields of the election are populated. Only the CEO is allowed to call
      it.

#. **Trans. 9**
    * Public -> Nominees
    * Manually triggered transition. EA and EO's are allowed to call it
    * When this transition is triggered, the second PDF and signature fields
      are wiped out.

#. **Trans. 10**
    * Public -> Voting
    * Automatically triggered transition when a specific date is reached.
    * In this transition, hashes with electors and voters are generated

#. **Trans. 11**
    * Voting -> Vote Counting
    * Automatically triggered transition when a specific date is reached.

#. **Trans. 12**
    * Vote Counting -> Results
    * Automatically triggered transition when a specific date is reached.

#. **Trans. 13**
    * Results -> Closed
    * Manually triggered transition. Only the CEO is allowed to call it

