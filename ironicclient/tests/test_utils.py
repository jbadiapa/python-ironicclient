# Copyright 2013 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import six

from ironicclient.common import utils
from ironicclient import exc
from ironicclient.tests import utils as test_utils


class UtilsTest(test_utils.BaseTestCase):

    def test_prettytable(self):
        output_dict = six.StringIO()
        utils.print_dict({'K': 'k', 'Key': 'Value'}, outfile=output_dict)
        self.assertEqual('''\
+----------+-------+
| Property | Value |
+----------+-------+
| K        | k     |
| Key      | Value |
+----------+-------+
''', output_dict.getvalue())

    def test_args_array_to_dict(self):
        my_args = {
            'matching_metadata': ['metadata.key=metadata_value'],
            'other': 'value'
        }
        cleaned_dict = utils.args_array_to_dict(my_args,
                                                "matching_metadata")
        self.assertEqual({
            'matching_metadata': {'metadata.key': 'metadata_value'},
            'other': 'value'
        }, cleaned_dict)

    def test_args_array_to_patch(self):
        my_args = {
            'attributes': ['foo=bar', '/extra/bar=baz'],
            'op': 'add',
        }
        patch = utils.args_array_to_patch(my_args['op'],
                                          my_args['attributes'])
        self.assertEqual([{'op': 'add',
                           'value': 'bar',
                           'path': '/foo'},
                          {'op': 'add',
                           'value': 'baz',
                           'path': '/extra/bar'}], patch)

    def test_args_array_to_patch_format_error(self):
        my_args = {
            'attributes': ['foobar'],
            'op': 'add',
        }
        self.assertRaises(exc.CommandError, utils.args_array_to_patch,
                          my_args['op'], my_args['attributes'])

    def test_args_array_to_patch_remove(self):
        my_args = {
            'attributes': ['/foo', 'extra/bar'],
            'op': 'remove',
        }
        patch = utils.args_array_to_patch(my_args['op'],
                                          my_args['attributes'])
        self.assertEqual([{'op': 'remove', 'path': '/foo'},
                          {'op': 'remove', 'path': '/extra/bar'}], patch)

    def test_print_dict_unicode(self):
        unicode_str = u'\u2026'
        output_file = six.StringIO()
        utils.print_dict({'K': 'k', 'Key': unicode_str}, outfile=output_file)
        self.assertIn(unicode_str, output_file.getvalue())
