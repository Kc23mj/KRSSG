
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>

int main() {
	


	//create a socket
	int network_socket; //socket descriptor
	network_socket = socket(AF_INET, SOCK_STREAM, 0);     // (domain, type, protocol)	    

	


	//specify an address for the socket
	struct sockaddr_in server_address;
	server_address.sin_family = AF_INET;
	server_address.sin_port = htons(9003); //htons used to convert the port no. to another format
	server_address.sin_addr.s_addr = INADDR_ANY;

	


	//checking connection status
	int connection_status = connect(network_socket, (struct sockaddr *)&server_address, sizeof(server_address));
	//check for error in the connection
	if(connection_status == -1){
		printf("Error in connection with the server!!\n\n");
	}


        
        //receive data from server
        char server_response[256];
        recv(network_socket, &server_response, sizeof(server_response), 0);

        printf("Server response is: %s\n\n", server_response);
       
   
       
       //close the connection
       close(network_socket);

	return 0;
}

