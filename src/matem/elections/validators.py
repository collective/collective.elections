# -*- coding: utf-8 -*-

import gnupg
gpg = gnupg.GPG()

from zope.interface import Invalid
from z3c.form import validator

from matem.elections import _


class GPGKeyValidator(validator.SimpleFieldValidator):
    """Ensure GPG key is valid.
    """

    def validate(self, value):
        super(GPGKeyValidator, self).validate(value)

        import_result = gpg.import_keys(value)
        if import_result.count == 0:
            raise Invalid(_(u"The GPG key is not valid"))


class GPGSignatureValidator(validator.SimpleFieldValidator):
    """Ensure GPG signature is valid.
    """

    def validate(self, value):
        super(GPGSignatureValidator, self).validate(value)

        # TODO: implement validator
