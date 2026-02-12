---
title: "Linux驱动开发笔记（一）字符驱动_linux字符驱动开发-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137809198?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.5k次，点赞21次，收藏31次。本文将通过字符驱动正式展开Linux驱动开发的学习。_linux字符驱动开发"
tags:
  - "clippings"
---
---

## 前言

  本文将通过 [字符驱动](https://so.csdn.net/so/search?q=%E5%AD%97%E7%AC%A6%E9%A9%B1%E5%8A%A8&spm=1001.2101.3001.7020) 正式展开 Linux 驱动开发的学习。

## 一、字符设备驱动程序框架

  字符设备驱动是一种Linux驱动，用于支持以字符为单位进行I/O操作的设备，如串口、终端等。字符设备驱动的设计原理主要包括定义一个 结构体 ，该结构体内部定义了一些设备的打开、关闭、读、写、控制函数；在结构体外分别实现这些函数；并向内核中注册或删除驱动模块。  
  字符设备驱动框架主要涉及Linux软件系统的层次关系，包括应用程序与底层驱动程序之间的交互过程。我们从下面的思维导图来解读内核源码。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b1634e36b4f1718ad43d488b412a3f06.png)

## 二、基本原理

### 1\. 设备号的申请与归还

  Linux中提供了两种字符定义方式：第一种方式，就是我们常见的变量定义；第二种方式，是内核提供的动态分配方式，调用该 函数 之 后，会返回一个struct cdev类型的指针，用于描述字符设备，笔者这里习惯性使用第一种。

```c
//第一种方式
static struct cdev chrdev;
//第二种方式
struct cdev *cdev_alloc(void);
1234
```

  register\_chrdev\_region函数用于静态地为一个字符设备申请一个或多个设备编号。函数原型如下所示：

```c
//保存新设备号到哈希表中防止冲突
int register_chrdev_region(dev_t from, unsigned count, const char *name)
12
```
- 参数
	- from：dev\_t类型的变量，用于指定字符设备的起始设备号，如果要注册的设备号已经被其他的设备注册了，那么就会导致注册失败。
	- count：指定要申请的设备号个数，count的值不可以太大，否则会与下一个主设备号重叠。
	- name：用于指定该设备的名称，我们可以在/proc/devices中看到该设备。
- 返回值： 返回0表示申请成功，失败则返回错误码

  使用register\_chrdev\_region函数时，都需要去查阅内核源码的Documentation/devices.txt文件， 这就十分不方便。因此，内核又为我们提供了一种能够动态分配设备编号的方式：alloc\_chrdev\_region。调用该函数，内核会自动分配给我们一个尚未使用的主设备号。 我们可以通过命令“cat /proc/devices”查询内核分配的主设备号。

```c
int alloc_chrdev_region(dev_t *dev, unsigned baseminor, unsigned count, const char *name)
1
```
- 参数：
	- dev：指向dev\_t类型数据的指针变量，用于存放分配到的设备编号的起始值；
	- baseminor：次设备号的起始值，通常情况下，设置为0；
	- count、name：同register\_chrdev\_region类型，用于指定需要分配的设备编号的个数以及设备的名称。
- 返回值： 返回0表示申请成功，失败则返回错误码

  内核还提供了register\_chrdev函数用于分配设备号。该函数是一个 内联 函数，它不仅支持静态申请设备号，也支持动态申请设备号，并将主设备号返回，函数原型如下所示。

```c
static inline int register_chrdev(unsigned int major, const char *name,
const struct file_operations *fops)
{
   return __register_chrdev(major, 0, 256, name, fops);
}
12345
```
- 参数：
	- major：用于指定要申请的字符设备的主设备号，等价于register\_chrdev\_region函数，当设置为0时，内核会自动分配一个未使用的主设备号。
	- name：用于指定字符设备的名称
	- fops：用于操作该设备的函数接口指针。
- 返回值： 主设备号

  使用register函数申请的设备号，则应该使用unregister\_chrdev函数进行注销。我们从以上代码中可以看到，使用register\_chrdev函数向内核申请设备号，同一类字符设备(即主设备号相同)，会在内核中申请了256个，通常情况下，我们不需要用到这么多个设备，这就造成了极大的资源浪费。

```c
//使用register函数申请的设备号，则应该使用unregister_chrdev函数进行注销。
static inline void unregister_chrdev(unsigned int major, const char *name)
{
__unregister_chrdev(major, 0, 256, name);
}
12345
```
- 参数：
	- major：指定需要释放的字符设备的主设备号，一般使用register\_chrdev函数的返回值作为实参。
	- name：执行需要释放的字符设备的名称。
- 返回值： 无

  当我们删除字符设备时候，我们需要把分配的设备编号交还给内核，对于使用register\_chrdev\_region函数以及alloc\_chrdev\_region函数分配得到的设备编号，可以使用unregister\_chrdev\_region函数实现该功能。

```c
void unregister_chrdev_region(dev_t from, unsigned count)
1
```
- 参数：
	- from：指定需要注销的字符设备的设备编号起始值，我们一般将定义的dev\_t变量作为实参。
	- count：指定需要注销的字符设备编号的个数，该值应与申请函数的count值相等，通常采用宏定义进行管理。
- 返回值： 无

### 2\. 保存file\_operations接口

  在完成第一步的设备号申请之后，我们要开始着手考虑如何利用file\_operations这个结构体中来编写读写函数。那如何将该结构体与我们的字符设备结构体相关联呢？内核提供了cdev\_init函数，来实现这个过程（cdev结构体在上节已经介绍过了）。

```c
void cdev_init(struct cdev *cdev, const struct file_operations *fops)
{
    //将cdev中的所有值清零
    memset(cdev, 0, sizeof *cdev);
    //用于初始化这个 list_head 成员，使其成为一个空的链表头。
    INIT_LIST_HEAD(&cdev->list);
    //用于初始化一个已经分配好的 struct kobject 结构体，并将其与指定的类型、父对象以及名称关联起来。
    kobject_init(&cdev->kobj, &ktype_cdev_default);
    cdev->ops = fops;
}
12345678910
```
- 参数：
	- cdev：struct cdev类型的指针变量，指向需要关联的字符设备结构体；
	- fops：file\_operations类型的结构体指针变量，一般将实现操作该设备的结构体file\_operations结构体作为实参。
- 返回值： 无

  cdev\_add函数用于向内核的cdev\_map散列表添加一个新的字符设备，如下所示：

```c
int cdev_add(struct cdev *p, dev_t dev, unsigned count)
{
    int error;
    //赋值字符设备的设备号
    p->dev = dev;
    //赋值设备驱动程序控制的实际同类设备的数量
    p->count = count;
    error = kobj_map(cdev_map, dev, count, NULL,
             exact_match, exact_lock, p);
    if (error)
        return error;

    kobject_get(p->kobj.parent);

    return 0;
}
12345678910111213141516
```
- 参数：
	- p：struct cdev类型的指针，用于指定需要添加的字符设备；
	- dev：dev\_t类型变量，用于指定设备的起始编号；
	- count：指定注册多少个设备。
- 返回值： 错误码

  cdev\_del函数用于从Linux内核系统中移除一个字符设备。当调用这个函数时，输入参数所代表的字符设备将从系统中注销，使其不可用。从系统中删除cdev，cdev设备将无法再打开，但任何已经打开的cdev将保持不变， 即使在cdev\_del返回后，它们的FOP仍然可以调用。

```c
//从内核中移除该字符设备
void cdev_del(struct cdev *p)
12
```
- 参数（p）： struct cdev类型的指针，用于指定需要删除的字符设备
- 返回值： 无

  需要注意的是，cdev\_del函数并不负责释放cdev结构体本身所占用的内存。如果cdev结构体是通过动态内存分配（如使用cdev\_alloc函数）创建的，那么在调用cdev\_del之后，还需要手动释放这块内存，以避免 内存泄漏 。

### 3\. 设备节点的创建和销毁

  device\_create是 Linux 内核中的一个函数，用于在内核中创建一个新的设备对象。这个函数是 设备驱动开发 中非常重要的一部分，它允许你将设备和其对应的类关联起来，并为设备提供一组属性和操作。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f64ac3e79f1b18a66e9cafa4f4fd3d7f.png)

```c
struct device *device_create(struct class *class, struct device *parent, dev_t devt, void *drvdata, const char *fmt, ...) 
1
```
- 参数
	- class: 指向一个 class 结构体的指针，表示这个设备所属的类
	- parent: 指向父设备的指针，如果设备没有父设备，可以设置为 NULL
	- dev\_t devt: 设备的设备号
	- drvdata: 要进行回调的数据
	- fmt: 指定设备的名称
- 返回值：成功：新创建的 device 结构体的指针；失败：ERR\_PTR( )

  device\_destroy 函数的主要功能是销毁指定的设备对象，并将其从内核的设备 模型 中移除。当设备不再需要时（例如，驱动被卸载或设备被移除），应该调用这个函数来清理相关的资源。

```c
void device_destroy(struct class *class, dev_t devt)
1
```
- 参数
	- class：指向注册此设备的struct类的指针；
	- devt：以前注册的设备的开发；
- 返回值： 无
- 注意事项
	- 顺序性：通常，你应该在调用 device\_destroy 之前，确保没有任何线程正在使用或引用这个设备对象。如果还有其他线程正在使用设备，销毁操作可能会导致未定义的行为或崩溃。
	- 引用计数：内核中的设备对象通常使用引用计数来管理其生命周期。在调用 device\_destroy 之前，确保没有其他地方持有对该设备对象的引用是很重要的。否则，设备对象可能不会被正确销毁。
	- 错误处理：虽然 device\_destroy 函数本身没有返回值来表示操作是否成功，但在调用它之前，你应该检查传入的参数是否有效，以确保不会传递无效的设备类或设备号。
	- 同步：如果你的驱动在多个线程或中断上下文中操作设备对象，你需要确保对 device\_destroy 的调用是同步的，以避免竞态条件。

**注：除了使用代码创建设备节点，还可以使用mknod命令创建设备节点。**

### 4\. 创建文件设备

#### 4.1 mknod

  mknod命令在Linux系统中用于创建特殊文件，包括字符设备文件和块设备文件。这些特殊文件为设备提供了接口，使得用户空间程序能够与内核空间的设备进行交互。mknod命令的语法为：

```c
mknod [- 选项(可不选)] [文件名称] [类型] [主设备号] [次设备号]
1
```
- 选项
	- Z：设置安全的上下文。
	- m：设置权限信息。
	- help：显示帮助信息。
	- version：显示版本信息。  
		参数包括：
- 文件名：要创建的设备文件名。
- 类型：指定要创建的设备文件类型
	- c、u代表（无缓冲区）字符设备文件
	- b代表（有缓冲区）块设备文件
	- p代表FIFO型特殊文件
- 主设备号：指定设备文件的主设备号，用于区分不同种类的设备。
- 次设备号：指定设备文件的次设备号，用于区分同一类型的多个设备。

#### 4.2 init\_special\_incode( )函数

  当我们使用上述命令，创建了一个字符设备文件时，实际上就是创建了一个设备节点inode结构体， 并且将该设备的设备编号记录在成员i\_rdev，将成员f\_op指针指向了字符设备通用的def\_chr\_fops结构体。

```c
void init_special_inode(struct inode *inode, umode_t mode, dev_t rdev)
{
    inode->i_mode = mode;
    //是否是字符类型
    if (S_ISCHR(mode)) {
        inode->i_fop = &def_chr_fops;
        inode->i_rdev = rdev;
    } 
    //是否是块类型
    else if (S_ISBLK(mode)) {
        inode->i_fop = &def_blk_fops;
        inode->i_rdev = rdev;
    } 
    //是否是FIFO类型
    else if (S_ISFIFO(mode))
        inode->i_fop = &pipefifo_fops;
    else if (S_ISSOCK(mode))
        ;    /* leave it no_open_fops */
    else
        printk(KERN_DEBUG "init_special_inode: bogus i_mode (%o) for inode %s:%lu\n", mode, inode->i_sb->s_id,inode->i_ino);
}
EXPORT_SYMBOL(init_special_inode);
12345678910111213141516171819202122
```

### 5\. 查找file\_operation接口

  用户空间使用open()系统调用函数打开一个字符设备时(int fd = open(“dev/xxx”, O\_RDWR))大致有以下过程：

1. 在虚拟文件系统VFS中的查找对应与字符设备对应 struct inode节点
2. 遍历散列表cdev\_map，根据inod节点中的 cdev\_t设备号找到cdev对象
3. 创建struct file对象(系统采用一个数组来管理一个进程中的多个被打开的设备，每个文件秒速符作为数组下标标识了一个设备对象)
4. 初始化struct file对象，将 struct file对象中的 file\_operations成员指向 struct cdev对象中的 file\_operations成员(file->fops = cdev->fops)
5. 回调file->fops->open函数  
	  下图中列出了open函数执行的大致过程：  
	![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f35e5bfae92c69cb29e60626c9e88703.png)

### 函数速查表

  看到这么多函数，笔者已经头晕了，以下是一个函数表，大家可以比对一下：

| 函数 | 功能 | 备注 |
| --- | --- | --- |
| register\_chrdev\_region | 分配设备号 | 静态申请 |
| alloc\_chrdev\_region | 分配未使用的设备号 | register\_chrdev\_region上位替代 |
| unregister\_chrdev\_region | 注销设备号 | 和register\_chrdev\_region函数及alloc\_chrdev\_region函数搭配使用 |
| register\_chrdev | 用于分配设备号 | 函数是一个内联函数，支持静态/动态，并将主设备号返回，等价于register\_chrdev\_region函数 |
| unregister\_chrdev | 注销设备号 | 注销register\_chrdev函数申请的设备号 |
| cdev\_init | 关联file\_operations |  |
| cdev\_add | 添加一个新的字符设备 |  |
| cdev\_del | 移除一个字符设备 |  |
| device\_create | 创建一个新的设备对象 |  |
| device\_destroy | 销毁指定的设备对象 |  |

## 三、程序编写

  具体流程如下：

- 内核模块入口获得相关寄存器并初始化
- 构造file\_operations接口并注册到内核
- 创建设备文件，绑定file\_operations接口
- 应用程序获得文件句柄后，使用库函数提供的write或ioctl函数发出控制命令。

### 1\. 模块初始化及关闭

```c
#define DEV_NAME "EmbedCharDev"
#define DEV_CNT (1)
#define BUFF_SIZE 128
//定义字符设备的设备号
static dev_t devno;
//定义字符设备结构体chr_dev
static struct cdev chr_dev;
static int __init chrdev_init(void)
{
   int ret = 0;
   printk("chrdev init\n");
   //第一步
   //采用动态分配的方式，获取设备编号，次设备号为0，
   //设备名称为EmbedCharDev，可通过命令cat /proc/devices查看
   //DEV_CNT为1，当前只申请一个设备编号
   ret = alloc_chrdev_region(&devno, 0, DEV_CNT, DEV_NAME);
   if (ret < 0) {
   printk("fail to alloc devno\n");
   //当获取失败时，直接返回对应的错误码
   goto alloc_err;
 }
 //第二步
 //关联字符设备结构体cdev与文件操作结构体file_operations
 cdev_init(&chr_dev, &chr_dev_fops);
 //第三步
 //添加设备至cdev_map散列表中
 ret = cdev_add(&chr_dev, devno, DEV_CNT);
 if (ret < 0) {
   printk("fail to add cdev\n");
   //当添加设备失败的话，需要将申请的设备号注销掉
   goto add_err;
 }
 return 0;

 add_err:
 //添加设备失败时，需要注销设备号
 unregister_chrdev_region(devno, DEV_CNT);
 alloc_err:
 return ret;
 }
 
 static void __exit chrdev_exit(void)
{
   printk("chrdev exit\n");
   unregister_chrdev_region(devno, DEV_CNT);
   cdev_del(&chr_dev);
}

module_init(chrdev_init);
module_exit(chrdev_exit);
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950
```

### 2\. 文件操作方式的实现

  首先我们先来编写自己的open函数和release函数，考虑到字符设备确实是一种虚拟设备，所以不需要确切的回应，这里选择仅打印。

```c
static int chr_dev_open(struct inode *inode, struct file *filp)
{
    printk("\nopen\n");
    return 0;
}

static int chr_dev_release(struct inode *inode, struct file *filp)
{
    printk("\nrelease\n");
    return 0;
}
1234567891011
```

  下面，我们开始实现字符设备最重要的部分，即利用文件操作方式结构体file\_operations实现write\\read函数。当我们的应用程序调用write\\read函数，实际上就是调用我们的chr\_dev\_write\\chr\_dev\_read函数，代码如下（示例）：

```c
static ssize_t chr_dev_write(struct file *filp, const char __user * buf, size_t count, loff_t *ppos)
{
   unsigned long p = *ppos;
   int ret;
   int tmp = count ;
   if (p > BUFF_SIZE)
      return 0;
   if (tmp > BUFF_SIZE - p)
      tmp = BUFF_SIZE - p;
   ret = copy_from_user(vbuf, buf, tmp);
   *ppos += tmp;
   return tmp;
}

static ssize_t chr_dev_read(struct file *filp, char __user * buf, size_t count, loff_t *ppos)
{
   unsigned long p = *ppos;
   int ret;
   int tmp = count ;
   if (p >= BUFF_SIZE)
      return 0;
   if (tmp > BUFF_SIZE - p)
      tmp = BUFF_SIZE - p;
   ret = copy_to_user(buf, vbuf+p, tmp);
   *ppos +=tmp;
   return tmp;
}
123456789101112131415161718192021222324252627
```

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137809198

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

![](https://i-blog.csdnimg.cn/blog_migrate/b1634e36b4f1718ad43d488b412a3f06.png)