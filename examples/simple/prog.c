#include <stdlib.h>
#include <stdio.h>
int main(int argc, char **argv){

  int a = atoi(argv[1]);
  int b = atoi(argv[2]);
  int c = atoi(argv[3]);
  
  if (a && b) {
    printf("L1\n");
  }

  if (b || c) {
    printf("L2\n");
  }

  if (!a) {
    printf("L3\n");
  }

  printf("L4\n");
  
  return 0;
}

