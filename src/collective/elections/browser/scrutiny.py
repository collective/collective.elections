# -*- coding: utf-8 -*-

import os
import gnupg
gpg = gnupg.GPG()
from zipfile import ZipFile, ZIP_DEFLATED
from tempfile import mkdtemp
import shutil

from zope.annotation.interfaces import IAnnotations

from Products.Five.browser import BrowserView


class GenerateEncryptedURN(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        admin_key = gpg.import_keys(self.context.gpg_key_admin).results[0]
        admin_fingerprint = admin_key['fingerprint']

        annotation = IAnnotations(self.context)
        votes = annotation['votes']
        # Create temporary folder where we are going to store votes
        vote_dir = mkdtemp(prefix="collective.elections")
        for index, vote in enumerate(votes):
            filename = os.path.join(vote_dir, "vote-%s" % index)
            vote_file = open(filename, "w")
            vote_file.write(vote)
            vote_file.close()

        zip_filename = os.path.join(vote_dir, "votes.zip")
        zip_file = ZipFile(zip_filename, "w", ZIP_DEFLATED)
        # Now, create a zip file in the same folder, containing the votes
        for root, dirs, files in os.walk(vote_dir):
            for file in files:
                filename = os.path.join(root, file)
                if filename != zip_filename:
                    zip_file.write(filename, file)

        zip_file.close()

        # Open the zip again, in read mode, and encrypt it
        zip_file = open(zip_filename, "r")
        result = gpg.encrypt(zip_file.read(), admin_fingerprint)
        zip_file.close()

        # Finally, remove the whole dir
        shutil.rmtree(vote_dir)

        # And return the encrypted file
        self.request.response.setHeader('Content-Type', 'application/octet-stream;charset="utf-8"')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename=votes')
        return result.data
