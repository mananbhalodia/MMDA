from django import forms
from .models import Dagr, Category, Keyword
from multiupload.fields import MultiFileField
from datetimewidget.widgets import DateTimeWidget


dateTimeOptions = {
    'format': 'yyyy-mm-dd HH:ii',
    'autoclose': True,
    'showMeridian' : False
    }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryID', 'categoryName']
        labels = {
            'categoryName':'Create Category'
        }

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['keywordID', 'name']
        labels = {
            'name':'Create Keyword'
        }

class DagrForm(forms.ModelForm):
    class Meta:
        model = Dagr
        fields = ['Guid','Location','RealName','AssignedName',
         'Size', 'Type','CategoryID','Author','LastModified', 'DateCreated',]
        widgets = {
        'LastModified':DateTimeWidget(options=dateTimeOptions),
        'DateCreated':DateTimeWidget(options=dateTimeOptions),
        'Location': forms.TextInput(attrs={'class':'form-control'}),
        'RealName':  forms.TextInput(attrs={'class':'form-control'}),
        "AssignedName":  forms.TextInput(attrs={'class':'form-control'}),
        "Size": forms.NumberInput(attrs={'class':'form-control'}),
        "Type":  forms.TextInput(attrs={'class':'form-control'}),
        "Category": forms.Select(attrs={'class':'form-control'}),
        "Author":  forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
        'LastModified': 'Date Last Modified',
        'DateCreated': 'Date Created',
        'CategoryID': 'Category',
        'RealName': 'Real Name',
        'AssignedName': 'Assigned Name',
        }

        def __init__(self, *args, **kwargs):
            # first call parent's constructor
            super(DagrForm, self).__init__(*args, **kwargs)
            # there's a `fields` property now
            self.fields['Location'].required = False
            self.fields['RealName'].required = False
            self.fields['LastModified'].required = False
            self.fields['CategoryID'].required = False
            self.fields['AssignedName'].required = False
            self.fields['Size'].required = False
            self.fields['Type'].required = False
            self.fields['DateCreated'].required = False
            self.fields['Author'].required = False

class HtmlParserForm(forms.Form):
    url =  forms.URLField(label="Enter Wesbite URL", max_length=300,
    widget=forms.TextInput(attrs={'class':'form-control'}))
    #depth = forms.IntegerField(label="Depth", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

class UploadForm(forms.Form):
    documents = MultiFileField(min_num=1, max_num=100, max_file_size=1024000*1024000*500)
    categorys = Category.objects.all()
    category = forms.ModelChoiceField(queryset=categorys,label="Category",required=False,
    widget=forms.Select(attrs={'class':'form-control'}))

class MetaDataForm(forms.Form):
    author = forms.CharField(label="Author",required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    size = forms.DecimalField(label="Size",required=False,  widget=forms.NumberInput(attrs={'class':'form-control'}))
    typ = forms.CharField(label="Type",required=False,  widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(label="Name", required=False,  widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(label="Location", required=False,  widget=forms.TextInput(attrs={'class':'form-control'}))

    categorys = Category.objects.all()
    category = forms.ModelMultipleChoiceField(queryset=categorys,label="Category",required=False,
    widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    keywords = Keyword.objects.all()
    keyword = forms.ModelMultipleChoiceField(queryset =keywords ,label="Keyword",required=False,
    widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    date = forms.DateTimeField(label="Date",required=False, widget=DateTimeWidget(options=dateTimeOptions))

class ReachForm(forms.Form):
    dagrs = Dagr.objects.all()
    dagr_id = forms.ModelMultipleChoiceField(queryset=dagrs,label="Choose DAGR ID",required=True,
    widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    ancestors = forms.IntegerField(label="Choose Depth Ancestors", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    descendants = forms.IntegerField(label="Choose Depth Descendants", required=False, widget=forms.TextInput(attrs={'class':'form-control'}))


class TimeForm(forms.Form):
    from_date = forms.DateTimeField(label="From Date", widget=DateTimeWidget(options=dateTimeOptions))
    to = forms.DateTimeField(label="To Date", widget=DateTimeWidget(options=dateTimeOptions))
