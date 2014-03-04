#coding=utf-8
# Name:        
# Purpose:
# Author:      libin
# Created:     
#-----------------------------------------------------------------------------------------------------------------------

import re
import urllib2


class infoMatcher():
    "负责从网页流中找出关键词"

    info = []
    def __init__(self,web,id):
        self.id =id
        self.web = web
        self.info = [self.id]

    def record_otherReasons(self,web_record,id_record):
        path_record = "D:\\other_reasons\\"+str(id_record)+".txt"
        open(path_record,"w").write(web_record)

    def filter_closed(self):
        filter0 = re.compile("您查找的用户ID有误或不存在，请尝试其他方式搜索",re.DOTALL)
        content0 = filter0.findall(self.web)
        self.content0 = "".join(content0)

    def filter(self):
        filter1 = re.compile("查看详细信息&gt;&gt;</a(.*?)婚",re.DOTALL)
        content = filter1.findall(self.web)
        self.content = "".join(content)
        #print(self.content)

    def getsex(self):
        filter_sex = re.compile(">(.*?)，",re.DOTALL)
        sex = filter_sex.findall(self.content)
        self.sex = "".join(sex)
        #self.sex=self.sex.decode("utf-8")

    def getage(self):
        filter_age = re.compile("，([0-9][0-9])岁",re.DOTALL)
        age = filter_age.findall(self.content)
        self.age = int("".join(age))
        #print(self.age)

    def getxinzuo(self):
        filter_xinzuo = re.compile("岁，(.*?)，",re.DOTALL)
        xinzuo = filter_xinzuo.findall(self.content)
        self.xinzuo = "".join(xinzuo)

    def getlocation(self):
        filter_location = re.compile("来自(.*?)<",re.DOTALL)
        location = filter_location.findall(self.content)
        self.location = "".join(location)

    def getheight(self):
        filter_height = re.compile("身高：</b>(.*?)厘米",re.DOTALL)
        height = filter_height.findall(self.content)
        self.height = int("".join(height))

    def getdegree(self):
        filter_degree = re.compile("学历：</b>(.*?)<",re.DOTALL)
        degree = filter_degree.findall(self.content)
        self.degree = "".join(degree)

    def domatch(self):
        self.filter()
        if self.content:
            self.getsex()
            self.getage()
            self.getxinzuo()
            self.getlocation()
            self.getheight()
            self.getdegree()
            # 将中文的bytes decode 成str存入info中，方便存入数据库和xls文件
            self.info+=[self.sex.decode("utf-8"),self.age,self.xinzuo.decode("utf-8"),self.location.decode("utf-8"),self.height,self.degree.decode("utf-8")]
        else:
            self.filter_closed()
            if self.content0:
                self.info+=["closed"]
            else:
                self.info+=["other reasons"]
                self.record_otherReasons(self.web,self.id)
        return self.info

def main():
        i = 110
        # url = "http://www.jiayuan.com/"+str(i)
        # request = urllib2.Request(url)
        # web_get = urllib2.urlopen(request).read()
        r=infoMatcher("欺诈行为",i).domatch()
        print(r)

if __name__ == '__main__':
    main()