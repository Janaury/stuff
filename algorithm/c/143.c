#include<stdio.h>

int main()
{
	int p,n,m;
    int result;
	while(1)
	{
		scanf("%d %d %d",&m,&p,&n);
		if(p==0)
		{
			break;
		}
		result = m > p * n ? m : p*n;
        printf("%d\n",result);
	}
    return 0;
}