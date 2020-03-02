import os
from parameterized import parameterized
from pyfakefs.fake_filesystem_unittest import TestCase

from zygoat.components import FileComponent
from zygoat.components import resources


ZG_PATH = os.path.join(os.getcwd(), '../..')
print(ZG_PATH)
FILENAME = '.editorconfig'
PKG = resources


def create_fc(base):
    component = FileTestComponent()
    component.filename = FILENAME
    component.resource_pkg = PKG
    component.base_path = base
    return component


class TestFileComponent(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @parameterized.expand([
        ('./',),
        ('frontend/',),
    ])
    def test_creation(self, base):
        comp = create_fc(base)
        os.listdir(os.path.join(ZG_PATH, base))
        comp.create()
        path = os.path.join(ZG_PATH, base, FILENAME)
        print(path)
        os.listdir(os.path.join(ZG_PATH, base))
        self.assertTrue(os.path.exists(path))
        self.assertFalse(os.stat(path).st_size == 0)
