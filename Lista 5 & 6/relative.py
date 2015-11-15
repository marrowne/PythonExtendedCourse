import re
import os.path
from lists import htmlBase

def linksDict(path, dict):
    fsource = open(path, 'r')
    source = fsource.read()
    fsource.close()

    match1_obj = re.compile("< *a.*href *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"")

    a_hrefs = [url.group() for url in match1_obj.finditer(source)]
        # find all a hrefs
    hrefs = map(lambda x: re.search("href *= *\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), a_hrefs)
        # take hrefs
    path1 = map(lambda x: re.search("\"[/.,:?_=&;\-%#a-zA-Z0-9]*\"", x).group(), hrefs)
        # take paths with quotations
    path2 = map(lambda x: x.strip('"'), path1)
    flinks = filter(lambda x: x != '', path2)
    absolute_links = htmlBase(path, flinks, False)

    # drop blank elements

    for x in absolute_links:
        if not re.match("https?://", x) and re.search(".html?", x):
            # removing online links
            if x in dict:
                if path not in dict[x]:
                    dict[x].append(x)
            else:
                dict[x] = [path]

class Links:
    def __init__(self, src):
        self.files_list = [os.path.join(root, filename)\
          for root, dirnames, filenames in os.walk(src)\
          for filename in filenames if re.search(".html?", filename)]
        self.dict = {}
        for x in self.files_list:
            linksDict(x, self.dict)

    def linksPrint(self):
        for x in self.dict:
            print(x, self.dict[x])