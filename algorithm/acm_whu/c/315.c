//有限域的大整数乘方
#include<stdio.h>

typedef long long int ll;

ll powerMod(ll base, ll index, ll mod){
    int i;
    ll result, next;
    if(base == 0 || base == 1){
        return base;
    }else{
        result = 1;
        next = base;
    }
    while(index != 0){
        if(index & 1 != 0){
            result = result * next % mod;
        }
        index >>= 1;
        next = next * next % mod;   
    }
    return result;
}


int main(){
    ll a,b,c;
    for(;;){
        scanf("%lld%lld%lld",&a,&b,&c);
        if(a == 0 && b == 0 && c == 0){
            break;
        }
        printf("%lld\n",powerMod(a,b,c));
    }
    return 0;
}