---
title: "Linux驱动开发笔记（十五）块设备驱动_块设备驱动框架-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139948013?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1k次，点赞35次，收藏28次。字符设备的学习我们暂时告一段落了，这部分内容我们主要进行块设备驱动的学习。_块设备驱动框架"
tags:
  - "clippings"
---
---

## 前言

  字符设备的学习我们暂时告一段落了，这部分内容我们主要进行块 [设备驱动](https://so.csdn.net/so/search?q=%E8%AE%BE%E5%A4%87%E9%A9%B1%E5%8A%A8&spm=1001.2101.3001.7020) 的学习。

## 一、块设备的引入

  块设备是 Linux 驱动的三大驱动类型之一，其通常是按照块为单位来访问数据，比如一块为512KB。块设备也是通过/dev目录下的文件系统节点来访问，块设备和字符设备区别仅仅在于内核内部管理数据的方式，也就是内核和驱动程序的接口不同。  
  块设备除了给内核提供和字符设备一样的接口外，还提供了专门面向块设备的接口，块设备的接口必须支持挂装文件系统，通过此接口，块设备能够容纳文件系统，因此 **应用程序一般通过文件系统来访问** 块设备上的内容，而 **不是直接和设备** 打交道。

### 1.1 块设备和字符设备的区别

  块设备主要是针对存储设备，例如SD卡、EMMC、SPI FLASH等，所以块设备其实介绍存储设备驱动，其和字符设备的区别主要为：

1. 块设备只能按照块为单位进行数据读写访问，块是VFS（虚拟文件系统）的基本传输单位，而字符设备是以字节为单位进行数据传输的；
2. 块设备在结构上是可以随机进行读取的，各块中均使用缓冲区来暂时安放数据。字符设备主要是数据流设备，不需要进行缓存；
3. 块设备的驱动和具体的存储外设有关，不同的设备其I/O口算法也存在差异；
4. 一般不需要特别注意内核中设备的关键数据结构

### 1.2 磁盘的基本概念

 1.扇区 —— 读写基本单位  
  每个磁道上可以存储数KB的数据，但计算机通常一次不需要读取这么多的数据，从而将磁道分为若干个扇区(Sector)，扇区是硬盘存储数据的物理单位。每个扇区存储的数据大小是128×2^N（N=0,1,2,3）。从DOS时代开始,每个扇区是512KB，从此业界形成了这种不成文的规定。即使计算机只需要扇区中的某个字节，也要把这个扇区中的字节全部读入，然后选择那个字节。  
 2.磁道 —— 数据存储的介质，可以分化成多个扇区  
  每个盘面被划分为多个狭窄的同心圆环，这样的同心圆环叫做磁道(Track)，数据存储在磁道上。磁道从最外圈（0号磁道）依次向内圈增长，硬盘数据的存放就是从最外圈开始。  
 3.柱面 —— 多个不同磁盘相同磁道共同组成  
  每个盘面相同编号的磁道形成一个柱面(Cylinder)，柱面的编号方式与磁道相同。需要注意的是，硬盘数据的读写是按照柱面进行的（而不是盘面）。即磁头读写数据时从同一柱面内的0号磁头依次开始进行操作，只有同一cylinder上的磁头全部操作完毕后才会移到next cylinder。因为选取磁头 只需要电子切换，而选取柱面需要柱面切换。电子切换速度比机械快，所以读取数据按照柱面而不是盘面进行。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ba2076337aa5e2b67e3f50f13e08e5bd.png)

## 二、块设备驱动框架

### 2.1 框架详解

  块设备框架由文件系统层、驱动层和硬件层组成，其中驱动层可以细分为通用块层、IO调度层、块设备驱动。其中，映射层中的文件系统会把所有数据打包成一个 request ，当有很多request的时候就会在通用层共同组成一个request\_queue，之后调度层会根据磁头位置调整request\_queue的顺序进行优化，最后在设备驱动进行处理。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ba4baa2ef43a03aa22dd42e40a59c3c0.png)  
**映射层（Mapping Layer）**  
  映射层是文件系统和底层存储设备之间的重要桥梁。它主要用于确定文件系统的块大小（block size），然后计算所请求的数据包含多少个块。同时，映射层会调用具体文件系统的 函数 来访问文件的inode，从而确定所请求的数据在磁盘上的逻辑地址。  
**通用块层（Generic Block Layer）**  
  通用块层是Linux内核中的中间层，位于块设备驱动层和文件系统层之间。它负责维持I/O请求在上层文件系统与底层物理磁盘之间的关系。通用块层通过bio（Block I/O） 结构体 来表示和管理一个I/O请求。其主要功能包括：抽象硬件细节、管理I/O请求、缓存和缓冲区管理。  
**I/O调度层（I/O Scheduler Layer）**  
  I/O调度层是通用块层的一部分，负责决定块设备上的I/O请求的执行顺序。其目标是优化系统的 性能 和响应速度。常见的I/O调度算法包括：  
 CFQ（完全公平队列）：  
根据进程的I/O请求历史和权重来调度I/O请求，试图公平地分配磁盘带宽给不同的进程。CFQ通过将I/O请求划分为不同的队列并进行轮转调度，实现了较高的公平性。  
 Deadline（截止时间）：  
使用截止时间来调度I/O请求。Deadline调度器将I/O请求分为读取和写入两类，并尽量在截止时间之前完成这些请求。它通过设定读写请求的时间限制，保证了I/O操作的及时性和较低的延迟。  
 NOOP（无操作）：  
简单地按照先到先服务（FIFO）的方式进行调度，不做任何优化。NOOP适用于那些具有自身优化机制的存储设备（如SSD），或者在I/O调度的开销远大于设备本身的情况下使用。  
**块设备驱动层（Block Device Driver Layer）**  
  块设备驱动层负责与具体的硬件设备进行直接的交互。它管理块设备的I/O操作，并将这些操作提交到底层硬件。其主要组成部分和功能包括：  
 请求队列（Request Queue）：  
请求队列用于管理和存储待处理的I/O请求。对于一些响应速度较慢的磁盘设备，请求队列可以缓冲这些请求，以提高系统的整体效率。  
 请求合并和排序：  
在向块设备提交请求之前，内核会先对请求进行合并和排序。这一预处理操作有助于减少磁盘寻道时间和I/O操作的次数，从而提高访问效率。  
 调度和派发请求：  
块设备驱动层利用I/O调度程序来决定请求的排列顺序和派发时机。调度程序通过优化请求的顺序和调度策略，最大化地利用磁盘资源，提升系统性能。  
 驱动程序接口：  
块设备驱动程序提供一组接口，供操作系统调用。这些接口包括打开设备、关闭设备、读写数据等。驱动程序负责将这些高层操作转换为底层的硬件指令，并执行相应的I/O操作。

### 2.2 核心数据结构

#### 2.2.1 block\_device

  block\_device 是一个重要的数据结构，用于表示一个具体的块设备对象，如硬盘或硬盘的分区。该结构体包含了管理和操作块设备所需的各种信息。

```c
struct block_device {
    dev_t bd_dev;     /* not a kdev_t - it's a search key */
    int bd_openers;
    struct inode *bd_inode;     /* will die */
    struct super_block *bd_super;
    struct mutex bd_mutex;     /* open/close mutex */
    struct list_head bd_inodes;
    void * bd_claiming;
    void * bd_holder;
    int bd_holders;
    bool bd_write_holder;
#ifdef CONFIG_SYSFS
    struct list_head bd_holder_disks;
#endif
    struct block_device *bd_contains;
    unsigned bd_block_size;
    struct hd_struct *bd_part;
    /*number of times partitions within this device have been opened.*/
    unsigned bd_part_count;
    int bd_invalidated;
    /*  bd_disk成员变量为gendisk结构体指针类型，内核使用block_device来表示
    具体块设备对象(硬盘/分区)，若是硬盘的话bd_disk就指向通用磁盘结构gendisk */
    struct gendisk *bd_disk;  
    struct request_queue *bd_queue;
    struct list_head bd_list;
    unsigned long bd_private;
    /* The counter of freeze processes */
    int bd_fsfreeze_count;
    /* Mutex for freeze */
    struct mutex bd_fsfreeze_mutex;
};
12345678910111213141516171819202122232425262728293031
```
- bd\_dev：设备号，dev\_t 类型，唯一标识一个设备，用作搜索键。
- bd\_openers：记录打开设备的次数，反映了当前有多少用户或进程正在使用该设备。
- bd\_inode：指向与设备关联的 inode 结构体，inode 是文件系统中的一个重-要数据结构，包含文件或设备的元数据。此成员将来可能会被移除。
- bd\_super：指向设备上的文件系统的超级块 super\_block 结构体，超级块包含文件系统的全局信息。
- bd\_mutex：用于同步设备的打开和关闭操作的互斥锁，确保这些操作的原子性。
- bd\_inodes：一个链表头，链表中包含了与设备相关的所有 inode 结构体。
- bd\_claiming：指向声称正在使用该设备的对象，用于协调设备的独占访问。
- bd\_holder：指向当前持有设备的对象，用于跟踪谁正在使用设备。
- bd\_holders：持有设备的对象计数，记录有多少对象当前持有该设备。
- bd\_write\_holder：布尔值，表示是否有持有者正在写设备。
- bd\_holder\_disks：如果启用了 SYSFS 配置选项，此链表用于管理持有设备磁盘的对象。
- bd\_contains：指向包含该设备的块设备（对于分区，它指向整个硬盘）。
- bd\_block\_size：块设备的块大小，单位是字节，决定了设备的最小读写单位。
- bd\_part：指向描述块设备分区的结构体 hd\_struct。
- bd\_part\_count：记录该设备内的分区被打开的次数。
- bd\_invalidated：指示设备是否已失效，如果设备失效，该值为非零。  
	\-bd\_disk：指向描述硬盘的通用磁盘结构 gendisk，内核使用 block\_device 来表示具体的块设备对象（如硬盘或分区），如果是硬盘，bd\_disk 就指向 gendisk 结构体。
- bd\_queue：指向块设备的请求队列 request\_queue，用于管理设备的 I/O 请求。
- bd\_list：块设备的链表头，用于将块设备链接到全局设备链表中。
- bd\_private：私有数据，用于驱动程序保存特定于设备的私有信息。
- bd\_fsfreeze\_count：文件系统冻结计数器，记录冻结文件系统的次数。
- bd\_fsfreeze\_mutex：用于文件系统冻结的互斥锁，确保冻结和解冻操作的原子性。

#### 2.2.2 gendisk

  gendisk是Linux内核中用于描述通用磁盘（Generic Disk）的数据结构。它包含了与磁盘设备相关的各种信息，如设备号、设备名称、操作函数集、请求队列等。在内核中，这个结构体用于管理和操作磁盘设备。下面是对该结构体各个成员变量的详细解释：

```c
struct gendisk {
    int major;              // 主设备号
    int first_minor;        // 第一个次设备号
    int minors;             // 次设备数量
    char disk_name[32];     // 设备名称
    struct block_device_operations *fops;  // 块设备操作集
    struct request_queue *queue;  // 请求队列
    void *private_data;     // 私有数据
};
123456789
```
- major：主设备号（major number），用于唯一标识一类设备。
- first\_minor：第一个次设备号（minor number）。
- minors：次设备数量，表示在这个通用磁盘结构下管理的次设备（或分区）的数量。
- disk\_name：设备名称，是一个字符数组，存储设备的名称。名称通常用于设备的识别和管理，比如 /dev/sda。
- fops：块设备操作集（block\_device\_operations），指向 struct block\_device\_operations 结构体。这个结构体包含了一组函数指针，定义了块设备的各种操作，如打开设备、关闭设备、读写数据等。这些函数由具体的块设备驱动程序实现。
- queue：请求队列（request\_queue），指向 struct request\_queue 结构体。请求队列用于管理对块设备的I/O请求。它负责处理和调度这些请求，提高I/O操作的效率。
- private\_data：私有数据指针，用于存储驱动程序的特定数据。这个指针通常用于保存驱动程序需要的额外信息，确保在操作设备时可以访问这些信息。

#### 2.2.3 block\_device\_operations

  block\_device\_operations 是用于描述块设备操作的一组函数指针集合。这些操作函数由具体的块设备驱动程序实现，并提供了对块设备的各种操作接口，如打开、关闭、读写、控制等。值得注意的是，这个operations结构体是 **给文件系统提供接口函数** ，而不是给应用层。

```c
struct block_device_operations {
    int (*open) (struct block_device *, fmode_t);
    void (*release) (struct gendisk *, fmode_t);
    int (*rw_page)(struct block_device *, sector_t, struct page *, int rw);
    int (*ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
    int (*compat_ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
    long (*direct_access)(struct block_device *, sector_t, void **, unsigned long *pfn, long size);
    unsigned int (*check_events) (struct gendisk *disk, unsigned int clearing);
    int (*media_changed) (struct gendisk *);
    void (*unlock_native_capacity) (struct gendisk *);
    int (*revalidate_disk) (struct gendisk *);
    int (*getgeo)(struct block_device *, struct hd_geometry *);
    void (*swap_slot_free_notify) (struct block_device *, unsigned long);
    struct module *owner;
};
123456789101112131415
```
- open：用于打开块设备，当用户或内核模块尝试打开设备时调用。
- remove：用于释放块设备，当设备不再使用时调用。
- rw\_page：用于读写指定的页。
- ioctl：用于块设备的I/O控制操作。
- direct\_access：用于直接访问块设备的特定部分。
- check\_events：用于检查块设备上的事件，例如介质更改。
- unlock\_native\_capacity：用于解锁设备的原始容量。
- revalidate\_disk：用于重新验证磁盘。
- getgeo：用于获取磁盘信息，包括磁头、柱面和扇区等信息。
- swap\_slot\_free\_notify：交换槽释放通知函数指针。

#### 2.2.4 request\_queue、request 和 bio

  大家如果仔细观察的话会在 block\_device\_operations 结构体中并没有找到 read 和 write 这样的读写函数，那么块设备是怎么从物理块设备中读写数据？这里就引前面提到的request\_queue、request 和 bio。这三者的关系有些类似于我们spi驱动框架一节讲述的transfer\_list和spi\_message，request\_queue下挂载着第一个request结构体，而不同request之间可以通过next\_rq进行链接，且其下挂载这bio结构体，不同的bio也可以通过bi\_next进行串联。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/566c00a6636e21719961b13f0969dbb2.png)

```c
//表示一个块设备的请求队列
struct request_queue {
    spinlock_t queue_lock;            //队列锁，用于保护队列操作的同步
    struct list_head queue;            //请求队列链表
    struct request  *last_merge;    //指向request结构体
    request_fn_proc *request_fn;    //请求处理函数指针
    make_request_fn *make_request_fn;//用于将 bio 转换为 request 的函数指针
    struct elevator_queue *elevator;//指向电梯算法调度器的指针
    struct gendisk *disk;            //关联的磁盘设备
    unsigned int nr_requests;        //队列中的请求数
    struct blk_plug plug;            //用于请求合并的结构体
    /* 其他成员变量 */
};
12345678910111213
```
```c
//一个块设备 I/O 请求
struct request {
    sector_t __sector;        //请求开始的扇区号。
    unsigned int nr_sectors;//请求涉及的扇区数。
    int cmd_flags;            //命令标志，如读/写标志
    struct bio *bio;        //链表中的第一个 bio 结构体。
    struct bio *biotail;    //链表中的最后一个 bio 结构体。
    struct request_queue *q;//指向请求队列的指针。
    struct list_head queuelist;//用于将请求加入队列的链表指针。
    struct list_head hash;    //用于哈希表的链表指针。
    struct request *next_rq;//指向下一个request的指针。
    /* 其他成员变量 */
};
12345678910111213
```
```c
//一个bio对应一个 I/O 请求
struct bio {
    sector_t bi_sector;         /* 要传输的第一个扇区 */
    struct bio *bi_next;        /* 下一个 bio */
    struct block_device *bi_bdev; /* 关联的块设备 */
    unsigned long bi_flags;     /* 状态、命令等标志 */
    unsigned long bi_rw;        /* 低位表示读/写，高位表示优先级 */
    struct bvec_iter bi_iter;   /* 迭代器，标明数据要操作的块设备的位置 */
    unsigned short bi_vcnt;              /* bio_vec 数量 */
    unsigned short bi_idx;              /* 当前 bvl_vec 索引 */
    unsigned short bi_phys_segments;  /* 不相邻的物理段的数目 */

    /* 物理合并和 DMA remap 合并后不相邻的物理段的数目 */
    unsigned short bi_hw_segments;

    unsigned int bi_size;       /* 以字节为单位所需传输的数据大小 */

    /* 为了计算最大的硬件尺寸，我们考虑这个 bio 中第一个和最后一个
       可合并的段的尺寸 */
    unsigned int bi_hw_front_size;
    unsigned int bi_hw_back_size;
    
    unsigned int bi_max_vecs;   /* bio 能持有的最大 bvl_vec 数量 */
    struct bio_vec *bi_io_vec;  /* 实际的 vec 列表 */
    bio_end_io_t *bi_end_io;    /* I/O 操作结束后的回调函数 */
    atomic_t bi_cnt;            /* 引用计数 */
    void *bi_private;           /* 私有数据 */

    bio_destructor_t *bi_destructor; /* 析构函数 */

    /* 
     * 我们可以在 bio 末尾内联一定数量的 vecs，
     * 以避免对少量 bio_vec 进行双重分配。
     * 这个成员必须显然地保持在 bio 的最后。
     */
    struct bio_vec bi_inline_vecs[0];
};

//数据传输最小单位
struct bio_vec {        
    struct page  *bv_page; //指向用于数据传输的页面所对应的page对象
    unsigned int bv_len;   //表示当前要传输的数据大小        
    unsigned int bv_offset;//表示数据在页面内的偏移量    
};

//
struct bvec_iter {
    sector_t bi_sector;
    unsigned int bi_size;
    unsigned int bi_idx;
    unsigned int bi_bvec_done;
};
12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152
```

  接下来我们刨开 bio 结结构体，bi\_rw 用来说明本次块 I/O 操作是还是写，bi\_io\_vec 指向了一个bio\_vec 结构对象数组中的首元素，一个 bio 由多个 bio\_vec 来组没，要完成一个块I /O操作，就要历 bio 中的每一个 bio \_vec。这时我们可以使用bi\_iter进行遍历，它描述了正在进行的 bio\_vec。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d76de740832ca5c81c8423359d51d02c.png)

## 三、块设备驱动的编写

### 3.1 块设备驱动注册

**1\. 注册块设备**  
  这里我们通常使用register\_blkdev函数来获取块设备的设备号，块设备允许按块为单位的访问，常见的块设备包括硬盘、光驱、USB存储设备等。

```c
//用于注册块设备，获得一个主编号
int register_blkdev(unsigned int major, const char *name);
12
```
- 参数
	- major: 设备的主设备号。如果设置为 0，系统会自动分配一个主设备号。
	- name: 设备的名称。
- 返回值
	- 成功：主设备号（正数）
	- 失败：负数

**2\. 申请并初始化gendisk设备**  
  使用 gendisk 之前要先申请， alloc\_disk 函数用于申请一个 gendisk，函数原型如下：

```c
//申请gendisk
struct gendisk *alloc_disk(int minors);
12
```
- 参数
	- minors: 该磁盘可以管理的次设备号（分区）的数量。例如，设置为 1 表示该磁盘不支持分区，设置为 16 表示支持 15 个分区。
- 返回值
	- 成功：指向 gendisk 结构体的指针
	- 失败：NULL
```c
//用于初始化块设备请求队列的函数
request_queue *blk_init_queue(request_fn_proc *rfn, spinlock_t *lock)
12
```
- 参数
	- rfn: 请求处理函数的指针。当队列中有新的 I/O 请求时，内核会调用这个函数处理请求。通常，它是设备驱动程序中用于实际处理 I/O 请求的函数。
	- lock: 指向用于保护请求队列的自旋锁的指针。在请求队列的操作中，这个锁用于同步对队列的访问。
- 返回值
	- 成功：指向 request\_queue 结构体的指针
	- 失败：NULL

**3\. 填充gendisk结构体**  
  将内核对块设备的读写的操作的地方 “请求队列“ 进行初始化，使用 blk\_init\_queue 函数来完成request\_queue 的申请与初始化，函数原型如下：

```c
request_queue *blk_init_queue(request_fn_proc *rfn, spinlock_t *lock)
1
```
- 参数
	- rfn： 请求处理函数指针，每个 request\_queue 都要有一个请求处理函数，请求处理函数request\_fn\_proc
	- lock: 指向用于保护请求队列的自旋锁的指针。在请求队列的操作中，这个锁用于同步对队列的访问。
- 返回值
	- 成功：指向 request\_queue 结构体的指针
	- 失败：NULL

  blk\_fetch\_request 函数来一次性完成请求的获取和开启，其函数原型如下：

```c
struct request *blk_fetch_request(struct request_queue *q);
1
```
- 参数
	- q: 指向请求队列 (request\_queue) 结构体的指针。
- 返回值
	- 成功：指向 request 结构体的指针，表示从请求队列中提取的请求；
	- 失败 ：NULL  
		  获取到request后，那么就要使用request去获取bio中的数据缓冲区的数据，使用bio\_data函数，其函数原型如下：
```c
static inline void *bio_data(struct bio *bio);
1
```
- 参数
	- bio: 指向 bio 结构体的指针。
- 返回值
	- 成功：返回一个指针，表示 bio 结构体中的数据缓冲区的起始地址。

**4\. 添加gendisk**  
  使用 alloc\_disk 申请到 gendisk 以后系统还不能使用，必须使用 add\_disk 函数将申请到的gendisk 添加到内核中， add\_disk 函数原型如下：

```c
void add_disk(struct gendisk *disk);
1
```
- 参数
	- disk: 指向 gendisk 结构体的指针。这个结构体表示一个块设备的磁盘，包含了磁盘的各种信息和操作函数。
```c
//示例
static int __init mydisk_init(void) {
   /* 初始化设备数据缓冲区 */
   dev_data = vmalloc(dev_size);
   if (!dev_data) {
       printk(KERN_ERR "vmalloc failed\n");
       return -ENOMEM;
   }
   memset(dev_data, 0, dev_size);

      /* 1. 注册块设备*/
   major = register_blkdev(0, MY_DISK_NAME);
   if (major <= 0) {
       printk(KERN_ERR "register_blkdev failed\n");
       put_disk(mydisk);
       blk_cleanup_queue(myqueue);
       vfree(dev_data);
       return -EBUSY;
   }
   
   /* 2. 分配和初始化 gendisk 结构体 */
   mydisk = alloc_disk(MY_DISK_MINORS);
   if (!mydisk) {
       printk(KERN_ERR "alloc_disk failed\n");
       blk_cleanup_queue(myqueue);
       vfree(dev_data);
       return -ENOMEM;
   }
   
   // 初始化自旋锁
   spin_lock_init(&myqueue_lock);

   //初始化请求队列
   myqueue = blk_init_queue(my_request, &myqueue_lock);
   if (!myqueue) {
       printk(KERN_ERR "blk_init_queue failed\n");
       vfree(dev_data);
       return -ENOMEM;
   }  
   
   /* 3. 填充 gendisk 结构体*/
   mydisk->major = major;
   mydisk->first_minor = 0;
   mydisk->fops = &my_fops;
   mydisk->queue = myqueue;
   set_capacity(mydisk, 1024); /* 设置容量为 1024 扇区 (512KB) */

   /* 4. 添加磁盘 */
   add_disk(mydisk);
   printk(KERN_INFO "mydisk: registered with major number %d\n", major);
       ...
       
   return 0;
}
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354
```

### 3.2 块设备驱动注销

  这里可以理解为注册函数的逆过程，具体流程不再详述，这里仅介绍一下各部分函数及框架。

```c
//从内核的块设备子系统中删除一个磁盘，使其不再可见。
del_gendisk(struct gendisk *disk)
12
```
- 参数
	- disk: 指向 gendisk 结构体的指针，该结构体表示要删除的磁盘。
```c
//释放 gendisk 结构体的引用计数，并在计数变为零时释放该结构体。
put_disk(struct gendisk *disk)
12
```
- 参数
	- disk: 指向 gendisk 结构体的指针，该结构体表示要释放的磁盘。
```c
//清理并释放请求队列结构体。
blk_cleanup_queue(struct request_queue *q)
12
```
- 参数
	- q: 指向请求队列 (request\_queue) 结构体的指针。
```c
//注销块设备驱动程序并释放与其主设备号相关联的资源。
unregister_blkdev(int major, const char *name)
12
```
- 参数
	- major: 要注销的块设备的主设备号。
	- name: 块设备的名称。
```c
//示例
static void __exit mydisk_exit(void) {
    del_gendisk(mydisk);           // 删除磁盘
    put_disk(mydisk);              // 释放 gendisk 结构体
    blk_cleanup_queue(myqueue);    // 清理请求队列
    unregister_blkdev(major, MY_DISK_NAME); // 注销块设备驱动程序
    vfree(dev_data);               // 释放设备数据缓冲区
}
12345678
```

### 3.3 request函数的编写

  request函数是blk\_init\_queue的关键参数，在块设备驱动程序中，request 函数是处理 I/O 请求的核心函数。它定义了如何处理传入的块设备 I/O 请求，并将这些请求传递给底层硬件。

```c
//遍历请求中的每个 bio 结构体。
#define rq_for_each_bio(bio, rq) \
    list_for_each_entry(bio, &rq->bio_list, bi_list)
123
```
- 参数
	- bio: bio 结构体的指针，用于在循环中存储当前的 bio。
	- rq: 指向 request 结构体的指针。
```c
//获取 bio 结构体中的数据缓冲区。
static inline void *bio_data(struct bio *bio);
12
```
- 参数
	- bio: 指向 bio 结构体的指针。
- 返回值
	- 成功：指向 bio 结构体中数据缓冲区的指针。
```c
//判断 bio 请求是读还是写。
#define bio_data_dir(bio) \
    ((bio)->bi_rw & REQ_WRITE ? WRITE : READ)
123
```
- 参数
	- bio: 指向 bio 结构体的指针。
- 返回值
	- 返回 READ 或 WRITE，表示 bio 请求的方向。  
		功能
```c
//完成请求并通知内核。
void __blk_end_request_all(struct request *req, int error);
12
```
- 参数
	- req: 指向 request 结构体的指针。
	- error: 错误码。如果请求成功，通常传入 0；如果失败，则传入负的错误码。
```c
//示例
static void my_request(struct request_queue *q) {
    struct request *req;
    // 获取下一个请求
    while ((req = blk_fetch_request(q)) != NULL) {  
        struct bio *bio;
        // 遍历请求中的每个 bio 结构体
        rq_for_each_bio(bio, req) {  
            // 获取 bio 结构体中的数据缓冲区
            void *buffer = bio_data(bio);
            // 获取 bio 请求的起始扇区
            sector_t sector = bio->bi_iter.bi_sector;  
            // 获取 bio 请求的扇区数
            unsigned int sectors = bio_sectors(bio); 
            // 计算数据偏移量 
            unsigned long offset = sector * KERNEL_SECTOR_SIZE; 
            // 计算数据字节数
            unsigned long nbytes = sectors * KERNEL_SECTOR_SIZE;  
            // 检查请求是否越界
            if ((offset + nbytes) > dev_size) { 
                printk(KERN_NOTICE "mydisk: bad request: sector=%llu, count=%u\n", sector, sectors);
                // 完成请求并返回错误
                __blk_end_request_all(req, -EIO);  
                continue;
            }
            
             // 判断请求是读操作还是写操作
            if (bio_data_dir(bio) == READ) {  
                // 读操作：将数据从设备缓冲区复制到用户缓冲区
                memcpy(buffer, dev_data + offset, nbytes);  
            } 
            else {
                // 写操作：将数据从用户缓冲区复制到设备缓冲区
                memcpy(dev_data + offset, buffer, nbytes);  
            }
        }
         // 完成请求并通知内核
        __blk_end_request_all(req, 0); 
    }
}
12345678910111213141516171819202122232425262728293031323334353637383940
```

## 四、磁盘设备使用方法

1. 加载完驱动后使用 `ls /dev/` 查看是否存在驱动，如果存在可以利用 `ls /dev/mydisk -l` 查询磁盘信息，如下所示： ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/56f0852f2c0b5a81659b0026fc5778ed.png)
2. 此时的硬盘并不能直接使用，需要进行初始化并分区 `mkfs.vfat /dev/mydisk`
3. 完成上面操作之后，我们可以创建一个temp文件夹进行测试，使用 `mount /dev/mydisk temp` 进行挂载
4. 在temp里面编写内容，使用 `cat test` 查看
5. 返回上级目录，用 `umount /dev/mydisk temp` 取消挂载，这时再次查看temp目录，发现里面没有文件，说明此时字符设备已经卸载了  
	![6.](https://i-blog.csdnimg.cn/blog_migrate/1004a6b730310618efb23fc38b838018.png)  
	**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139948013

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