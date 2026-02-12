---
title: "嵌入式音视频开发（二）ffmpeg音视频同步-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/145570479?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.4k次，点赞18次，收藏18次。前文中已经讲述了音视频处理的流程，需要我们将音频数据和视频数据分开处理，这个时候我们就需要音视频同步操作。"
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

  前文中已经讲述了音视频处理的流程，需要我们将音频数据和视频数据分开处理，这个时候我们就需要音视频同步操作。

## 一、音视频同步

  我们平常看视频的时候最烦恼的就是各种音画不同步，例如音频是100ms延时而视频需要150ms延时才能到达，这其中我们就需要进行音视频同步来解决这个问题。 音视频同步是多媒体处理中的一个关键问题，常用方法包括三种不同的同步策略：以视频为基准、以音频为基准和以外部时钟为基准。

### 1.1 基础概念

  在FFmpeg进行音视频解码时， **PTS** (Presentation Time Stamp) 是一个非常重要的概念，它表示每一帧数据（音频帧或视频帧）的展示时间，即该帧应该在播放设备上显示的精确时间。  
**时间基** （Timebase）是一个分数，表示每秒的时间单位。它用于将 PTS和 DTS（从基于时钟滴答的计数转换为实际的时间（秒）。常见的表示形式为 1/fps 或 1/sample\_rate例如，假设视频流的时间基准是1/90000，那么每个时间单位代表1/90000秒。因此，PTS值为90000时，相当于1秒。实际上ffmpeg内部存在多种时间基，在不同的阶段（结构体）中，对应的时间基的值都不相同。

| 表示方法 | 结构体 | 描述 | 作用 |
| --- | --- | --- | --- |
| time\_base | AVStream | 流的时间基 | 用于将 PTS 和 DTS 转换为实际时间 |
| time\_base | AVCodecContext | 编码器或解码器的时间基 | 用于内部处理和同步 |
| video\_codec\_timebase audio\_codec\_timebase | AVFormatContext | 格式上下文的时间基 | 用于整体管理和同步 |

  值得注意的是，虽然 AVPacket 和 AVFrame 本身没有直接的时间基字段，但它们的时间戳（PTS 和 DTS）是基于其所属流的时间基来解释的。

**时间戳** 可以简单理解为计时器，用于记录或设置对应时间点的操作。在 FFmpeg 中，时间戳用于同步音视频帧的播放时间。时间戳的计算公式如下：

- `timestamp（ffmpeg 内部时间戳） = PTS * 时间基`
- `time（秒） = PTS * 时间基`

  例如，假设我们有一个视频流，其时间基为 1/90000，若某帧的 PTS 值为 90000，则该帧的实际展示时间为 `time（秒） = PTS * 时间基 = 90000 * (1/90000) = 1 秒`

### 1.2 三种同步方法

  这里先简单举个例子，例如下图所示，原本的视频应在0.080秒有一帧，但是现在出现了掉帧，此时对应音频就需要加速播放或者也相应丢一帧。简单来说就是， **以谁为基准就由谁来维护时间轴** 。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c92a7721c8ff4fa4a9c806209752f5b8.png)  
  （1）以视频为基准：视频被视为主要的同步标准，音频的播放时间会根据视频帧的时间戳来进行调整。如果 **音频的播放时间比视频快** ，系统会 **延迟音频** 的播放，为避免过多积压可能会丢弃部分音频帧；如果 **音频播放落后于视频** ，系统会通过 **延时音频** 的播放来保证同步。  
  （2）以音频为基准：以音频为基准时，视频会根据音频的时间戳进行调整。如果 **视频的播放时间比音频快** ，系统会 **延迟视频** 的播放，直到音频达到相应的时间点；而 **视频播放落后于音频** ，系统会 **加速视频** 的播放，丢掉部分视频帧，从而保证音视频同步。  
  （3） 以外部时钟为基准：外部时钟同步是一种更为综合的方式，它使用一个外部时钟（例如系统时钟或硬件时钟）来同时控制音频和视频的播放。外部时钟会提供一个精确的 **时间基准** ， **视频和音频都需要根据这个时钟进行调整** 。

## 二、音视频同步的实现

### 2.1 时间基的转换问题

  前面提到了ffmpeg内部存在多种时间基，在不同的阶段（结构体）中，对应的时间基的值都不相同，此外视频流的时间基和音频流的时间基也不同。通常情况下需要使用av\_q2d()函数将AVRational 类型的时间基（Timebase）转换为双精度浮点数（double）。AVRational 是一个表示分数的结构体，通常用于表示时间基、帧率等需要精确表示的比率。

```c
typedef struct AVRational {
    int num; ///< 分子 (numerator)
    int den; ///< 分母 (denominator)
} AVRational;

// 通过 av_q2d 函数将时间基转换为浮点数后，可以将其乘以 PTS 或 DTS 来得到实际时间
double av_q2d(AVRational q) {
    return q.num / (double)q.den;
}
123456789
```

### 2.2 音频为基准

  音频为基准和视频为基准在实现逻辑上差不多，这里以音频为例。

#### 2.2.1 实现思路

  以音频为基准进行同步的基本思路是：

1. 选择音频流作为同步基准
2. 解码音频数据并更新当前音频时间戳
3. 解码视频数据并根据音频时间戳调整视频帧的显示时间，确保音视频同步
4. 通过适当的缓冲控制，确保播放的流畅性和稳定性

#### 2.2.2 代码大纲

```c
int main{
    // 初始化 FFmpeg 库
    av_register_all();
    AVFormatContext *fmt_ctx = NULL;

    // 打开输入文件并获取流信息
    if (open_input_file(&fmt_ctx, "input.mp4") < 0) {
          return -1;
    }

    // 查找音视频流并初始化解码器
    int audio_stream_idx = find_stream(fmt_ctx, AVMEDIA_TYPE_AUDIO);
    int video_stream_idx = find_stream(fmt_ctx, AVMEDIA_TYPE_VIDEO);

    AVCodecContext *audio_dec_ctx = init_decoder(fmt_ctx, audio_stream_idx);
    AVCodecContext *video_dec_ctx = init_decoder(fmt_ctx, video_stream_idx);

    // 循环读取数据包并同步播放
    AVPacket pkt;
    while (read_packet(fmt_ctx, &pkt) >= 0) {
        if (pkt.stream_index == audio_stream_idx) {
                process_audio_packet(&pkt, audio_dec_ctx);
            } else if (pkt.stream_index == video_stream_idx) {
                process_video_packet(&pkt, video_dec_ctx, audio_dec_ctx->time_base);
            }
        av_packet_unref(&pkt);
    }
    
    // 清理资源
    cleanup(fmt_ctx, audio_dec_ctx, video_dec_ctx);
}

// 解码音频数据包并更新当前音频时间戳
void process_audio_packet(AVPacket *pkt, AVCodecContext *dec_ctx) {
    int ret = avcodec_send_packet(dec_ctx, pkt);
    if (ret < 0) {
        fprintf(stderr, "Error sending a packet for decoding\n");
        return;
    }

    while (ret >= 0) {
        ret = avcodec_receive_frame(dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
            break;
        else if (ret < 0) {
            fprintf(stderr, "Error during decoding\n");
            break;
        }

        // 更新当前音频时间戳
        update_current_audio_pts(frame->pts, dec_ctx->time_base);
    }
}

void update_current_audio_pts(int64_t pts, AVRational time_base) {
    double pts_in_seconds = pts * av_q2d(time_base);
    current_audio_pts = pts_in_seconds;
}

void process_video_packet(AVPacket *pkt, AVCodecContext *dec_ctx, AVRational audio_time_base) {
    int ret = avcodec_send_packet(dec_ctx, pkt);
    if (ret < 0) {
        fprintf(stderr, "Error sending a packet for decoding\n");
        return;
    }

    while (ret >= 0) {
        ret = avcodec_receive_frame(dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
            break;
        else if (ret < 0) {
            fprintf(stderr, "Error during decoding\n");
            break;
        }

        // 获取视频帧的 PTS 并转换为秒
        double video_pts_in_seconds = frame->pts * av_q2d(dec_ctx->time_base);

        // 根据音频时间戳调整视频帧的显示时间
        sync_video_to_audio(video_pts_in_seconds, audio_time_base);
    }
}

void sync_video_to_audio(double video_pts, AVRational audio_time_base) {
    while (video_pts > current_audio_pts) {
        usleep(1000); // 简单的等待机制
        // 更新当前音频时间戳
        current_audio_pts = get_current_audio_pts(audio_time_base);
        // 其他操作
    }
}

double get_current_audio_pts(AVRational audio_time_base) {
    // 这里应该实现一个函数来获取最新的音频时间戳
    // 例如通过解码更多的音频帧或使用其他方法
    return current_audio_pts;
}
12345678910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879808182838485868788899091929394959697
```

### 2.3 外部时钟同步

#### 2.3.1 实现思路

  以外部时钟为基准进行同步的基本思路是：

1. 使用外部时钟（如系统时钟）作为基准
2. 解码音频数据包，根据外部时钟调整音频播放时间
3. 解码视频数据包，根据外部时钟调整视频帧的显示时间
4. 通过适当的缓冲控制，确保播放的流畅性和稳定性

#### 2.3.2 代码大纲

  这里的代码和上文差不多，只有调整部分的逻辑不太一样：

```c
// 获取当前外部时钟时间（秒）
double get_external_clock() {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now); // 使用单调递增的时钟避免系统时间变化的影响
    double elapsed = (now.tv_sec - start_time.tv_sec) + (now.tv_nsec - start_time.tv_nsec) / 1e9;
    return elapsed;
}

// 解码音频数据包并根据外部时钟调整音频播放时间
void process_audio_packet(AVPacket *pkt, AVCodecContext *dec_ctx) {
    int ret = avcodec_send_packet(dec_ctx, pkt);
    if (ret < 0) {
        fprintf(stderr, "Error sending a packet for decoding\n");
        return;
    }

    while (ret >= 0) {
        ret = avcodec_receive_frame(dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
            break;
        else if (ret < 0) {
            fprintf(stderr, "Error during decoding\n");
            break;
        }

        // 将音频帧的时间戳转换为秒
        double audio_pts_in_seconds = frame->pts * av_q2d(dec_ctx->time_base);

        // 根据外部时钟调整音频帧的播放时间
        sync_audio_to_external_clock(audio_pts_in_seconds, dec_ctx->time_base);
    }
}

void sync_audio_to_external_clock(double audio_pts, AVRational time_base) {
    double external_clock_time = get_external_clock(); // 获取外部时钟时间（秒）

    // 等待直到音频帧应该播放的时间
    while (audio_pts > external_clock_time) {
        usleep(1000); // 简单的等待机制
        external_clock_time = get_external_clock();
    }
    // 其他操作
}

void process_video_packet(AVPacket *pkt, AVCodecContext *dec_ctx, AVRational audio_time_base) {
    int ret = avcodec_send_packet(dec_ctx, pkt);
    if (ret < 0) {
        fprintf(stderr, "Error sending a packet for decoding\n");
        return;
    }

    while (ret >= 0) {
        ret = avcodec_receive_frame(dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
            break;
        else if (ret < 0) {
            fprintf(stderr, "Error during decoding\n");
            break;
        }

        // 获取视频帧的 PTS 并转换为秒
        double video_pts_in_seconds = frame->pts * av_q2d(dec_ctx->time_base);

        // 根据外部时钟调整视频帧的显示时间
        sync_video_to_external_clock(video_pts_in_seconds, dec_ctx->time_base);
    }
}

void sync_video_to_external_clock(double video_pts, AVRational video_time_base) {
    double external_clock_time = get_external_clock(); // 获取外部时钟时间（秒）

    // 等待直到视频帧应该显示的时间
    while (video_pts > external_clock_time) {
        usleep(1000); // 简单的等待机制
        external_clock_time = get_external_clock();
    }
    // 其他操作
}
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778
```

---

**免责声明：本文参考了网上公开的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/145570479

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