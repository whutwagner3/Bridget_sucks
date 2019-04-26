'''
This python file was written with the help and guidance of a tutorial found at
https://www.twilio.com/blog/2018/07/find-fix-website-link-rot-python-beautifulsoup-requests.html
and is intended to assist with vectorbase linkrot associated with NCBI gene IDs updating utilising xpath to find updated
nuccore links that reference other X?_[0-9]+ IDs in the main HTML body (this only occurs in a depreciated gene ID)
'''

from concurrent import futures
import multiprocessing as mp
import os
import uuid
import urllib3
from lxml import html
import requests



# Sources of data (file)
IN_PATH = os.path.join(os.getcwd(), 'urlin.txt')
OUT_PATH = os.path.join(os.getcwd(), 'urlout.txt')
URL_TIMEOUT = 10.0
_URL_Spider_ID = 'Spider {id}'.format(id=str(uuid.uuid4()))
URL_HEADERS = {'User-Agent': _URL_BOT_ID}

_URL_RE = 'https?:\/\/www.ncbi.nlm.nih.gov\/nuccore\/[=a-zA-Z0-9\_\/\?\&\.\-]+'  # proto://host+path+params
_FIND_URLS = "find . -type f | xargs grep -hEo '{regex}'".format(regex=_URL_RE)
_FILTER_URLS = "sed '/Binary/d' | sort | uniq > {urlin}".format(urlin=IN_PATH)
COMMAND = '{find} | {filter}'.format(find=_FIND_URLS, filter=_FILTER_URLS)

os.system(COMMAND)

'''
Main parser: return 
'''
def get_url_status(url):
    for local in ('localhost', '127.0.0.1', 'app_server'):
        if url.startswith('http://' + local):
            return (url, 0)
    clean_url = url.strip('?.')
    try:
        page = requests.get(clean_url)
        tree = html.fromstring(page.content)
        depreciated_links = tree.xpath('/html/body//a[contains(@href,"nuccore/X")]/@href')
        if depreciated_links:
            with open("To Update", 'a') as logfile:
                logfile.write(clean_url, "\t", depreciated_links)
        return (clean_url, response.status_code)
    except requests.exceptions.Timeout:
        return (clean_url, 504)
    except requests.exceptions.ConnectionError:
        return (clean_url, -1)


def bad_url(url_stat):
    if url_stat == -1:
        return True
    elif url_stat == 401 or url_status == 403:
        return False
    elif url_stat == 503:
        return False
    elif url_stat >= 400:
        return True
    else:
        return False


def run_workers(work, data, worker_threads=mp.cpu_count()*4):
    with futures.ThreadPoolExecutor(max_workers=worker_threads) as foreman:
        future_to_result = {
            foreman.submit(work, arg): arg for arg in data}
        for future in futures.as_completed(future_to_result):
            yield future.result()


with open(IN_PATH, 'r') as fr:
    urls = map(lambda l: l.strip('\n'), fr.readlines())
with open(OUT_PATH, 'w') as fw:
    url_id = 1
    max_strlen = -1
    for url_path, url_status in run_workers(get_url_status, urls):
        output = 'Currently checking: id={uid} host={uhost}'.format(
            uid=url_id, uhost=urllib3.util.parse_url(url_path).host)
        if max_strlen < len(output):
            max_strlen = len(output)
        print(output.ljust(max_strlen), end='\r')
        if bad_url(url_status) is True:
            fw.write('{}: {}\n'.format(url_path, url_status))
        url_id += 1

