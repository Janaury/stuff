#include<stdio.h>

int main(){
    int i;
    int total_num;
    int tmp,count,cn;
    
    while(scanf("%d",&total_num) != EOF){
        count = 0;
        for(i=0;i<total_num;i++){
            scanf("%d",&cn);
            if(count <= 0){
                tmp = cn;
                count = 1;
            }
            if(tmp == cn){
                count++;
            }else{
                count--;
            }
        }
        printf("%d\n", tmp);
    }
}