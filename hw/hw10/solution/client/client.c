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
#define MAX_RESPONSE 600

int main(int argc, char *argv[]) {
	
	char hostname[20];
	int portnum;
	int rc;
	char nice[20];
	int niceBool = 0;
	
	//check that the hostname and port number are properly entered as command line arguments
	if (argc == 3 || argc == 4) {
		strcpy(hostname, argv[1]);
		for (int i = 0; argv[2][i] != '\0'; i++) {
			if (!isdigit(argv[2][i])) {
				printf("Error: port must be an integer number\n");
				exit(-1);
			}
		}
		portnum = atoi(argv[2]);
		if (argc==4){
			strcpy(nice, argv[3]);
			if(strcmp(nice, "-nice")!=0){
				printf("Error: make sure optional fourth argument is -nice\n");
				exit(-1);
			} 
			niceBool = 1;
		}
	} else {
		printf("Usage: ./client hostname portnumber {-nice}\n");
		exit(-2);
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

	//variables to store sent and received messages
	char response[MAX_RESPONSE];
	char msg[MAX_MSG_LEN];
	char temp[MAX_MSG_LEN];
	//for listmore functionality
	char list[MAX_MSG_LEN] = "nicelist, ";
	char *rest;
	int loop;
	
	//variables for determining if input message has proper number of fields
	char *token;
	const char *delim = ", ";
	int count;
	
	while(1) {
		#include <unistd.h>
		sleep(1);
		//printf("STARTING LOOP\n");

		//get input from user
		printf("Waiting for message (stat, date, time, {filter})/more/exit:\n");	
		memset(msg, 0, MAX_MSG_LEN);
		while (fgets(msg, MAX_MSG_LEN, stdin) == NULL);
		//remove trailing newline
		char *temp = strchr(msg, '\n');
		if (temp != 0) *temp = '\0';


		if (strcmp(msg, "exit") == 0) {
			zmq_send(requester, msg, strlen(msg), 0);
			exit(0);
		}

		//check if input is valid (valid # of args/csv type format)
		char buffer[BUFSIZ];
		memset(buffer, 0, BUFSIZ);
		if ((strcmp(msg, "more") != 0)) {
			//use strtok to see how many fields were entered seperated by commas (proper format)
			strcpy(buffer, msg);
			token = strtok(buffer, delim);
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
		

		//for bbf, batch cmd of listmore to execute list and subsequent amount of mores
		if (strncmp(msg, "listmore", strlen("listmore")) == 0) {
			rest = msg + 10;
			strcat(list, rest);
			//first call list & see how many records match
			if (zmq_send(requester, list, strlen(list), 0) == -1) {
				printf("Failed to send message\n");
				continue;
			}
			memset(response, 0, MAX_RESPONSE);
			if (zmq_recv(requester, response, MAX_RESPONSE, 0) == -1) {
				printf("Failed to receive response\n");
				continue;
			}
			printf("%s\n",response);
			rest = response + 9;
			loop = atoi(rest);
			//call more corresponding to amt of records found in list
			//printf("%d records to loop\n", atoi(rest));
			for (int i = 0; i < loop; i++) {
				//printf("looping\n");
				if (zmq_send(requester, "nicemore", strlen("nicemore"), 0) == -1) {
					printf("Failed to send message\n");
					continue;
				}
				memset(response, 0, MAX_RESPONSE);
				if (zmq_recv(requester, response, MAX_RESPONSE, 0) == -1) {
					printf("Failed to receive response\n");
					continue;
				}
				printf("%s\n",response);
			}
			continue;	
		}

		//if nice envoked, prepend "nice" to send to python server
		if (niceBool) {
			strcpy(temp, msg);
			strcpy(msg, "nice");
			strcat(msg, temp);
		}

		//send to python via ZMQ
		printf("Sending message: %s\n", msg);		
		if (zmq_send(requester, msg, strlen(msg), 0) == -1) {
			printf("Failed to send message\n");
			continue;
		}
	
		//wait for response and then display it
		memset(response, 0, MAX_RESPONSE);
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
