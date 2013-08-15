===============
USER MANUAL
===============



Creating an Election
====================

Once you have the collective.elections product installed on your Plone instance you can add an election from the main Add new.. in the main page.

Then you have to fill the election fields.

	- Title: A suitable title for the election.
	- Description: A suitable description for the election.
	- Text: This text space is available to write down all the information about the election.
	- Chief Electoral officer: You must choice the user that will have the roll as Chief Electoral Officer in the election. 
	- Dates: This dates will prevent to change the election state until the choiced date has been reached.
		- Nomine selection date
		- Start of voting
		- End of voting
		- Publication of results
	- Results mode: So far the onli choice is Votes
	- GPG Public keys: The election will have 2 users with special roles in the election and Aministrator and an Officer this to users must create a GPG key (How to create GPG Key) and give their public keys to be used in the election. 
		- GPG public key of the election Admintrator: Public key of the Administrator user
		- GPG public key of the watch comission: Public key of the officer user
	- GPG mode: So far the use of GPG is mandatory

After fill the fields you can save the election and it will be created. 

Before continuing with the Election process the Plone Site Administrator should verify that the users choiced to be Administrator and Officer of the election have the required Permisions.
Site Setup -> Users and Groups 
On Users and Groups there will be Permissions created for the Election process (Election Administrator, Election Officials)in our example with choose sergio as officer and hugo as admistrator


Private State
-----------------
Administrator User
~~~~~~~~~~~~~~~~~~~
In Private state any field can be modified by the Election Administrator, once that everything is allright the Election Administrator changes the State to Sumit to internal.

Officer User
~~~~~~~~~~~~
In Private State officer cant see the election.

Normal User
~~~~~~~~~~~~
In Private State Normal user cant see the election.

Internal Revision State
---------------------------------------------
Administrator User
~~~~~~~~~~~~~~~~~~~
Adminstraror user can retract the election.

Officer User
~~~~~~~~~~~~
Officer user has to download the Configuration PDF and review that everything is ok, if something is wrong he can retract the election otherwise everything is ok and he must sign the file with his GPG Key (How to sign a file), then he must upload both files, when the files are uploaded correctly the officer can change the election state to Public.

Normal User
~~~~~~~~~~~~
In Internal Revision Normal user cant see the election.



Public Revision State
---------------------------------------------
When the Nominee selection date is reached the election state is changed to Nominee Selection

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator user can review the election configuration, if something wrong he can can recatract the election.

Officer User
~~~~~~~~~~~~
Officer user can review the election configuration, if something wrong he can can recatract the election.

Normal User
~~~~~~~~~~~~
Normal user can review the election configuration, if something wrong he can notify an officer or administrator so they can retract the election.


Nominee Selection State
---------------------------------------------
From this state the election cant be retracted.

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator must select the list of Electors and the list of Nominees from the list of users registered in the plone site (This will change in the future to a more general approach), after the administrator has selected the electors and nominees he must change the election state to Review Nominees  

Officer User
~~~~~~~~~~~~
Officer user can review the actual state of the election.

Normal User
~~~~~~~~~~~~
Normal user can review the actual state of the election.


Nominee Revision State
---------------------------------------------

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator can retract the state fo the election to select nominees.

Officer User
~~~~~~~~~~~~
Officer have to download the PDF with the election Rolls if something is wrong he can retract the election to select nominees otherwise the Election Rolls are ok and have to sign the PDF file with his GPG Key (How to sign a file), then he must upload both files, when the files are uploaded correctly the officer can change the election state to Public.

Normal User
~~~~~~~~~~~~
Normal user can review the actual state of the election.


Public State
---------------------------------------------
When the Start of voting date is reached the election state is changed to Voting.

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator user can review the Electoral Rolls, if something wrong he can can retract the election to Select Nominees.

Officer User
~~~~~~~~~~~~
Officer user can review the Electoral Rolls, if something wrong he can can retract the election to Select Nominees.

Normal User
~~~~~~~~~~~~
Normal user can review the Electoral Rolls, if something wrong he can notify an officer or administrator so they can retract the election to Select Nominees.



Voting State
---------------------------------------------
From this state the election cant be retracted. When the End of voting date is reached the election state is changed to Scrutiny.

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator user can cast a vote if hes in the electoral roll list only once. Otherwise he can review the actual state of the election.

Officer User
~~~~~~~~~~~~
Officer user can cast a vote if hes in the electoral roll list only once. Otherwise he can review the actual state of the election.

Normal User
~~~~~~~~~~~~
Normal user can cast a vote if hes in the electoral roll list only once. Otherwise he can review the actual state of the election.


Scrutiny State
---------------------------------------------
When the Publication of results date is reached the election state is changed to Results. When the unencrypted file is uploaded by the officer the votes are counted by the system.

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator have to download the encrypted urn, then he has to decrypt the downloaded urn with his GPG Key (How to decrypt a file) this process returns a zip file with the votes inside, then the administrator has to decrypt the votes with his GPG Key(How to decrypt zip file votes) this process returns a second zip file with votes inside, the administrator have to give this file to the Officer of the election.

Officer User
~~~~~~~~~~~~
Once the officer has recived the zip file with vote inside he has to decrypt the votes with his GPG Key(How to decrypt zip file votes)  this process returns a third  zip file with the votes inside this votes are already decrypted, the officer must sign the file with his GPG Key (How to sign a file), then he must upload both files.

Normal User
~~~~~~~~~~~~
Normal user can review the actual state of the election.



Results State
---------------------------------------------

Administrator User
~~~~~~~~~~~~~~~~~~~
Administrator user can review the resuls of the election and all the info about it.

Officer User
~~~~~~~~~~~~
Officer user can review the resuls of the election and all the info about it. The officer can close the election.

Normal User
~~~~~~~~~~~~
Normal user can review the resuls of the election and all the info about it.



Closed State
---------------------------------------------
All thee users can review the final state of the election.



GnuPG 
====================
collective.elections uses `GnuPG <http://www.gnupg.org/>`_ for all cryptographic functions. GnuPG is a complete and free implementation of the OpenPGP standard as defined by `RFC4880 <http://tools.ietf.org/html/rfc4880>`_. 

The user must have installed GnuPG package in order to use all the cryptographic functions used for this package. 



How to create GPG Key
----------------------

Once you have the GnuPG package installed on your system you can run the following command to create a GPG key.

gpg --gen-key

This command will give you a series of options:

	*You have to choose what kind of key you want to create you must choose DSA and Elgamal option.
	*You have to choose the keysize of 2048 bits long.
	*You have to choose for how long the Key will be valid, this key should be valid at least for duration of the election.
	*You have to introduce your Name, Email Addres and a comment, the software constructs and user ID with this info.
	*You have to introduce a password for your key.

After this options the gpg command will create your GPG key. You can only use it in the PC where you created it.

To export your public key to a file you can run the following command.

gpg --export -a "NAME" > FILE

NAME is the Name you introduced in the moment of creating your GPG key.
FILE is the name of the file were you want to save the public key.


Using the Pyton script for cryptographic funtions
=====================================================
For the easy use of the package we have included a python script (CrypTools)to be used in the cryptographic functions. The script was tested using python 2.7 and the GnuPG package installed.


How to sign a file
--------------------
Run CryoTools.py choice option 1

How to decrypt a file
------------------------------
Run CryoTools.py choice option 3

How to decrypt zip file votes
--------------------------------------
Run CryoTools.py choice option 4
