---
title: "RK3568驱动指南｜第五期-中断-第43章 特殊的软中断tasklet分析实验-CSDN博客"
source: "https://blog.csdn.net/BeiJingXunWei/article/details/133198638"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-09-14
description: "文章浏览阅读298次。在上面的代码中，tasklet_action_common()函数对任务链表中的每个tasklet进行处理。1. 无法处理长时间运行的任务：Tasklet适用于短时间运行的延迟工作，如果需要处理长时间运行的任务，可能会阻塞其他任务的执行。在多核系统中，此循环用于初始化每个CPU的tasklet_vec和tasklet_hi_vec。这种调度机制可以提高系统的效率。"
tags:
  - "clippings"
---
# 备注(声明)：


# 参考文章：
[RK3568驱动指南｜第五期-中断-第43章 特殊的软中断tasklet分析实验-CSDN博客](https://blog.csdn.net/BeiJingXunWei/article/details/133198638)


# 一、特殊的软中断tasklet分析实验

##  特殊的软中断tasklet分析实验
### 1 、轻量级的延迟处理机制


### 2 、软中断处理函数的定义(💌)
- 1 内核源码kernel/kernel/softirq.c文件中
```c
void __init softirq_init(void)
{
    int cpu;
 
    // 初始化每个可能的CPU的tasklet_vec和tasklet_hi_vec
    // 将tail指针设置为对应的head指针的初始位置
    for_each_possible_cpu(cpu) {
        per_cpu(tasklet_vec, cpu).tail =
            &per_cpu(tasklet_vec, cpu).head;
        per_cpu(tasklet_hi_vec, cpu).tail =
            &per_cpu(tasklet_hi_vec, cpu).head;
    }
 
    // 注册TASKLET_SOFTIRQ软中断，并指定对应的处理函数为tasklet_action
    open_softirq(TASKLET_SOFTIRQ, tasklet_action);
 
    // 注册HI_SOFTIRQ软中断，并指定对应的处理函数为tasklet_hi_action
    open_softirq(HI_SOFTIRQ, tasklet_hi_action);
}
```

#### 代码详细解释：
>  for_each_possible_cpu(cpu)：遍历每个可能的CPU。在多核系统中，此循环用于初始化每个CPU的tasklet_vec和tasklet_hi_vec。
> 
> per_cpu(tasklet_vec, cpu).tail = &per_cpu(tasklet_vec, cpu).head;：将每个CPU的tasklet_vec的tail指针设置为对应的head指针的初始位置。这样做是为了确保tasklet_vec的初始状态是空的。
> 
> per_cpu(tasklet_hi_vec, cpu).tail = &per_cpu(tasklet_hi_vec, cpu).head;：将每个CPU的tasklet_hi_vec的tail指针设置为对应的head指针的初始位置。这样做是为了确保tasklet_hi_vec的初始状态是空的。
> 
> open_softirq(TASKLET_SOFTIRQ, tasklet_action);：注册TASKLET_SOFTIRQ软中断，并指定对应的处理函数为tasklet_action。这样，在TASKLET_SOFTIRQ被触发时，将会调用tasklet_action函数来处理相应的任务。
> 
> open_softirq(HI_SOFTIRQ, tasklet_hi_action);：注册HI_SOFTIRQ软中断，并指定对应的处理函数为tasklet_hi_action。这样，在HI_SOFTIRQ被触发时，将会调用tasklet_hi_action函数来处理相应的任务。
> 



### 3 、tasklet_action函数
> 在执行__init **softirq_init函数时，会触发TASKLET_SOFTIRQ，然后会调用tasklet_action函数**

```c
static __latent_entropy void tasklet_action(struct softirq_action *a)
{
	tasklet_action_common(a, this_cpu_ptr(&tasklet_vec), TASKLET_SOFTIRQ);
}
```


### 5、tasklet_action_common函数

> 在上面的代码中，tasklet_action_common()函数**对任务链表中的每个tasklet进行处理**。它首先禁用本地中断，获取任务链表头指针，清空任务链表，并重新设置尾指针。然后它循环遍历任务链表，对每个tasklet进行处理。如果tasklet的锁获取成功，并且计数器为0，它将执行tasklet的处理函数，并清除状态标志位。如果锁获取失败或计数不为0，它将tasklet添加到任务链表的尾部，并触发指定的软中断。最后，它启用本地中断，完成任务处理过程。

```c
static void tasklet_action_common(struct softirq_action *a,
				  struct tasklet_head *tl_head,
				  unsigned int softirq_nr)
{
	struct tasklet_struct *list;
 
	// 禁用本地中断
	local_irq_disable();
	// 获取tasklet_head中的任务链表
	list = tl_head->head;
	// 清空tasklet_head中的任务链表
	tl_head->head = NULL;
	// 将tail指针重新指向head指针的位置
	tl_head->tail = &tl_head->head;
	// 启用本地中断
	local_irq_enable();
 
	// 遍历任务链表，处理每一个tasklet
	while (list) {
		struct tasklet_struct *t = list;
 
		// 获取下一个tasklet，并更新链表
		list = list->next;
 
		if (tasklet_trylock(t)) { // 尝试获取tasklet的锁
			if (!atomic_read(&t->count)) { // 检查count计数器是否为0
				if (!test_and_clear_bit(TASKLET_STATE_SCHED,
							&t->state))
					BUG(); // 如果state标志位不正确，则发生错误
				t->func(t->data); // 执行tasklet的处理函数
				tasklet_unlock(t); // 解锁tasklet
				continue;
			}
			tasklet_unlock(t); // 解锁tasklet
		}
 
		// 禁用本地中断
		local_irq_disable();
		// 将当前tasklet添加到tasklet_head的尾部
		t->next = NULL;
		*tl_head->tail = t;
		// 更新tail指针
		tl_head->tail = &t->next;
		// 触发软中断
		__raise_softirq_irqoff(softirq_nr);
		// 启用本地中断
		local_irq_enable();
	}
}
```

### 6、`__tasklet_schedule_common()`: 将tasklet加入到链表(💌)

> 通过上述代码，`__tasklet_schedule_common()`函数将tasklet**成功添加到链表的末尾**。**当软中断被触发时，系统会遍历链表并处理每个tasklet**。因此，在添加到链表后，tasklet将在适当的时机被系统调度和执行。



```c
static void __tasklet_schedule_common(struct tasklet_struct *t,
				      struct tasklet_head __percpu *headp,
				      unsigned int softirq_nr)
{
	struct tasklet_head *head;
	unsigned long flags;
 
	// 保存当前中断状态，并禁用本地中断
	local_irq_save(flags);
	// 获取当前CPU的tasklet_head指针
	head = this_cpu_ptr(headp);
	// 将当前tasklet添加到tasklet_head的尾部
	t->next = NULL;
	*head->tail = t;
	// 更新tasklet_head的尾指针
	head->tail = &(t->next);
	// 触发指定的软中断
	raise_softirq_irqoff(softirq_nr);
	// 恢复中断状态
	local_irq_restore(flags);
}
```


### 7、所以说tasklet是一个特殊的软中断


### 8、



## Tasklet相比自己添加软中断有一些优点和缺点
### 1 、优点：
> 1. `简化的接口和编程模型`：Tasklet提供了一个简单的接口和编程模型，使得在内核中处理延迟工作变得更加容易。相比自己添加软中断，Tasklet提供了更高级的抽象。
> 2. `低延迟`：Tasklet在软中断上下文中执行，避免了内核线程的上下文切换开销，因此具有较低的延迟。这对于需要快速响应的延迟敏感任务非常重要。
> 3. `自适应调度`：Tasklet具有自适应调度的特性，当多个Tasklet处于等待状态时，内核会合并它们以减少不必要的上下文切换。这种调度机制可以提高系统的效率。

### 2 、缺点：
> 1. 无法处理长时间运行的任务：Tasklet**适用于短时间运行的延迟工作**，如果需要处理长时间运行的任务，可能会阻塞其他任务的执行。**对于较长的操作，可能需要使用工作队列或内核线程来处理。**
> 2. 缺乏灵活性：Tasklet的执行受限于软中断的上下文，不适用于所有类型的延迟工作。某些情况下，可能需要更灵活的调度和执行机制，这时自定义软中断可能更加适合。
> 3. 资源限制：Tasklet的数量是有限的，系统中可用的Tasklet数量取决于架构和内核配置。如果需要大量的延迟工作处理，可能会受到Tasklet数量的限制。




### 3 、综上所述(💌)
> Tasklet提供了一种简单且低延迟的延迟工作处理机制，**适用于短时间运行的任务和对响应时间敏感的场景**。
然而，**对于长时间运行的任务和需要更灵活调度的情况，自定义软中断可能更合适**。在选择使用Tasklet还是自定义软中断时，需要根据具体的需求和系统特性进行权衡和决策。



### 4 、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、




# 二、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、




## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 三、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 四、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


# 五、

## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、


