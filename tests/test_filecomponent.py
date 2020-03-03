import os
import shutil

from unittest import TestCase
from parameterized import parameterized

from zygoat.components import FileComponent
from zygoat.components import resources
from zygoat.cli import _new
from zygoat.utils.files import use_dir


PATH = '/tmp/test-zg/'


class TestFileComponent(TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir(PATH)
            os.mknod(os.path.join(PATH, '.git'))
            with use_dir(PATH):
                _new('test')
        except:
            # Make sure the directory gets removed if there's an error
            # on setup (tearDownClass won't get called automatically if
            # setUpClass fails).
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(PATH)

    def test_creation(self):
        print(os.listdir(PATH))
        raise AssertionError
