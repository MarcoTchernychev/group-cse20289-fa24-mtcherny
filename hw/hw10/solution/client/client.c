//client.c
//Alicia Melotik
//amelotik@nd.edu
//Marco Tchernychev
//mtcherny@nd.edu

#include <zmq.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_MSG_LEN 64 
#define MAX_REPONSE 600

int main(int argc, char *argv[]) {
	
	char hostname[20];
	int portnum;
	int rc;
	
	//check that the hostname and port number are properly entered as command line arguments
	if (argc == 3) {
		strcpy(hostname, argv[1]);
		for (int i = 0; argv[2][i] != '\0'; i++) {
			if (!isdigit(argv[2][i])) {
				printf("Error: port must be an integer number\n");
				exit(-1);
			}
		}
		portnum = atoi(argv[2]);
	}
	
	//connect to port via zmq
	printf("Connecting to server on port %d\n", portnum);
	void *context = zmq_ctx_new();
	void *requester = zmq_socket(context, ZMQ_REQ);
	char pszRequest[25];
	sprintf(pszRequest, "tcp://%s:%d", hostname, portnum);
	rc = zmq_connect(requester, pszRequest);

	//check return code to see if connection to port was successful
	if (rc == 0) 
		printf("\tSuccessfully connected on port %d\n", portnum);
	else {
		printf("\tNetwork connection failed\n");
		exit(-1);
	}

	//variables to store 
	char response[MAX_RESPONSE];
	char msg[MAX_MSG_LEN];
	
	//variables for
	char *token;
	char temp[MAX_MSG_LEN];
	const char *delim = ", ";
	int count;
	
	while(1) {
		//get input from user
		printf("Waiting for message (stat, date, time, {filter})/more/exit:\n");	
		fgets(msg, MAX_MSG_LEN, stdin);
		//remove trailing newline
		msg[strlen(msg)-1] = '\0';

		if (strcmp(msg, "exit") == 0) {
			zmq_send(requester, msg, strlen(msg), 0);
			exit(0);
		}

		//check if input is valid (valid # of args/csv type format)
		if ((strcmp(msg, "more") != 0)) {
			//use strtok to see how many fields were entered seperated by commas (proper format)
			strcpy(temp, msg);
			token = strtok(temp, delim);
			count = 0;
			while (token != NULL) {
				token = strtok(NULL, delim);
				count++;
			}
			if ((count != 3) && (count != 4)) {
				printf("Message formatted incorrectly\n");
				continue;
			}
		}

		//send to python via ZMQ
		printf("Sending message: %s\n", msg);		
		if (zmq_send(requester, msg, strlen(msg), 0) == -1) {
			printf("Failed to send message\n");
			continue;
		}
	
		//wait for response and then display it
		memset(response, 0, MAX_MSG_LEN);
		if (zmq_recv(requester, response, MAX_RESPONSE, 0) == -1) {
			printf("Failed to receive response\n");
			continue;
		}
		printf("Received: %s\n", response);	
	
	}

	zmq_close(requester);
	zmq_ctx_destroy(context);
	return 0;
}
