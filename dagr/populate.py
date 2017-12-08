#create binary tree of Data
from .models import Dagr, Category, Relationships, Keyword, Dagr_keywords
import datetime
import math
import random
import radar
import dateutil.relativedelta

def create_binarytree():

    #create categorys
    for i in range(0,6):
        name = "category "+ str(i)
        Category.objects.create(categoryName=name)

    categorys = list(Category.objects.all())
    len_category = len(categorys)

    #create DAGRs
    for i in range(0,400):
        location = "home/"
        author = "Author" + str(i%7)
        size = i % 25
        typ = str(i%5)
        realName = str(i)
        assignedName = str(i)
        st = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        lastModified = radar.random_datetime(start=st, stop=datetime.datetime.now())
        dateCreated = datetime.datetime.now()
        categoryID = categorys[i%len_category]

        Dagr.objects.create(Location=location, RealName=realName, AssignedName=assignedName, LastModified=lastModified, DateCreated=dateCreated,CategoryID=categoryID, Size=size,Type=typ, Author=author)

    dagrs = list(Dagr.objects.all())

    #create Relationships
    for i in range(0,int(math.log(len(dagrs),2)-1)):
        parent = dagrs[i]
        child1 = dagrs[(2*i)+1]
        child2 = dagrs[(2*i)+2]
        date = datetime.datetime.now()

        Relationships.objects.create(ParentGUID=parent.Guid, ChildGUID=child1, DateCreated=date)
        Relationships.objects.create(ParentGUID=parent.Guid, ChildGUID=child2, DateCreated=date)


    #create Keywords
    for i in range(0,30):
        keyword = "keyword" + str(i)
        Keyword.objects.create(name=keyword)

    keywords = list(Keyword.objects.all())
    for i in range(0,len(dagrs)):
        guid = dagrs[i]
        for k in range(0,random.randint(1,3)):
            keyword1 = keywords[random.randint(0,29)]
            Dagr_keywords.objects.create(GUID=guid, keyword=keyword1)
