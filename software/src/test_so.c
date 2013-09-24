#include <stdio.h>
#include "pifwrap.h"

int main(void) {
  char buff[200];
  puts("This is a shared library test for pif...");

  pifVersion(buff, sizeof(buff));
  printf("%s\n", buff);

  return 0;
  }
