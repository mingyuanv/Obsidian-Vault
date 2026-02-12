---
title: "Linux驱动开发笔记（零）驱动基础知识及准备-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137785194?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读4k次，点赞26次，收藏79次。本文是Linux驱动开发系列第一期，归纳前期需准备的知识。介绍了Linux、MCU和FPGA编程的区别，阐述Linux内核模块，包括其定义、代码架构、头文件、模块参数和makefile说明。还讲解了驱动程序设计思路，如基本步骤、设备号、重要数据结构及数据访问函数。"
tags:
  - "clippings"
---
本文是Linux驱动开发系列第一期，归纳前期需准备的知识。介绍了Linux、MCU和FPGA编程的区别，阐述Linux内核模块，包括其定义、代码架构、头文件、模块参数和makefile说明。还讲解了驱动程序设计思路，如基本步骤、设备号、重要数据结构及数据访问函数。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

---

## 前言

  在简单结束应用层的开发学习后，本系列将开启驱动层的学习，本文作为该系列第一期旨在归纳前期需要准备的知识。

## 一、Liunx、MCU和FPGA编程的区别

**FPGA** 的编程更多地依赖于 [硬件描述语言](https://so.csdn.net/so/search?q=%E7%A1%AC%E4%BB%B6%E6%8F%8F%E8%BF%B0%E8%AF%AD%E8%A8%80&spm=1001.2101.3001.7020) （HDL），如VHDL或 Verilog ，用于描述电路的结构和行为。这种编程方法将硬件电路抽象为逻辑门、寄存器等基本元素，并通过编写代码来描述它们之间的连接关系和功能。相较于其他两种编程方式，FPGA编程需要频繁抓取时钟，这是因为FPGA的并行性、硬件描述方式、精确的时序控制需求以及 性能优化 等方面的要求。这种时钟抓取机制使得FPGA能够高效地处理复杂的数字逻辑任务，并在各种应用中实现高性能和灵活性。  
  相比之下， **MCU** 的编程通常更侧重于顺序执行和寄存器的直接操作。因为MCU的操作是顺序执行的，开发者可以通过直接读写寄存器来管理内部状态和操作。这种编程方式相对简单直观，但可能不如FPGA在并行处理和复杂逻辑实现上灵活。  
  至于 **Linux框架** 下的驱动编程，它与FPGA和单片机的编程方式有显著的不同。 Linux 驱动编程主要关注于设备与操作系统之间的交互，包括设备节点的创建、设备驱动程序的编写和与操作系统的接口实现等。驱动程序需要处理设备的硬件特性，并将其抽象为操作系统可以理解和操作的接口。这种编程方式更注重于 软件 的架构和接口设计，与硬件的交互通常是通过特定的接口和协议来实现的。

## 二、Linux内核模块

  在Linux系统中，设备驱动会以内核模块的形式出现，学习Linux内核模块编程是驱动开发的先决条件。 第一次接触Linux内核模块，我们将围绕着“Linux内核模块是什么”，“Linux内核模块的工作原理”以及 “我们该怎么使用Linux内核模块”这样的思路一起走进Linux内核世界。

### 1\. 什么是内核模块

  Linux内核模块是Linux内核向外部提供的一个插口，也被称为动态可加载内核模块（Loadable Kernel Module，LKM）。它是一个具有独立功能的程序，可以被单独编译，但不能独立运行。在运行时，内核模块被链接到内核作为内核的一部分在内核空间运行。  
  内核模块的主要作用是扩展内核的功能，而无需重新编译整个内核。例如，内核模块通常用于添加新的设备驱动程序、文件系统或其他功能到内核中。通过内核模块，Linux内核能够实现内核功能扩展，提供新的系统调用或特性，甚至实现内核的安全增强以增加系统的安全性。  
  这里展示一张图片可以让大家直观地感受一下Linux的内核体系(Monolithic Kernel)。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4661f8a07679e5bff5f73d26e07c7211.png)  
  可以看到Linux所使用的宏内核架构是将包括微内核(Microkernel)以及微内核之外的应用层IPC、文件系统功能、设备驱动模块都编译成一个整体。 其优点是执行效率非常高，但缺点也是十分明显的，一旦我们想要修改、增加内核某个功能时(如增加设备驱动程序)都需要重新编译一遍内核。 Linux操作系统正是采用了宏内核结构。为了解决这一缺点，linux中引入了内核模块这一机制。

### 2\. 内核模块的代码架构

  Linux内核模块的代码框架通常由下面几个部分组成：

- 模块加载函数(必须)： 当通过insmod或modprobe命令加载内核模块时，模块的加载函数就会自动被内核执行，完成本模块相关的初始化工作。
- 模块卸载函数(必须)： 当执行rmmod命令卸载模块时，模块卸载函数就会自动被内核自动执行，完成相关清理工作。
- 模块许可证声明(必须)： 许可证声明描述内核模块的许可权限，如果模块不声明，模块被加载时，将会有内核被污染的警告。
- 模块参数： 模块参数是模块被加载时，可以传值给模块中的参数。
- 模块导出符号： 模块可以导出准备好的变量或函数作为符号，以便其他内核模块调用。
- 模块的其他相关信息： 可以声明模块作者等信息。

| 参数 | 功能 |
| --- | --- |
| MODULE\_LICENSE() | 表示模块代码接受的软件许可协议，Linux内核遵循GPL V2开源协议，内核模块与linux内核保持一致即可 |
| MODULE\_AUTHOR() | 描述模块的作者信息 |
| MODULE\_DESCRIPTION() | 对模块的简单介绍 |
| MODULE\_ALIAS() | 给模块设置一个别名 |

  这里给出一个简单的示例（注:仅作介绍使用）：

```c
#include <linux/module.h>   // 包含内核模块所需的头文件  
#include <linux/kernel.h>  
 
// 模块许可证声明，这是必须的，且必须是这种形式的宏定义  
MODULE_LICENSE("Dual BSD/GPL");  
 
// 模块初始化函数，当模块被加载时调用  
static int __init my_module_init(void)  
{  
   // 初始化代码，比如申请资源、注册设备驱动等  
   printk(KERN_INFO "My module has been loaded.\n");  
     
   // 返回0表示初始化成功，非0值表示失败  
   return 0;  
}  
 
// 模块清理函数，当模块被卸载时调用  
static void __exit my_module_exit(void)  
{  
   // 清理代码，比如释放资源、注销设备驱动等  
   printk(KERN_INFO "My module has been unloaded.\n");  
}  
 
// 使用module_init和module_exit宏来指定初始化函数和清理函数  
module_init(my_module_init);  
module_exit(my_module_exit);
1234567891011121314151617181920212223242526
```

### 3\. 头文件

  前面我们已经接触过了Linux的应用编程，了解到Linux的头文件都存放在/usr/include中。 编写内核模块所需要的头文件，并不在上述说到的目录，而是在Linux内核源码中的include文件夹。编写内核模块中经常要使用到的头文件有以下两个：<linux/init.h>和<linux/module.h>。

```c
#include <linux/module.h>//包含内核模块信息声明的相关函数
#include <linux/init.h>//包含了 module_init()和 module_exit()函数的声明
#include <linux/kernel.h>//包含内核提供的各种函数，如printk
123
```

### 4\. 模块参数

  模块参数允许用户在加载模块时通过命令行指定参数值。这些参数在模块的加载过程中被获取，并转换成相应类型的值，然后赋值给对应的变量，这个过程常常发生在 函数 调用之前。

```c
module_param(name, type, perm)
/*
name： 我们定义的变量名
type： 参数的类型，目前内核支持的参数类型有byte，short，ushort，int，uint，long，ulong，charp，bool，
   invbool。其中charp表示的是字符指针，bool是布尔类型，其值只能为0或者是1；invbool是反布尔类型，其值
   也是只能取0或者是1，但是true值表示0，false表示1。变量是char类型时，传参只能是byte，char * 时只能是
   charp
perm： 表示的是该文件的权限，详细参考下表
*/
123456789
```

| 用户 | 参数 | 功能 |
| --- | --- | --- |
| 当前用户 | S\_IRUSR | 用户拥有读权限 |
|  | S\_IWUSR | 用户拥有写权限 |
| 当前用户组 | S\_IRGRP | 当前用户组的其他用户拥有读权限 |
|  | S\_IWUSR | 当前用户组的其他用户拥有写权限 |
| 其他用户 | S\_IROTH | 其他用户拥有读权限 |
|  | S\_IWOTH | 其他用户拥有写权限 |

  模块参数的使用通常涉及以下步骤：

- 在模块代码中声明变量，并使用module\_param()宏或module\_param\_named()宏来定义模块参数。这些宏接受三个参数：变量名、变量类型以及访问权限。访问权限用于定义在sysfs中对应文件的访问权限，与Linux文件访问权限的管理方式相同。
- 在加载模块时，用户可以通过命令行传递参数值给模块。这些值将被转换为相应的类型，并赋值给在模块代码中声明的变量。

### 5\. makefile说明

  对于内核模块而言，它是属于内核的一段代码，只不过它并不在内核源码中。 为此，我们在编译时需要到内核源码目录下进行编译。 编译内核模块使用的Makefile文件，和我们前面编译C代码使用的Makefile大致相同， 这得益于编译Linux内核所采用的Kbuild系统，因此在编译内核模块时，我们也需要指定环境变量ARCH和CROSS\_COMPILE的值。

```c
KERNEL_DIR=../../../kernel/

ARCH=arm64
CROSS_COMPILE=aarch64-linux-gnu-
export  ARCH  CROSS_COMPILE

obj-m := XXX.o
all:
   $(MAKE) -C $(KERNEL_DIR) M=$(CURDIR) modules

.PHONE:clean

clean:
   $(MAKE) -C $(KERNEL_DIR) M=$(CURDIR) clean
1234567891011121314
```

  以上代码中提供了一个关于编译内核模块的Makefile。  
  第1行：该Makefile定义了变量KERNEL\_DIR，来保存内核源码的目录，需要指定到内核编译输出目录下。  
  第3-5行： 指定了工具链并导出环境变量  
  第6行：变量obj-m保存着需要编译成模块的目标文件名。  
  第8行：$ (MAKE)的MAKE是Makefile中的宏变量，要引用宏变量要使用符号。这里实际上就是指向make程序，所以这里也可以把$ (MAKE)换成make，通过选项’-C’，可以让make工具跳转到源码目录下读取顶层Makefile。 ‘M=$(CURDIR)’表明返回到当前目录，读取并执行当前目录的Makefile，开始编译内核模块。CURDIR是make的内嵌变量，自动设置为当前目录。

## 三、 驱动程序设计思路

  在之前的应用开发中，我们多次使用到open、write及read函数等进行数据的传输，设备节点的链接等等操作。在驱动设计时，我们其实也是同样的套路，不同之处在于我们需要写出自己驱动的open等函数。

### 1\. 基本步骤

- 确定主设备号
- 定义自己的file\_operations结构体
- 根据file\_operations，实习对应的open、write、read等函数
- 注册驱动程序：将file\_operations信息告诉内核
- 入口函数：安装驱动时会自动调用
- 出口函数：卸载驱动时会自动调用
- 其他：创建其他设备节点，提供信息

### 2\. 设备号

  在内核中，dev\_t用来表示设备编号，dev\_t是一个32位的数，其中，高12位表示主设备号，低20位表示次设备号。 也就是理论上主设备号取值范围：0-2 <sup>12</sup> ，次设备号0-2 <sup>20</sup> 。 实际上在内核源码中\_\_register\_chrdev\_region(…)函数中，major被限定在0-CHRDEV\_MAJOR\_MAX，CHRDEV\_MAJOR\_MAX是一个宏，值是512。 在kdev\_t中，设备编号通过移位操作最终得到主/次设备号码，同样主/次设备号也可以通过位运算变成dev\_t类型的设备编号。

### 3\. 数据结构

  在驱动开发过程中，不可避免要涉及到三个重要的的内核数据结构分别包括文件操作方式(file\_operations)， 文件描述结构体(struct file)以及inode结构体，在我们开始阅读编写驱动程序的代码之前，有必要先了解这三个结构体。

#### 3.1 file\_operations

  file\_operations是 Linux 内核中的一个重要的数据结构，用于表示内核中的一个文件所支持的操作集合。这个结构体定义了一系列的文件操作函数，如打开文件、读取文件、写入文件、关闭文件等。这些函数被内核用于处理与文件相关的各种请求。

```c
struct file_operations {  
    struct module *owner;  
    loff_t (*llseek) (struct file *, loff_t, int);  
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);  
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);  
    ssize_t (*aio_read) (struct kiocb *, const struct iovec *, unsigned long, loff_t);  
    ssize_t (*aio_write) (struct kiocb *, const struct iovec *, unsigned long, loff_t);  
    int (*readdir) (struct file *, void *, filldir_t);  
    unsigned int (*poll) (struct file *, struct poll_table_struct *);  
    long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);  
    long (*compat_ioctl) (struct file *, unsigned int, unsigned long);  
    int (*mmap) (struct file *, struct vm_area_struct *);  
    int (*open) (struct inode *, struct file *);  
    int (*flush) (struct file *, fl_owner_t id);  
    int (*release) (struct inode *, struct file *);  
    int (*fsync) (struct file *, loff_t, loff_t, int datasync);  
    int (*aio_fsync) (struct kiocb *, int datasync);  
    int (*fasync) (int, struct file *, int);  
    int (*lock) (struct file *, int, struct file_lock *);  
    ssize_t (*sendpage) (struct file *, struct page *, int, size_t, loff_t *, int);  
    unsigned long (*get_unmapped_area)(struct file *, unsigned long, unsigned long, unsigned long, unsigned long);  
    int (*check_flags)(int);  
    int (*flock) (struct file *, int, struct file_lock *);  
    ssize_t (*splice_read)(struct file *, loff_t *, struct pipe_inode_info *, size_t, unsigned int);  
    ssize_t (*splice_write)(struct pipe_inode_info *, struct file *, loff_t *, size_t, unsigned int);  
    int (*setlease)(struct file *, long, struct file_lock **, void **);  
    long (*fallocate)(struct file *file, int mode, loff_t offset, loff_t len);  
};
12345678910111213141516171819202122232425262728
```

  这里是一些主要成员的解释：

- llseek： 用于修改文件的当前读写位置，并返回偏移后的位置。参数file传入了对应的文件指针，我们可以看到以上代码中所有的函数都有该形参，通常用于读取文件的信息，如文件类型、读写权限；参数loff\_t指定偏移量的大小；参数int是用于指定新位置指定成从文件的某个位置进行偏移，SEEK\_SET表示从文件起始处开始偏移；SEEK\_CUR表示从当前位置开始偏移；SEEK\_END表示从文件结尾开始偏移。
- read： 用于读取设备中的数据，并返回成功读取的字节数。该函数指针被设置为NULL时，会导致系统调用read函数报错，提示“非法参数”。该函数有三个参数：file类型指针变量，char\_\_user\*类型的数据缓冲区，\_\_user用于修饰变量，表明该变量所在的地址空间是用户空间的。内核模块不能直接使用该数据，需要使用copy\_to\_user函数来进行操作。size\_t类型变量指定读取的数据大小。
- write： 用于向设备写入数据，并返回成功写入的字节数，write函数的参数用法与read函数类似，不过在访问\_\_user修饰的数据缓冲区，需要使用copy\_from\_user函数。
- unlocked\_ioctl： 提供设备执行相关控制命令的实现方法，它对应于应用程序的fcntl函数以及ioctl函数。在 kernel 3.0 中已经完全删除了 struct file\_operations 中的 ioctl 函数指针。
- open： 设备驱动第一个被执行的函数，一般用于硬件的初始化。如果该成员被设置为NULL，则表示这个设备的打开操作永远成功。
- release： 当file结构体被释放时，将会调用该函数。与open函数相反，该函数可以用于释放

#### 3.2 file

  file是 Linux 内核中用于描述打开的文件或设备的一个核心数据结构。每当一个文件或设备被用户空间进程打开时，内核都会为其创建一个 struct file 结构体实例，并关联到该进程的文件描述符上。这个结构体包含了与该文件或设备相关的各种信息和操作。  
  struct file 的定义通常包括文件的偏移量、文件操作函数集（通过 f\_op 指向 file\_operations 结构体）、文件所有者、文件类型等信息。以下是一个简化的 struct file 的定义示例：

```c
struct file {  
    struct list_head    f_u;  
    struct dentry        *f_dentry;  
    struct vfsmount      *f_vfsmnt;  
    const struct file_operations *f_op;  
    mode_t                f_mode;  
    loff_t                f_pos;  
    unsigned int          f_flags;  
    fmode_t               f_mode_orig;  
    struct file_lock     *f_lock;  
    struct address_space *f_mapping;  
    /* ... 其他成员 ... */  
};
12345678910111213
```

  这里是一些主要成员的解释：

- f\_dentry: 指向描述文件或目录的 dentry 结构体的指针，它表示了文件系统中的对象。
- f\_vfsmnt:指向该文件或目录所在文件系统的挂载点的 vfsmount 结构体指针。
- f\_op: 指向与文件或设备关联的 file\_operations结构体的指针，该结构体包含了各种文件操作函数。
- f\_pos: 文件当前的读写位置（偏移量）。
- f\_flags: 文件的标志位，如O\_RDONLY、O\_WRONLY、O\_NONBLOCK 等。
- f\_lock: 指向文件锁的指针，用于支持文件的加锁操作。
- f\_mapping: 指向文件的地址空间映射的指针，用于管理文件的内存映射。

#### 3.3 inode

  inode是 Linux 内核中用于表示文件系统中一个具体文件或目录的元数据的数据结构。它包含了与文件或目录相关的各种信息，如权限、所有者、大小、时间戳等。inode 的存在使得文件系统能够高效地管理文件和目录。每个文件和目录在文件系统中都对应一个唯一的 inode。这些 inode 通常存储在磁盘的特定区域，称为 inode 表。通过 inode 的索引，文件系统能够快速地定位到文件或目录的数据块，并进行读写操作。

```c
struct inode {

   dev_t                     i_rdev;
   {......}
   union {
         /* linux内核管道 */
      struct pipe_inode_info *i_pipe;   
      /* 如果这是块设备，则设置并使用 */
      struct block_device    *i_bdev;   
      /* 如果这是字符设备，则设置并使用 */
      struct cdev            *i_cdev;      
      char                   *i_link;
      unsigned               i_dir_seq;
   };
   {......}
};
12345678910111213141516
```

  struct inode 结构体包含了很多字段，以下是一些重要的字段：

- umode\_t i\_mode: 文件类型和权限。
- uid\_t i\_uid: 文件的所有者。
- gid\_t i\_gid: 文件的组。
- kdev\_t i\_rdev: 如果文件是一个设备文件，这个字段表示设备的类型和编号。
- loff\_t i\_size: 文件的大小（以字节为单位）。
- struct timespec i\_atime: 文件的最后访问时间。
- struct timespec i\_mtime: 文件的最后修改时间。
- struct timespec i\_ctime: 文件的最后状态改变时间（如权限、所有者等的改变）。
- struct hlist\_node i\_hash: 用于哈希表，以快速查找 inode。
- struct list\_head i\_devices: 指向使用该 inode 的所有设备的列表。
- struct list\_head i\_wb\_list: 写入回调的列表。
- struct address\_space \*i\_mapping: 指向文件的地址空间的指针，用于页面缓存管理。
- struct inode\_operations \*i\_op: 指向该 inode 类型的操作的指针。
- struct file\_operations \*i\_fop: 指向文件操作的指针，如果这是一个设备文件。

#### 3.4 哈希表

  哈希表（Hash table，也叫散列表），是根据关键码值(Key value)而直接进行访问的数据结构。它通过把关键码值映射到表中一个位置来访问记录，以加快查找的速度。这个映射函数叫作散列函数，存放记录的数组叫作散列表。哈希表有以下几个特点：

- 直接访问：通过计算哈希值，可以直接定位到数据在哈希表中的存储位置，因此哈希表的查找、插入和删除操作的时间复杂度都是O(1)。
- 冲突处理：由于哈希函数可能会将不同的键映射到同一个位置，这种情况被称为冲突（collision）。为了处理这种冲突，有多种方法，如链地址法（开放寻址法的一种）和开放寻址法（包括线性探测、二次探测和双重散列）。
- 动态扩容：当哈希表中的数据量过大，导致冲突过多，性能下降时，哈希表会进行动态扩容，即创建一个新的、更大的哈希表，并将原哈希表中的数据重新映射到新哈希表中。

  哈希表在实际应用中非常广泛，例如在数据库索引、缓存系统、数据结构中的关联数组等地方都有使用。然而，哈希表并不适用于所有情况，它对于非均匀分布的数据具有较好的 性能 ，但对于均匀分布或具有特定模式的数据，性能可能较差。此外，哈希表也不支持范围查询。

#### 3.5 cdev结构体

  内核通过一个散列表(哈希表)来记录设备编号。 哈希表由数组和链表组成，吸收数组查找快，链表增删效率高，容易拓展等优点。  
  以主设备号为cdev\_map编号，使用哈希函数f(major)=major%255来计算组数下标(使用哈希函数是为了链表节点尽量平均分布在各个数组元素中，提高查询效率)； 主设备号冲突,则以次设备号为比较值来排序链表节点。 如下图所示，内核用struct cdev结构体来描述一个字符设备，并通过struct kobj\_map类型的散列表cdev\_map来管理当前系统中的所有字符设备。

```c
struct cdev {
   struct kobject kobj;
   struct module *owner;
   const struct file_operations *ops;
   struct list_head list;
   dev_t dev;
   unsigned int count;
} __randomize_layout;
12345678
```
- struct kobject kobj： 内嵌的内核对象，通过它将设备统一加入到“Linux设备驱动模型”中管理(如对象的引用计数、电源管理、热插拔、生命周期、与用户通信等)。
- struct module \*owner： 字符设备驱动程序所在的内核模块对象的指针。
- const struct file\_operations \*ops： 文件操作，是字符设备驱动中非常重要的数据结构，在应用程序通过文件系统(VFS)呼叫到设备设备驱动程序中实现的文件操作类函数过程中，ops起着桥梁纽带作用，VFS与文件系统及设备文件之间的接口是file\_operations结构体成员函数，这个结构体包含了对文件进行打开、关闭、读写、控制等一系列成员函数。
- struct list\_head list： 用于将系统中的字符设备形成链表(这是个内核链表的一个链接因子，可以再内核很多结构体中看到这种结构的身影)。
- dev\_t dev： 字符设备的设备号，有主设备和次设备号构成。
- unsigned int count： 属于同一主设备好的次设备号的个数，用于表示设备驱动程序控制的实际同类设备的数量。

#### 3.6 kobj\_map结构体

  在Linux内核中，struct kobj\_map是一个用于管理kobject（内核对象）映射的数据结构，其与上文提到的cdev结构体共同组成了存放设备号的哈希表结构，这有助于高效地管理大量的设备号及其对应的设备。通过哈希表，内核可以快速定位到特定的设备号，从而实现高效的设备号查找和管理。

```c
struct kobj_map {
    struct probe {
        //指向下一节点
        struct probe *next;
        //设备号
        dev_t dev;
        //次设备号数量
        unsigned long range;
        struct module *owner;
        kobj_probe_t *get;
        int (*lock)(dev_t, void *);
        //空指针
        void *data;
    } *probes[255];
    struct mutex *lock;
};
12345678910111213141516
```

  \*data用于保存cdev结构体中的指针。

### 4\. copy\_to\_user和copy\_from\_user

  在file\_operations结构体中，我们提到read和write函数时，需要使用copy\_to\_user函数以及copy\_from\_user函数来进行数据访问，写入/读取成 功函数返回0，失败则会返回未被拷贝的字节数。

```c
static inline long copy_from_user(void *to, const void __user * from, unsigned long n)
static inline long copy_to_user(void __user *to, const void *from, unsigned long n)
12
```
- 参数
	- to：指定目标地址，也就是数据存放的地址，
	- from：指定源地址，也就是数据的来源。
	- n：指定写入/读取数据的字节数。
- 返回值：写入/读取数据的字节数

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137785194

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

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

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

![](https://i-blog.csdnimg.cn/blog_migrate/4661f8a07679e5bff5f73d26e07c7211.png)