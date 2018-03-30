# MyLinuxC
专门存放学习Linux中遇到的著名算法
* [信号量](#信号量)  

# 信号量

1、多个进程要有一个东西来统一控制，那么一定在内核那里，有一个东东管着。
```
a、我们称之为信号量。
b、怎么获取这个东东呢，内核肯定有一套统一的标准。
c、P是荷兰语，Proberen，测试，表示-1
d、V是荷兰语，Verhogen，增量，表示+1
```
2、既然在内核中总应该提供一套标准、接口让我们去使用这个信号量吧？
```
int semget(key_t key, int num_sems, int semm_flags);  //获取或创建信号量
int semop(int sem_id, struct sembuf *sem_opa, size_t num_sem_ops); //操作信号量的value
int semctl(int sem_id, int sem_num, int command, …); //操作信号量本身
```
3、我们看多进程竞争stdout输出的例子：
```
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/sem.h>

int main(int argc, char *argv[])
{
    char message = 'X';
    int i = 0;
    if (argc > 1)
    {
        message = argv[1][0];
    }

    for (i = 0; i < 10; ++i)
    {
        printf("%c", message);
        fflush(stdout);
        sleep(rand() % 3);
        printf("%c", message);
        fflush(stdout);
        sleep(rand() % 2);
    }
    sleep(10);
    printf("\n%d - finished\n", getpid());

    exit(EXIT_SUCCESS);
}
```
输出：
```
(myapp_venv) ➜  myApp git:(v1.8_dev) ✗ gcc -o haha Dijkstra_1965_no_PV.c -lm
(myapp_venv) ➜  myApp git:(v1.8_dev) ✗ ./haha O & ./haha
[1] 76470
OXOXXOXXOOXOXXXOOOXOOOXXOOOOXXXXOXOXOXOX
```
发现输出特别乱，一会X，一会O，并不能让X和O分别成对出现。  
怎么解决呢？
```
(myapp_venv) ➜  myApp git:(v1.8_dev) ✗ gcc -o lala Dijkstra_1965_PV.c -lm
(myapp_venv) ➜  myApp git:(v1.8_dev) ✗ ./lala O & ./lala
[1] 76875
XXOOXXXXXXXXOOOOOOOO
76876 - finished
```
很好，这下子stdout资源在PV控制下有序输出。