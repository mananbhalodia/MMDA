import zipfile

def handlezipfile(zipf):
    with zipfile.ZipFile(zipf, "r", zipfile.ZIP_STORED) as openzip:
		filelist = openzip.infolist()
		for f in filelist:
            #usefule link
            #https://docs.python.org/3/library/zipfile.html#zipinfo-objects
            name = f.filename
            LastModified = f.date_time #may not return datetime in correct format.
            size = f.file_size

            if f.is_dir():
                typ = 'dir'
