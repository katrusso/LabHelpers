GOOGLEPATH = ~/google-cloud-sdk/bin/dev_appserver.py
CODEDIR = ../code
TESTDIR = ./
CLOUDDIR = ../cloud_git
SOURCES = $(CODEDIR)/helloworld/guestbook.py \
	$(CODEDIR)/webpages/*.py 
	#$(CODEDIR)/webpages/mainpage.py \
	#$(CODEDIR)/webpages/labpages.py \
	#$(CODEDIR)/webpages/meow.py
APPFILE = $(CODEDIR)/webpages/app.yaml #There should only be one 
HTMLFILES = $(CODEDIR)/helloworld/index.html
SYTLEDIRS = $(CODEDIR)/helloworld/stylesheets
BACKUPDIR = ../backup

all: copy

copy:
	cp $(SOURCES) .
	cp $(APPFILE) .
	cp $(HTMLFILES) .
	cp $(SYTLEDIRS) . -r 
appengine:
	$(GOOGLEPATH) ./
backup:
	cp $(SOURCES) $(BACKUPDIR)
	cp $(APPFILE) $(BACKUPDIR)
	cp $(HTMLFILES) $(BACKUPDIR)
	cp $(SYTLEDIRS) $(BACKUPDIR) -r 

backupengine:
	$(GOOGLEPATH) $(BACKUPDIR)

clean:
	rm *.py*
	rm *.yaml
	rm *.html
	rm stylesheets -r

cloudgit:
	gcloud init lab-helpers-546
	mv lab-helpers-546 $(CLOUDDIR)

cloudpush:
	cp -r $(CODEDIR) $(TESTDIR) $(CLOUDDIR)
