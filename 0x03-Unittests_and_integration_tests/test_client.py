#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.org
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # نمنع الاتصال الحقيقي ونراقب الدالة
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct result"""
        expected_result = {"name": org_name}
        mock_get_json.return_value = expected_result  # نتيجة مزورة

        client = GithubOrgClient(org_name)
        result = client.org

        # تحقق من القيمة المرجعة
        self.assertEqual(result, expected_result)

        # تحقق أن get_json استُدعيت مرة واحدة بالـ URL الصحيح
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
