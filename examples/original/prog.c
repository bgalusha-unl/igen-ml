#include <stdlib.h>
#include <stdio.h>
int main(int argc, char **argv){

  int a = atoi(argv[1]);
  int b = atoi(argv[2]);
  int c = atoi(argv[3]);
  
  if (a && b) {
    if (c > 1) {
      printf("L1\n");
    }
  }
  else {
    printf("L2\n");
  } 

  printf("L3\n");
  
  if (a || c) {
    printf("L4\n"); 
    if (b) {
	 printf("L5\n");
    }
  }

  return 0;
}
  


