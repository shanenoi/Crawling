from colorama import Fore,Style

import os
import re
import requests


def list_url(url, function_get_html, include, exclude):
    """
        Listing URL in html code with some option
    """

    def fix_url(pattern_url, link):
        fixed = None

        website = re.findall("([^:]+://[^/]+)", pattern_url)[0]
        if link.startswith("/"):
            fixed = website + link
        else:
            fixed = website + "/" + link

        open("fixed_urls", "a").write(f"{link}->{fixed}\n")
        return fixed

    html_code = function_get_html(url)

    urls = [
        i for i in re.findall('href="([^" ]+)"', html_code)
        if (
                not any([j in i for j in exclude]) and
                any([j in i for j in include])
        )
    ]
    return [
        link
        if link.startswith("http") else fix_url(url, link)
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
            self.file = open(file_name, "r+")
        except FileNotFoundError:
            self.file = open(file_name, "w+")

    def add(self, container):
        self.file.write(
            self.hash_object(container)
        )

    @staticmethod
    def __hash(value, p_num=3264):
        ar = [str(ord(i)) for i in str(value)]
        temp = sorted([int("".join(ar)), p_num])
        temp = str(temp[0] / temp[1])
        return temp \
            .replace("e-", "") \
            .replace(".", "")

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

    config_url = {
        "list_url": list_url,
        "include": ["/"],
        "exclude": ["facebook.", "google.", "messenger.", "youtube."]
    }
    folder_content = "cocoon_of_spider"
    deep_level = 5 # avoid going deeper and deeper of a url

    def __init__(self, function_process_url, file_store_process="crawled_urls"):
        super().__init__(file_store_process)
        self.function = function_process_url

    def get_html(self, url):
        html_code = ""
        try:
            html_code = requests.get(url).text
        except requests.exceptions.ConnectionError:
            pass
        """This code will save html code to file"""
        try:
            os.mkdir(self.folder_content)
        except FileExistsError:
            pass
        with open(
                "./{0}/{1}".format(
                    self.folder_content,
                    url.replace("/", "")
                ), "w"
        ) as f:
            f.write(re.sub("(<[^<>]+>)", "", html_code))
        """[+]"""
        return html_code

    def bit(self, url):
        for url in set(self.config_url["list_url"](
                url,
                self.get_html,
                self.config_url["include"],
                self.config_url["exclude"]
        )):
            if not self.isdone(url) and self.deep_level!=0:
                self.function(url)
                self.add(url)
                self.bit(url)
                self.deep_level -= 1

    def find_something_in_spiderhouse(self, regex_or_word):
        """
            [-] I have not optimized for multi line yet!
        """

        def recursion(link):
            if os.path.isfile(link):
                for num_line, line in enumerate(open(link, encoding="latin1")):
                    result = re.search(f".{{0,9}}{regex_or_word}.{{0,9}}", line)
                    if result:
                        print(
                                f"found in line: {num_line+1} " +
                                f"of {Fore.GREEN+link+Style.RESET_ALL}: "+
                                f"{Fore.BLUE}... {result.group()} ...{Style.RESET_ALL}"
                        )
            else:
                for ld in os.listdir(link):
                    recursion(f"{link}/{ld}")

        recursion(self.folder_content)
