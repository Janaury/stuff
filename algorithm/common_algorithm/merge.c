#include<stdio.h>


void merge(int* arr1, int size1, int* arr2, int size2, int* result_arr) {
    int i = 0,j = 0,k = 0;

    while (i < size1 && j < size2) {
        if (arr1[i] < arr2[j]) {
            result_arr[k++] = arr1[i++];
        } else {
            result_arr[k++] = arr2[j++];
        }
    }
    while (i < size1) {
        result_arr[k++] = arr1[i++];
    }

    while (j < size2) {
        result_arr[k++] = arr2[j++];
    }
}

int main(){
    int i;
    int a[] = {1,3,5,7,9};
    int b[] = {2,4,6,8,10};
    int big[10];
    merge(a, 5, b, 5, big);
    for(i=0;i<10;i++) {
        printf("%d ",big[i]);
    }
    printf("\n");
    return 0;
}
