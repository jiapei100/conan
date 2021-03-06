# coding=utf-8

import textwrap
import unittest

from conans.model.ref import ConanFileReference
from conans.paths import CONAN_PACKAGE_LAYOUT_FILE
from conans.test.utils.tools import TestClient


class RemoveEditablePackageTest(unittest.TestCase):
    conanfile = textwrap.dedent("""\
        from conans import ConanFile

        class APck(ConanFile):
            pass
        """)

    def setUp(self):
        self.reference = ConanFileReference.loads('lib/version@user/name')

        self.t = TestClient()
        self.t.save(files={'conanfile.py': self.conanfile,
                           CONAN_PACKAGE_LAYOUT_FILE: "", })
        self.t.run('link . {}'.format(self.reference))
        self.assertTrue(self.t.client_cache.installed_as_editable(self.reference))

    def test_unlink(self):
        self.t.run('link {} --remove'.format(self.reference))
        self.assertIn("Removed linkage for reference '{}'".format(self.reference), self.t.out)
        self.assertFalse(self.t.client_cache.installed_as_editable(self.reference))

    def test_unlink_not_linked(self):
        reference = 'otherlib/version@user/name'
        self.t.run('search {}'.format(reference), assert_error=True)
        self.t.run('link {} --remove'.format(reference))
        self.assertIn("Reference '{}' was not installed as editable".format(reference), self.t.out)
