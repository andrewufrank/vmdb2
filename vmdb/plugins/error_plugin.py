# Copyright 2017  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=



import logging
import sys

import cliapp

import vmdb


class ErrorPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(ErrorStepRunner())
        

class ErrorStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['error', 'teardown']

    def run(self, step_spec, settings, state):
        sys.stdout.write('ERROR: {}\n'.format(step_spec['error']))
        logging.error('%s', step_spec['error'])
        raise vmdb.StepError('an error occurred')

    def teardown(self, step_spec, settings, state):
        sys.stdout.write('ERROR: {}\n'.format(step_spec['teardown']))
        logging.error('error cleanup: %s', step_spec['teardown'])
