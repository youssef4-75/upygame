#include <iostream>

using namespace std;


int main(){
    int n;       
    cin >> n;
    int ver = power(4, n-1);
    cout << ver << endl;
    cout << ver*(n-1) << endl;
}