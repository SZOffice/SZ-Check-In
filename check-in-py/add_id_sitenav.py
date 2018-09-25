# -*- coding: utf-8 -*-  
import os, sys, time
from datetime import datetime
import json

now = datetime.now()
list_date = {}
jsvar = "const site_list = "
  
#read txt
def open_file(path):
    context = ""
    try:
        file_object = open(path)
        context = file_object.read()[len(jsvar):]
    except:
        print("open_file error:" + path)
    finally:
        file_object.close( )
    return context

def gen_report():
    list = json.loads(open_file("D:\itdev\SiteNav\data\others.js"), encoding='utf-8')
    #print(list)
    index = 1
    for site in list:
        site["id"] = str(index)
        index = index + 1
        child_index = 1
        if site.has_key("children"):
            for child in site["children"]:
                child["id"] = str(child_index)
                child_index = child_index + 1
                grandson_index = 1
                if child.has_key("children"):
                    for grandson in child["children"]:
                        grandson["id"] = str(grandson_index)
                        grandson_index = grandson_index + 1
                #print(child)

    f = open("temp.log", 'w')
    f.write(jsvar + json.dumps(list, encoding="gbk", ensure_ascii=False).encode('utf-8'))
    f.close()
    
    print("generated report")
    
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("not args")
    
    t = time.time()
    
    gen_report()

    print("total run time:")
    e = time.time()
    print(e-t)
