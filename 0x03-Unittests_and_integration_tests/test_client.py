#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.org
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct result"""
        expected_result = {"name": org_name}
        mock_get_json.return_value = expected_result 

        client = GithubOrgClient(org_name)
        result = client.org

        
        self.assertEqual(result, expected_result)

     
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos_url from org"""
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/testorg/repos")
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method returns list of repo names"""

        mock_get_json.return_value=[
            {"name":"abdelmouniam"},
            {"name":"harba"},
            {"name":"sifr"}
          ]

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            repo = client.public_repos()

            self.assertEqual(repo, ["abdelmouniam", "harba", "sifr"])

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license static method with different inputs"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


