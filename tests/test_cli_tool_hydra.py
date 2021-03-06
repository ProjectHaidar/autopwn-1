import autopwn
import builtins
import os
import pytest
import sys
import subprocess

from autopwn import _main, main
from mock import mock_open, patch
from collections import namedtuple

target_contents = '''
targets:
   - target_name: test
     target: 127.0.0.1
     url: /test
     port_number: 80
     protocol: https
     user_file: /tmp/users
     password_file: /tmp/passwords
     modules: ['tool/nmap']'''

def test_cli_tool_hydra(monkeypatch,tmpdir):
    test_target = tmpdir.join('target')
    test_target.write(target_contents)

    FakePopen = namedtuple('FakePopen', 'communicate')

    #monkeypatch.setattr(os.path, 'abspath', test_target)
    def fake(*args):
        assert args[0] == '/usr/bin/nmap -A -sS -sC -sV 127.0.0.1 -oA 20150420_autopwn_127.0.0.1_test/20150420_170645+0100_test_nmap_common_ports_127.0.0.1'
        return FakePopen(lambda : ('', ''))

    monkeypatch.setattr(subprocess, 'Popen', fake)

    monkeypatch.setattr(sys, 'argv', ['autopwn','-t', str(test_target)])
    autopwn._main(sys.argv[1:])
    assert len(autopwn.config.job_queue) == 1
