all: rsp.h cmd.h

%.h: %.py
	python3.6 $< > $@

clean:
	rm -f rsp.h cmd.h
