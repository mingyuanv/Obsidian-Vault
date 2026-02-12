---
title: "Linux驱动开发笔记（九）IIC子系统及其驱动_兼容linux同组iic下不同地址不同模块,同种功能驱动-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/139731877?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读1.4k次，点赞27次，收藏13次。IIC我们已经学习过很多次了，在应用部分我们已经介绍过其应用层的开发，这章我们将继续驱动部分的开发。本次实验采用MPU6050，使用了input子系统及IIC子系统构成。MPU6050是全球首例整合性6轴（3轴陀螺仪+3轴加速度计）运动处理组件，也可以通过扩展实现9轴运动处理（在连接三轴磁传感器后）。它集成了三轴MEMS陀螺仪和三轴MEMS加速度计，以及一个可扩展的数字运动处理器DMP（Digital Motion Processor）。_兼容linux同组iic下不同地址不同模块,同种功能驱动"
tags:
  - "clippings"
---
---

## 前言

[IIC](https://so.csdn.net/so/search?q=IIC&spm=1001.2101.3001.7020) 我们已经学习过很多次了，在应用部分我们已经介绍过其应用层的开发，这章我们将继续驱动部分的开发。本次实验采用 MPU6050 ，使用了input子系统及IIC子系统构成。

## 一、IIC驱动框架

[i2c总线](https://so.csdn.net/so/search?q=i2c%E6%80%BB%E7%BA%BF&spm=1001.2101.3001.7020) 包括i2c设备(i2c\_client)和i2c驱动(i2c\_driver)，当我们向 linux 中注册设备或驱动的时候，按照i2c总线匹配规则进行配对，这也意味着我们不再需要手动创建，而是使用设备树机制引入，设备树节点是与paltform总线相配合使用，在匹配成功之后自动进入.probe函数。  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/37b852a39881d438877559e728466f5f.png#pic_center)  
**I2C core框架**  
  提供了核心数据结构的定义和相关接口函数，用来实现I2C适配器驱动和设备驱动的注册、注销管理，以及I2C通信方法上层的、与具体适配器无关的代码，为系统中每个I2C总线增加相应的读写方法。  
**I2C总线驱动**  
  定义描述具体I2C总线适配器的i2c\_adapter数据结构、实现在具体I2C适配器上的I2C总线通信方法，并由i2c\_algorithm数据结构进行描述。 经过I2C总线驱动的的代码，可以为我们控制I2C产生开始位、停止位、读写周期以及从设备的读写、产生ACK等。  
**I2C 设备驱动**  
  I2C 设备驱动通过I2C适配器与CPU通信，其中主要包含i2c\_driver和i2c\_client数据结构，i2c\_driver结构对应一套具体的驱动方法。i2c\_client数据结构由内核根据具体的设备注册信息自动生成，设备驱动根据 硬件 具体情况填充。

## 二、总线驱动

  一个完整的iic驱动函数包括两部分，即iic总线驱动和设备驱动，而总线部分的驱动通常情况下在外设出厂时就由厂商提供，这里我们便简单了解即可。

### 2.1 iic总线的运行机制

1. 注册i2C总线
2. 将i2C驱动添加到i2C总线的驱动链表中
3. 遍历i2C总线上的设备链表，根据i2c\_device\_match函数进行匹配，如果匹配调用i2c\_device\_probe函数
4. i2c\_device\_probe函数会调用I2C驱动的probe函数

### 2.2 重要数据结构

  在应用层的学习中我们已经介绍过i2c\_algorithm,i2c\_client和i2c\_adapter结构体，感兴趣可以回顾下。

#### 2.2.1 i2c\_driver结构体

```c
struct i2c_driver {
        unsigned int class;
        
        int (*probe)(struct i2c_client *, const struct i2c_device_id *);
        int (*remove)(struct i2c_client *);

        struct device_driver driver;
        const struct i2c_device_id *id_table;

        int (*detect)(struct i2c_client *, struct i2c_board_info *);
        const unsigned short *address_list;
        struct list_head clients;
            ...
    };
1234567891011121314
```
- probe： i2c设备和i2c驱动匹配后，回调该函数指针。
- id\_table： struct i2c\_device\_id 要匹配的从设备信息。
- address\_list： 设备地址
- clients： 设备链表
- detect： 设备探测函数

#### 2.2.2 i2c总线结构体

```c
//定义总线，维护着两个链表(I2C驱动、I2C设备)，管理I2C设备和I2C驱动的匹配和删除等
struct bus_type i2c_bus_type = {
            .name           = "i2c",
            .match          = i2c_device_match,
            .probe          = i2c_device_probe,
            .remove         = i2c_device_remove,
            .shutdown       = i2c_device_shutdown,
    };
12345678
```

### 2.3 匹配规则

  一般来说，i2c的匹配方式有三种，包括设备树，ACPI和字符匹配，这部分的对比前章已经介绍过了。现在我们习惯性采用设备树的匹配方式：

```c
static int i2c_device_match(struct device *dev, struct device_driver *drv)
{
    struct i2c_client       *client = i2c_verify_client(dev);
    struct i2c_driver       *driver;

    //设备树匹配方式，比较 I2C 设备节点的 compatible 属性和 of_device_id 中的 compatible 属性
    if (i2c_of_match_device(drv->of_match_table, client))
        return 1;

    //ACPI 匹配方式
    if (acpi_driver_match_device(dev, drv))
        return 1;

    driver = to_i2c_driver(drv);
    //i2c总线传统匹配方式，比较 I2C设备名字和 i2c驱动的id_table->name 字段是否相等
    if (i2c_match_id(driver->id_table, client))
        return 1;

    return 0;
}
1234567891011121314151617181920
```

## 三、设备树的修改

  下面是瑞芯微官方给出的ic3控制器的设备树代码：

```bash
//存放于“rk3568.dtsi”
i2c2: i2c@fe5b0000 {

        //驱动名称
        compatible = "rockchip,rk3399-i2c";
        
        //寄存器
        reg = <0x0 0xfe5b0000 0x0 0x1000>;
        
        //时钟源
        clocks = <&cru CLK_I2C2>, <&cru PCLK_I2C2>;
        clock-names = "i2c", "pclk";
        
        //中断源
        interrupts = <GIC_SPI 48 IRQ_TYPE_LEVEL_HIGH>;
        
        pinctrl-names = "default";
        pinctrl-0 = <&i2c2m0_xfer>;
        #address-cells = <1>;
        #size-cells = <0>;
        status = "disabled";

//存放于“rk3568-pinctrl.dtsi”
i2c2 {
        /omit-if-no-ref/
        i2c2m0_xfer: i2c2m0-xfer {
            rockchip,pins =
                /* i2c2_sclm0 */
                <0 RK_PB5 1 &pcfg_pull_none_smt>,
                /* i2c2_sdam0 */
                <0 RK_PB6 1 &pcfg_pull_none_smt>;
        };

        /omit-if-no-ref/
        i2c2m1_xfer: i2c2m1-xfer {
            rockchip,pins =
                /* i2c2_sclm1 */
                <4 RK_PB5 1 &pcfg_pull_none_smt>,
                /* i2c2_sdam1 */
                <4 RK_PB4 1 &pcfg_pull_none_smt>;
        };
    };
123456789101112131415161718192021222324252627282930313233343536373839404142
```

  接下来就是我们要编写的内容，这部分编写方式和以前一样即可。

```bash
&i2c2 {
     status = "okay";

    pinctrl-names = "default";
    pinctrl-0 = <&i2c2m0_xfer>;     
    #address-cells = <1>;
    #size-cells = <0>;
    /*添加你的I2C设备参考*/
    myi2c: myi2c@68 {
        compatible = "company,myi2c";
        reg = <0x68>;
        status = "okay";
 };
12345678910111213
```

## 四、设备驱动的编写

### 4.1 相关API函数

#### 4.1.1 i2c\_add\_adapter( )

  使用这个函数时，不需要提前指定适配器编号，内核会负责管理和分配编号，适合于大多数情况下的使用。

```c
//自动分配 I2C 适配器编号
int i2c_add_adapter(struct i2c_adapter *adapter);
12
```

  适配器编号（ adapter ->nr）在注册过程中由系统自动设置，具体的步骤如下：

- 适配器初始化：调用这个函数之前，需要先初始化 i2c\_adapter 结构体，填充相关字段。
- 自动分配编号：内核会自动选择一个可用的编号，并将其分配给 adapter->nr。
- 注册适配器：将适配器注册到 I2C子系统中，使其可以被使用。

**注：相似地还还存在int i2c\_add\_numbered\_adapter(struct i2c\_adapter** \* **adapter)函数，这个函数用于手动设置 I2C 适配器编号。调用这个函数之前，需要先初始化 i2c\_adapter 结构体，并填充 adapter->nr 字段和其他相关字段。**  
i2c\_register\_driver 函数用于在 Linux 内核中注册一个 I2C 驱动。这个函数是 I2C 子系统的一部分，用于将一个 I2C 驱动程序注册到 I2C 驱动程序模型中，以便内核能够识别并管理该驱动程序。

#### 4.1.2 i2c\_register\_driver( )

  这个函数是 I2C 子系统的一部分，用于将一个 I2C 驱动程序注册到 I2C 驱动程序模型中，以便内核能够识别并管理该驱动程序。

```c
//在 Linux 内核中注册一个 I2C 驱动
int i2c_register_driver(struct module *owner, struct i2c_driver *driver);
12
```
- 参数:
	- owner：通常使用 THIS\_MODULE 宏来指定当前模块
	- driver：指向一个 i2c\_driver 结构体，该结构体包含了驱动程序的相关信息和操作函数
- 返回值：
	- 0：成功注册
	- 负数：注册失败

**注：#define i2c\_add\_driver(driver)宏定义是对i2c\_register\_driver函数的调用，也可以直接使用这个宏定义进行注册**

#### 4.1.3 i2c\_transfer( )

  i2c\_transfer 是一个底层函数，它可以执行多条消息的读写操作。

```c
//在 I2C 总线上进行数据传输
int i2c_transfer(struct i2c_adapter *adap, struct i2c_msg *msgs, int num);
12
```
- 参数
	- adap：指向 i2c\_adapter 结构体的指针，表示 I2C 适配器。
	- msgs：指向 i2c\_msg 结构体数组的指针，每个 i2c\_msg 结构体表示一条 I2C 消息。
	- num：消息数量。
- 返回值
	- 正值：表示成功传输的消息数量。
	- 负值：表示传输失败，返回一个负的错误代码。

**注：i2c\_msg结构体之前在应用开发实验时已经介绍过了， 这里简单回忆一下：**

```c
//描述一个iic消息
struct i2c_msg {
    __u16 addr;     //iic设备地址
    __u16 flags;    //消息传输方向和特性。I2C_M_RD：表示读取消息；0：表示发送消息
    __u16 len;      //消息数据的长度
    __u8 *buf;      //字符数组存放消息，作为消息的缓冲区
        ... 
};
12345678
```

#### 4.1.4 i2c\_master\_send( )

  i2c\_master\_send 是一个便捷函数，用于向 I2C 设备发送数据。

```c
复制代码
int i2c_master_send(const struct i2c_client *client, const char *buf, int count);
12
```
- 参数
	- client：指向 i2c\_client 结构体的指针，表示目标 I2C 设备。
	- buf：指向数据缓冲区的指针。
	- count：要发送的数据长度。
- 返回值
	- 正值：表示成功发送的字节数。
	- 负值：表示发送失败，返回一个负的错误代码。

#### 4.1.5 i2c\_master\_recv( )

  i2c\_master\_recv 是一个便捷函数，用于从 I2C 设备接收数据。

```c
int i2c_master_recv(const struct i2c_client *client, char *buf, int count);
1
```
- 参数
	- client：指向 i2c\_client 结构体的指针，表示目标 I2C 设备。
	- buf：指向接收缓冲区的指针。
	- count：要接收的数据长度。
- 返回值
	- 正值：表示成功接收的字节数。
	- 负值：表示接收失败，返回一个负的错误代码。

#### 4.1.6 i2c\_transfer\_buffer\_flags( )

```c
//用于在 I2C 总线上进行带有特定标志的数据传输
int i2c_transfer_buffer_flags(const struct i2c_client *client, char *buf, int count, u16 flags);
12
```
- 参数
	- client：指向 i2c\_client 结构体的指针，表示目标 I2C 设备。
	- buf：指向数据缓冲区的指针。
	- count：要传输的数据长度。
	- flags：传输标志。
- 返回值
	- 正值：表示成功传输的字节数。
	- 负值：表示传输失败，返回一个负的错误代码。

#### 4.1.7 i2c\_del\_driver( )

  这个函数与 i2c\_register\_driver 相对应，i2c\_register\_driver 用于注册一个 I2C 驱动程序，而 i2c\_del\_driver 用于注销它。

```c
//从I2C 子系统中注销一个 I2C 驱动程序
void i2c_del_driver(struct i2c_driver *driver);
12
```
- 参数
	- driver：指向一个 i2c\_driver 结构体，该结构体表示要注销的 I2C 驱动程序

#### 4.1.8 i2c\_set\_clientdata

  这个函数用于在I2C驱动的probe函数中设置私有数据指针。这个私有数据通常是指向设备结构体或者其他相关数据结构的指针，它允许驱动在后续的操作中能够方便地访问这些数据。

```c
void i2c_set_clientdata(struct i2c_client *client, void *data);
1
```
- 参数
	- client：指向I2C设备客户端结构体的指针。
	- data：要设置的私有数据指针，通常指向一个自定义的设备结构体或其他相关数据。

### 4.2 MPU6050

#### 4.2.1 基本介绍

  MPU6050是全球首例整合性6轴（3轴陀螺仪+3轴加速度计）运动处理 组件 ，也可以通过扩展实现9轴运动处理（在连接三轴磁传感器后）。它集成了三轴MEMS陀螺仪和三轴MEMS加速度计，以及一个可扩展的数字运动处理器DMP（Digital Motion Processor）。MPU6050通过I2C接口与微控制器通信，广泛应用于需要精确姿态测量的场合，如无人机、机器人和智能穿戴设备等。

#### 4.2.2 主要特点

1. 整合性：MPU6050免除了组合陀螺仪与加速器时间轴之差的问题，减少了大量的封装空间。
2. 灵活性：MPU6050的角速度全格感测范围为±250、±500、±1000与±2000°/sec(dps)，可准确追踪快速与慢速动作；用户可程式控制的加速器全格感测范围为±2g、±4g、±8g与±16g，满足各种应用需求。
3. 接口：MPU6050支持最高至400kHz的I2C接口，对于需要高速传输的应用，也可使用SPI接口（但请注意，SPI接口仅在MPU-6000上可用）。
4. 稳定性：MPU6050具有内建的温度感测器和在工作环境下仅有±1%变动的振荡器，保证了测量数据的稳定性。
5. 尺寸与封装：MPU6050采用QFN封装（无引线方形封装），尺寸为4x4x0.9mm，可承受最大10000g的冲击。
6. 电源：VDD供电电压为2.5V±5%、3.0V±5%、3.3V±5%；VDDIO为1.8V±5%或VDD。
7. 功耗：陀螺仪运作电流5mA，待命电流5μA；加速器运作电流350μA，省电模式电流20μA@10Hz。
8. 性能：陀螺仪敏感度131 LSBs/°/sec，加速度计范围±2g至±16g。

#### 4.2.3 引脚对应表

| MPU6050引脚 | 说明 | 泰山派引脚 |
| --- | --- | --- |
| SCL | SCL引脚 | GPIO0\_B5 |
| SDA | SDA引脚 | GPIO0\_B6 |
| XDA | 没有使用 |  |
| XCL | 没有使用 |  |
| AD0 | 接地 | GND |
| INT（Interrupt） | 悬空或者接地 |  |
| GND | GND | GND |
| VCC | 电源 | 3.3V |

### 4.3 驱动编写

#### 4.3.1 IIC驱动的设计框架

  本次实验大致采用input子系统和IIC子系统，这里着重讲一下这部分的设计思路：

1. 本实验采用设备树匹配的方式进行匹配，故而需要设置i2c\_driver结构体。
```c
//定义ID匹配表
static const struct i2c_device_id gtp_device_id[] = {
    {"company,myi2c", 0},
    {}
};
//定义设备树匹配表
static const struct of_device_id mpu6050_of_match_table[] = {
    {.compatible = "company,myi2c"},
    {}
};
//定义i2c设备结构体
struct i2c_driver mpu6050_driver = {
    .probe = mpu6050_probe,
    .remove = mpu6050_remove,
    .id_table = gtp_device_id,
    .driver = {
        .owner = THIS_MODULE,
        .name = "company,myi2c",
        .of_match_table = mpu6050_of_match_table,
    },
};
123456789101112131415161718192021
```
1. 出入口函数的编写，通常情况下这里需要编写module\_init和module\_exti，并且在其中分别使用i2c\_register\_driver( )函数和i2c\_del\_driver( )函数进行 i2c 驱动的注册和注销。但是这里引入一个 **module\_i2c\_driver(driver)** 宏定义，这个宏定义可以 **自动进行iic总线的注册和注销** ，故而不需要前两个函数的编写。
2. probe函数的编写，这部分内容我们需要的进行内存申请，之后便可以进行选择利用字符设备的方式还是input子系统，笔者这里选择趁热打铁使用input设备，这里流程不太熟悉的可以回顾上章内容。之后利用i2c\_set\_clientdata将数据和设备链接起来。
3. remove函数的编写，这部分与probe函数对应即可，如果选择字符设备的方式，则依次进行device\_destroy(设备删除)、class\_destroy(清除类)、cdev\_del(清除设备号)、unregister\_chrdev\_region(注销字符设备)；若采用input的子系统，则仅需要使用input\_unregister\_device(注销input设备即可）。
4. 具体外设的初始化、读、写函数的编写，这部分内容根据厂商提供的寄存器、时序图操作即可。
5. 若使用字符设备的话，这里还需要编写operations结构体相关函数，包括open、write、read、release，并利用cdev\_init()函数与设备进行绑定。

#### 4.3.2.probe函数

```c
static int mpu6050_probe(struct i2c_client *client, const struct i2c_device_id *id){
    struct mpu6050_data *data;
    int ret = 0;
    printk(KERN_EMERG "mpu6050_probe enter!\n");

    data = devm_kzalloc(&client->dev, sizeof(struct mpu6050_data), GFP_KERNEL);
    if (!data){
        printk(KERN_EMERG "devm_kzalloc err!\n");
        return -ENOMEM;
    }
    
    data->client = client;

    ret = mpu6050_init_device(client);
    if(ret < 0){
        printk(KERN_EMERG "mpu6050_init_device err!\n");
        return ret;
    }

    data->input_dev = devm_input_allocate_device(&client->dev);
    if (!data->input_dev){
        printk(KERN_EMERG "devm_input_allocate_device err!\n");
        return -ENOMEM;
    }
        
    data->input_dev->name = "mpu6050";
    data->input_dev->id.bustype = BUS_I2C;

    input_set_abs_params(data->input_dev, ABS_X, -32768, 32767, 0, 0);
    input_set_abs_params(data->input_dev, ABS_Y, -32768, 32767, 0, 0);
    input_set_abs_params(data->input_dev, ABS_Z, -32768, 32767, 0, 0);
    input_set_abs_params(data->input_dev, ABS_RX, -32768, 32767, 0, 0);
    input_set_abs_params(data->input_dev, ABS_RY, -32768, 32767, 0, 0);
    input_set_abs_params(data->input_dev, ABS_RZ, -32768, 32767, 0, 0);

    ret = input_register_device(data->input_dev);
    if (ret < 0){
        printk("input_register_device err!\n");
        return ret;
    }

    i2c_set_clientdata(client, data);

    INIT_DELAYED_WORK(&data->work, mpu6050_report_data);
    schedule_delayed_work(&data->work, msecs_to_jiffies(100));
   
    return 0;
}
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748
```

#### 4.3.3.remove函数

```c
static int mpu6050_remove(struct i2c_client *client){
    struct mpu6050_data *data = i2c_get_clientdata(client);
    printk(KERN_EMERG "mpu6050_remove enter!\n");

    cancel_delayed_work_sync(&data->work);
    input_unregister_device(data->input_dev);

    return 0;
}
123456789
```

#### 4.3.4 mpu6050初始化函数

```c
static int mpu6050_init_device(struct i2c_client *client)
{
    int error = 0;
    error += i2c_write_mpu6050(client, PWR_MGMT_1, 0x00);
    error += i2c_write_mpu6050(client, SMPLRT_DIV, 0x07);
    error += i2c_write_mpu6050(client, CONFIG, 0x06);
    error += i2c_write_mpu6050(client, ACCEL_CONFIG, 0x01);

    if (error < 0) {
        printk(KERN_DEBUG "mpu6050_init_device error\n");
        return error;
    }
    return 0;
}
1234567891011121314
```

#### 4.3.5 write/read函数

```c
static int i2c_write_mpu6050(struct i2c_client *mpu6050_client, u8 address, u8 data){
    int error = 0;
    u8 write_data[2];
    struct i2c_msg send_msg;

    write_data[0] = address;
    write_data[1] = data;

    send_msg.addr = mpu6050_client->addr;
    send_msg.flags = 0;
    send_msg.buf = write_data;
    send_msg.len = 2;

    error = i2c_transfer(mpu6050_client->adapter, &send_msg, 1);
    if (error != 1) {
        printk(KERN_DEBUG "i2c_write_mpu6050 error\n");
        return -EIO;
    }
    return 0;
}

static int i2c_read_mpu6050(struct i2c_client *mpu6050_client, u8 address, void *data, u32 length){
    int error = 0;
    u8 address_data = address;
    struct i2c_msg mpu6050_msg[2];

    mpu6050_msg[0].addr = mpu6050_client->addr;
    mpu6050_msg[0].flags = 0;
    mpu6050_msg[0].buf = &address_data;
    mpu6050_msg[0].len = 1;

    mpu6050_msg[1].addr = mpu6050_client->addr;
    mpu6050_msg[1].flags = I2C_M_RD;
    mpu6050_msg[1].buf = data;
    mpu6050_msg[1].len = length;

    error = i2c_transfer(mpu6050_client->adapter, mpu6050_msg, 2);
    if (error != 2) {
        printk(KERN_DEBUG "i2c_read_mpu6050 error\n");
        return -EIO;
    }
    return 0;
}
12345678910111213141516171819202122232425262728293031323334353637383940414243
```

#### 4.3.6 report函数

```c
static void mpu6050_report_data(struct work_struct *work)
{
    struct mpu6050_data *data = container_of(work, struct mpu6050_data, work.work);
    struct i2c_client *client = data->client;
    s16 accel_data[3];
    s16 gyro_data[3];
    u8 buffer[14];
    int ret;

    ret = i2c_read_mpu6050(client, ACCEL_XOUT_H, buffer, 14);
    if (ret < 0) {
        dev_err(&client->dev, "Failed to read data: %d\n", ret);
        return;
    }

    accel_data[0] = (buffer[0] << 8) | buffer[1];
    accel_data[1] = (buffer[2] << 8) | buffer[3];
    accel_data[2] = (buffer[4] << 8) | buffer[5];
    gyro_data[0] = (buffer[8] << 8) | buffer[9];
    gyro_data[1] = (buffer[10] << 8) | buffer[11];
    gyro_data[2] = (buffer[12] << 8) | buffer[13];

    //用于报告绝对坐标事件
    input_report_abs(data->input_dev, ABS_X, accel_data[0]);
    input_report_abs(data->input_dev, ABS_Y, accel_data[1]);
    input_report_abs(data->input_dev, ABS_Z, accel_data[2]);
    input_report_abs(data->input_dev, ABS_RX, gyro_data[0]);
    input_report_abs(data->input_dev, ABS_RY, gyro_data[1]);
    input_report_abs(data->input_dev, ABS_RZ, gyro_data[2]);

    input_sync(data->input_dev);
    schedule_delayed_work(&data->work, msecs_to_jiffies(100));
}
123456789101112131415161718192021222324252627282930313233
```

---

**免责声明：本内容部分参考野火科技及其他相关公开资料，若有侵权或者勘误请联系作者。**

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/139731877

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