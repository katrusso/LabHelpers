CODEDIR = ../code
TESTDIR = ./
SOURCES = $(CODEDIR)/webpages/*.py  \
	$(CODEDIR)/classes/*.py \
	$(CODEDIR)/admin/*.py \
	$(CODEDIR)/html/html_constants.py 
IMAGES = $(CODEDIR)/webpages/images/* 
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
	cp $(IMAGES) stylesheets
appengine:
	dev_appserver.py ./
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
