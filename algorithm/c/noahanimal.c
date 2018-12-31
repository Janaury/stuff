#include<stdio.h>
#include<string.h>

int main(){
    int i,j;
    int tmp1,tmp2;
    int spt[100001];
    int space[100],point[100];
    int animal_num, total_space;
    int total_points;
    while(scanf("%d",&animal_num) != EOF){
        for(i=0;i<animal_num;i++){
            scanf("%d%d",&space[i],&point[i]);
        }
        scanf("%d",&total_space);
        memset(spt, 0, sizeof(spt));
        for(i=0;i<animal_num;i++){
            for(j=total_space;j>=0;j--){
                if(j >= space[i]){
                	tmp1 = spt[j];
                	tmp2 = spt[j - space[i]] + point[i];
                    spt[j] = tmp1 > tmp2? tmp1 : tmp2;
                }
            }
        }
        total_points = spt[total_space];
        printf("%d\n",total_points);
    }
    return 0;
}