---
title: "嵌入式音视频开发（零）移植ffmpeg及推流测试_ffmpeg移植-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/145419071?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读906次，点赞6次，收藏18次。笔者最近需要进行网络推流项目的学习，从今天开始将更新这部分内容，希望大家可以一起学习。_ffmpeg移植"
tags:
  - "clippings"
---
## 系列文章目录

[嵌入式](https://so.csdn.net/so/search?q=%E5%B5%8C%E5%85%A5%E5%BC%8F&spm=1001.2101.3001.7020) 音视频开发（零）移植ffmpeg及推流测试  
嵌入式 [音视频开发](https://so.csdn.net/so/search?q=%E9%9F%B3%E8%A7%86%E9%A2%91%E5%BC%80%E5%8F%91&spm=1001.2101.3001.7020) （一）ffmpeg框架及内核解析  
嵌入式音视频开发（二） [ffmpeg](https://so.csdn.net/so/search?q=ffmpeg&spm=1001.2101.3001.7020) 音视频同步  
嵌入式音视频开发（三）直播协议及编码器

---

## 前言

笔者最近需要进行<span style="background:#b1ffff">网络推流项目</span>的学习，从今天开始将更新这部分内容，希望大家可以一起学习。

---

## 一、ffmpeg

  FFmpeg 是一个<span style="background:#affad1">开源的、多功能的命令行工具集</span>，广泛用于视频、音频的处理和转换。它由几个组件构成，其中最核心的就是 ffmpeg 命令行工具、libavcodec 库（用于编解码）、libavformat 库（用于处理文件格式）等。它不仅仅是一个工具，还是一个包含多种库的多媒体处理框架，广泛用于视频编辑、流媒体、编码、解码等场景。  
  FFmpeg由三个组件构成：ffmpeg（核心命令行工具，用于处理音视频文件）、ffplay（一个简单的媒体播放器，基于 FFmpeg 库）以及ffprobe（用于流式传输协议（如 RTMP、RTSP）的相关工具）。它可以实现视频格式转换、视频流媒体、视频编辑、音频提取、批处理等功能。

## 二、前期准备

[移植文件](https://download.csdn.net/download/sincerelover/90362205)

### 2.1 ffmpeg的移植

  Ubuntu系统可以使用apt安装工具进行简易安装，如果想获取最新版本则需要手动安装。  
  如果是板级添加ffmepg则可以参考立创吴工分享的步骤进行操作即可 [【Buildroot】添加ffmpeg](https://lceda001.feishu.cn/wiki/AOQpwvlm7iZcPOkYoyvcGk1wnrQ?login=from_csdn) ，开发板上Ubuntu系统这样也可以添加成功。

### 2.2 流媒体服务器

  这里笔者使用的是采用 [mediamtx](https://github.com/bluenviron/mediamtx/releases/) ，这是一个很简单的推流服务器，而且不需要额外配置环境。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/611274d3a4994764a228674ae0f1f16a.png)  
  这里根据需求选择对于的版本即可，例如你需要在PC端Linux环境下就选则XXX\_linux\_amd64.tar.gz，而在arm端则选择对应的armX框架，例如笔者选择的是XXX\_linux\_amdv8.tar.gz。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/19b13901eb2c416e9394e350076ae202.png#pic_center)  
  下载完成后进入文件夹，可以看到以上3个文件拷贝，将其到开发板并启动服务（切记要先启动再推流）。

```bash
# 在后台运行mediamtx流媒体服务器
./mediamtx &
12
```

  除此之外，nginx作为老牌流服务器，在链接稳定性上还是更胜一筹，如果大家会自己编译也可以选择这个，在笔者的压缩包有已经编好的文件，大家也可以直接移植到arm上（可能会提升缺少logs/eroXX文件，你直接创建一个就可以了）。  
  最后采用`./nginx -p /etc/nginx` 执行，采用 `ps aux|grep nginx` 进行查询是否开启。

### 2.3 VLC播放器

  常用的工具为 [VLC播放器](https://www.videolan.org/) （以后也可以自己写一个类似的拉流播放器），选择媒体→打开网络串流→输入推流地址，如下所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/46f71d99a1dd48cea36ad8ff104363f8.png)

## 三、推流测试

```bash
# 进行网络推流，这里要选择你自己的摄像头和推流地址
ffmpeg -f v4l2 -i /dev/video4 -bufsize 2000k -async 1 -framerate 30 -pix_fmt yuv420p -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -rtsp_transport tcp -f rtsp rtsp://192.168.234.25:8554/streamSS

# 指令解释：
 -f v4l2：指定输入格式为 Video4Linux2，这是 Linux 操作系统下视频设备的一个接口。
 -i /dev/video4：指定Linux 下的视频设备节点，代表一个视频捕捉设备。
 -bufsize 2000k：设置内部缓冲区大小为 2000k 字节，这有助于控制数据流的速率。
 -async 1：这个参数用于调整音视频同步。值 1 表示允许小的同步调整。
 -framerate 30：设置视频捕捉的帧率。
 -pix_fmt yuv420p：指定像素格式。yuv420p 是一种视频像素格式，属于 YUV 家族。
 -vcodec libx264：指定视频编码器为 libx264，这是一个非常高效的视频编码库。
 -preset:v ultrafast：设置编码预设。ultrafast 预设意味着编码速度最快，但可能会牺牲压缩效率和质量。
 -tune:v zerolatency：优化编码器设置以减少延迟。这对于实时流非常有用。
 -rtsp_transport tcp：指定 RTSP 流的传输协议为 TCP。相比于 UDP，TCP 提供了更可靠的传输。
 -f rtsp [推流地址]：指定输出格式为 RTSP（实时流协议），用于实时视频流的传输。
123456789101112131415
```

  这里的播放效果和网络、芯片性能和摄像头性能均有关系，要想获取更好的显示效果可以根据需求选择。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/18165f51c9bd47a2aa2b733937298189.png#pic_center)

---

**免责声明：本文参考了网上公开的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/145419071

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