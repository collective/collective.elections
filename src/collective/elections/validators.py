# -*- coding: utf-8 -*-
import tempfile
import gnupg
import os
gpg = gnupg.GPG()

from gnupg import _make_binary_stream

from zope.interface import Invalid
from z3c.form import validator

from collective.elections import _


class GPGKeyValidator(validator.SimpleFieldValidator):
    """Ensure GPG key is valid.
    """

    def validate(self, value):
        super(GPGKeyValidator, self).validate(value)

        if value:
            import_result = gpg.import_keys(value)
            if import_result.count == 0:
                raise Invalid(_(u"The GPG key is not valid"))


class GPGSignatureValidator(validator.SimpleFieldValidator):
    """Ensure GPG signature is valid. This validator works with the fields name
    So, for this to work, make sure you name your fields correctly.

    The idea is you should put 2 fields in your schema, one for the file, and
    the other one for the signature.

    The signature field name should be the same as the file one, but should
    end with "_signature".
    So, if the field where you upload a file is called "my_file", then the
    field where you upload the signature for that file should be called
    "my_file_signature", and this field should contain this validator.
    """

    def validate(self, value):
        super(GPGSignatureValidator, self).validate(value)

        data = ''
        ending = "_signature"
        _len = len(ending)

        signature = self.field.getName()
        signed_file = signature[:-_len]

        file = self.request.form.get('form.widgets.%s' % signed_file)
        if file:
            file.seek(0)
            data = file.read()
            file.seek(0)
        else:
            pdf_field = getattr(self.context, signed_file, None)
            if pdf_field:
                data = pdf_field.data

        # It would be nice to be able to do this from a stream,
        # but unfortunately, gnupg expects files
        fd, fn = tempfile.mkstemp(prefix='elections')
        os.write(fd, data)
        os.close(fd)

        sig = _make_binary_stream(value.data, gpg.encoding)

        verify = gpg.verify_file(sig, fn)

        if not verify.valid:
            if hasattr(verify, 'status'):
                # Error codes gnupg.py line 150
                if verify.status == 'signature bad':
                    raise Invalid(_(u"This signature is not valid for the uploaded file."))
                else:
                    raise Invalid(_(u"Error: %s." % verify.status))

            else:
                raise Invalid(_(u"Invalid signature."))


class IsPDFFile(validator.SimpleFieldValidator):
    """
    Ensure uploaded file is a PDF file
    """

    def validate(self, value):
        super(IsPDFFile, self).validate(value)

        # TODO: Actually implement the validator


class IsZIPFile(validator.SimpleFieldValidator):
    """
    Ensure uploaded file is a ZIP file
    """

    def validate(self, value):
        super(IsZIPFile, self).validate(value)

        # TODO: Actually implement the validator
