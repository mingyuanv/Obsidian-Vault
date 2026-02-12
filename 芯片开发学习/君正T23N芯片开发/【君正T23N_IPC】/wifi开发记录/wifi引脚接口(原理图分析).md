
[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/知识积累/AI扩展/ATBM6031-X接口类型]]

> [!PDF|note] [[芯片开发学习/君正T23N芯片开发/sdk_资料库/君正T23N开发资料/BSP/T23 BSP开发参考V1.1.pdf#page=31&selection=280,1,356,2&color=note|T23 BSP开发参考V1.1, p.31]]
> > pio_num 即 GPIO 号。计算公式为： PA(n) = 0 * 32 + n PB(n) = 1 * 32 + n ... 例如：申请 PB(10) = 1 * 32 + 10 = 42 $ echo 42 > export 申请后在“/sys/class/gpio”目录下即会出现 gpio42 目录
> 
> 


![Pasted image 20250414211441.png](../../../../通用文件夹/媒体库/图片库/Pasted%20image%2020250414211441.png)




# 1.wifi的引脚



![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422229.png](assets/wifi引脚接口(原理图分析)/file-20250810171422229.png)

![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422334.png](assets/wifi引脚接口(原理图分析)/file-20250810171422334.png)



<span style="background:#fdbfff">复位</span>
![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422444.png](assets/wifi引脚接口(原理图分析)/file-20250810171422444.png)
## 在wifi 驱动源码中的表现形式
[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/wifi开发记录/wifi驱动调试记录-高拓讯达#4、驱动数据结构解析]]

[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/wifi开发记录/wifi驱动调试记录-高拓讯达#5、修改外部调用（复位&扫卡动作）]]

# 2.核心板用到的引脚





![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422524.png](assets/wifi引脚接口(原理图分析)/file-20250810171422524.png)

<span style="background:#d3f8b6">这六个引脚，在图形化界面配置好了。</span>



![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422599.png](assets/wifi引脚接口(原理图分析)/file-20250810171422599.png)

//<span style="background:#affad1"> WiFi 电源使能引脚</span>，使用 PA6

![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422677.png](assets/wifi引脚接口(原理图分析)/file-20250810171422677.png)

#define WL_WAKE_HOST    GPIO_PB(28)     //<span style="background:#affad1"> WiFi 唤醒主机引脚</span>，使用 PB28

![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422754.png](assets/wifi引脚接口(原理图分析)/file-20250810171422754.png)
PB26

 //<span style="background:#affad1"> WiFi 使能引脚</span>，使用 PB26


## 在内核驱动源码中的表现形式
[[芯片开发学习/君正T23N芯片开发/【君正T23N_IPC】/wifi开发记录/wifi驱动调试记录-高拓讯达#调整君正sdk内核配置]]


# 3.引脚解析（AI）

#### **1. MSC1_CMD功能定义**

- **核心作用**：`MSC1_CMD`是存储控制器的**命令传输通道**，用于主机（如CPU）<span style="background:#affad1">向存储设备发送控制命令（如读写请求、初始化指令）或接收设备响应</span>[3](https://www.xjishu.com/zhuanli/55/CN105528049.html)[4](https://blog.csdn.net/aloneboyooo/article/details/132687349)。
- **协议支持**：常见于SD卡、eMMC等存储接口协议中，遵循相应时序和电气规范[3](https://www.xjishu.com/zhuanli/55/CN105528049.html)。
![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422833.png](assets/wifi引脚接口(原理图分析)/file-20250810171422833.png)
### 2.**WAKE_HOST_WIFI引脚定义解析**


![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422677.png](assets/wifi引脚接口(原理图分析)/file-20250810171422677.png)

<span style="background:#fdbfff">pb28</span>


32
#### **1. 核心功能定义**

`WAKE_HOST_WIFI`（或类似名称如`WL_HOST_WAKE`）是Wi-Fi模块与主控芯片之间的 **唤醒信号接口**，主要用于以下场景：

- **数据唤醒**：当Wi-Fi模块接收到网络数据（如TCP/UDP报文）时，通过该引脚向主控发送中断信号，触发CPU从低功耗模式恢复并处理数据[1](https://blog.csdn.net/Teacian/article/details/106556456)[6](https://developer.aliyun.com/ask/449202)。
- **状态同步**：维持Wi-Fi模块与主控之间的通信状态同步，避免因休眠导致数据丢失[2](https://wenku.csdn.net/answer/e10677160a274616994b24e46dad64b7)[7](https://blog.csdn.net/jinron10/article/details/82915093)。

---

#### **2. 电平特性与触发逻辑**

- **有效电平**：
    - **高电平有效**：常见配置，默认低电平，当数据到达时拉高，直到主控处理完成后恢复低电平[1](https://blog.csdn.net/Teacian/article/details/106556456)[7](https://blog.csdn.net/jinron10/article/details/82915093)。
    - **低电平有效**：部分模块可能采用此设计，需根据硬件手册确认[5](https://blog.csdn.net/lzg2011/article/details/117521109)]。
- **触发方式**：通常为边沿触发（如上升沿），需在主控GPIO配置中设置对应的中断模式[1](https://blog.csdn.net/Teacian/article/details/106556456)[7](https://blog.csdn.net/jinron10/article/details/82915093)。

---

#### **3. 硬件连接与配置**

- **引脚映射**：
    - 需将`WAKE_HOST_WIFI`连接到主控的GPIO引脚，并配置为中断输入模式[1](https://blog.csdn.net/Teacian/article/details/106556456)[5](https://blog.csdn.net/lzg2011/article/details/117521109)]。
    - **示例电路**：部分模块要求外部上拉电阻（如10kΩ）以确保默认电平稳定[7](https://blog.csdn.net/jinron10/article/details/82915093)]。
- **协同引脚**：
    - **WL_REG_ON**：Wi-Fi模块电源使能引脚，控制模块上下电[1](https://blog.csdn.net/Teacian/article/details/106556456)[5](https://blog.csdn.net/lzg2011/article/details/117521109)]。
    - **SDIO_CLK/DATA**：数据传输总线，与唤醒信号配合实现高效通信[5](https://blog.csdn.net/lzg2011/article/details/117521109)[7](https://blog.csdn.net/jinron10/article/details/82915093)]。

#### **4. 驱动与系统适配**

- **驱动配置**：
    - 在Linux内核中需注册GPIO中断服务函数，响应`WAKE_HOST_WIFI`信号并唤醒系统[1](https://blog.csdn.net/Teacian/article/details/106556456)[7](https://blog.csdn.net/jinron10/article/details/82915093)]。
    - 示例代码片段（基于Linux驱动）：
        
        c
        
        复制
        
        `// 定义唤醒引脚及中断处理函数   #define WL_HOST_WAKE_GPIO  123   request_irq(gpio_to_irq(WL_HOST_WAKE_GPIO), wifi_wake_handler, IRQF_TRIGGER_RISING, "wifi_wake", NULL);`  
        
- **电源管理**：在休眠模式下，需保持`WL_REG_ON`供电，否则Wi-Fi模块状态可能丢失[1](https://blog.csdn.net/Teacian/article/details/106556456)[5](https://blog.csdn.net/lzg2011/article/details/117521109)]。
### **总结**

`WAKE_HOST_WIFI`是Wi-Fi模块与主控协同工作的关键接口，需确保硬件连接正确、电平逻辑匹配，并在驱动中实现高效的中断响应。开发时建议优先参考目标模块的官方文档（如全志H6、海思Hi3516等平台的适配说明）[5](https://blog.csdn.net/lzg2011/article/details/117521109)[7](https://blog.csdn.net/jinron10/article/details/82915093)]。





### **3.WIFI_RST_N引脚定义解析**

![君正T23N芯片开发/【君正T23N\_IPC】/wifi开发记录/assets/wifi引脚接口(原理图分析)/file-20250810171422754.png](assets/wifi引脚接口(原理图分析)/file-20250810171422754.png)
PB26



#### **1. 核心功能定义**

`WIFI_RST_N` 是<span style="background:#b1ffff"> **WiFi模块的复位控制引脚**</span>，常见于嵌入式设备或通信模块（如ESP8266、ESP32等）。其核心作用是通过电平信号控制WiFi模块的硬件复位，常用于模块初始化异常、死机或需要强制重启的场景[2](https://blog.csdn.net/xiaoyuanwuhui/article/details/83795393)[3](https://blog.csdn.net/IT_BOY__/article/details/71856076)。

---

#### **2. 电平逻辑与操作**

- **低电平有效**：
    - 当 `WIFI_RST_N` 被拉低（通常持续几十毫秒以上），WiFi模块会触发硬件复位，内部状态机重置并重新初始化[3](https://blog.csdn.net/IT_BOY__/article/details/71856076)[8](https://www.cnblogs.com/guguobao/p/10147130.html)。
    - 复位后需恢复高电平，否则模块将无法正常工作。
- **默认状态**：
    - 大部分设计中，该引脚默认通过上拉电阻保持高电平（如10kΩ），避免意外复位[5](https://blog.csdn.net/viiicion/article/details/125340363)[8](https://www.cnblogs.com/guguobao/p/10147130.html)]。

---

#### **3. 典型应用场景**

1. **系统启动初始化**：
    - 主控芯片（如MCU）在启动时拉低 `WIFI_RST_N` 以复位WiFi模块，确保其从稳定状态开始通信[8](https://www.cnblogs.com/guguobao/p/10147130.html)]。
2. **异常恢复**：
    - 当WiFi模块出现响应超时、断连等问题时，主控通过此引脚强制重启模块[5](https://blog.csdn.net/viiicion/article/details/125340363)]。
3. **低功耗管理**：
    - 在某些低功耗设计中，通过周期性复位模块实现休眠唤醒策略[5](https://blog.csdn.net/viiicion/article/details/125340363)]。

---

#### **4. 硬件设计注意事项**

- **驱动能力**：
    - 主控GPIO需具备足够的驱动能力（如推挽输出模式），避免电平不稳导致复位失败[8](https://www.cnblogs.com/guguobao/p/10147130.html)]。
- **抗干扰设计**：
    - 避免长走线或靠近高频信号线，防止误触发复位。必要时并联电容（如0.1μF）滤除噪声[3](https://blog.csdn.net/IT_BOY__/article/details/71856076)]。
- **兼容性验证**：
    - 部分模块（如ESP8266）的 `RST` 引脚可能与其他功能复用，需查阅具体芯片手册确认[2](https://blog.csdn.net/xiaoyuanwuhui/article/details/83795393)[3](https://blog.csdn.net/IT_BOY__/article/details/71856076)]。

#### **5. 典型操作流程示例**

**场景：STM32通过GPIO控制ESP8266复位**

c

复制

`// 引脚配置：PA1 -> WIFI_RST_N  void WiFi_Reset(void) {     HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET); // 拉低复位    HAL_Delay(100);                                       // 保持低电平100ms    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);   // 恢复高电平  }`

**说明**：通过短暂拉低 `WIFI_RST_N` 实现可靠复位，适用于固件更新或通信异常后的恢复[8](https://www.cnblogs.com/guguobao/p/10147130.html)]。

---

### **总结**

`WIFI_RST_N` 是WiFi模块硬件复位的关键控制引脚，其设计需遵循低电平触发、稳定驱动和抗干扰原则。合理使用该引脚可提升系统稳定性和容错能力[2](https://blog.csdn.net/xiaoyuanwuhui/article/details/83795393)[5](https://blog.csdn.net/viiicion/article/details/125340363)[8](https://www.cnblogs.com/guguobao/p/10147130.html)]。








