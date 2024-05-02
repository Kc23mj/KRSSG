#include <iostream>
#include <thread>
#include <vector>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

// Function to handle communication with a single client
void handleClient(int clientSocket) {
    char buffer[1024];
    int bytesRead;

    // Receive data from client
    while ((bytesRead = recv(clientSocket, buffer, sizeof(buffer), 0)) > 0) {
        // Process received data (You can replace this with your application logic)
        buffer[bytesRead] = '\0';
        std::cout << "Received from client: " << buffer << std::endl;

        // Echo back to client
        send(clientSocket, buffer, bytesRead, 0);
    }

    // Close socket when communication is done
    close(clientSocket);
}

int main() {
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);

    // Create socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        std::cerr << "Error creating socket" << std::endl;
        return 1;
    }

    // Bind socket to port
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(12345); // Choose your desired port number
    if (bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Error binding socket" << std::endl;
        return 1;
    }

    // Listen for incoming connections
    if (listen(serverSocket, 5) < 0) {
        std::cerr << "Error listening" << std::endl;
        return 1;
    }

    std::cout << "Server listening on port 12345" << std::endl;

    // Accept and handle incoming connections in separate threads
    while (true) {
        // Accept connection
        clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &clientAddrLen);
        if (clientSocket < 0) {
            std::cerr << "Error accepting connection" << std::endl;
            continue;
        }

        // Handle communication with client in a separate thread
        thread clientThread([int clientSocket](){
            handleClient(clientSocket);
        });
        clientThread.detach(); // Detach the thread to allow it to run independently
    }

    // Close server socket
    close(serverSocket);

    return 0;
}

