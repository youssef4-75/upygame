#include <iostream>

using namespace std;

int power(int base, int pow){
    if (pow == 0) return 1;
    if(pow == 1) return base;
    if (pow%2==0) return power(base, pow/2)**2;
    return po;

}

int main(){
    int n;
    cin >> n;        
    int ver = power(3, n - 2);
    cout << 4*ver*(n-1) << endl;
}