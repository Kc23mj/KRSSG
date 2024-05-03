
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

using namespace std;

int main() {
    // Connect to server
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(8080);
    serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));

    // Receive L and R from server
    int L, R;
    read(clientSocket, &L, sizeof(int));
    read(clientSocket, &R, sizeof(int));

    // Game loop
    while (true) {
        int guess = rand() % (R - L + 1) + L;
        write(clientSocket, &guess, sizeof(int));
        char serverResponse[1024];
        read(clientSocket, &serverResponse, sizeof(serverResponse));
        cout << "Server: " << serverResponse << endl;
        if (strcmp(serverResponse, "Correct Guess") == 0) {
                int i;
		read(clientSocket, &i, sizeof(int));
		char str1[] = "Client ";int z = 0;
		while(str1[z] != '\0') z++;
		char n = '0' + i;
		str1[z++] = n; str1[z] = '\0';
		char str2[] = " is excaped!!";
                char clientResponse[1024];
		strcpy(clientResponse, str1);
		strcat(clientResponse, str2);
		write(clientSocket, &clientResponse, sizeof(clientResponse));
	       	cout << "You escaped!" << endl;
            break;
        }
    }


    // Close socket
    close(clientSocket);
sleep(2);
return 0;
}


