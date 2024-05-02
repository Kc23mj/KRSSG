#include <iostream>

void printPlusTen(int num) {
    // Lambda expression capturing 'num' by value and adding 10 to it
    auto addTen = [num]() {
        int result = num + 10;
        std::cout << "Result: " << result << std::endl;
    };

    // Calling the lambda function
    addTen();
}

int main() {
    int number = 5;
    printPlusTen(number);
    return 0;
}

