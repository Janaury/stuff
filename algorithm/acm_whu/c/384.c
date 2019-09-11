#include<stdio.h>

int main(){
    int n,i;
    long long int a,b;
    scanf("%d",&n);
    for(i=0;i<n;i++){
        scanf("%lld%lld",&a,&b);
        printf("Case #%d: %lld\n",i+1,(a+b)*(b-a+1)/2);
    }
    return 0;
}