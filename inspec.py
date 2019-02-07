#!/usr/share/python/sd-agent/bin/python
#
# Copyright (c) 2018 Andrei Skopenko <andrei@skopenko.net>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import yaml
import subprocess
import os

sys.path.append('/usr/share/python/sd-agent')
from checks import AgentCheck


class Beanstalkd(AgentCheck):
    '''Tracks beanstalkd metrics
    '''

    def check(self, instance):

        # check inspec binary
        execute = '/usr/bin/inspec'
        if not os.access(execute, os.X_OK):
            raise Exception(u'InSpec binary not found')

        # Attempt to load the profile_path setting from the instance config.
        if 'profile_path' not in instance:
            raise Exception(u'Please specify path to inspec profile')

        # Attempt to load the tags from the instance config.
        tags = instance.get('tags', [])

        cmd = [execute, 'exec', instance['profile_path']]
        if 'attributes_file' in instance:
            cmd.extend(['--attrs', instance['attributes_file']])
        if 'controls' in instance:
            cmd.append('--controls')
            cmd.extend(instance['controls'])
        cmd.extend(['--reporter', 'json-min'])

        sp = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = sp.communicate()
        if err:
            raise Exception(u'Could not execute inspec checks: %s' % err)

        stats = yaml.load(out)
        self.log.debug(u"InSpec raw data: {0}".format(stats))

        metrics = {'passed': 0, 'failed': 0, 'total': 0}
        for ctrl in stats['controls']:
            metrics['total'] += 1
            if ctrl['status'] == 'passed':
                metrics['passed'] += 1
            else:
                metrics['failed'] += 1

        for metric, value in metrics.iteritems():
            try:
                self.gauge('%s.%s' % ('inspec', metric), value, tags)
            except Exception as e:
                self.log.error(u'Could not submit metric: %s: %s' % (repr(metric), str(e)))

        self.log.debug(u"InSpec metrics: {0}".format(metrics))

if __name__ == '__main__':
    # Load the check and instance configurations
    check, instances = Beanstalkd.from_yaml('/etc/sd-agent/conf.d/inspec.yaml')
    for instance in instances:
        print "\nRunning the check against profile_path {} and attributes_file {}".format(
            instance['profile_path'], instance['attributes_file'])
        check.check(instance)
        print 'Metrics: {}'.format(check.get_metrics())
