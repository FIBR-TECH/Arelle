import os
import requests
from multiprocessing import Pool
import time
import json
import TestArelle

# set where to save files
CACHE_DIR = 'cache'

# arelle config dir (contains edgartaxonomies-all-years.xml, hmrc-taxonomies.xml etc.)
#XMLS_DIR = r'C:\Lendflo\Arelle-master\arelle\config'
XMLS_DIR = r'/home/ubuntu/env/lib/python3.5/site-packages/arelle/config'
# dir with XBRL samples
XBLR_SAMPLES_DIR = 'samples'


def get_file(url):
    locations = url.split('://')
    assert len(locations) == 2, "Tu ma być 2 kuuurłaaaa"
    dest = os.path.join(CACHE_DIR, os.sep.join(locations).replace('/', os.sep))
    dirs = os.path.dirname(dest)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    if os.path.exists(dest):
        return True

    print("Downloading: {}".format(url))
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(dest, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
                return True
        else:
            print("File {} is unavailable".format(url))
    except Exception as ex:
        print("Exception: {}".format(str(ex)))

    return False


def extract_links(path_to_dir_with_xmls):
    results = []
    for item in os.listdir(path_to_dir_with_xmls):
        if not item.endswith('.xml'):
            continue

        print("Processing {}".format(item))
        with open(os.path.join(path_to_dir_with_xmls, item), 'rt') as f:
            for line in f:
                start_index = line.find('>http')
                while start_index != -1:
                    end_index = line.find('.xsd<', start_index+1)
                    if end_index == -1:
                        end_index = line.find('.xml<', start_index+1)
                        if end_index == -1:
                            break
                    url = line[start_index + 1:end_index + 4]
                    if url not in results:
                        results.append(url)
                    start_index = line.find('>http', start_index+1)
    return results


if __name__ == "__main__":

    # find links in schema templates
    links = extract_links(XMLS_DIR)
    print("Found {} links".format(len(links)))

    if len(links) == 0:
        print("Something went wrong! Make sure you set correct XMLS_DIR AND CACHE_DIR")
        exit(1)

    # download all
    with Pool() as pool:
        results = pool.map(get_file, links)

    # now prepare .json file with cached links
    timeNow = time.time()
    timeNowStr = time.strftime('%Y-%m-%dT%H:%M:%S UTC', time.gmtime(timeNow))

    xlinks = {}
    for index, value in enumerate(links):
        if results[index]:
            xlinks[value] = timeNowStr

    file = os.path.join(os.path.dirname(os.path.abspath(CACHE_DIR)), "cachedUrlCheckTimes.json")
    print("Saving JSON file to: {}".format(file))
    with open(file, 'wt') as f:
        json.dump(xlinks, f, indent=0)

    # run tests which will also download additional caches
    TestArelle.run_test(XBLR_SAMPLES_DIR)

    print("\nDone. Auf Wiedersehen!")
