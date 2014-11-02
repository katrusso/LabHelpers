
CODEDIR = ../code
TESTDIR = ./
CLOUDDIR = ../cloud_git
SOURCES = $(CODEDIR)/webpages/*.py  \
	$(CODEDIR)/classes/*.py \
	$(CODEDIR)/html/html_constants.py 
APPFILE = $(CODEDIR)/webpages/app.yaml #There should only be one 
HTMLFILES = $(CODEDIR)/helloworld/index.html
SYTLEDIRS = $(CODEDIR)/webpages/stylesheets
BACKUPDIR = ../backup

all: copy

copy:
	cp $(SOURCES) .
	cp $(APPFILE) .
	cp $(HTMLFILES) .
	cp -R $(SYTLEDIRS) .
appengine:
	$(GOOGLEPATH) ./
backup:
	cp $(SOURCES) $(BACKUPDIR)
	cp $(APPFILE) $(BACKUPDIR)
	cp $(HTMLFILES) $(BACKUPDIR)
	cp -R $(SYTLEDIRS) $(BACKUPDIR)

backupengine:
	$(GOOGLEPATH) $(BACKUPDIR)

clean:
	rm *.py*
	rm app.yaml
	rm *.html
	rm -R stylesheets

cloudgit:
	gcloud init lab-helpers-546
	mv lab-helpers-546 $(CLOUDDIR)

cloudpush:
	cp -R $(CODEDIR) $(TESTDIR) $(CLOUDDIR)
