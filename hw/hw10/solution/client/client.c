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

#define MAX_MSG_LEN 256

int main(int argc, char *argv[]) {
	
	char *hostname;
	int portnum;
	int rc;
	if (argc == 1) && (strcmp(argv[1], "exit") == 0) {
		//exit on python server then here

		exit(0);
	} else if (argc == 3) {//ADD CORRECT ARG #
		strcpy(hostname, argv[1]);
		if (isdigit(argv[2])) {
			portnum = atoi(argv[2]);
		} else { //incorrect second arg for port number
			
		}	
	}
	
	//connect to port via zmq
	printf("Connecting to server on port %d\n", portnum);
	void *context = zmq_ctx_new();
	void *requester = zmq_socket(context, ZMQ_REQ);
	char pszRequest[25];
	sprintf(pszRequest, "tcp://%s:%d", hostname, portnum);
	rc = zmq_connect(requester, pszRequest);

	if (rc == 0) 
		printf("\tSuccessfully connected on port %d\n", portnum);
	else {
		printf("\tNetwork connection failed\n");
		exit(-1);
	}

	char response[MAX_MSG_LEN];
	char msg[MAX_MSG_LEN];
	
	char *token;
	const char *delim = ", ";
	int count = 1;
	
	while(1) {
		//get input from user
		printf("Waiting for message (stat, date, time, filter)/list/more:\n");	
		fgets(msg, MAX_MSG_LEN, stdin);
		//remove trailing newline
		msg[strlen(msg)-1] = "\0";

		//check if input is valid (valid # of args/csv type format)
		if (strcmp(msg, "list") != 0) && (strcmp(msg, "more") != 0) {
			//use strtok to see how many fields were entered seperated by commas (proper format)
			token = strtok(msg, delim);
			while (token != NULL) {
				token = strtok(NULL, delim);
				count++;
			}
			if (count != 4) {
				printf("Message formatted incorrectly"
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
		if (zmq_recv(requester, response, 20, 0) == -1) {
			printf("Failed to receive response\n");
			continue;
		}
		printf("Recieved: %s\n", response);	
	
	}

	zmq_close(requester);
	zmq_ctx_destroy(context);
	return 0;
}
