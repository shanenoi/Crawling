from colorama import Fore,Style

import os
import re
import requests


def list_url(url, function_get_html, include, exclude):
    """
        Listing URL in html code with some option
    """

    def fix_url(pattern_url, link):
        if link.startswith('/'):
            return pattern_url + link
        else:
            return re.findall('([^:]+://[^/]+)', pattern_url)[0] + '/' + link

    html_code = function_get_html(url)

    urls = [
        i for i in re.findall('href="([^" ]+)"', html_code)
        if (
                True not in [j in i for j in exclude] and
                True in [j in i for j in include]
        )
    ]
    return [
        link
        if link.startswith('http') else fix_url(url, link)
        for link in urls
    ]


class CurrentTask(object):
    """
        [-] Save Process
        [-] You can use it for
            [+] URL scanning
            [+] Array processing
            ...
    """

    def __init__(self, file_name):
        try:
            self.file = open(file_name, 'r+')
        except FileNotFoundError:
            self.file = open(file_name, 'w+')

    def add(self, container):
        self.file.write(
            self.hash_object(container)
        )

    @staticmethod
    def __hash(value, p_num=3264):
        ar = [str(ord(i)) for i in str(value)]
        temp = sorted([int(''.join(ar)), p_num])
        temp = str(temp[0] / temp[1])
        return temp \
            .replace('e-', '') \
            .replace('.', '')

    def hash_object(self, value):
        return self.__hash(str(
            value.__repr__()
        ))

    def isdone(self, container):
        self.file.seek(0)
        return self.hash_object(container) in self.file.read()


class Spider(CurrentTask):
    """
        [-] Basically, it's just a recursion spider!
    """

    config = {
        'list_url': list_url,
        'include': ['.'],
        'exclude': []
    }
    folder_content = "spider's house"

    def __init__(self, function_process_url, file_store_process):
        super().__init__(file_store_process)
        self.function = function_process_url

    def get_html(self, url):
        html_code = requests.get(url).text
        '''This code will save html code to file'''
        try:
            os.mkdir(self.folder_content)
        except FileExistsError:
            pass
        with open(
                './{0}/{1}'.format(
                    self.folder_content,
                    url.replace('/', '')
                ), 'w'
        ) as f:
            f.write(re.sub('(<[^<>]+>)', '', html_code))
        '''[+]'''
        return html_code

    def bit(self, url):
        for url in self.config['list_url'](
                url,
                self.get_html,
                self.config['include'],
                self.config['exclude']
        ):
            if not self.isdone(url):
                self.function(url)
                self.add(url)
                self.bit(url)

    def find_something_in_spiderhouse(self, regex_or_word):
        """
            [-] I have not optimized for multi line yet!
        """

        def recursion(link):
            if os.path.isfile(link):
                for line in open(link, encoding='latin1'):
                    result = re.search(f'.{{0,9}}{regex_or_word}.{{0,9}}', line)
                    if result:
                        print(
                            f'found in {Fore.GREEN+link+Style.RESET_ALL}: ... {Fore.BLUE+result.group()+Style.RESET_ALL} ...'
                        )
            else:
                for ld in os.listdir(link):
                    recursion(f'{link}/{ld}')

        recursion(self.folder_content)
