#include <iostream>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <vector>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

using namespace std;

// Function to handle client connections and gameplay
void handleClient(int clientSocket)
{
    // Generate random numbers L and R
    srand(time(0));
    int L = rand() % 90001 + 10000;               // L: 10^4 <= L <= 10^5
    int R = (L + 10 ^ 4) + rand() % (190001 - L); // R: L + 10^4 <= R <= 2*10^5
    int X = L + rand() % (R - L + 1);             // Random number in [L, R]

    // Send L and R to client
    write(clientSocket, &L, sizeof(int));
    write(clientSocket, &R, sizeof(int));

    // Game loop
    while (true)
    {
        int guess;
        read(clientSocket, &guess, sizeof(int));
        if (guess > X)
        {
            cout << "Too High" << endl;
            write(clientSocket, "Too High", sizeof("Too High"));
        }
        else if (guess < X)
        {
            cout << "Too Low" << endl;
            write(clientSocket, "Too Low", sizeof("Too Low"));
        }
        else
        {
            cout << "Correct Guess! Prisoner escaped." << endl;
            write(clientSocket, "Correct Guess", sizeof("Correct Guess"));
            close(clientSocket);
            return;
        }
    }
}

int main()
{
    // Server setup
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(8080);
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
    listen(serverSocket, 5);

    // Accept connections
    while (true)
    {
        int clientSocket = accept(serverSocket, NULL, NULL);
        thread clientThread(handleClient,clientSocket);
        clientThread.detach();
    }

    close(serverSocket);
    return 0;
}
