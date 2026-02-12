---
title: "shell 创建子进程及并行延时执行命令方法_shell 子进程-CSDN博客"
source: "https://blog.csdn.net/weixin_42330983/article/details/128284931?ops_request_misc=%257B%2522request%255Fid%2522%253A%25229963551f57246d7c067707618454e88c%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=9963551f57246d7c067707618454e88c&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-128284931-null-null.142^v102^pc_search_result_base7&utm_term=%E5%BD%93%E5%89%8DShell%E5%88%9B%E5%BB%BA%E7%9A%84%E5%AD%90%E8%BF%9B%E7%A8%8B&spm=1018.2226.3001.4187"
author:
published:
created: 2025-04-27
description: "文章浏览阅读2.2k次，点赞2次，收藏8次。子进程，是从父子进程的概念出发的，unix操作系统的进程从init进程开始（init进程为1,而进程号0为系统原始进程，以下讨论的进程原则上不包括进程0)均有其对应的子进程，就算是由于父进程先行结束导致的孤儿进程，也会被init领养，使其父进程ID为1。也因为所有的进程均有父进程，事实上，所有进程的创建，都可视为子进程创建过程。在apue一书里提及unix操作系统进程的创建，大抵上的模式都是进行fork+exec类系统调用。理解子进程的创建执行，需要至少细分到二个步骤，包括。_shell 子进程"
tags:
  - "clippings"
---
## shell 创建子进程方法

### 1\. 什么是shell子进程

子进程，是从父子进程的概念出发的， [unix操作系统](https://so.csdn.net/so/search?q=unix%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F&spm=1001.2101.3001.7020) 的进程从init进程开始（init进程为1,而进程号0为系统原始进程，以下讨论的进程原则上不包括进程0)均有其对应的子进程，就算是由于父进程先行结束导致的孤儿进程，也会被init领养，使其父进程ID为1。  
也因为所有的进程均有父进程，事实上，所有进程的创建，都可视为子进程创建过程。在apue一书里提及unix操作系统进程的创建，大抵上的模式都是进行fork+exec类系统调用。  
理解子进程的创建执行，需要至少细分到二个步骤，包括  
1） 通过fork创建子进程环境，  
2） 通过exec加载并执行进程代码。  
而shell子进程（以下均称subshell），顾名思义，就是由“当前shell进程”创建的一个子进程

### 2\. <span style="background:#b1ffff">shell什么情况下会产生子进程</span>

#### 2.1 提交后台作业 &

```bash
command &
1
```

#### 2.2 管道 |

```bash
command1 | command2
1
```

#### 2.3 括号命令列表 ()

```bash
(cmd1;cmd2;cmd3)
1
```

#### 2.4 <span style="background:#affad1">执行外部脚本、程序</span>

```bash
bash ./test.sh
1
```

说明：大致上子进程的创建包括以上四种情况了。需要说明的是只要是符合上边四种情况之一，便会创建(fork)子进程，<span style="background:#d3f8b6">不因是否是函数，命令，或程序，也不会因为是内置函数(buitin)或是外部程序。  </span>
shell中有一个变量<span style="background:#affad1"> BASH_SUBSHELL 可以查看子 shell 的信息</span>，该变量的初始值为0，每启动一个子 shell 该变量就会自动加1。  
由下面的案例可以看到bash\_subshell在子进程中的值是1，可以确定（）开启了子进程。

```bash
[root@imx6sabresd ~]# cat test.sh 
#!/bin/bash
# 功能描述：子Shell演示示例
# 父Shell
#set -x
hi="parent shell"
echo "+++++++++++++"
echo -e "\033[31m+ 父Shell +\033[0m"
echo "+++++++++++++"
echo "PWD=$PWD"
echo "PID=$$"
echo "bash_subshell=$BASH_SUBSHELL"
# 通过()开启子Shell
(
sub_hi="subshell"
echo -e "\t+++++++++++++"
echo -e "\t\033[33m+ 子Shell +\033[0m"
echo -e "\t+++++++++++++"
echo -e "\tPWD=$PWD"
echo -e "\tPID=$$"
echo -e "\tbash_subshell=$BASH_SUBSHELL"
echo -e "\thi=$hi"
echo -e "\tsubhi=$sub_hi"
cd /opt;echo -e "\tPWD=$PWD"
)
# 返回父Shell
echo "+++++++++++++++++"
echo "+ 返回父Shell +"
echo "+++++++++++++++++"
echo "PWD=$PWD"
echo "hi=$hi"
echo "sub_hi=$sub_hi"
echo "bash_subshell=$BASH_SUBSHELL"
123456789101112131415161718192021222324252627282930313233
```

结果如下：子进程方法  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/73afe8def594ce6628f91b4f807861f1.png)

### 3.使用括号来创建子进程

例子：  
如果在脚本中加入一个延时执行程序，并发执行，不想要影响源程序执行，可以引入括号

```bash
echo "start"
(sleep 5
echo "hello world") &
echo "1"
sleep 1
echo "2"
sleep 1
echo "3"
sleep 1
echo "4"
sleep 0.5
echo "4.5"
123456789101112
```

结果如下：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/924844aa533138aabf4d38c2ca8acbb1.png)  
参考链接：https://zhuanlan.zhihu.com/p/543308214

打赏作者

¥1 ¥2 ¥4 ¥6 ¥10 ¥20

扫码支付： ¥1

获取中

扫码支付

您的余额不足，请更换扫码支付或 [充值](https://i.csdn.net/#/wallet/balance/recharge?utm_source=RewardVip)

打赏作者

实付 元

[使用余额支付](https://blog.csdn.net/weixin_42330983/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏 搜索 ![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

![](https://i-blog.csdnimg.cn/blog_migrate/73afe8def594ce6628f91b4f807861f1.png) ![](https://i-blog.csdnimg.cn/blog_migrate/924844aa533138aabf4d38c2ca8acbb1.png)