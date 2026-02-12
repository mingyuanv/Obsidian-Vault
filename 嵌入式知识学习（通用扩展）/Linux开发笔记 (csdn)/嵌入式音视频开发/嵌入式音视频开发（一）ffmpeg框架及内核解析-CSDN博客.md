---
title: "嵌入式音视频开发（一）ffmpeg框架及内核解析-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/145543066?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.3k次，点赞21次，收藏17次。前节简单介绍了ffmpeg，本节进行FFmpeg的整体架构和内核解读，以及常用命令行的使用。_嵌入式音视频开发"
tags:
  - "clippings"
---
## 系列文章目录

[嵌入式](https://so.csdn.net/so/search?q=%E5%B5%8C%E5%85%A5%E5%BC%8F&spm=1001.2101.3001.7020) 音视频开发（零）移植ffmpeg及推流测试  
嵌入式 [音视频开发](https://so.csdn.net/so/search?q=%E9%9F%B3%E8%A7%86%E9%A2%91%E5%BC%80%E5%8F%91&spm=1001.2101.3001.7020) （一）ffmpeg框架及内核解析  
嵌入式音视频开发（二） [ffmpeg](https://so.csdn.net/so/search?q=ffmpeg&spm=1001.2101.3001.7020) 音视频同步  
嵌入式音视频开发（三）直播协议及编码器

---

---

## 前言

  前节简单介绍了ffmpeg，本节进行FFmpeg的整体架构和内核解读，以及常用命令行的使用。

## 一、ffmpeg的内核

### 1.1 框架解析

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/dfe88a0bff784df6b80239670459b188.png)  
  从图像中，我们可以看到FFmpeg 主要由以下核心库组成，每个库负责不同的功能：

- libavformat —— 负责解析和封装多媒体文件（如 MP4、FLV、MKV）。
- libavcodec —— 负责音视频编解码（支持 H.264、AAC、MP3 等）。
- libavfilter —— 提供音视频滤镜功能（如添加水印、调整亮度）。

  除此之外还有附件库：

- libavutil —— 提供通用工具函数（如内存管理、日志处理）。
- libswscale —— 处理视频像素格式转换和缩放（如 RGB 转 YUV）。
- libswresample —— 处理音频格式转换（如 44.1kHz 到 48kHz）。

### 1.2 内核解析

  FFmpeg 的底层由 C 语言实现，核心包含多个关键部分，如下图所示：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/25d02bb9aa6249a38e678174a73360f1.png)  
  例如我们现在有一个视频文件（包含音频流和视频流），我们需要将它播放或者推流出来，那我们的思路是什么？无非就是先解包，然后解码，再编码，最后送到对应的输出设备（外设或者服务器流）。具体来说，我们在使用ffmpeg进行音视频处理的时候通常需要经历以下几个阶段：解封装（输入）、解码、滤镜处理（可选）、编码（可选）以及再封装（输出）。  
  输入阶段（解封装）：使用AVFormatContext来表示输入媒体文件或流。通过avformat\_open\_input()打开文件，并使用avformat\_find\_stream\_info()读取流信息。这个阶段主要任务是解析文件格式，识别其中的音视频流；  
  解码阶段：对于每一条流（音频或视频），找到对应的解码器并创建AVCodecContext实例。使用avcodec\_find\_decoder()查找合适的解码器，并用avcodec\_open2()打开它。然后通过av\_read\_frame()循环读取数据包，并使用avcodec\_send\_packet()与avcodec\_receive\_frame()进行解码操作；  
  滤镜处理（可选）：如果需要对音频或视频应用滤镜，会涉及到AVFilterGraph和AVFilterContext。你需要构建滤镜图，配置所需滤镜链，比如裁剪、缩放、颜色校正等。使用avfilter\_graph\_create\_filter()添加滤镜，并通过avfilter\_link()连接它们；  
  编码阶段（可选）：在某些应用场景下，如推流时，可能需要将解码后的帧重新编码。这一步骤与解码类似，但需使用编码器而不是解码器。首先通过avcodec\_find\_encoder()选择编码器，然后设置编码参数并打开编码器。之后，使用avcodec\_send\_frame()发送帧给编码器，并从avcodec\_receive\_packet()获取编码后的数据包。  
  输出阶段（再封装）：将编码后的数据包写入到输出文件或推送至流媒体服务器。这通常涉及再次使用AVFormatContext，但对于输出来说，可能是调用avformat\_write\_header()初始化输出格式，然后使用av\_interleaved\_write\_frame()写入数据包，最后调用av\_write\_trailer()完成输出。

### 1.3 相关结构体

  在ffmpeg处理音视频的过程中，我们着重用到的就是以下几个结构体：AVFormatContext、AVCodecContext以及AVFilterContext。  
（1） **AVFormatContext** ：解析文件格式，识别音视频流并准备后续处理

- 创建输出格式上下文
```c
// 统一不同输出格式（如 MP4、FLV、RTMP）的初始化流程
int avformat_alloc_output_context2(AVFormatContext **ctx, AVOutputFormat *oformat,
                                   const char *format_name, const char *filename);
参数说明：
- ctx:指向 AVFormatContext 指针的指针
- oformat:指向 AVOutputFormat结构体，表示输出格式个，传入 NULL会自动匹配
- format_name:这是一个字符串，指定输出格式的名字，常见的格式名称包括 "mp4", "flv", "rtmp" 等
- filename:指定输出文件的路径或 URL
12345678
```
- 文件 I/O：支持 avio\_read()、avio\_write() 操作
```c
// 该函数用于从媒体文件中读取一帧数据（音频或视频包），并将其存储在 AVPacket 结构体中
int av_read_frame(AVFormatContext *s, AVPacket *pkt);
说明：
- s: 指向 AVFormatContext，包含输入文件的所有信息
- pkt: 指向 AVPacket，用于存储读取到的数据包，AVPacket 包含了编码后的数据和相关的时间戳等信息
12345
```

  实际上，FFmpeg 中通常不使用av\_write\_frame() 的函数，而选择之功能最接近的是 av\_interleaved\_write\_frame() 。相较于av\_write\_frame()，该函数可以自动管理交织（interleave）顺序，确保音频和视频帧按时间戳交错排列。

```c
// 直接写入一个交织的 AVPacket 到输出文件
int av_interleaved_write_frame(AVFormatContext *s, AVPacket *pkt);
参数说明：
- s: 指向 AVFormatContext，包含输出文件的所有信息。
- pkt: 指向 AVPacket，包含要写入的数据包。
12345
```
- 流管理：音视频数据流以 AVStream 形式存在
```c
// 添加一个新的流（音频、视频或其他数据流）。
AVStream *avformat_new_stream(AVFormatContext *s, const AVCodec *c);
参数说明：
- s: 指向目标AVFormatContext的指针
- c: 可选的指向AVCodec结构体的指针,如果提供了此参数，则新流将自动关联到该编解码器,如果为NULL，则需要手动设置流的相关属性

// 用于写入媒体文件的头部信息，并且准备格式上下文进行后续的数据写入操作
int avformat_write_header(AVFormatContext *s, AVDictionary **options);
参数说明：
- s: 指向已经配置好的AVFormatContext的指针
- options: 一个指向AVDictionary类型的指针，用于传递额外的选项给复用器

// 用于打开一个URL以进行I/O操作，通常用于指定输出文件的位置
int avio_open(AVIOContext **s, const char *url, int flags);
参数说明：
- s: 输出参数，指向将被分配的AVIOContext结构体的指针
- url: 要打开的资源路径或URL
- flags: 打开模式标志，如读取(AVIO_FLAG_READ)、写入(AVIO_FLAG_WRITE)等
123456789101112131415161718
```
- 封装/解封装器：
```c
// 解析格式
int avformat_find_stream_info(AVFormatContext *ic, AVDictionary **options);
参数说明：
- ic: 指向 AVFormatContext，包含输入文件的所有信息
- options: 可选参数，指向AVDictionary 结构体，可以传递一些额外的选项给解复用器
12345
```

（2） **AVCodecContext** ：配置解码器/编码器参数，执行编解码操作

- 初始化编码器/解码器
```c
// 该函数负责注册所有编解码器（新版本中avcodec_register_all() 不再是必需的
void avcodec_register_all(void);
12
```
```c
// 根据给定的编解码器ID查找对应的解码器编码器只需要将decoder换为encoder即可）
const AVCodec *avcodec_find_decoder(enum AVCodecID id);

// 过名称来查找解码器编码器只需要将decoder换为encoder即可）
const AVCodec *avcodec_find_decoder_by_name(const char *name);
12345
```
```c
// 分配并初始化 AVCodecContext
AVCodecContext *avcodec_alloc_context3(const AVCodec *codec);
参数说明：
- codec: 指向 AVCodec 结构体，表示将使用的编解码器，如果不确定编解码器，可以传递 NULL
1234
```
```c
// 打开编码器
int avcodec_open2(AVCodecContext *avctx, const AVCodec *codec, AVDictionary **options);
参数说明：
- avctx: 指向要初始化的AVCodecContext
- codec: 指向已选择的 AVCodec 结构体
- options:指向 AVDictionary，用于存储通过 av_dict_set() 函数设置各种选项
123456
```
- 解码过程
```c
// 将压缩的数据包（AVPacket）发送给解码器进行解码。
int avcodec_send_packet(AVCodecContext *avctx, const AVPacket *avpkt);
参数说明：
- avctx: 指向 AVCodecContext，包含解码器的所有信息
- avpkt: 指向要解码的AVPacket结构体，如果avpkt为 NULL，则表示没有更多的数据包需要发送
12345
```
```c
// 从解码器接收解码后的帧（AVFrame）
int avcodec_receive_frame(AVCodecContext *avctx, AVFrame *frame);
参数说明：
- avctx: 指向 AVCodecContext
- frame: 指向 AVFrame结构体的指针，用于存储解码后的帧数据
12345
```
- 编码过程
```c
// 将原始帧（AVFrame）发送给编码器进行编码。
int avcodec_send_frame(AVCodecContext *avctx, const AVFrame *frame);
参数说明：
- avctx: 指向 AVCodecContext
- frame: 指向要编码的 AVFrame 结构体
12345
```
```c
// 从编码器接收编码后的数据包（AVPacket）
int avcodec_receive_packet(AVCodecContext *avctx, AVPacket *avpkt);
参数说明：
- avctx: 指向 AVCodecContext
- avpkt: 指向 AVPacket 结构体，用于存储编码后的数据包
12345
```
- 优化
	- 采用 SIMD 指令集加速（x86 SSE、ARM NEON），内部使用 Threading API 进行多线程优化

（3） **AVFilterContext** ：构建和管理滤镜链

- 创建和配置滤镜链
	- avfilter\_graph\_create\_filter() 创建滤镜链
	- avfilter\_graph\_parse\_ptr() 解析滤镜链字符串，并添加到滤镜图中
- 编辑滤镜链
	- av\_buffersrc\_add\_frame() 将数据帧添加到滤镜图的输入端。
	- av\_buffersink\_get\_frame() 从滤镜图的输出端获取处理后的数据帧。

（4） **libswscale** ：图像处理

```c
//  创建一个缩放/转换上下文，包含了所有必要的参数和状态信息
struct SwsContext *sws_getContext(
    int srcW, int srcH, enum AVPixelFormat srcFormat,
    int dstW, int dstH, enum AVPixelFormat dstFormat,
    int flags, SwsFilter *srcFilter,
    SwsFilter *dstFilter, const double *param);
 - 参数说明：
    - srcW, srcH: 源图像的宽度和高度。
    - srcFormat: 源图像的颜色格式（如 AV_PIX_FMT_RGB24）。
    - dstW, dstH: 目标图像的宽度和高度。
    - dstFormat: 目标图像的颜色格式（如 AV_PIX_FMT_YUV420P）。
    - flags: 缩放算法标志（如 SWS_BILINEAR）。

// 执行缩放/格式转换
int sws_scale(struct SwsContext *c, const uint8_t *const srcSlice[], const int srcStride[],  
                        int srcSliceY,  int srcSliceH, uint8_t *const dst[],  const int dstStride[]);
参数说明：
- c:指向 SwsContext 结构体，包含了缩放和格式转换所需的所有上下文信息
- srcSlice[]:源图像的数据指针数组
- srcStride[]: 源图像每行的步长（字节数）
- srcSliceY:开始转换的源图像的高度偏移量，通常设置为 0 表示从图像顶部开始
- srcSliceH: 要转换的源图像的高度
- dst[]: 目标图像的数据指针数组
- dstStride[]: 目标图像每行的步长
123456789101112131415161718192021222324
```

| 色彩格式 | 说明 |
| --- | --- |
| AV\_PIX\_FMT\_YUV420P | YUV 4:2:0，常见于 H.264 编码 |
| AV\_PIX\_FMT\_YUYV422 | YUV 4:2:2，部分摄像头格式 |
| AV\_PIX\_FMT\_RGB24 | 每像素 24 位 RGB |
| AV\_PIX\_FMT\_BGR24 | 每像素 24 位 BGR |
| AV\_PIX\_FMT\_NV12 | 现代 GPU 常用的 YUV 4:2:0 |

（5） **libswresample** ：音频格式转换

- 采样率转换、通道数调整
	- swr\_alloc\_set\_opts()（创建转换上下文）
	- swr\_convert()（执行转换）

（6） **libavutil** ：通用工具库，如：数据类型转换、时间基准处理（AVRational）、日志管理、哈希计算（MD5、SHA）

### 1.4 FFmpeg内部数据流

#### 1.4.1 典型的解码流程

```c
avformat_open_input()   // 打开媒体文件
avformat_find_stream_info()  // 解析流信息
avcodec_find_decoder()   // 查找解码器
avcodec_alloc_context3() // 分配解码上下文
avcodec_open2()  // 打开解码器
while (av_read_frame()) {
    avcodec_send_packet() // 送入解码器
    avcodec_receive_frame() // 获取解码后数据
}
123456789
```

#### 1.4.2 典型的编码与推流流程

```c
avformat_alloc_output_context2()  // 创建输出格式上下文
avcodec_find_encoder()  // 查找编码器
avcodec_alloc_context3()  // 分配编码上下文
avcodec_open2()  // 打开编码器
while (获取原始帧) {
    avcodec_send_frame()  // 送入编码器
    avcodec_receive_packet()  // 获取压缩数据
    av_interleaved_write_frame()  // 推流（可选）
}
123456789
```

#### 1.4.3 典型的滤镜处理流程

```c
avfilter_graph_alloc()  // 创建滤镜图
avfilter_graph_parse_ptr()  // 解析滤镜描述
avfilter_graph_config()  // 配置滤镜
while (处理帧) {
    av_buffersrc_add_frame()  // 送入滤镜
    av_buffersink_get_frame()  // 获取输出
}
1234567
```

## 二、常用命令行工具及语法

### 2.1 基本语法

```bash
ffmpeg <global-options> <input-options> -i <input> <output-options> <output>  
1
```
- 全局参数（global-options）：日志输出，文件覆盖等全局选项.
- 输入文件参数（input-options）：读取文件的输入选项
- 输出文件参数（output-options）：转换（编解码器，质量等）或过滤或流映射

  常用高频命令行参数如下所示：

| 参数 | 说明 |
| --- | --- |
| \-c | 指定编码器 |
| \-c copy | 直接复制，不经过重新编码 |
| \-c:v | 指定视频编码器 |
| \-c:a | 指定音频编码器 |
| \-i | 指定输入文件 |
| \-an | 去除音频流 |
| \-vn | 去除视频流 |
| \-preset | 指定输出的视频质量，会影响文件的生成速度，有以下几个可用的值 ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow |
| \-y | 不经过确认，输出时直接覆盖同名文件 |

### 2.2 视频/音频格式转换

**格式转换**

```bash
// 将 input.mp4 转换为 output.avi（自动检测编解码器）
ffmpeg -i input.mp4 output.avi

// 将 MP3 转换为 WAV
ffmpeg -i input.mp3 output.wav
12345
```

**指定编码格式**

```bash
// 使用 H.264 编码 和 AAC 音频编码 进行转换
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
12
```

### 2.3 视频编辑

**裁剪视频**

```bash
// 截取区间（截取 10-30 秒）
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:30 -c copy output.mp4
-ss：起始时间（秒或 hh:mm:ss）
-to：结束时间

// 按时长裁剪（从 10 秒处开始，截取 20 秒）
ffmpeg -i input.mp4 -ss 10 -t 20 -c copy output.mp4
-t：截取的持续时间

// 裁剪视频画面（区域裁剪）
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4
- crop=width:height:x:y
    -(640, 480)：裁剪后的宽高
    -(100, 50)：裁剪起始位置（左上角坐标）
1234567891011121314
```

**视频合并**

```bash
// 直接合并多个相同格式的视频
ffmpeg -i "concat:input1.mp4|input2.mp4" -c copy output.mp4

// 不同格式视频合并（需要重新编码）
ffmpeg -i input1.mp4 -i input2.mp4 -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]" 
    /-map "[outv]" -map "[outa]" output.mp4
- concat=n=2:v=1:a=1：合并 2 个视频，带视频流 v=1 和音频流 a=1
1234567
```

### 2.3 音频处理

**提取音频**

```bash
ffmpeg -i input.mp4 -q:a 0 -map a output.mp3
1
```

**替换视频的音频**

```bash
ffmpeg -i input.mp4 -i new_audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4
1
```

**调整音量**

```bash
ffmpeg -i input.mp3 -af "volume=2.0" output.mp3
    - volume=2.0：音量变为原来的 2 倍
12
```

### 2.4 录屏与推流

**录屏**

```bash
ffmpeg -f gdigrab -framerate 30 -i desktop output.mp4
1
```

**录制摄像头**

```bash
ffmpeg -f v4l2 -i /dev/video0 output.mp4
 - /dev/video0：摄像头设备
12
```

**直播推流（RTMP）**

```bash
ffmpeg -re -i input.mp4 -c:v libx264 -b:v 1000k -f flv rtmp://live_url
 - rtmp://live_url：推流服务器地址
12
```

---

**免责声明：本文参考了网上公开的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/145543066

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