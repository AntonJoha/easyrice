prog: install

config: 
	mkdir -p ~/.config/easyrice
	cp example_config ~/.config/easyrice/config
	cp example_commands ~/.config/easyrice/commands

install: a.out
	ln -s $(CURDIR)/a.out /usr/bin/easyrice_deamon
	ln -s $(CURDIR)/Start.py /usr/bin/easyrice

a.out: deamon.c
	gcc deamon.c -Wall -Werror
remove:
	rm -rf ~/.config/easyrice
	rm -f /usr/bin/easyrice
	rm -f /usr/bin/easyrice_deamon
