from django.shortcuts import render
from django.http import HttpResponse
from .forms import DagrForm, HtmlParserForm, UploadForm, MetaDataForm, ReachForm, TimeForm, KeywordForm, CategoryForm
from .models import Dagr, Dagr_keywords, Keyword, Category, Relationships
from django.shortcuts import redirect
import datetime
import dateutil.relativedelta
from django.db import connection
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.db import models
import zipfile
from django.views import View
from .html_parser import multi as parse_url
from django.views.decorators.http import require_http_methods
# Create your views here.

def message(request,message=None):
    return render(request, 'dagr/base.html',{'message':message})

def add_category(request):
    message = None
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save(commit=True)
            message = str(cd['categoryName']) + " Category created"
        else:
            message = "Invalid data"

    form = CategoryForm()

    return render(request, 'dagr/add_manually.html', {'form':form,"message":message})

def add_keyword(request):
    message = None
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save(commit=True)
            message = str(cd['name']) + " Keyword created"
        else:
            message="Invalid Keyword"

    form = KeywordForm()

    return render(request, 'dagr/add_manually.html', {'form':form,"message":message})

#add dagr by manually entering the data
def add_manually(request):
    message = None
    if request.method == 'POST':
        form_dagr = DagrForm(request.POST)
        if form_dagr.is_valid():
            try:
                form_dagr.save()
                message = form_dagr.cleaned_data['AssignedName'] + " Saved Successfully"
            except ValidationError as e:
                message = e.message
        else:
            message = "Invalid Input"
            return render(request, 'dagr/add_manually.html',{'form':form_dagr,'message':message})
    else:
        form_dagr = DagrForm()

    return render(request, 'dagr/add_manually.html',{'form':form_dagr,'message':message})

def add_url(request):
    message = None
    if request.method == 'POST':
        form = HtmlParserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            meta = parse_url(cd['url'])
            try:
                create_dagr_meta(meta)
                message="URL added Successfully"
            except ValidationError as e:
                message = e.message
                return render(request, 'dagr/add_url.html',{'form':form,'message':message})
        else:
            message="Invalid URL"

    form = HtmlParserForm()

    return render(request, 'dagr/add_url.html',{'form':form,'message':message})

def create_dagr_meta(url_meta):
    meta = url_meta[0]
    #change date into valid format
    #example from: 2017-11-01T19:26:16Z to 2017-11-01 19:26
    if (len(meta['title']) > 0 ):
        date_created = datetime.datetime.now()
        last_modified = datetime.datetime.now()
        if len(meta["lastmod"]) > 0:
            last_modified = meta['lastmod'].replace("T"," ").replace("Z","")[0:-3]
        if len(meta["pubdate"]) > 0:
            date_created = meta['pubdate'].replace("T"," ").replace("Z","")[0:-3]

        #get or create category
        category, created = Category.objects.get_or_create(categoryName=meta['category'])

        parent = Dagr.objects.create(AssignedName=meta["title"], RealName=meta["title"],Location=meta['location'], LastModified=last_modified, DateCreated=date_created, CategoryID=category, Size=0, Type=meta["doctype"])

        for k in meta['keywords']:
            key_word, created = Keyword.objects.get_or_create(name=k)

            Dagr_keywords.objects.get_or_create(GUID=parent, keyword=key_word)

        for i in range(1,len(url_meta) ):
            if len(url_meta[i]) > 0:
                child = create_dagr_meta(url_meta[i])
                if child != None:
                    Relationships.objects.create(ParentGUID=parent.Guid, ChildGUID=child)

        return parent
    else:
        return None

#useful source
#https://docs.djangoproject.com/en/1.11/ref/files/uploads/#module-django.core.files.uploadhandler
def add_file(request):
    count = None
    message = None
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            #get category of uploaded files
            categ = cd['category']
            #if cd['category']:
            #categ = Category.objects.get(categoryID=cd['category'])

            #loop through all uploaded files
            count  = 0
            for f in cd['documents']:
                #location of current file
                #loc = f.temporary_file_path
                loc = f.name

                #check if uploaded file is a zipfile
                #if zipfile.is_zipfile(f):
                    #handlezipfile(f, categ,loc)
                #else:
                try:
                    dagr = handlefile(f.name, categ, f.size, f.content_type,loc)
                    count = count + 1
                except ValidationError as e:
                    message = f.name + " " + e.message
                    return  render(request, 'dagr/add_file.html',{'form':form,'count':count, 'message':message})

        else:
            message = "Invalid input"

    else:
        form = UploadForm()

    return render(request, 'dagr/add_file.html',{'form':form,'count':count, 'message':message})

#useful link
#https://docs.python.org/3/library/zipfile.html#zipinfo-objects
def handlezipfile(f, categ, loc):
    #create parent dagr form parent directory
    parent = handlefile(f.name, categ, f.size, f.content_type, loc)

    #open and get contents of zip file
    with zipfile.ZipFile(f, "r", zipfile.ZIP_STORED) as openzip:
        filelist = openzip.infolist()
        for child_f in filelist:
            #loc is location of current file
            loc =  str(parent.Location) + "/" + str(parent.AssignedName)
            #if zipfile then handle zip file
            if zipfile.is_zipfile(child_f):
                child = handlezipfile(child_f, categ, loc)
            else:
                child = handlefile(child_f.name, categ, child_f.size, child_f.content_type, loc)

            Relationships.create(ParentGUID=parent.Guid, ChildGUID=child, DateCreated=datetime.datetime.now())
    return parent

#creates a dagr from a file
def handlefile(name, category, siz, content_type, location):
    return Dagr.objects.create(AssignedName=name, RealName=name,Location=location, LastModified=datetime.datetime.now(), DateCreated=datetime.datetime.now(), CategoryID=category, Size=siz, Type=content_type)

def update_dagr(request,guid=None):
    message =  None
    dagr = Dagr.objects.get(Guid=guid)
    if dagr:
        if request.method == 'POST':
            form_dagr = DagrForm(request.POST, instance=dagr)
            if form_dagr.is_valid():
                form_dagr.save()
                message = "Updated Successfully"
                return render(request,'dagr/base.html',{'message':message})
            else:
                message = "Invalid Input " + str(form_dagr.errors)
        form_dagr = DagrForm(instance=dagr)
        form_dagr.fields['RealName'].widget.attrs['readonly'] = True
    else:
        return redirect('dagr:metadata')

    str_guid = str(guid)
    return render(request,'dagr/dagr_update.html',{'message':message,'form':form_dagr,'guid':str_guid })

def delete_dagr(request,guid=None):
    guid = Dagr.objects.get(Guid=guid)
    if guid:
        guid.delete()
        m = "Successfully deleted"
    else:
        m = "Object doesn't Exist"

    return render(request,'dagr/base.html',{'message':m})

#processes metadata queries
def metadata(request,results=None):

    if request.method == 'POST':
        metaForm = MetaDataForm(request.POST)
        print(metaForm['date'])
        if metaForm.is_valid():
            cd = metaForm.cleaned_data
            results = Dagr.objects.all()
            if cd['author']:
                results = results.filter(Author=cd['author'])
            if cd['size']:
                results = results.filter(Size=cd['size'])
            if cd['keyword']:
                key = Keyword.objects.get(keywordID=cd['keyword'])
                guids = Dagr_keywords.objects.filter(keyword=key)
                results = results.filter(keywords__in=guids)
            if cd['typ']:
                results = results.filter(Type=cd['typ'])
            if cd['date']:
                print(cd['date'])
                results = results.filter(DateCreated=cd['date'])
            if cd['category']:
                results = results.filter(CategoryID=cd['category'])
            if cd['name']:
                #Q(income__gte=5000) | Q(income__isnull=True)
                results = results.filter(Q(AssignedName__icontains=cd['name']) | Q(RealName__icontains=cd['name']))
                #results = results.filter()
            if cd['location']:
                results = results.filter(Location=cd['location'])

    else:
        metaForm = MetaDataForm()
        results = None
    return render(request,'dagr/query.html', {'form':metaForm,'results':results})

def reach(request):
    results = None
    if request.method == 'POST':
        form = ReachForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            guid = Dagr.objects.get(Guid=cd['dagr_id'])
            results = list()
            if cd['ancestors']:
                results = guid.get_parents(cd['ancestors'])
            if cd['descendants']:
                results2 = guid.get_children(cd['descendants'])
                results.extend(results2)
        else:
            return render(request, 'dagr/base.html', {'message':"Invalid form input"})
    else:
        form = ReachForm()

    return render(request, 'dagr/reach.html', {'form':form,'results':results})

def time_range(request, rang=None):
    midnight_today = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(0,0))
    now = datetime.datetime.now()
    if rang == 'yesterday':
        start_time = midnight_today + dateutil.relativedelta.relativedelta(hours=-24)
        end_time = midnight_today
    elif rang == 'last_week':
        end_time = midnight_today + dateutil.relativedelta.relativedelta(days=-1)
        start_time = end_time + dateutil.relativedelta.relativedelta(days=-7)
    elif rang == 'last_month':
        start_time = midnight_today.replace(day=1) + dateutil.relativedelta.relativedelta(months=-1)
        end_time = midnight_today.replace(day=31)  + dateutil.relativedelta.relativedelta(months=-1)
    elif rang == 'last_year':
        start_time = datetime.datetime.now().replace(month=1,day=1) + dateutil.relativedelta.relativedelta(months=-12)
        end_time = datetime.datetime.now().replace(month=12,day=31) + dateutil.relativedelta.relativedelta(months=-12)
    else:
        results = "No Time Range Chosen"
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()

    #results = Dagr.objects.all()
    #results = Dagr.objects.filter(LastModified__date__lte=end_time.date())
    results = Dagr.objects.filter(LastModified__gte=start_time,LastModified__lte=end_time)
    results = results.order_by('LastModified')

    return render(request, 'dagr/report.html', {'results':results})

def time(request):
    results = None
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            message = "Valid"
            cd = form.cleaned_data
            start_time = cd['from_date']
            end_time = cd['to']

            results = Dagr.objects.filter(LastModified__gte=start_time,LastModified__lte=end_time)

        else:
            message = "Invalid data"
    else:
        form = TimeForm()

    return render(request, "dagr/time_range.html", {'form':form,'results':results })

def descendant(request,descendant=None):
    if descendant == "orphan":
        results = "Orphan"
        query = "SELECT DISTINCT Guid FROM dagr_dagr EXCEPT SELECT DISTINCT ChildGUID_id FROM dagr_Relationships;"
        #query = "SELECT DISTINCT Guid FROM dagr_Dagr MINUS  SELECT UNIQUE(childGUID) FROM dagr_Relationships"
    elif descendant == "sterile":
        results = "Sterile"

        query = "SELECT DISTINCT Guid FROM dagr_dagr EXCEPT SELECT DISTINCT ParentGUID FROM dagr_Relationships;"
    else:
        results = "No Descendants report"

    guids = [result["Guid"] for result in raw_sql(query)]
    results =  Dagr.objects.filter(Guid__in=guids)
    return render(request, 'dagr/report.html', {'results':results})

def raw_sql(sql):
    results = None
    with connection.cursor() as cursor:
        cursor.execute(sql)
        desc = cursor.description
        results =  [dict(zip([col[0] for col in desc],row)) for row in cursor.fetchall()]

    return results

def duplicate_entry(sender, instance,created, **kwargs):
	r = Dagr.objects.filter(Location = instance.Location, RealName =instance.RealName)
	if (len(r) > 1) and created == True:
		raise ValidationError("DAGR not saved: Duplicate entry:")
	else :
		return False

#ignals
models.signals.post_save.connect(duplicate_entry, sender=Dagr)
