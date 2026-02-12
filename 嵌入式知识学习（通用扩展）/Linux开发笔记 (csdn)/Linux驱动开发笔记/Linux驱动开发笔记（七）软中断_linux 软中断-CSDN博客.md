---
title: "Linux驱动开发笔记（七）软中断_linux 软中断-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139506557?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.1k次，点赞14次，收藏23次。前节我们已经进行了外部中断的学习，这部分进行进阶内容——软中断。在Linux内核中，tasklet是一种特殊的软中断机制，被广泛用于处理中断下文相关的任务。它是一种常见且有效的方法，在多核处理系统上可以避免并发问题。Tasklet绑定的函数在同一时间只能在一个CPU上运行，因此不会出现并发冲突。然而，需要注意的是，tasklet绑定的函数中不能调用可能导致休眠的函数，否则可能引起内核异常。//初始化一个 work_struct 结构体，并指定工作函数。_linux 软中断"
tags:
  - "clippings"
---
---

## 前言

  前节我们已经进行了 [外部中断](https://so.csdn.net/so/search?q=%E5%A4%96%E9%83%A8%E4%B8%AD%E6%96%AD&spm=1001.2101.3001.7020) 的学习，这部分进行进阶内容——软中断。

## 一、软中断

  软中断是利用 [硬件中断](https://so.csdn.net/so/search?q=%E7%A1%AC%E4%BB%B6%E4%B8%AD%E6%96%AD&spm=1001.2101.3001.7020) 的概念，用 软件 方式进行模拟，实现宏观上的异步执行效果。很多情况下，软中断和"信号"有些类似，同时，软中断又是和硬中断相对应的，“硬中断是外部设备对CPU的中断”，“软中断通常是硬中断服务程序对内核的中断”，“信号则是由内核(或其他进程)对某个进程的中断”。软中断是一组静态定义的下半部接口，可以在所有处理器上同时执行，即使两个类型相同也可以。但一个软中断不会抢占另一个软中断，唯一可以抢占软中断的是硬中断。

### 1\. 两部分模型引入

  在 Linux 内核中，中断处理是一个复杂的过程，特别是在高负载的系统中，中断处理需要尽可能地高效和快速。为了提高中断处理的效率，Linux内核引入了中断处理的两部分模型——“上半部”和“下半部”的概念。

#### 1.1 上半部（Top Half）

- 作用：主要负责快速地响应硬件中断，确认中断发生，保存中断相关的硬件信息，然后调度执行下半部处理。
- 特点：运行在中断上下文，通常不会进行耗时的操作，而是快速标记并准备好数据。
- 执行环境：直接在硬件中断发生时执行，通常在一个预先定义好的中断处理函数中。

#### 1.2 下半部（Bottom Half）

- 作用：处理上半部不能或者不宜完成的工作，比如耗时较长的I/O操作、内存分配等。
- 特点：可以延迟执行，不运行在中断上下文，可以睡眠，可以并发执行。
- 执行环境：可以是软中断、tasklet、工作队列等。

#### 1.3 为什么需要上半部和下半部

- 效率：上半部只负责快速响应和准备数据，而将耗时的操作放到下半部去处理，避免中断处理程序占用过长时间。
- 并发性：下半部可以在系统其他部分运行时并发执行，提高了系统的并发性。
- 可移植性：将中断处理分解为两部分，使得内核更加模块化，提高了代码
- 的可移植性。

### 2\. 软中断相关数据结构

#### 2.1 softirq\_vec变量

&emspl; 在软中断申请 函数 open\_softirq( )中只有一个赋值语句， 其重点是softirq\_vec变量，在内核源码中找到这个变量如下所示：

```c
//软中断“中断向量表”
static struct softirq_action softirq_vec[NR_SOFTIRQS]
12
```

  这是一个长度为NR\_SOFTIRQS的softirq\_action类型数组，长度NR\_SOFTIRQS在软中断的“中断编号”枚举类型中有定义， 长度为10。这个数组是一个全局的数组，作用等同于硬中断的中断向量表，以下是对这些软中断类型的简要说明：

- HI\_SOFTIRQ (高优先级软中断):
	- 通常用于需要尽快处理的高优先级任务。
	- 由于其高优先级，它会优先于其他软中断类型执行。
- TIMER\_SOFTIRQ (定时器软中断):
	- 与系统定时器相关，例如内核定时器或POSIX定时器。
	- 负责处理到期的定时器回调。
- NET\_TX\_SOFTIRQ (网络传输发送软中断):
	- 负责处理网络数据包的发送。
	- 当数据包准备好发送时，此软中断会被触发。
- NET\_RX\_SOFTIRQ (网络传输接收软中断):
	- 负责处理网络数据包的接收。
	- 当网络接口接收到数据包时，此软中断会被触发。
- BLOCK\_SOFTIRQ (块设备软中断):
	- 与块设备（如硬盘）的I/O操作相关。
	- 当块设备操作完成（如读取或写入）时，此软中断会被触发。
- IRQ\_POLL\_SOFTIRQ (中断轮询软中断):
	- 用于中断轮询机制。
	- 当需要模拟中断行为（如某些虚拟化环境）时，此软中断可能会被使用。
- TASKLET\_SOFTIRQ (任务软中断):
	- 通常用于执行一些不太紧急但需要异步执行的任务。
	- 它是旧式的软中断类型，现在已经被workqueue所替代。
- SCHED\_SOFTIRQ (调度软中断):
	- 与内核调度器相关。
	- 当进程状态发生变化（如变为可运行状态）时，此软中断可能会被触发。
- HRTIMER\_SOFTIRQ (高精度定时器软中断):
	- 尽管你提到它是未使用的，但在某些Linux内核版本中，它用于处理高精度定时器事件。
- RCU\_SOFTIRQ (RCU软中断):
	- RCU（Read-Copy Update）是一种同步机制，允许读者和写者并发访问共享数据。
	- RCU软中断通常用于RCU机制的清理工作。
- NR\_SOFTIRQS:
	- 这是一个宏，表示软中断类型的总数。
	- 它用于索引和遍历软中断数组。

  以上这些用于标识软中断的不同类型或优先级，每个枚举常量对应一个特定的软中断类型。

#### 2.2 softirq\_action结构体

```c
//软中断结构体
struct softirq_action
{
    void    (*action)(struct softirq_action *);
};
12345
```

  它只有一个参数，就是注册软中断函数的参数open\_softirq。至此我们知道数组softirq\_vec就是软中断的中断向量表， 所谓的注册软中断函数就是根据中断号将中断服务函数的地址写入softirq\_vec数组的对应位置。

### 3\. 相关API函数

```c
//注册软中断
void open_softirq(int nr, void (*action)(struct softirq_action *))
{
    softirq_vec[nr].action = action;
}
12345
```
- 参数：
	- nr：用于指定要“注册”的软中断中断编号
	- action：指定软中断的中断服务函数
- 返回值：无
```c
//触发软中断
void raise_softirq(unsigned int nr);
12
```
- 参数：
	- nr：指定要触发的软中断
- 返回值：无
```c
//在禁用硬件中断的情况下，触发软中断使用raise_softirq_irqoff函数
void raise_softirq_irqoff(unsigned int nr);
12
```
- 参数：
	- nr: 软中断的编号或优先级。它是一个整数，表示要注册的软中断的标识符。
- 返回值：无

## 二、tasklet

### 1\. tasklet的定义

  在Linux内核中，tasklet是一种特殊的软中断机制，被广泛用于处理中断下文相关的任务。它是一种常见且有效的方法，在多核处理系统上可以避免并发问题。Tasklet绑定的函数在同一时间只能在一个CPU上运行，因此不会出现并发冲突。然而，需要注意的是，tasklet绑定的函数中不能调用可能导致休眠的函数，否则可能引起内核异常。

### 2\. 相关数据结构

  tasklet\_struct 结构体定义了 tasklet 的基本属性，它们被用于创建、管理和执行 tasklet。在编写 Linux 内核模块时，可以通过操作 struct tasklet\_struct 结构体来创建和管理自定义的 tasklet。

```c
struct tasklet_struct
{
    struct tasklet_struct *next;
    unsigned long state;
    atomic_t count;
    void (*func)(unsigned long);
    unsigned long data;
};
12345678
```
- 成员的解释：
	- next：指向下一个 tasklet 的指针。Linux 内核使用一个链表来管理所有的 tasklet，这个成员用于将 tasklet 连接到链表中的下一个元素。
	- state：表示 tasklet 的状态。在 Linux 内核中，tasklet 有三种状态：TASKLET\_STATE\_SCHED（已调度）、TASKLET\_STATE\_RUN（正在执行）和 TASKLET\_STATE\_DISABLED（已禁用）。这个状态字段用于记录 tasklet 当前的状态。
	- count：表示 tasklet 的引用计数。引用计数用于确保 tasklet 在执行期间不会被销毁。当 tasklet 被触发时，引用计数会增加，当 tasklet 执行完成时，引用计数会减少只有当引用计数归零时，tasklet 才能被销毁。
	- fun：指向 tasklet 处理函数的指针。当 tasklet 被触发时，这个函数会被调用以执行任务。这个函数接受一个 unsigned long 类型的参数，通常用于传递一些数据给 tasklet 处理函数。
	- data;：用于传递给 tasklet 处理函数的参数。这个参数在 tasklet 被触发时会传递给处理函数。

### 3\. 相关API函数

#### 3.1 softirq\_init( )

  在 Linux 内核 源代码 中，softirq\_init() 函数通常位于 kernel /softirq.c 文件中。该函数在系统启动时被调用，以确保软中断系统在运行时能够正常工作。

```c
/*
  1.分配软中断向量的空间。
  2.初始化活动向量和挂起向量。
  3.初始化软中断计数器。
  4.设置每个 CPU 的软中断向量指针。
  5.如果是多处理器系统（SMP），则设置 irq_balance
 软中断，并启动 IRQ 平衡例程。
*/
void __init softirq_init(void);
123456789
```

**注: 通常情况下我们不需要直接修改或者操作该函数，它是 Linux 内核初始化过程中的一部分。**

#### 3.2 tasklet\_init( )

```c
//根据设置的参数填充tasklet_struct结构体结构体
void tasklet_init(struct tasklet_struct *t,
  void (*func)(unsigned long), unsigned long data)
{
    t->next = NULL;
    t->state = 0;
    atomic_set(&t->count, 0);
    t->func = func;
    t->data = data;
}
12345678910
```
- 参数：
	- t：指定要初始化的tasklet\_struct结构体
	- func：指定tasklet处理函数，等同于中断中的中断服务函数
	- data：指定tasklet处理函数的参数。
- 返回值：无

#### 3.3 tasklet\_schedule( )

  和软中断一样，需要一个触发函数触发tasklet，函数定义如下所示：

```c
static inline void tasklet_schedule(struct tasklet_struct *t)
{
    if (!test_and_set_bit(TASKLET_STATE_SCHED, &t->state))
            __tasklet_schedule(t);
}
12345
```
- 参数：
	- t：tasklet\_struct结构体。
- 返回值：无

### 4\. 软中断的设计框架

1. 出入口函数的编写，即module\_init和module\_exti，这部分主要用来进行字符设备的申请注册及卸载。
- 在module\_init中主要alloc\_chrdev\_region(内存申请)、cdev\_init(字符设备的申请)，cdev\_add(字符设备的添加)、class\_create(类的创建)、device\_create(设备的创建)。
- 在module\_exti中主要包括device\_destroy(设备删除)、class\_destroy(清除类)、cdev\_del(清除设备号)、unregister\_chrdev\_region(取消注册字符设备)
1. 相关openrations函数的编写  
	 这部分内容包括open、release、write、read函数，这里我们主要进行open函数的介绍：首先，利用of\_find\_node\_by\_path函数获取按键设备树节点；再利用of\_get\_named\_gpio获取按键使用的GPIO；用gpio\_reques申请GPIO并通过gpio\_direction\_input设置引脚方向；使用irq\_of\_parse\_and\_map获取中断号并初始tasklet\_init。
2. 编写中断函数并在合适的位置使用tasklet\_schedule进行软中断的调度。
3. 编写tasklet\_hander函数，进行中断下文的设计。
```c
/*以下内容是tasklet的示例框架*/

#include <linux/interrupt.h>  
#include <linux/tasklet.h>  
    
/* tasklet 的处理函数 */  
static void tasklet_func(unsigned long data)  
{  
    printk(KERN_INFO "Tasklet is running...\n");  
    /* 在这里执行你的 tasklet 处理逻辑 */  
}  
  
/* 声明一个 tasklet */  
static struct tasklet_struct my_tasklet;  
  
/* 模块初始化函数 */  
static int __init tasklet_module_init(void)  
{  
    /*........省略.........*/
    printk(KERN_INFO "Tasklet module loaded\n"); 
    /*调度tasklet_init函数*/
    tasklet_init(&my_tasklet, tasklet_func, (unsigned long)NULL); 
    /*调度tasklet_schedule函数*/
    tasklet_schedule(&my_tasklet); //一般来说这部分是放置在中断服务程序中的  
    return 0;  
}  
  
/* 模块退出函数 */  
static void __exit tasklet_module_exit(void)  
{  
    printk(KERN_INFO "Tasklet module unloaded\n");  
    /* .........省略........... */  
}  
  
module_init(tasklet_module_init);  
module_exit(tasklet_module_exit);  
MODULE_LICENSE("GPL");
12345678910111213141516171819202122232425262728293031323334353637
```

## 三、 工作队列机制

  工作队列通常由一个队列结构和一个后台线程组成。中断处理程序将任务添加到队列中，后台线程负责处理队列中的任务。这种方式可以避免在中断上下文中执行耗时的操作，保持系统的响应 性能 。

| 名称 | 执行方式 | 特点 | 适用范围 |
| --- | --- | --- | --- |
| 软中断 | 同步 | 任务会立即执行，避免执行耗时操作 | 用于需要快速响应并且执行时间较短的任务 |
| Tasklet | 同步 | 更高的优先级 | 处理需要快速响应但不需要立即执行的任务 |
| 工作队列 | 异步 | 较为通用的机制，可以处理各种类型的延迟任务 | 适合执行较长的、可能会阻塞的任务 |

### 1\. work\_struct结构体

  “工作队列”中的大部分内容由内核帮我们完成， 我们只需要定义一个具体的工作、初始化工作即可，在驱动中一个工作结构体代表一个工作，工作结构体如下所示：

```c
struct work_struct {
    atomic_long_t data;
    struct list_head entry;
    work_func_t func;
};
12345
```
- 成员的解释：
	- data：用于传递工作函数的参数。通常，工作函数会使用这个字段来获取执行所需的参数。
	- entry：用于将 work\_struct 结构体链接到工作队列中。这是一个 list\_head 类型的字段，它允许将多个工作组织成一个链表。
	- func：指向工作函数的指针。工作函数是实际执行工作的函数，当工作队列中的工作被执行时，这个函数会被调用。

### 2\. INIT\_WORK宏定义

  内核提初始化宏定义如下所示：

```c
//初始化一个 work_struct 结构体，并指定工作函数。
#define INIT_WORK(_work, _func)
12
```

  该宏共有两个参数，\_work用于指定要初始化的工作结构体，\_func用于指定工作的处理函数。

  驱动工作函数执行后相应内核线程将会执行工作结构体指定的处理函数，驱动函数如下所示。

### 3\. schedule\_work( )

```c
//启动工作函数
static inline bool schedule_work(struct work_struct *work)
{
    return queue_work(system_wq, work);
}
12345
```

**注：这部分的程序与tasklet相似，只需要更改相关的初始化、fun函数和启动函数（schedule），其他的均可直接使用。**

---

**免责声明：本文参考了野火的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139506557

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