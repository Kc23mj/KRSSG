#include <iostream>
#include <unistd.h>
#include <thread>
using namespace std;
void nterminal(){

	pid_t pid = fork();

	if(pid == 0){
		execl("/usr/bin/x-terminal-emulator", "x-terminal-emulator", "-e", "./client", NULL);
	
	}
	else if(pid > 0) {
		cout << "Output generated in a new terminal"<<endl;
	}

	else{
		cerr << "Failed to fork a new process."<< endl;
		
	}

	
}

int main(){

        for(int i = 0; i < 4; i++){
	thread t(nterminal);
	t.detach();
	}

	 sleep(2);
	 cout << "All shown simultaneously!!" << endl;
	return 0;
}
