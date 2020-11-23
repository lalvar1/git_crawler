import unittest
from crawler import GitHubCrawler


class TestModule(unittest.TestCase):
    def setUp(self):
        mock_input = {
            "keywords": [
                "openstack",
                "nova",
                "css"
            ],
            "proxies": [
                "177.37.240.52:8080",
                "170.238.255.90:3113"
            ],
            "type": "repository"
        }
        self.crawler = GitHubCrawler(mock_input)

    def test_get_html(self):
        url = "https://github.com/search?q=openstack+nova+css&type=repositories"
        proxy = "200.0.226.122:8080"
        content = self.crawler.get_html(url, proxy)
        self.assertIsNotNone(content)

    def test_get_html_failure(self):
        url = "https://gitrub.com/search?q=openstack+nova+css&type=repositories"
        proxy = "200.0.226.122:8080"
        content = self.crawler.get_html(url, proxy)
        self.assertRaises(Exception)

    def test_get_search_results(self):
        parsed = self.crawler.get_search_results()
        mocked_parsed_values = [{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage',
                                 'extra': {'owner': 'atuldjadhav'}, 'language_stats':
                                     {'CSS': '52.0', 'JavaScript': '47.2', 'HTML': '0.8'}},
                                {'url': 'https://github.com/michealbalogun/Horizon-dashboard',
                                 'extra': {'owner': 'michealbalogun'}, 'language_stats': {'Python': '100.0'}}]
        self.assertEqual(parsed, mocked_parsed_values)

    def test_get_owner_stats(self):
        mocked_stats = {'michealbalogun': {'Python': '100.0'},
                        'atuldjadhav': {'CSS': '52.0', 'JavaScript': '47.2', 'HTML': '0.8'}}
        owners_input = {'/michealbalogun/Horizon-dashboard', '/atuldjadhav/DropBox-Cloud-Storage'}
        owner_stats = self.crawler.get_owner_stats(owners_input)
        self.assertEqual(owner_stats, mocked_stats)


if __name__ == '__main__':
    unittest.main()
