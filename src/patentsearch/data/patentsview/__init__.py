from bs4 import BeautifulSoup
import requests
import datetime
import sys
import json
import os
import time
download_url = 'http://www.patentsview.org/download/'


def _process_pv_tr(r: BeautifulSoup):
    '''
    Parsing based on the current structure of patentsview download page

    '''
    tds = r.find_all('td')
    result = None
    if(len(tds) == 4):
        details = r.find_all('td')[0]
        description = r.find_all('td')[1].get_text()
        rows_text = r.find_all('td')[2].get_text()
        if(rows_text):
            rows_text = rows_text.replace(',', '')
        else:
            sys.exit('expected rows, review format\n')
        rows = 0
        try:
            rows = int(rows_text)
        except:  # noqa
            sys.exit(
                'expected int rows,got %s review format\n' %
                rows_text)
        name = details.find('a').get_text()
        size_text = details.find('span', class_='filesize').get_text()
        size_text, *tail = size_text.split(' ')
        try:
            size = float(size_text)
        except:  # noqa
            sys.exit(
                'expected float size,got %s review format\n' %
                size_text)
        unit, *tail = tail
        unit = unit[0:2]
        url = details.find('a')['href']
        result = (name, description, rows, size, unit, url)
    return result


class PatentsView:
    '''
    pv = PatentsView()
    //last_update
    pv.last_update
    //this will give you all data available
    pv

    //you can get the details of a specific content as follows for example
    pv.brf_sum_txt
    '''

    def __init__(self):
        response = requests.get(download_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        last_update = soup.find_all('p', class_='one-line')
        date_string = last_update[0].get_text()
        self.__dict__['_last_update'] = datetime.datetime.strptime(
            date_string, '%B %d, %Y')
        main_section = soup.find('section', class_='mainContent')
        main_table = main_section.find('table')
        data = [_process_pv_tr(r)
                for r in main_table if r.name == 'tr']
        data = [d for d in data if(d)]
        self.__dict__['available_data'] = []
        for d in data:
            (name, description, rows, size, unit, url) = d
            name = name.replace(' ', '_')
            self.available_data.append(name)
            self.__dict__[name] = {
                'description': description,
                'rows': rows,
                'size': size,
                'unit': unit,
                'url': url}

    def download(self, dataset: str, download_path: str):
        if(not os.path.isdir(download_path)):
            raise ValueError(
                '%s is not a valid directory to download' %
                download_path)
        if(dataset not in self.available_data):
            raise ValueError(
                '%s is not a valid dataset to download' %
                dataset)
        chunk_size = 1024 * 1024
        relative_file_path = requests.utils.urlparse(
            self.__dict__[dataset].get('url')).path[1:]
        download_file_path = os.path.join(download_path, relative_file_path)
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        start_time = time.time()
        sys.stderr.write(
            '\n Starting download, each = in the download indicator  \
            represents 2% of download\n')
        with requests.get(self.__dict__[dataset].get('url'), stream=True) as \
                response:
            indicator = True
            dl = 0
            try:
                total_length = int(response.headers.get('content-length'))
            except:  # noqa
                indicator = False

            with open(download_file_path, 'wb') as fs:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        fs.write(chunk)
                        if(indicator):
                            dl += len(chunk)
                            done = int(50 * dl / total_length)
                            sys.stderr.write("\r[%s%s]" % (
                                '=' * done, ' ' * (50 - done)))
                            sys.stderr.flush()

        time_taken = time.time() - start_time
        sys.stderr.write(
            '\nDownloaded %s in %s time\n' %
            (download_file_path, str(time_taken)))

    @property
    def last_update(self):
        '''
        When you download the archive from patentsview, the directory hierarchy
        is like  data/20181127/bulk-downloads/brf_sum_txt.tsv
        Providing last_update in the same format, so can check if there is a
        need to download new version.
        '''
        return self._last_update.strftime('%Y%m%d')

    def __setattr__(self, name, value):
        raise Exception("read only!")

    def __repr__(self):
        d = {
            'last_update': self.last_update
        }

        for item in self.available_data:
            d = {**d, item: self.__dict__[item]}
        return json.dumps(d)
