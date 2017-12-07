import os
import unittest
import builtins
import subprocess
from classes.provider.dependency_provider import DependencyProvider

class DependencyProviderTest(unittest.TestCase):

    def setUp (self):
        self._provider = DependencyProvider()

    def get_instance_test (self):
        # test normal behavior - test
        dao = self._provider.get_instance('EventDao')
        self.assertEqual(
            dao.__module__ + '.' + dao.__class__.__name__,
            'test.classes.EventDao.EventDao'
        )

        _filter = self._provider.get_instance('UserFilter')
        self.assertEqual(
            _filter.__module__ + '.' + _filter.__class__.__name__,
            'test.classes.UserFilter.UserFilter'
        )
