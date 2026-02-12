---
title: "Linux应用开发笔记（二）Makefile及其编写_makefile编写-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137197917?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读703次，点赞30次，收藏13次。在Linux中编译程序需要使用make命令，而make则依赖于Makefile文件。在实际的使用中，Makefile关注于项目的构建过程，而GCC则关注于源代码的编译。两者在软件开发中各有其重要作用，通常一起使用以完成项目的编译和构建任务。_makefile编写"
tags:
  - "clippings"
---
> 提示：文章写完后，目录可以自动生成，如何生成可参考右边的帮助文档

---

## 前言

  在 Linux 中编译程序需要使用 [make命令](https://so.csdn.net/so/search?q=make%E5%91%BD%E4%BB%A4&spm=1001.2101.3001.7020) ，而make则依赖于Makefile文件。在实际的使用中，Makefile关注于项目的构建过程，而GCC则关注于 源代码 的编译。两者在软件开发中各有其重要作用，通常一起使用以完成项目的编译和构建任务。

## 一、Makefile的基本知识

  Makefile是一个用于自动化编译和构建程序的工具，它包含一个或多个规则，每个规则说明如何基于一个或多个文件生成一个或多个输出文件。这些规则定义了哪些文件是源文件，哪些文件是目标文件，以及如何使用 编译器 或链接器从源文件生成目标文件。Makefile的基本结构包括目标、依赖和命令三部分。 **目标通常是要生成的文件名，依赖是用来生成目标的输入文件名，命令是生成目标时需要运行的命令** 。使用Makefile的好处是自动化了构建过程，只需要简单地执行make命令，Makefile就会按照定义的规则自动完成编译和链接等操作，从而生成最终的可执行文件。此外，Makefile还可以方便地管理多个源文件之间的依赖关系，以及处理复杂的构建任务。在编写Makefile时，需要遵循一定的语法和规则，以确保其正确性和可读性。同时，还需要根据具体的项目需求来定制Makefile，以满足不同的构建需求。

### 1\. Makefile的引入

  我们的.c源文件转化为可执行文件的过程大致如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7131642ddcb08213e05071bcc6e7975a.png)  
  这里首先需要提到无敌的“gcc -o”命令，继续以hello.c文件为例：

```c
gcc -o hello hello.c
1
```

  这将产生一个可以在“当前环境”下执行的hello文件。此时，gcc -o命令独自完成了包括预处理，编译、汇编和连接的过程。但是由于该命令每次都会将所有文件重新编排一遍，故而在大型项目时直接全编译不太合理，此时就需要我们逐步编译。

### 2\. Makefile的基本语法

#### 2.1 基本规则

```c
目标:[依赖1] [依赖2]
[tab]命令
//例子：
test:a.o b.o
    gcc -o test a.o b.o
a.o:a.c
    gcc -c -o a.o a.c    
b.o:b.c
    gcc -c -o b.o b.c    
123456789
```

若不存在目标或者依赖的更新时间晚于目标时，则执行该文档。

#### 2.2 通配符：%.o

- $@ 表示规则中的目标
- $^ 表示规则中的所有依赖, 组成一个列表, 以空格隔开, 如果这个列表中有重复的项则消除重复项
- $< 表示规则中的第一个依赖
- $? 第一变化的依赖
```c
目标:[依赖1] [依赖2]
[tab]命令
//例子：
test:a.o b.o
    gcc -o test a.o b.o
%.o:%.c
    gcc -c -o $@ $<
1234567
```

#### 2.3 PHONY

  在Makefile中，PHONY是一个特殊的标记，用于指明一个目标是伪目标（phony target）。伪目标并不是实际要生成的文件，而是执行某些特定的命令或操作。使用PHONY可以避免当Makefile中的目标名称与实际文件名冲突时，导致命令不被执行的问题。具体来说，当Makefile中的目标与实际文件重名时，如果没有将目标定义为PHONY，make工具会误认为目标文件已经存在且是最新的，从而不会执行相应的命令。而通过将目标定义为PHONY，可以确保无论是否存在同名文件，make都会执行相应的命令。此外，使用PHONY还可以提高make的执行效率，因为将目标定义为PHONY后，make不会试图寻找该目标的隐含规则，从而减少了不必要的搜索和匹配操作。例如：

```c
# 声明clean为伪文件
.PHONY:clean
clean:
        # shell命令前的 - 表示强制这个指令执行, 如果执行失败也不会终止
        -rm $(obj) $(target) 
        echo "hello, 我是测试字符串"
123456
```

#### 2.4 即使变量和延时变量

A = XXX；//定义时赋值  
B:=XXX; //使用时再赋值  
C?=XXX; //第一次定义时才起效（若已定义过则直接忽略）  
D +=XXX; //附加，取决与前面定义为哪种类型

**makefile的使用：make \[目标/空\]：目标：执行该目标； 空：执行文件中第一个目标**

### 二、 Makefile的函数

#### 3.1 $(foreach var,list,text)

  具体而言，$(foreach var, list, text)函数会将列表list中的每个元素依次赋值给变量var，并根据每个元素生成一段文本text。然后，将所有生成的文本段连接在一起，并返回结果。

```c
list := a c b
text := $(foreach f,$(list),.$(f).o)
all:
    @echo text = $(text)
//输出结果为: a.o c.o b.o
12345
```

#### 3.2 ( f i l t e r p a t t e r n, t e x t ) 和 (filter pattern,text)和 (filterpattern,text)和(filter-out pattern,text)

  二者分别是指在text中挑选出符合/不符合pattern格式的值。

```c
list := a c b d/
A := $(filter %/,text)
B := $(filter-out %/,text)
all:
    @echo A = $(A)
    @echo B = $(B)
//输出结果为:A= d/
//            B= a c b
12345678
```

#### 3.3 $(wildcard pattern)

  用于匹配指定模式的而文件列表:  
  1、具体来说，它会返回一个包含所有匹配文件名的列表（包括文件路径），这些文件名之间用空格分开。  
  2、模式可以包含通配符，如\*（表示匹配任意长度的任意字符）和?（表示匹配任意单个字符）等，用于匹配文件名中的字符。  
  值得注意的是，pattern只能是该文件列表下的。

```c
list := a c b d/
text := $(foreach f,$(list),$(f).o)
A := $(wildcard *.o)
all:
    @echo A = $(A)
//输出结果为: a.o c.o b.o
123456
```

#### 3.4 $(patsubst pattern,replacement,text)

  用于替换文本中匹配某个模式的部分 ，会在文本text中查找与给定模式pattern匹配的部分，(其中pattern可以使用通配符%来匹配任意长度的任意字符），并将其替换为replacement，它返回替换后的新文本。

```c
list := a.c c.c
A := $(patsubst %.c,/%.o,$(list))
all:
    @echo A = $(A)
//输出结果为: a.o c.o
12345
```

## 三、Makefile的编写

### 1.编写的核心

- Makefile中要确定被编译的文件、目录，Makefile始终包含于Makefile\_build中。
- 顶层目录和各个子目录下均需要存在Make\_file文件。

### 2.通用模板解析

  在顶层目录下执行make，导致顶层Makefile的第一个目标all被处理，并进入到Makefile\_build文件中继续执行命令。

```c
//Makefile(top)
obj-y += xxx.o //读取当前目录下.c文件
obj-y += /yyy  //读取子目录(sub)
all : start_recursive_build $(TARGET)
    @echo $(TARGET) has been built!
start_recursive_build:
    make -C ./ -f $(TOPDIR)/Makefile.build //使用Makefile.build处理顶层目录
1234567
```

  在build中具体编译子目录和当前目录下的.c文件并链接生成build-in.o文件

```c
//Makefile_build(top)
PHONY := __build
__build:
//清零变量
obj-y :=
subdir-y :=
EXTRA_CFLAGS :=
//包含底层模块中的Makefile(top)，里面有各种obj-y，确定文件目录
include Makefile
__subdir-y      := $(patsubst %/,%,$(filter %/, $(obj-y)))
subdir-y        += $(__subdir-y)
//预先处理子目录a/得到子目录下的build-in.o
subdir_objs := $(foreach f,$(subdir-y),$(f)/built-in.o)

# 得到子目录下的.o文件
cur_objs := $(filter-out %/, $(obj-y))
dep_files := $(foreach f,$(cur_objs),.$(f).d)
dep_files := $(wildcard $(dep_files))

ifneq ($(dep_files),)
  include $(dep_files)
endif

PHONY += $(subdir-y)

__build : $(subdir-y) built-in.o

$(subdir-y):
        make -C $@ -f $(TOPDIR)/Makefile.build
        
built-in.o : $(cur_objs) $(subdir_objs)
        $(LD) -r -o $@ $^

dep_file = .$@.d

%.o : %.c
        $(CC) $(CFLAGS) $(EXTRA_CFLAGS) $(CFLAGS_$@) -Wp,-MD,$(dep_file) -c -o $@ $<

.PHONY : $(PHONY)
123456789101112131415161718192021222324252627282930313233343536373839
```

  执行完这条指令后会返回到Makefile(top)中，继续编译当前目录(顶层目录)中的c文件，再将生成的o文件和子目录产生的build-in.o链接生成当前目录下的build-in.o(top)

```c
//Makefile(top)
tart_recursive_build:
        make -C ./ -f $(TOPDIR)/Makefile.build

$(TARGET) : built-in.o
        $(CC) -o $(TARGET) built-in.o $(LDFLAGS)
123456
```

  最后便可以链接到所有目录下的.o文件件到一个app中。

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137197917

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

![](https://i-blog.csdnimg.cn/blog_migrate/7131642ddcb08213e05071bcc6e7975a.png)