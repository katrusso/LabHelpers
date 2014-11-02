
CODEDIR = ../code
TESTDIR = ./
CLOUDDIR = ../cloud_git
SOURCES = $(CODEDIR)/webpages/*.py  \
	$(CODEDIR)/classes/*.py \
	$(CODEDIR)/admin/*.py \
	$(CODEDIR)/html/html_constants.py 
APPFILE = $(CODEDIR)/webpages/app.yaml #There should only be one 
HTMLFILES = $(CODEDIR)/helloworld/index.html
SYTLEDIRS = $(CODEDIR)/webpages/stylesheets
BACKUPDIR = ../backup
TESTBACKUPDIR = ../testingbackup

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
	
testbackup:
	cp -R . $(TESTBACKUPDIR)

backupengine:
	$(GOOGLEPATH) $(BACKUPDIR)

clean:
	find . -not \( -name 'test*py' -or -name 'Makefile' \) -delete
cloudgit:
	gcloud init lab-helpers-546
	mv lab-helpers-546 $(CLOUDDIR)

cloudpush:
	cp -R $(CODEDIR) $(TESTDIR) $(CLOUDDIR)
