---
title: "Linux驱动开发笔记（十二）并发与竞争_linux 驱动里面多线程吗?-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139864168?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1k次，点赞36次，收藏11次。Linux的子系统我们已经大致学习完了，笔者最近相到似乎一直没有好好学习一下并发和竞争这一部分内容（在网络编程中曾经简单提到过Linux应用开发笔记（五）网络编程（二）多线程编程。_linux 驱动里面多线程吗?"
tags:
  - "clippings"
---
---

## 前言

Linux 的子系统我们已经大致学习完了，笔者最近相到似乎一直没有好好学习一下并发和竞争这一部分内容（在 [网络编程](https://so.csdn.net/so/search?q=%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B&spm=1001.2101.3001.7020) 中曾经简单提到过 [Linux应用开发笔记（五）网络编程（二）多线程编程](https://blog.csdn.net/sincerelover/article/details/137463670?spm=1001.2014.3001.5501) ）。

---

## 一、并发与竞争的引入

### 1.1 并发

  以下图为例，我们的CPU在同时处理多个任务的时候也可能采取类似“分时复用”的手法，即在不同的工作时间块内切换执行的任务，使得在实际效果上好像认为是这些任务是在同时运行的，这种操作方法我们称为并发。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/33b950895c02d5c05069bdde60f51ac1.png)  
  通常情况下，通过并发执行多个任务，可以充分利用多核处理器， **提高程序的执行效率** ， **减少资源的闲置时间** 。

### 1.2 竞争

  在并发的过程中，经常产生不同的程序共享一个资源的情况，这种行为既可以减少资源但也会产生抢占的问题，这种情况我们称之为竞争。

### 1.3 解决方法

  其实竞争的产生可以理解为是多个线程或进程需要访问和修改相同的资源（如全局变量、文件、数据库等），且没有适当的同步机制。那么如何解决这个问题呢？在Linux中提供了 **原子操作、自旋锁、互斥锁、信号量** 等同步机制。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bfb327b9eac08bcd1e48c1acf4e6cf41.png)

## 二、原子操作

### 2.1 概念

  原子操作是一种不可分割的操作，确保在多线程或多进程环境下，该操作可以在没有中断的情况下完成。原子操作在执行过程中不会被其他线程或进程打断，确保了数据的一致性和正确性。  
  在 并发编程 中，多个线程或进程可能会同时访问和修改共享数据。普通的读写操作可能会引发竞争条件（Race Condition），导致数据不一致。原子操作提供了一种机制，确保共享数据的修改是安全的，即使在高度并发的环境中。  
  在 [Linux内核](https://so.csdn.net/so/search?q=Linux%E5%86%85%E6%A0%B8&spm=1001.2101.3001.7020) 中使用 atomic\_t和atomic64\_t结构体分别来完成32位系统和64位系统的整形数据原子操作，两个结构体定义在“内核源码/include/linux/types.h”文件中，具体定义如下：

```c
typedef struct {
     int counter;
 } atomic_t;
 
 #ifdef CONFIG_64BIT
 typedef struct {
     long counter;
} atomic64_t;
 #endif
123456789
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/77311f04efa4befa9dbc5f90a1c28200.png#pic_center)  
**注：这是64位系统的函数集，如果是32位只需要将函数名中的64删去即可。**

### 2.2 使用方法

  我们可以使用以下代码定义一个64位系统的原子整型变量，其实细心的读者可能会发现我们在之前中断实验的时候已经使用过这种方式了，当时为了防止持续进入中断 函数 导致计数出错。

```c
static atomic64_t v = ATOMIC_INIT(1);//初始化原子类型变量v,并设置为1
1
```

  之后我们便可以根据对原子量进行赋值来定义不同的状态，从而告诉cpu这个资源已经占用，例如：

```c
//本次的所有实验均为拒绝重复打开驱动 
static int open(struct inode *inode,struct file *file)
{
    //判断是否是重复进入
    if(atomic64_read(&v) != 1){
        return -EBUSY;
        printk("\t This process has opened! \n");
    }
    
    //第一次进入，将v的值设置为0
    atomic64_set(&v,0);
    return 0;
}

static int release_test(struct inode *inode,struct file *file)
{
    atomic64_set(&v,1);//将原子类型变量v的值赋1
    return 0;
}
12345678910111213141516171819
```

## 三、自旋锁

### 3.1 概念

  自旋锁（spin lock）是一种非阻塞锁，也就是说，如果某线程需要获取锁，但该锁已经被其他线程占用时，该线程不会被挂起，而是在不断的消耗CPU的时间，不停的试图获取锁。如果在自旋完成后前面锁定同步资源的线程已经释放了锁，那么该线程便不必阻塞，并且直接获取同步资源，从而避免切换线程的开销。

```c
//表示自旋锁
typedef struct spinlock {
    union {
        struct raw_spinlock rlock;

#ifdef CONFIG_DEBUG_LOCK_ALLOC
# define LOCK_PADSIZE (offsetof(struct raw_spinlock, dep_map))
        struct {
            u8 __padding[LOCK_PADSIZE];
            struct lockdep_map dep_map;
        };
#endif
     };
} spinlock_t;
1234567891011121314
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9859faabd987c18946c7590b9d8db844.png#pic_center)  
  上图是自旋锁的相关API，一般来说我们使用这些函数就足够了，下图是中断的自旋锁API，这里仅进行补充。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/34c1061c5fa938622457fa2e514da766.png#pic_center)  
**注：为了保险起见，我们通常选择使用spin\_lock\_irqsave进行自旋锁获取。**

### 3.2 使用方法

代码如下（示例）：

```c
//定义spinlock_t类型的自旋锁变量spinlock_test
static spinlock_t spinlock_test;

//定义全局变量flag，flag等于1表示设备没有被打开，等于0则证明设备已经被打开了
static int flag = 1;

static int open(struct inode *inode,struct file *file)
{
    //自旋锁加锁
    spin_lock(&spinlock_test);
    
    if(flag != 1){
    spin_unlock(&spinlock_test);//自旋锁解锁
    return -EBUSY;
     }
     
    flag = 0;
    //自旋锁解锁
    spin_unlock(&spinlock_test);
    return 0;
}

static int release_test(struct inode *inode,struct file *file)
{
    spin_lock(&spinlock_test);//自旋锁加锁
    flag = 1;
    spin_unlock(&spinlock_test);//自旋锁解锁
    return 0;
}

static int __init init(void)
{
    //初始化自旋锁
    spin_lock_init(&spinlock_test);
      ...
}

12345678910111213141516171819202122232425262728293031323334353637
```

### 3.3 自旋锁死锁

  自旋锁死锁是指两个或多个事物在同一资源上相互占用，并请求锁定对方的资源，从而导致恶性循环的现象。当多个进程因竞争资源而造成的一种僵局（互相等待），若无外力作用，这些进程都将无法向前推进，这种情况就是死锁。自旋锁死锁发生存在两种情况：  
（1）拥有自旋锁的进程A在内核态阻塞了，内核调度B进程，碰巧B进程也要获得自旋锁，此时B只能自旋转。而此时抢占已经关闭(在单核条件下)不会调度A进程了，B永远自旋，产生死锁。  
  相应的解决办法是，在自旋锁的使用过程中要尽可能短的时间内拥有自旋锁，而且不能在临界区中调用导致线程休眠的函数。  
（2）进程A拥有自旋锁，中断到来，CPU执行中断函数，中断处理函数，中断处理函数需要获得自旋锁，访问共享资源，此时无法获得锁，只能自旋，从而产生死锁。  
  对于中断引发的死锁，最好的解决方法就是在获取锁之前关闭本地中断，由于Linux内核运行是非常复杂的，很难确定某个时刻的中断状态，因此建议使用 spin\_lock\_irqsave/spin\_unlock\_irqrestore，因为这一组函数会保存中断状态，在释放锁的时候会恢复中断状态。

## 四、信号量

### 4.1 概念

  信号量是操作系统中最典型的用于同步和互斥的手段，本质上是一个全局变量，信号量的值表示控制访问资源的线程数，可以根据实际情况来自行设置，如果在初始化的时候将信号量量值设置为 **大于1** ，那么这个信号量就是计数型信号量， **允许多个线程同时访问共享资源** ；如果将信号量量值设置 **为1** ，那么这个信号量就是二值信号量， **同一时间内只允许一个线程访问共享资源** ；信号量的 **值不能小于0** ，当信号量的值 **为0时，想访问共享资源的线程必须等待** ，直到信号量大于0时，等待的线程才可以访问。

```c
//表示一个信号量
 struct semaphore {
     raw_spinlock_t      lock;
     unsigned int        count;
     struct list_head    wait_list;
 };
123456
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1f0462818749373a35e38aaed27842b0.png)  
  **当访问共享资源时，信号量执行“减1”操作，访问完成后再执行“加1”操作，这里的down函数可以理解为减1操作，up函数可以理解为加1操作。**

### 4.2 使用方法

代码如下（示例）：

```c
//定义一个semaphore类型的结构体变量semaphore_test
struct semaphore semaphore_test;

static int open(struct inode *inode,struct file *file)
{
    //信号量数量减1
    down(&semaphore_test);
    return 0;
}

static int release_test(struct inode *inode,struct file *file)
{
    //信号量数量加1
    up(&semaphore_test);
    return 0;
}

static int __init init(void)
{
    //初始化信号量结构体semaphore_test，并设置信号量的数量为1
    sema_init(&semaphore_test,1);
      ...
}

123456789101112131415161718192021222324
```

## 五、互斥锁

### 5.1 概念

  互斥锁为资源引入一个状态：锁定或者非锁定。某个线程要更改共享数据时，先将其锁定，此时资源的状态为“锁定”，其他线程不能更改；直到该线程释放资源，将资源的状态变成“非锁定”，其他的线程才能再次锁定该资源。互斥锁和信号量功能相同，但具体的实现方式是不同的，此外使用互斥锁效率更高、更简洁，所以如果使用到的信号量“量值”为 1，一般将其修改为使用互斥锁实现。

```c
struct mutex {
     atomic_long_t       owner;
     spinlock_t      wait_lock;
 #ifdef CONFIG_MUTEX_SPIN_ON_OWNER
     struct optimistic_spin_queue osq; /* Spinner MCS lock */
 #endif
     struct list_head    wait_list;
 #ifdef CONFIG_DEBUG_MUTEXES
     void            *magic;
 #endif
 #ifdef CONFIG_DEBUG_LOCK_ALLOC
     struct lockdep_map  dep_map;
 #endif
 };
1234567891011121314
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9cb5ed6afa9815c84610ea297152eaaa.png)

### 5.2 使用方法

代码如下（示例）：

```c
//定义mutex类型的互斥锁结构体变量mutex_test
struct mutex mutex_test;

static int open(struct inode *inode,struct file *file)
{
    //互斥锁加锁
    mutex_lock(&mutex_test);
    return 0;
}

static int release_test(struct inode *inode,struct file *file)
{
    //互斥锁解锁
    mutex_unlock(&mutex_test);
    return 0;
}

static int __init init(void)
{
    //对互斥体进行初始化
    mutex_init(&mutex_test);
      ...
}
1234567891011121314151617181920212223
```

---

**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139864168

作者主页：https://blog.csdn.net/sincerelover

实付 元

[使用余额支付](https://blog.csdn.net/sincerelover/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部