# MyLinuxC
专门存放学习Linux中遇到的著名算法
* [信号量](#信号量)  
* [银行家算法](#银行家算法)  

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

# 银行家算法


思想：
```
你借出去的钱，也算是自己的钱。
如果你手上的钱能满足借你钱的那个人的资金需求，那么它的钱就连本带利还给你。  
```

以下来自维基百科：假设四个进程。  
```
Available：系统当前拥有的资源。  
Allocation：进程已经拥有的资源。  
Max：进程需要的资源。 
 

 Allocation　　　Max　　　Available
 　　ＡＢＣＤ　　ＡＢＣＤ　　ＡＢＣＤ
 P1　００１４　　０６５６　　１５２０　
 P2　１４３２　　１９４２　
 P3　１３５４　　１３５６
 P4　１０００　　１７５０
```
计算出四个进程的Need资源：
```
 NEED
 ＡＢＣＤ
 ０６４２　
 ０５１０
 ０００２
 ０７５０
```
四个进程的处理结果初始化：
```
 FINISH
 false
 false
 false
 false
```
接下来找出need比available小的(千万不能把它当成4位数 他是4个不同的数)
```
   NEED　　Available
 ＡＢＣＤ　　ＡＢＣＤ
 ０６４２　　１５２０
 ０５１０<-
 ０００２
 ０７５０
```
P2的需求小于能用的，所以配置给他再回收
```
  NEED　　Available
 ＡＢＣＤ　　ＡＢＣＤ
 ０６４２　　１５２０
 ００００　＋１４３２
 ０００２－－－－－－－
 ０７５０　　２９５２
 ```
此时P2 FINISH的false要改成true(己完成)
```
 FINISH
 false
 true
 false
 false
 ```
接下来继续往下找，发现P3的需求为0002，小于能用的2952，所以资源配置给他再回收
```
 　NEED　　Available
 ＡＢＣＤ　　Ａ　Ｂ　Ｃ　Ｄ
 ０６４２　　２　９　５　２
 ００００　＋１　３　５　４
 ００００－－－－－－－－－－
 ０７５０　　３　12　10　6
 ```
同样的将P3的false改成true
```
 FINISH
 false
 true
 true
 false
 ```
依此类推，做完P4→P1，当全部的FINISH都变成true时，就是安全状态。  


代码结果：
```
(chanzai_data_venv) ➜  MyLinuxC git:(master) ✗ python Dijkstra_1965_banker.py
比较，need=[7, 4, 3], Available=[3, 3, 2]
比较不通过，跳过...
比较，need=[1, 2, 2], Available=[3, 3, 2]
比较通过，资源回归..
回归后, Available=[5, 3, 2]
比较，need=[6, 0, 0], Available=[5, 3, 2]
比较不通过，跳过...
比较，need=[0, 1, 1], Available=[5, 3, 2]
比较通过，资源回归..
回归后, Available=[7, 4, 3]
比较，need=[4, 3, 1], Available=[7, 4, 3]
比较通过，资源回归..
回归后, Available=[7, 4, 5]
比较，need=[7, 4, 3], Available=[7, 4, 5]
比较通过，资源回归..
回归后, Available=[7, 5, 5]
比较，need=[6, 0, 0], Available=[7, 5, 5]
比较通过，资源回归..
回归后, Available=[10, 5, 7]
检查通过
正确的任务顺序： [1, 3, 4, 0, 2]
(chanzai_data_venv) ➜  MyLinuxC git:(master) ✗ 

```
