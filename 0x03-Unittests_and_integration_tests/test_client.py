import unittest
from unittest.mock import patch
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        # بيانات وهمية تمثل رد الـ API على قائمة الريبو
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]

        client = GithubOrgClient("some_org")
        repos = client.public_repos()

        expected = ["repo1", "repo2", "repo3"]
        self.assertEqual(repos, expected)

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]

        client = GithubOrgClient("some_org")
        repos = client.public_repos(license="apache-2.0")

        expected = ["repo2"]
        self.assertEqual(repos, expected)


if __name__ == "__main__":
    unittest.main()
