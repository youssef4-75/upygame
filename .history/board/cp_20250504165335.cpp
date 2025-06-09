#include <iostream>

using namespace std;

int power(int base, int pow){
    if (pow == 0) return 1;
    if(pow == 1) return base;
    if (pow%2==0) {
        return power(base, pow/2)2;
    }
    return base*power(base, (pow-1)/2)^2;
}

int main(){
    int n=4;       
    int ver = 4*2;
    cout << ver << endl;
    cout << 4*ver*(n-1) << endl;
}