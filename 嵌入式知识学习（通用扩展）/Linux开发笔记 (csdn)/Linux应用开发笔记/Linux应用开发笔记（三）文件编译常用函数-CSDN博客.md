---
title: "Linux应用开发笔记（三）文件编译常用函数-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137246755?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读475次，点赞9次，收藏8次。在文件I/O编辑中，我们常常用到open()，read()，write()，lseek()和close()函数，本文将深入简出地介绍这些函数的功能和参数。"
tags:
  - "clippings"
---
---

## 前言

   在文件I/O编辑中，我们常常用到open()，read()，write()， [lseek](https://so.csdn.net/so/search?q=lseek&spm=1001.2101.3001.7020) ()和close() 函数 ，本文将深入简出地介绍这些函数的功能和参数。

---

## 一、open()函数

   此函数用于创建或打开一个文件。它的返回值是一个非负整数，用于在内核中唯一标识一个打开的文件、设备或其他输入/输出资源。例如：

```c
#include <fcntl.h>  
#include <sys/stat.h>  
#include <sys/types.h>  
  
int open(const char *pathname, int flags, mode_t mode);

//example
fd =  open("test.text", O_WRONLY | O_CREAT, 0777);
fd1 =  open("test.text",O_RDWR);
123456789
```
- pathname：要打开或创建的文件的路径名。
- flags：指定文件如何被打开或创建的文件状态标志。常用的标志有：  
	**O\_RDONLY** ：只读打开。  
	**O\_WRONLY** ：只写打开。  
	**O\_RDWR** ：读写打开。  
	**O\_CREAT** ：如果文件不存在则创建它。需要第三个参数指定权限。  
	**O\_TRUNC** ：如果文件已存在并且是以写方式打开的，则将其长度截断为0。  
	**O\_APPEND** ：每次写时都追加到文件的末尾。 … 以及其他标志。
- mode：如果使用了O\_CREAT标志，这里需要传入一个mode\_t类型的参数来指定新文件的权限，否则则可以省略mode只传输前两个参数即可。
- 返回值：成功时返回一个非负的文件描述符，失败时返回-1。

## 二、read()函数

   此函数用于从打开的文件中 [读取数据](https://so.csdn.net/so/search?q=%E8%AF%BB%E5%8F%96%E6%95%B0%E6%8D%AE&spm=1001.2101.3001.7020) 。它接受文件描述符、缓冲区指针和要读取的字节数作为参数，并将读取的数据放入提供的缓冲区中。例如：

```c
#include <unistd.h>  
  
ssize_t read(int fd, void *buf, size_t count);

//example
count = read(fd, buf, sizeof(buf));
123456
```
- fd：文件描述符，通常由open()返回。
- buf：指向一个缓冲区的指针，用于存储读取的数据。
- count：要读取的字节数。
- 返回值：成功时返回读取的字节数，到达文件末尾或出错时返回小于count的值，出错时返回-1。

## 三、write()函数

   此函数用于将数据写入打开的文件。它接受 [文件描述符](https://so.csdn.net/so/search?q=%E6%96%87%E4%BB%B6%E6%8F%8F%E8%BF%B0%E7%AC%A6&spm=1001.2101.3001.7020) 、数据缓冲区指针和要写入的字节数作为参数，并将数据从缓冲区写入文件。

```c
#include <unistd.h>  
  
ssize_t write(int fd, const void *buf, size_t count);

//example
count = write(fd, buf, count);
123456
```
- fd：文件描述符。
- buf：指向包含要写入数据的缓冲区的指针。
- count：要写入的字节数。
- 返回值：成功时返回写入的字节数，出错时返回-1。

## 四、lseek()函数

   此函数用于改变当前文件的读写位置。它允许你设置文件的偏移量，这样你可以在文件的任意位置开始读取或写入。

```c
#include <unistd.h>  
  
off_t lseek(int fd, off_t offset, int whence);
123
```
- fd：文件描述符。
- offset：相对于whence的偏移量。
- whence：确定偏移量的起始位置，可以是以下值之一：  
	**SEEK\_SET** ：从文件开始处计算偏移量。  
	**SEEK\_CUR** ：从当前读写位置计算偏移量。  
	**SEEK\_END** ：从文件末尾计算偏移量。
- 返回值：成功时返回新的文件偏移量（相对于文件开头的字节数），出错时返回-1。

## 五、close()函数

   此函数用于关闭已打开的文件。在关闭文件后，你无法再对其进行读取或写入操作，并且系统资源会得到释放。

```c
#include <unistd.h>  
  
int close(int fd);
123
```
- fd：要关闭的文件描述符。
- 返回值：成功时返回0，出错时返回-1。

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137246755

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