#include <iostream>

void workload()
{
    for (volatile int i = 0; i < 100000000; ++i)
        ; // Busy loop
}

int main()
{
    workload();
    return 0;
}
