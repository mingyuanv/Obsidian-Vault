---
title: "Linux驱动开发笔记（十四）PWM子系统-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139916682?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读2.2k次，点赞23次，收藏35次。PWM子系统用于管理PWM波的输出，与我们之前学习的其他子系统类似，PWM具体实现代码由芯片厂商提供并默认编译进内核， 而我们可以使用内核(pwm子系统)提供的一些接口函数来实现具体的功能，例如使用PWM波控制显示屏的背光、控制无源蜂鸣器、伺服电机、电压调节等等。_pwm子系统"
tags:
  - "clippings"
---
---

## 前言

  PWM子系统用于管理 [PWM波](https://so.csdn.net/so/search?q=PWM%E6%B3%A2&spm=1001.2101.3001.7020) 的输出，与我们之前学习的其他子系统类似，PWM具体实现代码由芯片厂商提供并默认编译进内核， 而我们可以使用内核(pwm子系统)提供的一些接口函数来实现具体的功能，例如使用PWM波控制显示屏的背光、控制无源蜂鸣器、伺服电机、电压调节等等。

---

## 一、PWM子系统

### 1.1 基础知识

**脉冲宽度调制(PWM)** ，是英文“Pulse Width Modulation”的缩写，简称脉宽调制，是利用微处理器的数字输出来对模拟电路进行控制的一种非常有效的技术。  
**占空比** 是PWM中最重要的概念之一，它指的是在一个周期内高电平所占周期总时长的比例，例如：若占空比为50%，则表明一个中期内高低电平的时长相同各占50%。

### 1.2 系统框架

  下图为PWM子系统框架，其可大致分为三层，即用户层、核心层及 硬件 层。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/9ff8a5fdc59559ed49d4f3586aba2a14.png)  
  内核的PWM core，向下对实际pwm控制器驱动，提供了pwm\_chip,soc厂商编程控制器驱动，只需注册 结构体 ，配置好private\_data，实例化pwm\_ops操作，编写具体函数即可。 向上为其他驱动调用提供了统一的接口，通过pwm\_device，关联pwm\_chip,其他驱动或者用户程序通过接口来操作pwm\_device结构体。  
  pwm\_chip层实际上也是核心层的一部分，其主要对应一个pwm控制器，一个pwm控制器可包含多个pwm\_device，针对一个pwm\_chip，提供了访问pwm 控制器的方法，通过pwm\_chip提供的方法，实现对pwm 控制器的配置  
  在硬件层，pwm控制器驱动soc厂商已经写好，我们要做的是在设备树(或者是设备树插件)中开启控制器节点， 描述pwm设备节点，然后驱动中调用内核PWM提供的接口，来实现pwm驱动控制。  
  值得注意的是，PWM驱动有两条路径可以选择，第一种就是按照我们以往的流程，进行应用层的编辑，调用设备驱动来获取核心层提供的数据；第二种则是利用上章的sysfs文件系统直接调用核心层数据，这种方法可以不进行设备树的匹配和设备驱动的编写。  
  目前主流的 pwm 设备驱动都是集成到 sysfs 文件系统中，通过 cat 和 echo 操作来控制。sysfs接口对PWM驱动进行功能调试，主要调试命令示例如下，以pwmchip0为例：

| 命令 | 描述 |
| --- | --- |
| ls /sys/class/pwm/pwmchip0/ | 查看PWM控制器节点 |
| echo 0 > export | 打开指定PWM通道信号 |
| echo 50000> pwm0/period | 设置PWM周期，单位为 ns |
| echo 25000> pwm0/duty\_cycle | 设置PWM信号占空比，这里不能直接设置占空比，而是设置的一个周期的 ON 时间，也就是高电平时间 |
| echo normal> pwm0/duty\_cycle | 设置PWM的极性，这里有normal和inversed两种 |
| echo 1 > pwm0/enable | 使能某个PWM通道信号 |
| echo 0 > pwm0/enable | 禁止某个PWM通道信号 |

  具体过程可以参考这个视频： [sysfs操作pwm的流程](https://www.bilibili.com/video/BV1um42157VT?p=6&vd_source=937f3264dce76f586bc0a69ee24dfafa) ，我们接下来的部分就继续另一种方式——设备驱动的编写，如果采用sysfs这种方式的话，我们已经实现了所有过程。

### 1.3 重要结构体

**PWM设备结构** 定义一个代表PWM设备的结构体，包括设备的硬件相关信息和操作方法。

```c
struct pwm_device {
    struct device dev;             
    const struct pwm_ops *ops; 
    int hwpwm;
         ...
};
123456
```
- 成员描述：
	- dev：设备结构体
	- ops：设备操作集
	- hwpwm： 硬件PWM编号

**PWM操作结构** 定义一组操作方法，用于控制PWM设备。

```c
struct pwm_ops {
    int  (*request)(struct pwm_chip *chip,
 struct pwm_device *pwm);    
    void (*free)(struct pwm_chip *chip,
 struct pwm_device *pwm);      
    int (*config)(struct pwm_device *pwm, int duty_ns, int period_ns);
    int (*enable)(struct pwm_device *pwm);
    void (*disable)(struct pwm_device *pwm);
       ...
};
12345678910
```
- 成员描述：
	- request：申请PWM设备
	- free：释放PWM设备
	- config：PWM设备配置函数
	- enable：PWM设备使能
	- disable：PWM设备关闭

**PWM芯片结构** 定义一个代表PWM芯片的结构体，包含多个PWM设备。

```c
struct pwm_chip {
    struct device *dev;          
    const struct pwm_ops *ops;   
    int npwm; 
    int base;             
    struct pwm_device *pwms;  
    struct list_head    list;             
        ...
};
123456789
```
- 成员描述：
	- dev：设备结构体
	- ops：芯片操作集
	- npwm：芯片中的PWM设备数量
	- pwms：PWM设备数组
	- list：链表
	- base：索引号

### 1.4 PWM注册流程

1. 首先，定义具体的PWM操作方法，这些方法将实现实际的硬件控制。
```c
static int my_pwm_config(struct pwm_device *pwm, int duty_ns, int period_ns) {
    // 配置PWM设备
}

static int my_pwm_enable(struct pwm_device *pwm) {
    // 启用PWM设备
}

static void my_pwm_disable(struct pwm_device *pwm) {
    // 禁用PWM设备
}

static const struct pwm_ops my_pwm_ops = {
    .config = my_pwm_config,
    .enable = my_pwm_enable,
    .disable = my_pwm_disable,
    // 其他操作方法
};
123456789101112131415161718
```
1. 创建和初始化PWM芯片结构体。
```c
static struct pwm_chip my_pwm_chip = {
    .ops = &my_pwm_ops,
    .npwm = 1,  // 假设只有一个PWM设备
};
1234
```
1. 使用PWM子系统提供的API将PWM芯片注册到内核。
```c
static int my_pwm_probe(struct platform_device *pdev) {
    int ret;
    my_pwm_chip.dev = &pdev->dev;
    //
    注册一个 pwm 控制器设备
    ret = pwmchip_add(&my_pwm_chip);
    if (ret < 0) {
        dev_err(&pdev->dev, "Failed to add PWM chip: %d\n", ret);
        return ret;
    }

    return 0;
}

static int my_pwm_remove(struct platform_device *pdev) {
    //注销一个 pwm 控制器设备
    return pwmchip_remove(&my_pwm_chip);
}
123456789101112131415161718
```
1. 定义和注册平台驱动，将PWM芯片与具体的硬件平台关联起来。
```c
static const struct of_device_id my_pwm_of_match[] = {
    { .compatible = "my,pwm", },
    {},
};
MODULE_DEVICE_TABLE(of, my_pwm_of_match);

static struct platform_driver my_pwm_driver = {
    .probe = my_pwm_probe,
    .remove = my_pwm_remove,
    .driver = {
        .name = "my_pwm",
        .of_match_table = my_pwm_of_match,
    },
};

module_platform_driver(my_pwm_driver);
12345678910111213141516
```

## 二、设备驱动的编写

### 2.1 相关API函数

#### 2.1.1 pwm\_config( )

```c
//配置PWM设备的周期和占空比
int pwm_config(struct pwm_device *pwm, int duty_ns, int period_ns);
12
```
- 参数：
	- pwm：指向要配置的PWM设备的指针
	- duty\_ns：占空比（单位：纳秒）
	- period\_ns：周期（单位：纳秒）
- 返回值：
	- 成功：0
	- 失败：负值错误码

#### 2.1.2 pwm\_enable( )

```c
/启用PWM设备
int pwm_enable(struct pwm_device *pwm);
12
```
- 参数：
	- pwm：指向要启用的PWM设备的指针。
- 返回值：
	- 成功：0
	- 失败：负值错误码。

#### 2.1.3 pwm\_disable( )

```c
//禁用PWM设备
void pwm_disable(struct pwm_device *pwm);
12
```
- 参数：
	- pwm：指向要禁用的PWM设备的指针。
- 返回值：无

#### 2.1.4 pwm\_request( )

```c
//获取PWM设备
struct pwm_device *pwm_request(int pwm_id, const char *label);
12
```
- 参数：
	- pwm\_id：PWM设备的ID。
	- label：PWM设备的标签，用于识别该设备。
- 返回值：
	- 成功：指向PWM设备的指针
	- 失败：NULL

#### 2.1.5 pwm\_free( )

```c
//释放PWM设备
void pwm_free(struct pwm_device *pwm);
12
```
- 参数：
	- pwm：指向要释放的PWM设备的指针。
- 返回值：无

#### 2.1.6 pwm\_set\_polarity( )

```c
//设置pwm极性
static inline int pwm_set_polarity(struct pwm_device *pwm, enum pwm_polarity polarity);
12
```
- 参数：
	- pwm：PWM设备的指针
	- polarity：要设置的极性，可选参数包括norma（PWM\_POLARITY\_NORMAL）和inversed（极性翻转，PWM\_POLARITY\_INVERSED）
- 返回值：无

#### 2.1.7 devm\_of\_pwm\_get( )

  devm\_of\_pwm\_get() 函数是 devm\_pwm\_get() 的一个变体，专门设计用于基于设备树（Device Tree, DT）信息获取 PWM 设备。在 Linux 内核中使用它可以简化通过设备树节点获取 PWM 设备的过程。

```c
//从指定设备（dev）的DTS节点中，获得对应的PWM设备
struct pwm_device *devm_of_pwm_get(struct device *dev, struct device_node *np, const char *con_id);
12
```
- 参数：
	- pwm：PWM设备的指针
	- np: 要从中检索 PWM 设备的设备树节点。
	- con\_id: PWM 消费者的字符串标识符。如果不需要，可以为 NULL。
- 返回值：
	- 成功：指向表示 PWM 设备的 pwm\_device 结构体的指针
	- 失败：错误指针（ERR\_PTR）

**注** ：在rk3568中，厂商已经对pwm\_config、pwm\_enable、pwm\_set\_polarity进行封装，当调用这些函数的时候都会自动执行pwm\_apply\_state函数。对于其他芯片若未进行封装，则调用这些函数会执行pwm\_ops结构体中的相关函数。  
 此外，devm\_of\_pwm\_get函数也是是对of\_pwm\_get函数（从指定的设备树节点获取PWM）进行的扩展封装， 它的优点是在驱动移除之前自动注销申请的pwm。

### 2.2 设备树的编写

  以下是厂商对pwm8进行的设置，我们不做修改。

```bash
//rk3568.dtsi
pwm8: pwm@fe6f0000 {
        compatible = "rockchip,rk3568-pwm", "rockchip,rk3328-pwm";
        reg = <0x0 0xfe6f0000 0x0 0x10>;
        #pwm-cells = <3>;
        pinctrl-names = "active";
        pinctrl-0 = <&pwm8m0_pins>;
        clocks = <&cru CLK_PWM2>, <&cru PCLK_PWM2>;
        clock-names = "pwm", "pclk";
        status = "disabled";
    };
    
//rk3568-pinctrl.dtsi
pwm8 {
        /omit-if-no-ref/
        pwm8m0_pins: pwm8m0-pins {
            rockchip,pins =
                /* pwm8_m0 */
                <3 RK_PB1 5 &pcfg_pull_none>;
        };

        /omit-if-no-ref/
        pwm8m1_pins: pwm8m1-pins {
            rockchip,pins =
                /* pwm8_m1 */
                <1 RK_PD5 4 &pcfg_pull_none>;
        };
    };

1234567891011121314151617181920212223242526272829
```

  这部分是我们要修改的部分，在pwm8中对其进行简单设置，之后在根目录下进行mypwm节点的创建。

```bash
pwm8 {
    status = "okay";
    pinctrl-names = "active";
    pinctrl-0 = <&pwm8m0-pins>;
};

&{/} {
    mypwm: mypwm {
        status = "okay";
        compatible = "mypwm";

        back {
            pwm-names = "mypwm";
              #pwm0通道，0占空比，周期为20ms，正极性
            pwms = <&pwm0 0 20000000 1>;
        };
    };
};
123456789101112131415161718
```

### 3\. 驱动设计思路

1. 由于我们任然采用设备树的匹配方式，这里就不再赘述了，简单进行一个设备的匹配。
```c
static const struct of_device_id of_pwm_match[] = {
    {.compatible = "mypwm"},
    {},
};

static struct platform_driver pwm_demo_driver = {
    .probe          = pwm_probe,
    .remove         = pwm_remove,
    .driver         = {
            .name   = "mypwm",
            .of_match_table = of_pwm_match,
    },
};
12345678910111213
```
1. 在.prob函数中申请、设置、使能PWM，当设备空闲时在.remove中进行设备的移除和释放。此外，考虑到这里我们使用了module\_platform\_driver(driver)宏定义，省去了module\_init和module\_exit，所以这里还要进行字符设备的申请注册及注销释放等操作。
```c
static int pwm_demo_probe(struct platform_device *pdev)
{
    int ret = 0;
    struct device_node *child; // 保存子节点
    struct device *dev = &pdev->dev;
    printk("match success \n");

    /*--------------第一部分-----------------*/
    //获取子节点
    child = of_get_next_child(dev->of_node, NULL);
    if (child)
    {
            /*--------------第二部分-----------------*/
            //获取pwm
            pwm_test = devm_of_pwm_get(dev, child, NULL);
            if (IS_ERR(pwm_test))
            {
                    printk(KERN_ERR" pwm_test,get pwm  error!!\n");
                    return -1;
            }
    }
    else
    {
            printk(KERN_ERR" pwm_test of_get_next_child  error!!\n");
            return -1;
    }

    /*--------------第三部分-----------------*/
    //配置PWM
    pwm_config(pwm_test, 1000, 5000);
    pwm_set_polarity(pwm_test, PWM_POLARITY_INVERSED);
    pwm_enable(pwm_test);

    return ret;
}

static int pwm_demo_remove(struct platform_device *pdev)
{
    //释放PWM
    pwm_config(pwm_test, 0, 5000);
    pwm_free(pwm_test);
    return 0;
}
12345678910111213141516171819202122232425262728293031323334353637383940414243
```
1. 进行相关operations操作集的编写，这里就不再赘述了。

**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139916682

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