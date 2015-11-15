# This module contains function and classes responsible for finding dead links(photos)
# in folder and it's subfolders. It contains functions checking online destinations as well

import urllib.request
import re
import ssl
import functools
import os.path
import multiprocessing.pool

def links(source, online):
    """
    Function returns list of all adresses in <a href = "adress"> in HTML file

    :param source: string containing destination file destination
    :param online: True if source html is online
    :return: list of absolute paths to online and local destinations
    """

    match1_obj = re.compile("< *a.*href *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"")

    a_hrefs = [url.group() for url in match1_obj.finditer(source)]
        # find all a hrefs
    hrefs = map(lambda x: re.search("href *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), a_hrefs)
        # take hrefs
    path1 = map(lambda x: re.search("\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), hrefs)
        # take paths with quotations
    path2 = map(lambda x: x.strip('"'), path1)
    flinks = filter(lambda x: x != '', path2)
        # drop blank elements
    return list(flinks)

def photos(source, online):
    """
    Function returns list of all adresses in <img href = "adress"> and <img src = "adress" in HTML file

    :param source: string, destination of file
    :param online: True if source html is online
    :return: list of absolute paths to online and local destinations
    """

    match_obj = re.compile("< *img.*src *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"")

    a_imgs = [url.group() for url in match_obj.finditer(source)]
    imgs = map(lambda x: re.search("src *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), a_imgs)
    path1 = map(lambda x: re.search("\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), imgs)
    path2 = map(lambda x: x.strip('"'), path1)
    flinks = list(filter(lambda x: x != '', path2))

    match_obj = re.compile("< *img.*href *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"")

    a_imgs = [url.group() for url in match_obj.finditer(source)]
    imgs = map(lambda x: re.search("href *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), a_imgs)
    path1 = map(lambda x: re.search("\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), imgs)
    path2 = map(lambda x: x.strip('"'), path1)
    flinks = flinks + list(filter(lambda x: x != '', path2))

    return flinks

def htmlBase(path, links, online=True):
    """
    :param path: path to HTML
    :param links: list of links
    :param online: False is path to HTML is in local destination /default True/
    :return: base path
    """
    if re.match(".*\.(html?|php)", path):
        base_path = re.match(".*/", path).group()
    elif path[-1:] == '/':
        base_path = path
    else:
        base_path = path + '/'

    if online:
        return list(map(lambda x: x if re.match('https?://', x) else (base_path + x), links))
    else:
        base_path = re.match(".*/", path).group()
        return list(map(lambda x: x if (re.match('/?home/', x) or \
                                        re.match('https?://', x)) else (base_path + x), links))

def status(link):
    """
    Returns status of link

    :param link: local or online destination (string)
    :return: raises error and returns False if link causes problem, otherwise returns only True
             urllib.error.URLError: can't find HTML on the web
             FileExistsError: Local file does not exists
             ssl.SSLError: sometimes caused eg. SSL certificate error
    """
    global curr_link
    curr_link = link
    if re.match("https?://", link):
        status = urllib.request.urlopen(link).getcode()
        # print(status, "\t[", link, "]")
        return status == 200
    else:
        if os.path.isfile(link):
            # print("OK\t\'{}\'".format(link))
            return True
        else:
            # print("Failure\t\'{}\'".format(link))
            raise FileExistsError

def checkFile(path):
    obj = LinkChecker(path)
    links_thr1 = multiprocessing.pool.ThreadPool(processes=1)
    links_thr2 = multiprocessing.pool.ThreadPool(processes=1)
    result1 = links_thr1.apply_async(obj.checkLinks)
    result2 = links_thr2.apply_async(obj.checkImages)
    res = result1.get() == True and result2.get() == True
    del obj
    return res


class LinkChecker:
    def __init__(self, path):
        """
        LinkChecker object constructor

        :param path: path to file
        :return: Linkchecker object
        """
        try:
            self.path = path
            if re.match('https?://', path):
                self.online = True
            else:
                self.online = False
            if self.online:
                with urllib.request.urlopen(path) as url:
                    self.source = url.read().decode("utf-8")
            else:
                fsource = open(path, 'r')
                self.source = fsource.read()
                fsource.close()
            links_thr = multiprocessing.pool.ThreadPool(processes=1)
            img_thr = multiprocessing.pool.ThreadPool(processes=1)
            links_res = links_thr.apply_async(links, (self.source, self.online))
            img_res = img_thr.apply_async(photos, (self.source, self.online))
            self.links = links_res.get()
            self.images = img_res.get()
        except urllib.error.HTTPError:
            print("Can't connect the webpage!")

    def checkLinks(self):
        """
        Check if all paths are working
        :return: True if all links working, otherwise False
        """
        try:
            links_with_bases = htmlBase(self.path, self.links, self.online)
            statuses = map(lambda x: status(x), links_with_bases)
            return functools.reduce(lambda x, y: x and y, statuses, True) == True
        except ssl.SSLError:
            print("Błąd SSL")
        except urllib.error.URLError:
            print("Cannot connect to link\t", curr_link)
        except FileExistsError:
            print("File '{}' does not exists.".format(curr_link))

    def checkImages(self):
        """
        Check if all paths are working
        :return: True if all images working, otherwise False
        """
        try:
            links_with_bases = htmlBase(self.path, self.images, self.online)
            statuses = map(lambda x: status(x), links_with_bases)
            statuses2 = statuses
            return functools.reduce(lambda x, y: x and y, statuses2, True) == True
        except ssl.SSLError:
            print("Błąd SSL")
        except urllib.error.URLError:
            print("Cannot connect to image\t", curr_link)
        except FileExistsError:
            print("File '{}' does not exists".format(curr_link))

class FileIterator:
    def __iter__(self):
        return self

    def __next__(self, file):
        return checkFile(file)

def listOfFiles(src):
    return [os.path.join(root, filename)\
        for root, dirnames, filenames in os.walk(src)\
        for filename in filenames if re.search(".html?", filename)]

def checkFolder(path):
    obj = FileIterator()
    for file in listOfFiles(path):
        print("[{}]".format(file))
        print(obj.__next__(file) == True)
