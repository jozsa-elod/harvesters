#!/usr/bin/env python3
# ----------------------------------------------------------------------------
#
# Copyright 2018 EMVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ----------------------------------------------------------------------------


# Standard library imports
from logging import DEBUG
import os
import sys
import unittest

# Related third party imports

# Local application/library specific imports
from harvesters.core import Harvester
from harvesters_util.logging import get_logger


def get_cti_file_path():
    name = 'HARVESTERS_TEST_TARGET'
    if name in os.environ:
        # Run tests with specified GenTL Producer:
        cti_file_path = os.getenv(name)
    else:
        try:
            import genicam2
        except ImportError:
            # Failed to import genicam2 module; suggest the expected
            # solution to the client:
            raise ImportError(
                'You must specify a target GenTL Producer either using '
                'HARVESTERS_TEST_TARGET or installing genicam2 module.'
            )
        else:
            # Run tests with the default test target, TLSimu:
            dir_name = os.path.dirname(genicam2.__file__)
            cti_file_path = os.path.join(dir_name, 'TLSimu.cti')
    
    return cti_file_path
    
    
class TestHarvesterCoreBase(unittest.TestCase):
    _cti_file_path = get_cti_file_path()
    sys.path.append(_cti_file_path)

    def __init__(self, *args, **kwargs):
        #
        super().__init__(*args, **kwargs)

        #
        self._harvester = None
        self._ia = None
        self._thread = None
        self._logger = get_logger(name='harvesters', level=DEBUG)

    def setUp(self):
        #
        super().setUp()

        #
        self._harvester = Harvester(logger=self._logger)
        self._harvester.add_cti_file(self._cti_file_path)
        self._harvester.update_device_info_list()

    def tearDown(self):
        #
        if self.ia:
            self.ia.destroy()

        #
        self._harvester.reset()

        #
        self._ia = None

        #
        super().tearDown()

    @property
    def harvester(self):
        return self._harvester

    @property
    def ia(self):
        return self._ia

    @ia.setter
    def ia(self, value):
        self._ia = value

    @property
    def general_purpose_thread(self):
        return self._thread

    @general_purpose_thread.setter
    def general_purpose_thread(self, value):
        self._thread = value

    def is_running_with_default_target(self):
        return True if 'TLSimu.cti' in self._cti_file_path else False


if __name__ == '__main__':
    unittest.main()
