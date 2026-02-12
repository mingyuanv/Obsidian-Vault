---
title: "学习笔记之Linux常用指令及VMware的一些常见问题-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/136966317?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读351次，点赞3次，收藏4次。本文介绍了作者暂停FPGA学习后转向立创泰山派Linux系统操作的过程，包括SDK烧录教程和Linux常用命令如ls、mkdir、git等。此外，还提供了扩展VM内存、安装VMTools以实现剪贴板共享以及修复VM网络连接的步骤。"
tags:
  - "clippings"
---
本文介绍了作者暂停FPGA学习后转向立创泰山派Linux系统操作的过程，包括SDK烧录教程和Linux常用命令如ls、mkdir、git等。此外，还提供了扩展VM内存、安装VMTools以实现剪贴板共享以及修复VM网络连接的步骤。

摘要生成于 [C知道](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract) ，由 DeepSeek-R1 满血版支持， [前往体验 >](https://ai.csdn.net/?utm_source=cknow_pc_ai_abstract)

由于暂时没有 [FPGA](https://so.csdn.net/so/search?q=FPGA&spm=1001.2101.3001.7020) 的项目，对FPGA的学习先暂时告一段落，后续还会更新(PS:ROTS有机会再填坑吧)。这段时间，我将更新基于立创泰山派的 LINUX 系统操作。本次的学习将全程采用立创推出的泰山派（2+8版本），详细的SDK [烧录](https://so.csdn.net/so/search?q=%E7%83%A7%E5%BD%95&spm=1001.2101.3001.7020) 可以看立创的官方博客：https://lceda001.feishu.cn/wiki/SRaFwXXNUi5Lmtkf4nqcKhyxnJ3  
这一部分十分麻烦，笔者也是成功烦死了一众大佬（看不见图形界面知道很慌），具体也可以去b站搜索泰山派看具体视频（长达3小时）。

---

## 1\. Linux指令

<table align="center"><thead><tr><th>种类</th><th>表达式</th><th>作用</th></tr></thead><tbody><tr><td colspan="1" rowspan="3">ls</td><td><p>ls /a/b/directory</p></td><td><p>列出指定目录下的文件和目录</p></td></tr><tr><td>ls -l</td><td><p>以长格式列出文件和目录的详细信息，包括文件权限、所有者、大小等</p></td></tr><tr><td>ls -a</td><td><p>显示所有文件，包括隐藏文件</p></td></tr><tr><td colspan="1" rowspan="2">mkdir</td><td><p>mkdir 目录</p></td><td>创建文件夹</td></tr><tr><td><p>mkdir -p /路径/目录</p></td><td>递归创建目录</td></tr><tr><td></td><td>cd</td><td><p>进入当前用户的主目录(通常是 <code>/home/username)</code></p></td></tr><tr><td colspan="1" rowspan="4">cd</td><td>cd 目录</td><td>进入指定目录</td></tr><tr><td><p>cd..</p></td><td>进入上级目录</td></tr><tr><td>cd../..</td><td>进入上上级目录</td></tr><tr><td>cd -</td><td>进入上次访问目录</td></tr><tr><td>pwd</td><td>pwd</td><td>显示当前工作目录的路径</td></tr><tr><td>touch</td><td>touch 文件名</td><td>创建空文件</td></tr><tr><td>cat</td><td>cat 文件名</td><td>查看文件内容，可用于链接文件并显示</td></tr><tr><td>cp</td><td>cp 文件名</td><td>复制文件或目录</td></tr><tr><td colspan="1" rowspan="3">rm</td><td>rm file.txt</td><td>删除文件</td></tr><tr><td>rm -r directory</td><td>删除目录</td></tr><tr><td>rm -rf*</td><td>删库跑路（不可逆）</td></tr><tr><td colspan="1" rowspan="4">mv</td><td><p>mv file.txt /a/b/destination/</p></td><td>将文件移动到目标位置</td></tr><tr><td>mv oldname.txt newname.txt</td><td>将文件重命名</td></tr><tr><td>mv file1.txt file2.txt /a/b/destination/</td><td>将多个文件移动到目标位置</td></tr><tr><td>mv directory/ /a/b/destination/</td><td>将目录移动到目标位置</td></tr><tr><td>grep</td><td>grep -r -n "要查找的字符" *</td><td><p>在当前目录及其子目录中 <span>递归</span> 搜索包含字符串，并在找到的行前显示行号，其中*可以是全目录也可以是子目录</p></td></tr><tr><td>find</td><td><p>find [路径] [选项] [操作]</p></td><td>查找文件</td></tr><tr><td>tar</td><td><p>tar [选项] [压缩文件名] [文件或目录...]</p></td><td><p>常用文件打包和压缩工具：</p><p>-c：创建压缩文件</p><p>-x：提取压缩文件</p><p>-z：使用gzip <span>算法</span> 压缩文件</p><p>-j：使用bzip2算法压缩文件</p><p>-f：指定归档文件名称</p><p>-v：显示详细处理信息</p></td></tr></tbody></table>

## 2\. Git常用指令

在Linux中，Git是一个非常强大的分布式 版本控制系统 ，它可以帮助开发者更有效地管理项目的代码、跟踪代码的变更历史，以及协作开发。以下是Git在Linux中的一些主要用途这里简单的列出几个git优点：

- 多人协作开发：Git 允许多个团队成员同时对同一代码库进行修改和提交，有效提高协作开发效率。
- 版本控制 ：Git 记录所有修改历史，并且可以方便地回退或者查看历史版本，可以避免由于误操作导致代码丢失的问题。
- 分支管理：Git 支持创建并管理多个分支，可以在不影响主干代码的同时，方便进行代码测试、版本迭代、功能开发、修复等操作。
- 远程仓库：Git 可以轻松地与远程仓库进行交互，方便在多个不同的部署环境中同步代码库。

| 指令 | 作用 |
| --- | --- |
| git status | 查看仓库状态 |
| git add 文件名 | 添加文件到暂存区 |
| git commit -m "提交信息" | 提交更改到仓库 |
| git log | 查看提交历史 |
| git branch 分支名 | 创建新分支 |
| git checkout 分支名 | 切换到分支 |
| git push 远程仓库名 分支名 | 推送代码 |
| git pull 远程仓库名 分支名 | 拉取代码 |
| git checkout | 撤销对文件的修改 |

## 3\. 扩展虚拟机内存（VM）

前段时间在边缘SDK时出现了存储空间不足的问题，然后发现单纯的在虚拟机设置页面扩展并不能起作用（需要在关机时使用），如下图所示。之后在看到其他博主的方法后解决了这一问题，详细地址如下： [VMware Tools （ubuntu系统）安装详细过程与使用\_怎样安装ubuntu中的tools-CSDN博客](https://blog.csdn.net/zxf1242652895/article/details/78203473 "VMware Tools （ubuntu系统）安装详细过程与使用_怎样安装ubuntu中的tools-CSDN博客") 。

![](https://i-blog.csdnimg.cn/blog_migrate/80d67bcc9b837f8231f47fc6defd9384.png)

![](https://i-blog.csdnimg.cn/blog_migrate/03e9b4d861c35c612da0dc029f72640b.png)

在设置完上述部分后，我们继续开机，并且在命令行输入：

```csharp
sudo apt-get install gparted
```

在安装完毕之后，再输入：

```
sudo gparted
```
![](https://i-blog.csdnimg.cn/blog_migrate/05e72e97e4705666c3bae5c7c23d555b.png)

打开后可以看到这样的画面，然后选中要扩展的磁盘，点击resize（橘色小箭头），之后进行分配应用即可。

![](https://i-blog.csdnimg.cn/blog_migrate/02f60bc23a4ddbe78e449aa420389d5d.png) ![](https://i-blog.csdnimg.cn/blog_migrate/ab925322f411f7c271f12fb4770f5dfd.png)

## 4\. 安装VMTools

想必很多新手和笔者一样都在吐槽自己的主机和VM的虚拟机不能共享剪切板（主要是手打代码太麻烦了而且容易出错），这里可以使用VMtools进行一个共享剪切板的操作。具体的操作流程可以参考： [VMware Tools （ubuntu系统）安装详细过程与使用\_怎样安装ubuntu中的tools-CSDN博客](https://blog.csdn.net/zxf1242652895/article/details/78203473 "VMware Tools （ubuntu系统）安装详细过程与使用_怎样安装ubuntu中的tools-CSDN博客")

这里主要讲一下笔者发现的一个小bug（可能是我自己哪里细节不太好），笔者直接将软盘生成的VMtools压缩文件利用命令tar解压时会产生解压不出来的情况（直接提前到XXX也不行），然后便可以将他先复制到你想要的目录再选择解压到此处（虽然不知道为什么0.0）。

## 5\. 修复VM的网络连接

VMware 虚拟机连接不了网络的问题可能有多种原因，笔者今天突然发现VM断网了，找了很多方法都没有用，结果发现连网络连接图标都没有，这里附上最后找到并成功解决问题的一篇帖子：

[Ubuntu无网络连接/无网络标识解决方法\_ubuntu网络连接不上-CSDN博客](https://blog.csdn.net/qq_45400167/article/details/125874887 "Ubuntu无网络连接/无网络标识解决方法_ubuntu网络连接不上-CSDN博客")

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/136966317

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

![](https://i-blog.csdnimg.cn/blog_migrate/80d67bcc9b837f8231f47fc6defd9384.png)