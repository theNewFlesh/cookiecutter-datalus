{%- set cc = cookiecutter -%}
{%- set repo_ = (cc.repo | replace('-', '_')) -%}
{%- set abrv = (cc.repo[0] + "ct") -%}
import unittest

import {{ repo_ }}.core.tools as {{ abrv }}
# ------------------------------------------------------------------------------


class ToolsTests(unittest.TestCase):
    def test_dummy(self):
        {{ abrv }}.dummy()
