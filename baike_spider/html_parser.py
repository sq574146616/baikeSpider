import re
import urllib
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, new_url, html_count):
        if new_url is None or html_count is None:
            return

        soup = BeautifulSoup(html_count, 'html.parser')
        new_urls = self._get_new_urls(new_url, soup)
        new_data = self._get_new_data(new_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, url, soup):
        new_urls = set()

        links = soup.find_all('a', href=re.compile(r"/item/(.*)"))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(url, new_url)
            new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, url, soup):
        res_data = {}

        res_data['url'] = url

        # <dd class ="lemmaWgt-lemmaTitle-title" ><h1>Python</h1>
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()

        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_='lemma-summary')
        res_data['summary'] = summary_node.get_text()

        return res_data