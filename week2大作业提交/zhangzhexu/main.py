from multiprocessing import Pool
from start_urls import urls
from spider import get_links_from


def get_all_links_from(o_url):
    for i in range(1,100):
        get_links_from(o_url,i)


if __name__ == '__main__':
    pool = Pool()
    # pool = Pool(processes=6)
    pool.map(get_all_links_from,urls.split())

