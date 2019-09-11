#include<stdio.h>
#define N 1000010

int a[N][4];

int main()
{
	int i=0;
    int n;
	a[2][0]=1;
	a[2][1]=1;
	a[2][2]=1;
	a[2][3]=2;
	a[1][3]=1;

	for(i=3;i<N;i++)
	{
		a[i][0]=a[i-1][3];
		a[i][1]=(a[i-1][0]+a[i-1][2])%10000;
		a[i][2]=(a[i-1][0]+a[i-1][1])%10000;
		a[i][3]=(a[i-1][0]+a[i-1][1]+a[i-1][2]+a[i-1][3])%10000;
	}
	
	while(scanf("%d",&n)==1)
	{
		printf("%d\n",a[n][3]);
	}
	return 0;
}