# coding=utf-8

import textwrap
import unittest

from conans.model.ref import ConanFileReference
from conans.paths import CONAN_PACKAGE_LAYOUT_FILE
from conans.test.utils.tools import TestClient, TestServer


class ForbiddenCommandsTest(unittest.TestCase):
    conanfile = textwrap.dedent("""\
        from conans import ConanFile

        class APck(ConanFile):
            pass
        """)

    def setUp(self):
        self.reference = ConanFileReference.loads('lib/version@user/name')

        test_server = TestServer()
        self.servers = {"default": test_server}
        self.t = TestClient(servers=self.servers, users={"default": [("lasote", "mypass")]})
        self.t.save(files={'conanfile.py': self.conanfile,
                           CONAN_PACKAGE_LAYOUT_FILE: "", })
        self.t.run('link . {}'.format(self.reference))
        self.assertTrue(self.t.client_cache.installed_as_editable(self.reference))

    def test_export(self):
        self.t.run('export . {}'.format(self.reference), assert_error=True)
        self.assertIn("Operation not allowed on a package installed as editable", self.t.out)

    def test_create(self):
        self.t.run('create . {}'.format(self.reference), assert_error=True)
        self.assertIn("Operation not allowed on a package installed as editable", self.t.out)

    def test_create_update(self):
        self.t.run('create . {} --update'.format(self.reference), assert_error=True)
        self.assertIn("Operation not allowed on a package installed as editable", self.t.out)

    def test_upload(self):
        self.t.run('upload --force {}'.format(self.reference), assert_error=True)
        self.assertIn("Operation not allowed on a package installed as editable", self.t.out)

    def test_export_pkg(self):
        self.t.run('export-pkg -f . {}'.format(self.reference), assert_error=True)
        self.assertIn("Operation not allowed on a package installed as editable", self.t.out)

    def test_copy(self):
        self.t.run('copy --force {} ouser/ochannel'.format(self.reference), assert_error=True)
        self.assertIn("Operation not allowed on a package installed as editable", self.t.out)

    def test_remove(self):
        self.t.run('remove {} --force'.format(self.reference), assert_error=True)
        self.assertIn("Package 'lib/version@user/name' is installed as editable, unlink it first "
                      "using command 'conan link lib/version@user/name --remove'", self.t.out)
