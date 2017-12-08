from django.db import models
from django.urls import reverse


class Category(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(unique=True,max_length=100)

    class Meta:
        ordering = ('categoryName','categoryID')

    def __str__(self):
        return self.categoryName

# Create your models here.
class Dagr(models.Model):
    Guid = models.AutoField(primary_key=True)

    #location, realname, last modified will together serve as a candidate key
    #which will help in identifying duplicate content
    Location = models.CharField(max_length=300)
    RealName = models.CharField(max_length=200)     #dagr real name
    AssignedName = models.CharField(max_length=300)     #user assigned name
    LastModified = models.DateTimeField()   #last time file was modified
    DateCreated = models.DateTimeField()    #date file was created

    CategoryID = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dagrs')
    Size = models.DecimalField(max_digits=20, decimal_places=4)   #memory size of file
    Type = models.CharField(max_length=300)      #type of file e.g pdf, html, doc

    Author = models.CharField(default="N/A", max_length=200)  #name of user who created file

    class Meta:
        ordering = ('AssignedName','Type','Author')

    def __str__(self):
        return self.AssignedName

    # Down command. Gets all children recursively until n = 0 is reached. n is the
    # number of levels down to go. Stores and returns the GUID of all children and the root.
    def get_children(self, n, include_self=True):
        r = []
        if n < 0:
            return r
        else:
            if include_self:
                r.append(self)
            for c in Relationships.objects.filter(ParentGUID=self.Guid):
                dagr = c.ChildGUID
                #Dagr.objects.get(Guid=c.ChildGUID.Guid)
                r_ = dagr.get_children(n-1,include_self=True)
                if 0 < len(r_):
                    r.extend(r_)

        return r

    # Up command. Gets all parents recursively until n = 0 is reached. n is the
    # number of levels up to go. Stores and returns the GUID of all parents and the root.
    def get_parents(self, n, include_self=True):
        r = []
        if n < 0 :
            return r
        else :
            if include_self:
                r.append(self)
            for c in Relationships.objects.filter(ChildGUID=self):
                dagr = Dagr.objects.get(Guid=c.ParentGUID)
                r_ = dagr.get_parents(n-1, include_self=True)
                if 0 < len(r_):
                    r.extend(r_)
        return r

    def get_absolute_url(self):
        return reverse('dagr:update_dagr', args=[self.Guid])

#models captures the relationship between files
class Relationships(models.Model):
    ParentGUID =  models.IntegerField()
    ChildGUID = models.ForeignKey(Dagr, on_delete=models.CASCADE, related_name='children')
    DateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ParentGUID',)
        unique_together = (('ParentGUID','ChildGUID'),)

    def __str__(self):
        return ( str(self.ParentGUID) + str(self.ChildGUID))

class Keyword(models.Model):
    keywordID = models.AutoField(primary_key=True)
    name = models.CharField(unique=True,blank=True,max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Dagr_keywords(models.Model):
    GUID = models.ForeignKey(Dagr, on_delete=models.CASCADE, related_name='keywords')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="dagrs")

    def __str__(self):
        return str(self.GUID) + str(self.keyword)

    class Meta:
        ordering = ('keyword',)
