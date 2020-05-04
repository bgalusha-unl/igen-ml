#include <stdlib.h>
#include <stdio.h>
int main(int argc, char **argv){

	int a = atoi(argv[1]);
	int b = atoi(argv[2]);
	int c = atoi(argv[3]);
	int d = atoi(argv[4]);
	int e = atoi(argv[5]);
	int f = atoi(argv[6]);
	int g = atoi(argv[7]);
	int h = atoi(argv[8]);
	int i = atoi(argv[9]);
	int j = atoi(argv[10]);
	int k = atoi(argv[11]);
	int l = atoi(argv[12]);
	int m = atoi(argv[13]);
	int n = atoi(argv[14]);
	int o = atoi(argv[15]);
	int p = atoi(argv[16]);
	
	printf("L1\n");

	if (a) {
		printf("L2\n");
	}
	if (a && p) {
		printf("L3\n");
	}
	if (a && b && c && d && e && f && g && h && i && j && k && l && m && n && o && p) {
		printf("L4\n");
	}

	if (a || b || c || d || e || f || g) {
		printf("L5\n");
	}

	if (k && l || m && n || o && p) {
		printf("L6\n");
	}

	if (!h && !k) {
		printf("L7\n");
	}

	return 0;
}
  


