import os
import re
import requests

def list_url(url, function_getHtml, include, exclude):
    '''
        Listing URL in html code with some option
    '''
    
    def fix_url(url, link):
        if link.startswith('/'):
            return url+link
        else:
            return re.findall('([^:]+://[^/]+)', url)[0] +'/'+ link

    html_code = function_getHtml(url)

    urls = [
        i for i in re.findall('href="([^" ]+)"', html_code) 
        if (
            True not in [j in i for j  in exclude] and
            True in [j in i for j in include]
        )
    ]
    return [
            link
            if link.startswith('http') else fix_url(url, link)
            for link in urls
    ]


class CurrentTask(object):
    '''
        [-] Save Process
        [-] You can use it for 
            [+] URL scanning
            [+] Array processing
            ...
    '''

    def __init__(self, file_name):
        try:
            self.file = open(file_name, 'r+')
        except FileNotFoundError:
            self.file = open(file_name, 'w+')


    def add(self, object):
        self.file.write(
            self.hash_object(object)
        )
    
    
    @staticmethod
    def __hash(value, pnum=3264):
        ar = [str(ord(i)) for i in str(value)]
        temp = sorted([int(''.join(ar)), pnum])
        temp = str(temp[0]/temp[1])
        return temp.replace('e-', '')[-9:]


    def hash_object(self, object):
        return self.__hash(str(object.__repr__()
        ))


    def isdone(self, object):
        self.file.seek(0)
        return self.hash_object(object) in self.file.read()


class Spider(CurrentTask):

    '''
        [+] Basicly, it's just a recursion spider
    '''

    config = {
            'list_url': list_url,
            'include': ['.'],
            'exclude': []
    }
    folder_content = 'data'

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
                ),'w'
        ) as f:
            f.write(re.sub('(<[^<>]+>)', '', html_code))
        '''[+]'''
        return html_code


    def deep(self, url):
        for url in self.config['list_url'](
                url,
                self.get_html,
                self.config['include'],
                self.config['exclude']
        ):
            if not self.isdone(url):
                self.function(url)
                self.add(url)
                self.deep(url)
