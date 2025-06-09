#include <iostream>

using namespace std;

int power(int base, int pow){
    if (pow == 0) return 1;
    if(pow == 1) return base;
    if (pow%2==0) {
        int a = power(base, pow/2);
        return a*a;
    }
    int a = power(base, (pow - 1) / 2);
    return base * a * a;
}

int main(){
    int n=4;       
    int ver = power();
    cout << ver << endl;
    cout << 4*ver*(n-1) << endl;
}