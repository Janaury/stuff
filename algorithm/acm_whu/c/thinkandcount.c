#include<stdio.h>

typedef struct info{
    int height;
    int width;
}Info;

char board[2000][2005];
int sw_line[2000][2005];
int rm,cm;
Info stack[2005];

void statistic(){
    int i,j;
    int count = 0;
    for(i=0;i<rm;i++){
        count = 0;
        for(j=cm-1;j>-1;j--){
            if(board[i][j] == 'w'){
                count++;
            }else{
                count = 0;
            }
            sw_line[i][j] = count;
        }
    }
}

long long countFrom(int col){
    int i;
    long long total = 0;
    long long add = 0;
    int height = 0;
    int s = 0;
    for(i=0;i<rm;i++){
        height = 1;
        while(sw_line[i][col] < stack[s].width){
            add -= stack[s].width * stack[s].height;
            height += stack[s].height;
            s--;
        }
        add += height * sw_line[i][col];
        total += add;
        s++;
        stack[s].height = height;
        stack[s].width = sw_line[i][col];
    }
    return total;
}

int main(){
    int i;
    long long count = 0;
    stack[0].height = 0;
    stack[0].width = 0;
    while(scanf("%d%d",&rm,&cm) != EOF){
        count = 0;
        for(i=0;i<rm;i++){
            scanf("%s",board[i]);
        }
        statistic();
        for(i=0;i<cm;i++){
            count += countFrom(i);
        }
        printf("%lld\n",count);
    }

}
