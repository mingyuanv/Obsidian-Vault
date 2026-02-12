---
title: "shell脚本语言(超全超详细)-CSDN博客"
source: "https://blog.csdn.net/weixin_43288201/article/details/105643692"
author:
published:
created: 2025-04-27
description: "文章浏览阅读10w+次，点赞1.1k次，收藏8.7k次。本文详细介绍Shell脚本的基础知识，包括脚本调用、语法规范、变量操作、条件测试及控制语句等内容，旨在帮助读者快速掌握Shell脚本编程技巧。"
tags:
  - "clippings"
---
本文详细介绍Shell脚本的基础知识，包括脚本调用、语法规范、变量操作、条件测试及控制语句等内容，旨在帮助读者快速掌握Shell脚本编程技巧。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

## 1、shell的概述

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/439cb8fff6f43452b5686673f5874164.jpeg#pic_center)  
shell 是一种脚本语言  
脚本：本质是一个文件，文件里面存放的是 特定格式的指令，系统可以使用脚本解析器 翻译 或解析 指令 并执行（它不需要编译）  
shell 既是应用程序 又是一种脚本语言（应用程序 解析 脚本语言）  
shell命令解析器：  

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/92516cdb7ef604bc5954fc8a64522c70.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c0a602acd0215cfbcb5ba0bf99745edf.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c626da74d42502f4cc7e937928c9160f.png)  


## 2、脚本的调用形式

#### 打开终端时系统自动调用：/etc/profile 或 ~/.bashrc


用户手动调用：用户实现的脚本  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/50b1e0f869a822043d9195bf1aeee4df.png)

## 3、shell语法初识

### 3.1、


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ea8396e8cc6cb0acaf259da1781ea987.png)

### 3.2、

#### 第一步：编写脚本文件

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1791a8531784fe91d00613d74bf5c34c.png)

#### 第二步：加上可执行权限

**chmod +x xxxx.sh**  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/62e6826ba422317830e694d94edc9356.png)

#### 第三步：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0d3fa2355a464637c32edc4fe1aff89f.png)

##### 三种执行方式 （./xxx.sh bash xxx.sh. xxx.sh）

三种执行方式的不同点（./xxx.sh bash xxx.sh. xxx.sh）



如果#！指定指定的解析器不存在 才会使用系统默认的解析器

###### bash xxx.sh:指明先用bash解析器解析

如果bash不存在 才会使用默认解析器

###### . xxx.sh 直接使用默认解析器解析（不会执行第一行的#！指定的解析器）但是第一行还是要写的

三种执行情况：  
打开终端就会有以后个解释器，我们称为当前解释器  
我们指定解析器的时候（使用./xxx.sh 或 bash xxx.sh）时会创建一个子shell解析 脚本  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c8cbabcbefa31e11756ea2eb071da906.png)

#### <span style="background:#b1ffff">注意：windows下 写脚本 在linux下执行 注意</span>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a4aa6c77983c52477b22c59ada3121f8.png)  
执行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/09e1aefc72305608c30a79fbefe81227.png)  
将windows文件 转换成 unix文件  
方法一：dos2unix 如果没有该插件 需要安装  
sudo apt-get install dos2unix  
dos2unix shell脚本  
转换成功就可以执行运行
方法二：
需要用vi打开脚本，在最后一行模式下执行  
:set ff=unix  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/18d13d6dc00f490e2ea8061eac934a74.png)

## 4、变量

<span style="background:#d3f8b6">定义变量  </span>
<span style="background:#d3f8b6">变量名=变量值  </span>
如：num=10  
<span style="background:#affad1">引用变量  </span>
<span style="background:#affad1">$变量名  </span>

<span style="background:#d3f8b6">unset ：清除变量值  </span>
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c117ff68be810e3b641df6fed0d1949c.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b243548d1d5a22c92bcc0c20cba4e8cc.png)  
<span style="background:#affad1">从键盘获取值read</span>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bce20c913a88f6bcb083fa148870ad9c.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9107f1a575f5ca16d3b471318e304159.png)

### 案例：


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0edf0b9903e0c52e9ad474584ef09a8c.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aa6ca06fc47f1a8794d1ac90321d3ba1.png)

### 案例：读取多个值

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/feb4272a6bb0d81d2d57d9e63978602c.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dc922fcac1ba01467ac61eb12b3df544.png)

### 案例<span style="background:#d3f8b6">只读变量</span>：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e18d674a9d5c6f99e6d9bf085e5a8518.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/998ce5ab05d0366bfb76148283acac31.png)

### <span style="background:#b1ffff">查看环境变量：env</span>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a67da76df237c2ca22cb77ac1bc68bc8.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/02593f5a09da06ed2e1d8e9d820734a8.png)

#### 


命令用法:  
source FileName  
作用:在当前bash环境下读取并执行FileName中的命令。  
注:该命令通常用命令“.”来替代。  
如:source.bash\_rc 与..bash\_rc 是等效的。  
注意:source命令与shell scripts的区别是，  
source在当前bash环境下执行命令，而scripts是启动一个子shell来执行命令。这样如果把设置环境变量(或alias等等)的命令写进scripts中，就只会影响子shell,无法改变当前的BASH,所以通过文件(命令列)设置环境变量时，要用source 命令。

06\_sh.sh

```c
#!/bin/bash
expor DATA=250
12
```

用source 是文件生效  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/19227afd8dabf7bd5c3d4c0bc5aecede.png)  
使用 env可以查看到环境变量中已经有 DATA  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e45837be7b46b09c9ea331614a10ac9c.png)  
<span style="background:#affad1">可以在终端直接中读取： </span> 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/13aa1a3e172ee060134ec158f542c856.png)  
在其他sh脚本读取：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a62611f238348d827de079eafad8a73a.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d00184cbdfdf365ccf4763d067fe51a8.png)

### 注意事项：

1、<span style="background:#d3f8b6">变量名只能包含英文字母下划线，不能以数字开头</span>  
1\_num=10 错误  
num\_1=20 正确  
2、<span style="background:#d3f8b6">等号两边不能直接接空格符</span>，<span style="background:#affad1">若变量中本身就包含了空格，则整个字符串都要用双引号、或单引号括起来  </span>
3、双引号 单引号的区别  

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d9c588c26aac3ea537611fd2c35612db.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/47db4c245338b97d9ad14f35159bc822.png)  
如果想在PATH变量中 追加一个路径写法如下：（重要！！！！）

```cpp
export PATH=$PATH:/需要添加的路径
1
```


## 5、预设变量

### <span style="background:#b1ffff">shell直接提供无需定义的变量</span>

![Pasted image 20250428000220.png](../../../通用文件夹/媒体库/图片库/Pasted%20image%2020250428000220.png)
### 案例：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2f5e474a840379656a12fc5021d41654.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d39e6ebd80b7c08c2544012913a2a181.png)

### <span style="background:#b1ffff">脚本标量的特殊用法</span>


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/317cb656da02ea6e0cbf00d69a4fb119.png)  
![在这里插入图片描述]![嵌入式知识学习（通用扩展）（未）/Linux开发笔记 (csdn)/shell脚本语言/assets/shell脚本语言(超全超详细)-CSDN博客/file-20250810171439671.png](assets/shell脚本语言(超全超详细)-CSDN博客/file-20250810171439671.png)g)  

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e16fe6e0a7d6f0bf5f8713228ea65511.png)  

![嵌入式知识学习（通用扩展）（未）/Linux开发笔记 (csdn)/shell脚本语言/assets/shell脚本语言(超全超详细)-CSDN博客/file-20250810171439868.png](assets/shell脚本语言(超全超详细)-CSDN博客/file-20250810171439868.png)


![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4204adf3f72d8e41e679f6f5bb235b78.png)

## 6、变量的扩展

### 6.1、判断变量是否存在

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d291e43bd9b15adfb4da937fd0125eec.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a6290732b6dcaf83cc24081f8b75a2a1.png)

### 6.2、<span style="background:#b1ffff">字符串的操作</span>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ae0d349fe339b17d0d1f715745e075d6.png)

## 7、条件测试

test命令：用于测试字符串、文件状态和数字
test命令有两种格式:
test condition 或\[ condition \]
使用方括号时，要注意在条件两边加上空格。

### 7.1、<span style="background:#b1ffff">文件测试</span>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/159376900403ea9a873c71841021a74e.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/13570893aa480148c097c9a199ca02bd.png)

### 7.2、<span style="background:#b1ffff">字符串测试</span>

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/560f8917302b2d1aa78a2d6e01a64d4c.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8dd1efe7db24a445f90a9c0da1650311.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/28086c8b322757d2aaab56388f6933c5.png)

### 7.3、数值测试

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/06b8af34c9f0ab30e29406a21efbe5e4.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6f22faf6da0d24bbe47bd1353be5c993.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/75aafea52d7b0aef3b4e4b2c90bede22.png)

### 7.4、符合语句测试

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0f1c32d616632add5614d6c169cc10a2.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/04a4459a7b091f49a272d8170c4f14cb.png)

## 8、控制语句

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e8046e3877db84d8b1fdb1b8b8c86842.png)

### 8.1、if控制语句

```cpp


1234567891011121314
```

#### 案例：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/67684dc92b3df1bbe03269b379f1543f.png)

#### 案例：判断当前路径下有没有文件夹 有就进入创建文件 没有 就创建文件夹 再进入创建文件

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/caffead1d01abc8fa1e20c5944174b8c.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/58eb9e92cab26f67e20fa45d15648198.png)

#### 案例：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2bff88621b8e7132ffdb5b4781a0b767.png)  
运行结果：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/205b1f453ae19978810b00afcfa9f710.png)

### 8.2、case

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/741995107703bf03c3aab67e240de67b.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3543f032c9e715e2d36b437fc6583067.png)

### 8.3、for循环语句

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1785c580ca4591c103b1ae6d4a8532b2.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7671b502c4ad004f9020218a3ddd3993.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/58a3873f47beecdfd3f77759345085db.png)

#### 案例：

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/89bcc09a4ab57393763bf74e46b55d03.png)

#### 案例：扫描当前文件

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0addfd80f503214d08348e3489604422.png)

### 8.4、while

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/50b732429b8206167c2006a2f25d1071.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/784a2cba01b267d09037fd45ec13ca4b.png)

### 8.5、until

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7c992ce671c02b4be01249d9305ce884.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e214573663522a553a5c4cccba7e2136.png)

### 8.6、break continue

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c5fc270903c416849134f569adca64eb.png)

## 9、函数

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bdfe7f34eb6ecfdcfa36885485a4e29c.png)  
所有函数在使用前必须定义，必须将函数放在脚本开始部分，直至shell解释器首次发现它时，才可以使用  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a21b7acfc7a696166215398a7daaf4b2.png)

#### 案例：求最值

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a46596d8a89929e925b91033b0bff489.png)

#### 案例：函数分文件

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1df93188ebb96dc0bf9f1a4ab9a63eac.png)  
fun.sh  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3b6536ae393768432fd78f4155f97344.png)  
24\_sh.sh  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a1294ba33cdc4b89043f10682c326a82.png)

实付 元

[使用余额支付](https://blog.csdn.net/weixin_43288201/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏 ![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

![](https://i-blog.csdnimg.cn/blog_migrate/439cb8fff6f43452b5686673f5874164.jpeg#pic_center) ![](https://i-blog.csdnimg.cn/blog_migrate/92516cdb7ef604bc5954fc8a64522c70.png) ![](https://i-blog.csdnimg.cn/blog_migrate/c0a602acd0215cfbcb5ba0bf99745edf.png) ![](https://i-blog.csdnimg.cn/blog_migrate/c626da74d42502f4cc7e937928c9160f.png) ![](https://i-blog.csdnimg.cn/blog_migrate/50b1e0f869a822043d9195bf1aeee4df.png) ![](https://i-blog.csdnimg.cn/blog_migrate/ea8396e8cc6cb0acaf259da1781ea987.png) ![](https://i-blog.csdnimg.cn/blog_migrate/1791a8531784fe91d00613d74bf5c34c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/62e6826ba422317830e694d94edc9356.png) ![](https://i-blog.csdnimg.cn/blog_migrate/0d3fa2355a464637c32edc4fe1aff89f.png) ![](https://i-blog.csdnimg.cn/blog_migrate/c8cbabcbefa31e11756ea2eb071da906.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a4aa6c77983c52477b22c59ada3121f8.png) ![](https://i-blog.csdnimg.cn/blog_migrate/09e1aefc72305608c30a79fbefe81227.png) ![](https://i-blog.csdnimg.cn/blog_migrate/18d13d6dc00f490e2ea8061eac934a74.png) ![](https://i-blog.csdnimg.cn/blog_migrate/c117ff68be810e3b641df6fed0d1949c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/b243548d1d5a22c92bcc0c20cba4e8cc.png) ![](https://i-blog.csdnimg.cn/blog_migrate/bce20c913a88f6bcb083fa148870ad9c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/9107f1a575f5ca16d3b471318e304159.png) ![](https://i-blog.csdnimg.cn/blog_migrate/0edf0b9903e0c52e9ad474584ef09a8c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/aa6ca06fc47f1a8794d1ac90321d3ba1.png) ![](https://i-blog.csdnimg.cn/blog_migrate/feb4272a6bb0d81d2d57d9e63978602c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/dc922fcac1ba01467ac61eb12b3df544.png) ![](https://i-blog.csdnimg.cn/blog_migrate/e18d674a9d5c6f99e6d9bf085e5a8518.png) ![](https://i-blog.csdnimg.cn/blog_migrate/998ce5ab05d0366bfb76148283acac31.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a67da76df237c2ca22cb77ac1bc68bc8.png) ![](https://i-blog.csdnimg.cn/blog_migrate/02593f5a09da06ed2e1d8e9d820734a8.png) ![](https://i-blog.csdnimg.cn/blog_migrate/19227afd8dabf7bd5c3d4c0bc5aecede.png) ![](https://i-blog.csdnimg.cn/blog_migrate/e45837be7b46b09c9ea331614a10ac9c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/13aa1a3e172ee060134ec158f542c856.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a62611f238348d827de079eafad8a73a.png) ![](https://i-blog.csdnimg.cn/blog_migrate/d00184cbdfdf365ccf4763d067fe51a8.png) ![](https://i-blog.csdnimg.cn/blog_migrate/d9c588c26aac3ea537611fd2c35612db.png) ![](https://i-blog.csdnimg.cn/blog_migrate/47db4c245338b97d9ad14f35159bc822.png) ![](https://i-blog.csdnimg.cn/blog_migrate/abb6e35d2077066a5bb56c68e71e6286.png) ![](https://i-blog.csdnimg.cn/blog_migrate/2f5e474a840379656a12fc5021d41654.png) ![](https://i-blog.csdnimg.cn/blog_migrate/d39e6ebd80b7c08c2544012913a2a181.png) ![](https://i-blog.csdnimg.cn/blog_migrate/555677be158c84e8faf8b5d4ccd42ee3.png) ![](https://i-blog.csdnimg.cn/blog_migrate/317cb656da02ea6e0cbf00d69a4fb119.png) ![](https://i-blog.csdnimg.cn/blog_migrate/c18c0639e5523227793cbf5c940422e1.png) ![](https://i-blog.csdnimg.cn/blog_migrate/e16fe6e0a7d6f0bf5f8713228ea65511.png) ![](https://i-blog.csdnimg.cn/blog_migrate/6ecaffc07591301479665446d5ffb818.png) ![](https://i-blog.csdnimg.cn/blog_migrate/4204adf3f72d8e41e679f6f5bb235b78.png) ![](https://i-blog.csdnimg.cn/blog_migrate/d291e43bd9b15adfb4da937fd0125eec.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a6290732b6dcaf83cc24081f8b75a2a1.png) ![](https://i-blog.csdnimg.cn/blog_migrate/ae0d349fe339b17d0d1f715745e075d6.png) ![](https://i-blog.csdnimg.cn/blog_migrate/159376900403ea9a873c71841021a74e.png) ![](https://i-blog.csdnimg.cn/blog_migrate/13570893aa480148c097c9a199ca02bd.png) ![](https://i-blog.csdnimg.cn/blog_migrate/560f8917302b2d1aa78a2d6e01a64d4c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/8dd1efe7db24a445f90a9c0da1650311.png) ![](https://i-blog.csdnimg.cn/blog_migrate/28086c8b322757d2aaab56388f6933c5.png) ![](https://i-blog.csdnimg.cn/blog_migrate/06b8af34c9f0ab30e29406a21efbe5e4.png) ![](https://i-blog.csdnimg.cn/blog_migrate/6f22faf6da0d24bbe47bd1353be5c993.png) ![](https://i-blog.csdnimg.cn/blog_migrate/75aafea52d7b0aef3b4e4b2c90bede22.png) ![](https://i-blog.csdnimg.cn/blog_migrate/0f1c32d616632add5614d6c169cc10a2.png) ![](https://i-blog.csdnimg.cn/blog_migrate/04a4459a7b091f49a272d8170c4f14cb.png) ![](https://i-blog.csdnimg.cn/blog_migrate/e8046e3877db84d8b1fdb1b8b8c86842.png) ![](https://i-blog.csdnimg.cn/blog_migrate/67684dc92b3df1bbe03269b379f1543f.png) ![](https://i-blog.csdnimg.cn/blog_migrate/caffead1d01abc8fa1e20c5944174b8c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/58eb9e92cab26f67e20fa45d15648198.png) ![](https://i-blog.csdnimg.cn/blog_migrate/2bff88621b8e7132ffdb5b4781a0b767.png) ![](https://i-blog.csdnimg.cn/blog_migrate/205b1f453ae19978810b00afcfa9f710.png) ![](https://i-blog.csdnimg.cn/blog_migrate/741995107703bf03c3aab67e240de67b.png) ![](https://i-blog.csdnimg.cn/blog_migrate/3543f032c9e715e2d36b437fc6583067.png) ![](https://i-blog.csdnimg.cn/blog_migrate/1785c580ca4591c103b1ae6d4a8532b2.png) ![](https://i-blog.csdnimg.cn/blog_migrate/7671b502c4ad004f9020218a3ddd3993.png) ![](https://i-blog.csdnimg.cn/blog_migrate/58a3873f47beecdfd3f77759345085db.png) ![](https://i-blog.csdnimg.cn/blog_migrate/89bcc09a4ab57393763bf74e46b55d03.png) ![](https://i-blog.csdnimg.cn/blog_migrate/0addfd80f503214d08348e3489604422.png) ![](https://i-blog.csdnimg.cn/blog_migrate/50b732429b8206167c2006a2f25d1071.png) ![](https://i-blog.csdnimg.cn/blog_migrate/784a2cba01b267d09037fd45ec13ca4b.png) ![](https://i-blog.csdnimg.cn/blog_migrate/7c992ce671c02b4be01249d9305ce884.png) ![](https://i-blog.csdnimg.cn/blog_migrate/e214573663522a553a5c4cccba7e2136.png) ![](https://i-blog.csdnimg.cn/blog_migrate/c5fc270903c416849134f569adca64eb.png) ![](https://i-blog.csdnimg.cn/blog_migrate/bdfe7f34eb6ecfdcfa36885485a4e29c.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a21b7acfc7a696166215398a7daaf4b2.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a46596d8a89929e925b91033b0bff489.png) ![](https://i-blog.csdnimg.cn/blog_migrate/1df93188ebb96dc0bf9f1a4ab9a63eac.png) ![](https://i-blog.csdnimg.cn/blog_migrate/3b6536ae393768432fd78f4155f97344.png) ![](https://i-blog.csdnimg.cn/blog_migrate/a1294ba33cdc4b89043f10682c326a82.png)