#include<stdio.h>

int modPower(int base, int exponent, int mod){
    int total = 1;

    while(exponent != 0){
        if (exponent & 0x1 == 1) {
            total = (total * base) % mod;
        }
        base = (base * base) % mod; 
        exponent >>= 1;
    }

    return total;
}

int main(){
    int base, exponent, mod;
    printf("please input base, exponent and mod: ");
    scanf("%d%d%d", &base, &exponent, &mod);
    printf("the result is: %d\n", modPower(base, exponent, mod));
    return 0;

}
