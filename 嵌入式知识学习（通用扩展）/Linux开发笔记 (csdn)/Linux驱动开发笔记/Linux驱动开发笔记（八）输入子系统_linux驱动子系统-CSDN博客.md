---
title: "Linux驱动开发笔记（八）输入子系统_linux驱动子系统-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139597040?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.5k次，点赞13次，收藏30次。Linux 的 input 子系统是一个用于处理和管理输入设备（例如键盘、鼠标、触摸屏、游戏控制器等）的框架。它的作用是将硬件输入设备产生的原始输入数据转换成系统可以识别和使用的输入事件，并将这些事件传递给用户空间的应用程序。_linux驱动子系统"
tags:
  - "clippings"
---
---

## 前言

Linux 的 input 子系统是一个用于处理和管理输入设备（例如键盘、鼠标、 [触摸屏](https://so.csdn.net/so/search?q=%E8%A7%A6%E6%91%B8%E5%B1%8F&spm=1001.2101.3001.7020) 、游戏控制器等）的框架。它的作用是将 硬件 输入设备产生的原始输入数据转换成系统可以识别和使用的输入事件，并将这些事件传递给用户空间的应用程序。

---

## 一、输入子系统

### 1\. 子系统的引入

  引入子系统是操作系统设计中一个重要的实践，它有助于管理复杂性、提高可扩展性和维护性。子系统将操作系统的不同功能模块化，每个子系统专注于特定的功能。例如，input子系统专门处理各种输入设备的数据。这种模块化设计可以简化内核的复杂性，使得每个子系统更易于开发、测试和维护。  
  子系统提供标准化的接口和框架，简化了驱动程序的开发。开发人员只需关注如何与具体设备交互，而不必关心数据如何传递到用户空间。  
  这种模块化和标准化设计有助于增强系统的稳定性。每个子系统都是相对独立的模块，出问题时可以单独调试和修复，而不影响其他部分。例如，input子系统出问题时，主要影响输入设备，而不会波及网络、存储等其他子系统。

### 2\. 组成部分

  linux为了统一各个输入设备，将输入子系统分为了Drivers(驱动层)、Input Core(输入子系统核心层)、Handlers(事件处理层)三部分：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/209da87a44e5f38d1128ac751ae40fbf.png#pic_center)

***Drivers***  
  设备驱动程序负责与实际的硬件设备进行交互，将设备的原始输入数据传递给 input core。每种输入设备（如键盘、鼠标）通常都有相应的驱动程序。  
***Input Core***  
  这是 input 子系统的核心部分，为Drivers提供了规范及接口并通知Handlers对事件进行处理。负责管理输入设备和事件，处理设备注册、事件分发等工作。  
***Handlers***  
  事件处理程序负责接收来自 input core 的输入事件，并将其传递给用户空间的应用程序或其他内核子系统。常见的事件处理程序包括键盘事件处理器、鼠标事件处理器等。

### 3\. 事件处理流程

1. 驱动程序检测到输入事件：  
	当输入设备（如键盘或鼠标）产生输入数据时，设备驱动程序会检测到这些事件。
2. 驱动程序生成输入事件：  
	驱动程序将这些原始数据转换成标准的 input 事件结构，并将其传递给 input core。
3. Input core 分发事件：  
	input core 接收到驱动程序传递的事件后，将其分发给相应的事件处理程序。
4. 事件处理程序处理事件：  
	事件处理程序（如键盘或鼠标事件处理程序）接收到事件后，将其转换成用户空间可以理解的格式，并通过 input 事件接口传递给用户空间的应用程序。
5. 用户空间应用程序接收事件：  
	用户空间的应用程序通过读取 /dev/input/eventX 设备文件来接收和处理这些输入事件。

### 4\. 相关数据结构

  我们可以将所有输入设备的输入信息将被抽象成以下 结构体 ：

```c
//输入事件
struct input_event{
    struct timeval time;//事件产生的时间
    __u16 type;         //输入设备的类型，鼠标、键盘、触摸屏
    __u16 code;            //设备类型的不同其含义也不同，如其类型是按键表示为按键号
    __s16 value;        //设备类型的不同其含义也不同，如其类型是按键表示为按键值
}
1234567
```

  我们可以利用struct input\_dev结构体来代表一个具体的输入设备， 后面将会根据具体的设备来初始化这个结构体。

```c
struct input_dev {
    const char *name;   //提供给用户的输入设备的名称
    const char *phys;   //提供给编程者的设备节点的名称
    const char *uniq;   //指定唯一的ID号
    struct input_id id; //输入设备标识ID

    unsigned long propbit[BITS_TO_LONGS(INPUT_PROP_CNT)];

    unsigned long evbit[BITS_TO_LONGS(EV_CNT)];   //指定设备支持的事件类型
    unsigned long keybit[BITS_TO_LONGS(KEY_CNT)]; //记录支持的键值
    unsigned long relbit[BITS_TO_LONGS(REL_CNT)]; //记录支持的相对坐标位图
    unsigned long absbit[BITS_TO_LONGS(ABS_CNT)]; //记录支持的绝对坐标位图
    unsigned long mscbit[BITS_TO_LONGS(MSC_CNT)];
    unsigned long ledbit[BITS_TO_LONGS(LED_CNT)];
    unsigned long sndbit[BITS_TO_LONGS(SND_CNT)];
    unsigned long ffbit[BITS_TO_LONGS(FF_CNT)];
    unsigned long swbit[BITS_TO_LONGS(SW_CNT)];
    /*----------以下结构体成员省略----------------*/
};
12345678910111213141516171819
```
- evbit:用于指定支持的事件类型，这要根据实际输入设备能够产生的事件来选择，可选选项如下所示。

| 输入子系统事件类型 | 取值 | 描述 |
| --- | --- | --- |
| EV\_SYN | 0x00 | 同步事件 |
| EV\_KEY | 0x01 | 用于描述键盘、按钮或其他类似按键的设备 |
| EV\_REL | 0x02 | 用于描述相对位置变化，例如鼠标移动 |
| EV\_ABS | 0x03 | 用于描述绝对位置变化，例如触摸屏的触点坐标 |
| EV\_MSC | 0x04 | 其他事件类型 |
| EV\_SW | 0x05 | 用于描述二进制开关类型的设备，例如拨码开关 |
| EV\_LED | 0x11 | 用于 LED 事件，表示 LED 灯的状态 |
| EV\_SND | 0x12 | 用于声音事件，表示声音的播放相关事件 |
| EV\_REP | 0x14 | 用于重复事件，表示键盘重复发送事件 |
| EV\_FF | 0x15 | 用于力反馈事件，表示力反馈设备的输出事件 |
| EV\_PWR | 0x16 | 用于电源事件，表示电源状态变化 |
| EV\_FF\_STATUS | 0x17 | 用于力反馈状态事件，表示力反馈设备的状态变化 |
| EV\_MAX | 0x1f | 输入事件类型的最大值 |
| EV\_CNT | (EV\_MAX+1) | 输入事件类型的数量 |

- keybit：记录支持的键值，“键值”在程序中用于区分不同的按键，可选“键值”如下所示。

| 按键键值 | 描述 |
| --- | --- |
| KEY\_RESERVED | 0 |
| KEY\_ESC | 1 |
| KEY\_1 | 2 |
| KEY\_2 | 3 |
| KEY\_3 | 4 |
| KEY\_4 | 5 |

## 二、程序编写

### 1\. 相关API函数

#### 1.1 input\_allocate\_device ( )

```c
//申请input_dev结构体
struct input_dev *input_allocate_device(void);
12
```
- 参数：无
- 返回值：申请到的 input\_dev。

#### 1.2 input\_free\_device ( )

```c
//释放掉申请到的input_dev
void input_free_device(struct input_dev *dev);
12
```
- 参数
	- dev：需要释放的input\_dev。
- 返回值：无

#### 1.3 input\_register\_device ( )

```c
//初始化input_dev
int input_register_device(struct input_dev *dev);
12
```
- 参数
	- dev：要注册的 input\_dev 。
- 返回值：0，input\_dev 注册成功；负值，input\_dev 注册失败

#### 1.4 input\_unregister\_device ( )

```c
//注销input_dev
void input_unregister_device(struct input_dev *dev);
12
```
- 参数
	- dev：要注销的 input\_dev
- 返回值：无

#### 1.5 input\_event ( )

```c
//上报事件
void input_event(struct input_dev *dev, unsigned int type, unsigned int code, int value);
12
```
- 参数：
	- dev：指定输设备(input\_dev结构体)。
	- type：事件类型。
	- code：编码。
	- value：指定事件的值。
- 返回值： 无

#### 1.6 input\_report\_key ( )和input\_sync ( )

```c
//发送上报结束事件
static inline void input_report_key(struct input_dev *dev, unsigned int code, int value)
{
    input_event(dev, EV_KEY, code, !!value);
}
//上报按键事件
static inline void input_sync(struct input_dev *dev)
{
    input_event(dev, EV_SYN, SYN_REPORT, 0);
}
12345678910
```

#### 1.7 request\_any\_context\_irq ( )

  request\_any\_context\_irq( ) 是一个 Linux 内核函数，用于请求一个 IRQ（中断请求）并指定中断处理程序。在具体使用时，它能够在硬中断上下文或线程上下文中处理中断，取决于内核的运行状态和中断源的性质。这个函数可以在硬中断上下文中执行，也可以在软中断上下文中执行，从而灵活地处理各种中断处理需求。

```c
//请求一个 IRQ（中断请求）并指定中断处理程序
int request_any_context_irq(unsigned int irq, irq_handler_t handler, unsigned long flags, const char *name, void *dev_id);
12
```
- 参数
	- irq: 需要处理的中断号
	- handler: 指向中断处理程序的指针（函数指针）。当中断发生时，这个处理程序会被调用
	- flags: 用于指定中断的触发类型和其他选项（如共享中断）。常见的标志包括：
		- IRQF\_TRIGGER\_RISING: 上升沿触发
		- IRQF\_TRIGGER\_FALLING: 下降沿触发
		- IRQF\_TRIGGER\_HIGH: 高电平触发
		- IRQF\_TRIGGER\_LOW: 低电平触发
		- IRQF\_SHARED: 共享中断线
	- name: 用于标识设备的名字，主要用于调试。
	- dev\_id: 设备标识符，通常是指向设备数据结构的指针。当中断处理程序被调用时，这个指针会被传递给它。
- 返回值
	- 成功：0
	- 失败：错误码

**request\_irq()和request\_any\_context\_irq()的区别**

- 中断上下文：
	- request\_irq()：这个函数注册的中断处理程序将在中断上下文（interrupt context）中执行。中断上下文是一个特殊的内核执行上下文，它与任何特定的进程无关，也不允许进行睡眠操作（例如，调用msleep()或schedule()）。因此，中断处理程序必须非常快地运行，并且只能执行非阻塞的操作。
	- request\_any\_context\_irq()：这个函数是request\_irq()的一个变体，它允许中断处理程序在任何上下文中执行，包括中断上下文、进程上下文和软中断上下文。这为中断处理程序提供了更大的灵活性，但也需要更多的注意来确保代码的正确性和性能。
- 中断嵌套和线程化：
	- request\_irq()：默认情况下，它不支持中断嵌套和线程化（即，不支持将中断处理程序作为内核线程运行）。然而，通过传递特定的标志给request\_irq()，可以启用这些特性。
	- request\_any\_context\_irq()：这个函数通常与中断线程化（threaded interrupts）一起使用。当中断处理程序需要执行可能阻塞的操作时，可以将其标记为可线程化的。在这种情况下，当中断发生时，内核会调度一个内核线程来执行中断处理程序，而不是直接在中断上下文中执行。这允许中断处理程序进行睡眠操作，但也会增加中断处理的延迟。
- 使用场景：
	- request\_irq()：通常用于注册那些可以快速完成并且不需要睡眠的中断处理程序。
	- request\_any\_context\_irq()：通常用于那些需要更多灵活性或需要执行可能阻塞的操作的中断处理程序。然而，由于它在任何上下文中都可以执行，因此需要更加小心地处理并发和同步问题。

#### 1.8 gpiod\_get ( )

```c
//获取 GPIO 描述符（GPIO descriptor）的函数
struct gpio_desc *gpiod_get(struct device *dev, const char *con_id, enum gpiod_flags flags);
12
```
- 参数
	- dev: 指向请求 GPIO 的设备结构体指针。
	- con\_id: GPIO 的连接 ID（Connection ID），这是一个字符串，标识在设备树或 ACPI 中的 GPIO 属性名称。
	- flags: GPIO 标志，用于指定 GPIO 的方向和初始状态等。
- 返回值
	- 成功：时返回指向 gpio\_desc 结构体的指针。
	- 失败：时返回错误指针（ERR\_PTR），可以使用 IS\_ERR 宏来检查

### 2\. input子系统驱动的设计框架

1. 平台设备的匹配
```c
//设备树匹配表
 static const struct of_device_id button_dt_ids[] = {
    { .compatible = "button_interrupt", },
    { /* Sentinel */ }
};
//驱动结构体的定义
static struct platform_driver button_input = {
    .probe = button_probe,
    .remove = button_remove,
    .driver = {
        .name = "button-input",
        .of_match_table = of_match_ptr(button_dt_ids),
        .owner = THIS_MODULE,
    },
};
123456789101112131415
```
1. 入口、出口函数的编写：  
	 通常情况下，如果使用字符设备这部分我们需要在module\_init和module\_exti进行字符设备和类的创建、注销，而在input子系统中我们不需要这样的操作。值得注意的是，这里可以使用 **module\_platform\_driver(driver)** 宏定义，他可以理解为以上两个函数的上位替代， **会自动进行平台设备的申请和注销** ，进一步简化程序。
2. probe函数的编写  
	 这部分主要进行的工作有利用devm\_kzalloc(申请内存)、input\_allocate\_device(申请input\_dev结构体)、input\_register\_device(注册输入设备)
3. remove函数编写  
	 这部分主要进行input\_unregister\_device(注销input设备)并利用input\_free\_device释放资源。
4. 事件相关内容的编写  
	 输入子系统通过事件将信息从内核层传递到用户层，驱动程序在检测到输入设备的事件（例如按键按下或释放）时，生成输入事件并报告给内核输入子系统。典型的函数包括 input\_report\_key() 和 input\_sync()。

### 3\. 具体功能的实现

#### 3.1 probe函数的编写

  本次实验采用平台设备的写法，考虑到在input子系统中，我们不需要进行设备号的申请和类的创建，这里便不进行module\_init和module\_exti的编写。代码如下（示例）：

```c
//这里还用到了上章讲到的tasklet和work软中断，在宏定义通过更改DEFER_TEST实现切换
static int button_probe(struct platform_device *pdev)
{
    struct button_data *priv;
    struct gpio_desc *gpiod;
    struct input_dev *i_dev;
    int ret;

    pr_info("button_probe\n");
    priv = devm_kzalloc(&pdev->dev, sizeof(*priv), GFP_KERNEL);
    if (!priv)
        return -ENOMEM;

    i_dev = input_allocate_device();
    if (!i_dev) {
        devm_kfree(&pdev->dev, priv);
        return -ENOMEM;
    }

    i_dev->open = btn_open;
    i_dev->close = btn_close;
    i_dev->name = "key input";
    i_dev->dev.parent = &pdev->dev;
    priv->button_input_dev = i_dev;
    priv->pdev = pdev;

    set_bit(EV_KEY, i_dev->evbit);
    set_bit(KEY_1, i_dev->keybit);

    gpiod = gpiod_get(&pdev->dev, "button", GPIOD_IN);
    if (IS_ERR(gpiod)) {
        ret = PTR_ERR(gpiod);
        devm_kfree(&pdev->dev, priv);
        input_free_device(i_dev);
        return ret;
    }

    priv->irq = gpiod_to_irq(gpiod);
    priv->button_input_gpiod = gpiod;

    ret = input_register_device(priv->button_input_dev);
    if (ret) {
        pr_err("Failed to register input device\n");
        gpiod_put(priv->button_input_gpiod);
        devm_kfree(&pdev->dev, priv);
        input_free_device(i_dev);
        return ret;
    }

    platform_set_drvdata(pdev, priv);

    // 初始化去抖动工作
    INIT_DELAYED_WORK(&priv->debounce_work, button_debounce_work);

    ret = request_any_context_irq(priv->irq, button_input_irq_handler, IRQF_TRIGGER_FALLING, "input-button", priv);
    if (ret < 0) {
        dev_err(&pdev->dev, "Request GPIO IRQ failed\n");
        input_unregister_device(priv->button_input_dev);
        gpiod_put(priv->button_input_gpiod);
        devm_kfree(&pdev->dev, priv);
        return ret;
    }

#if (DEFER_TEST == 0)
    tasklet_init(&button_tasklet, button_tasklet_handler, 0);
#elif (DEFER_TEST==1)
    /*初始化button_work*/
    INIT_WORK(&button_work, button_work_hander);
#endif

    return 0;
}
}

1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374
```

#### 3.2 remove函数

```c
static int button_remove(struct platform_device *pdev)
{
    struct button_data *priv = platform_get_drvdata(pdev);
    
#if (DEFER_TEST == 0)
    tasklet_kill(&button_tasklet);
#endif

    cancel_delayed_work_sync(&priv->debounce_work);
    free_irq(priv->irq, priv);
    input_unregister_device(priv->button_input_dev);
    gpiod_put(priv->button_input_gpiod);
    devm_kfree(&pdev->dev, priv);

    return 0;
}
12345678910111213141516
```

#### 3.3 按键消抖

  这里我们先介绍一下schedule\_delayed\_work( )，其在 [Linux内核](https://so.csdn.net/so/search?q=Linux%E5%86%85%E6%A0%B8&spm=1001.2101.3001.7020) 中用于调度延迟工作。。通过这种方式，可以避免在中断处理程序或其他时间敏感的上下文中执行可能耗时的操作。函数定义如下：

```c
bool schedule_delayed_work(struct delayed_work *dwork, unsigned long delay);
1
```
- 参数
	- sdwork: 指向要调度的延迟工作结构体，该结构体包含了要执行的工作（通常是一个回调函数）以及相关的数据。
	- delay: 延迟时间，以jiffies为单位
- 返回值
	- true：表示工作已成功调度
	- false：表示工作未被调度
```c
//按键消抖
static void button_debounce_work(struct work_struct *work)
{
    struct button_data *priv = container_of(work, struct button_data, debounce_work.work);
    int button_status;

    button_status = gpiod_get_value(priv->button_input_gpiod);
    input_report_key(priv->button_input_dev, KEY_1, button_status);
    input_sync(priv->button_input_dev);
}

//中断服务函数
static irqreturn_t button_input_irq_handler(int irq, void *dev_id)
{
    struct button_data *priv = dev_id;
     // 调试信息：记录去抖动工作被执行
    pr_info("Debounce work executed\n");

    // 调度去抖动工作
    schedule_delayed_work(&priv->debounce_work, msecs_to_jiffies(DEBOUNCE_DELAY_MS));
    
#if (DEFER_TEST==0)
    tasklet_schedule(&button_tasklet);
#elif (DEFER_TEST==1)
    schedule_work(&button_work);  //触发工作
#endif    

    return IRQ_HANDLED;
}
1234567891011121314151617181920212223242526272829
```

---

**免责声明：本文参考了野火的部分资料，仅供学习参考使用，若有侵权或勘误请联系笔者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139597040

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