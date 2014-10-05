GOOGLEPATH=~/google-cloud-sdk/bin/dev_appserver.py
SOURCES=../code/helloworld/guestbook.py
APPFILE=../code/helloworld/app.yaml 

all: copy

copy:
	cp $(SOURCES) .
	cp $(APPFILE) .
appengine:
	$(GOOGLEPATH) ./
clean:
	rm *.py*
	rm *.yaml
