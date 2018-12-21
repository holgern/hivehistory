from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
import mock
import click
from click.testing import CliRunner
from pprint import pprint
from steemhistory.cli import cli


class Testcases(unittest.TestCase):
    def test_posts(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['posts', 'beembot', './'])
        self.assertEqual(result.exit_code, 0)
