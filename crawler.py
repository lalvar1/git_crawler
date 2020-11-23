import requests
import re
import random
import json
import operator


class GitHubCrawler:
    """Class to crawl GitHub search results"""
    def __init__(self, search_input):
        self.url = "https://github.com"
        self.type = search_input["type"]
        self.keywords = search_input["keywords"]
        self.proxies = search_input["proxies"]

    type = property(operator.attrgetter('_type'))

    @type.setter
    def type(self, input_type):
        supported_types = ['repository', 'issues', 'wikis']
        if input_type not in supported_types:
            raise Exception(f"Specified type is not supported. Supported types are: {supported_types}")
        self._type = input_type

    @staticmethod
    def get_html(url, proxy):
        """
         Get html decoded content
        :param url: target url
        :param proxy: proxy to be used for triggering the http request
        :return: decoded html content
        """
        try:
            html = requests.get(url, proxies={"http": proxy})
            return html.content.decode()
        except Exception as e:
            print(f'Error while getting HTML content. Error was: {e}')
            return

    def get_search_results(self):
        """
        Get searched urls, with owner's info
        :return: list of dicts
        """
        regex_pattern = 'data-hydro-click-hmac.*href=\"(.*?)\">'
        search_items = ','.join(self.keywords).replace(',', '+')
        search_url = f'{self.url}/search?q={search_items}&type={self.type}'
        search_proxy = self.proxies[random.randint(0, len(self.proxies)-1)]
        html_content = self.get_html(search_url, search_proxy)
        parsed_values = re.findall(regex_pattern, html_content)
        owners_data = self.get_owner_stats(set(parsed_values)) if self.type.upper() == "REPOSITORY" else None
        result = [{"url": f'{self.url}{value}', "extra": {"owner": value.split('/')[1]},
                   "language_stats": owners_data[value.split('/')[1]] if owners_data else None}
                  for value in parsed_values]
        return result

    def get_owner_stats(self, owners):
        """
        Get owner languages for a given repository
        :param owners: list of strings, specifying repo of the owner
        :return: languages hashmap
        """
        owners_data ={}
        regex_pattern = 'itemprop="keywords".*?="(.*?)"'
        search_proxy = self.proxies[random.randint(0, len(self.proxies)-1)]
        for owner in owners:
            owner_url = f'{self.url}/{owner}'
            html_content = self.get_html(owner_url, search_proxy)
            languages = re.findall(regex_pattern, html_content)
            languages_dict = {language.split()[0]: language.split()[1] for language in languages}
            owners_data[owner.split('/')[1]] = languages_dict
        return owners_data


if __name__ == "__main__":
    mock_input = {
        "keywords": [
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [
            "177.37.240.52:8080",
            "200.0.226.122:8080"
        ],
        "type": "repository"
    }
    crawler = GitHubCrawler(mock_input)
    search_results = crawler.get_search_results()
    print(json.dumps(search_results, indent=2))
