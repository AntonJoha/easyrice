#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/fcntl.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>

#define EXIT_SUCCESS 0

int main(int argc, char* argv[])
{
	if (argc < 3)
	{
		fprintf(stderr, "Too few arguments");
		_exit(EXIT_FAILURE);
	}
	/*
	if (makeDeamon() != 0)
	{
		fprintf(stderr, "Error with DEAMON\n");
		_exit(EXIT_FAILURE);
	}
	*/
	daemon(0,0);

	char **c = malloc(sizeof(char*)*4);
	c[0] = malloc(sizeof(char)*4);
	strcpy(c[0], "feh");
	c[1] = malloc(12*sizeof(char));
	strcpy(c[1], "--bg-center");
	c[2] = malloc(sizeof(char)* ( 1 + strlen(argv[2])));
	strcpy(c[2], argv[2]);
	fprintf(stderr,"Here");
	while (1)
	 {
	 	int ret = fork();
	 	if (ret == -1)
	 	{
	 		fprintf(stderr, "ERROR forking");
	 		_exit(EXIT_FAILURE);
	 	}
	 	//This is going to stop here so no worries
	 	if (ret == 0)
	 	{
	 		execv("/usr/bin/easyrice", argv);
	 		perror("This shouldn't happen");
	 		_exit(EXIT_FAILURE);
	 	}
	 	wait(0);
	 	ret = fork();
	 	if (ret == -1)
	 	{
	 		fprintf(stderr, "ERROR FORKING");
	 		_exit(EXIT_FAILURE);
	 	}
	 	if (ret == 0)
	 	{
	 		execv("/bin/feh",c);
	 		perror("This shouldn't happen");
	 		_exit(EXIT_FAILURE);
	 	}
	 	wait(0);
	 	fprintf(stderr,"DONE?");
	 	sleep(60);

	 }
}