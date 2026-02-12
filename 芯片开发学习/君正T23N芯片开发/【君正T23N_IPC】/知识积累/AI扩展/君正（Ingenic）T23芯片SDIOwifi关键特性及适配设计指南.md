

### **君正（Ingenic）T23芯片关键特性及适配设计指南**

君正T23是一款面向物联网和多媒体应用的<span style="background:#b1ffff">32位RISC处理器</span>，搭载XBurst2双核CPU（主频1.5GHz），集成丰富外设接口和低功耗管理单元。以下结合ATBM6031-X WiFi模块、SDIO总线、`WAKE_HOST_WIFI`信号等需求，解析T23的设计要点。

---

#### **1. T23芯片与外设接口配置**
##### **1.1 SDIO接口支持**
- **硬件资源**：  
  T23支持 **SDIO 3.0控制器**（兼容SDIO 2.0），可配置为4位模式，最高时钟频率50MHz。  
  - **关键引脚**（以GPIO复用为例）：  
    | **SDIO信号** | **T23 GPIO引脚（示例）** |  
    |--------------|--------------------------|  
    | SDIO_CLK     | PB8                      |  
    | SDIO_CMD     | PB9                      |  
    | SDIO_DATA0   | PB10                     |  
    | SDIO_DATA1   | PB11                     |  
    | SDIO_DATA2   | PB12                     |  
    | SDIO_DATA3   | PB13                     |  

- **设备树配置**（示例片段）：  
  ```dts
  &sdio {
      status = "okay";
      bus-width = <4>;          // 4位模式
      max-frequency = <50000000>; // 50MHz
      cap-sd-highspeed;          // 支持高速模式
      non-removable;             // 固定设备（如WiFi模块）
      vmmc-supply = <&vcc_sdio>; // SDIO电源（3.3V）
      pinctrl-names = "default";
      pinctrl-0 = <&sdio_pins>;  // 引脚复用配置
  };
  ```

##### **1.2 GPIO与中断配置（WAKE_HOST_WIFI）**
- **硬件连接**：  
  ATBM6031-X的`WAKE_HOST_WIFI`引脚连接至T23的GPIO中断引脚（如PA15），触发方式通常为**低电平有效**（需根据模块手册确认）。  

- **设备树配置**：  
  ```dts
  wifi {
      compatible = "atbm,atbm6031";
      wake-host-gpio = <&gpa 15 GPIO_ACTIVE_LOW>; // PA15，低电平触发
      vddio-supply = <&vcc_3v3>;                  // 模块IO电源
      pinctrl-names = "default";
      pinctrl-0 = <&wifi_wake_pin>;
  };
  ```

- **驱动适配**：  
  T23的GPIO中断需在驱动中注册回调函数，示例代码：  
  ```c
  static irqreturn_t wifi_wake_irq_handler(int irq, void *dev_id) {
      // 唤醒主控，处理WiFi事件
      disable_irq_nosync(irq);  // 临时禁用中断
      schedule_work(&wake_work); // 调度工作队列
      return IRQ_HANDLED;
  }

  // 中断注册
  ret = request_irq(gpio_to_irq(GPIO_WAKE_HOST), wifi_wake_irq_handler,
                   IRQF_TRIGGER_LOW | IRQF_NO_SUSPEND, "wifi_wake", NULL);
  ```

---

#### **2. 低功耗管理优化**
##### **2.1 电源模式切换**
- **T23低功耗模式**：  
  - **IDLE模式**：CPU暂停，外设保持运行（WiFi模块可唤醒）。  
  - **SLEEP模式**：仅RTC和部分唤醒源有效，需通过`WAKE_HOST_WIFI`中断唤醒。  

- **配置步骤**：  
  1. 在进入休眠前，启用PA15的中断唤醒功能：  
     ```c
     ingenic_pm_configure_wakeup_source(WAKEUP_SRC_GPIO, GPIO_PA(15), 1);
     ```  
  2. 在休眠期间，WiFi模块保持最低工作电流（通常<1mA）。  

##### **2.2 动态电源控制**
- **WiFi模块供电**：  
  通过T23的GPIO控制WiFi的`WL_REG_ON`引脚（如PC7），在休眠时关闭模块电源：  
  ```c
  // 使能电源
  gpiod_set_value(gpio_wl_reg_on, 1);
  mdelay(10); // 等待模块启动

  // 休眠时关闭电源
  gpiod_set_value(gpio_wl_reg_on, 0);
  ```


---

#### **4. 调试与验证**
##### **4.1 SDIO功能测试**
1. **识别测试**：  
   - 系统启动后，检查`dmesg | grep mmc`，确认SDIO设备成功枚举。  
   - 示例输出：  
     ```
     mmc0: new high-speed SDIO card at address 0001
     ```  

2. **数据传输测试**：  
   - 使用`iwlist scan`扫描WiFi网络，验证数据吞吐量。  
   - 抓取SDIO_CLK波形，确认频率稳定在50MHz（示波器带宽≥100MHz）。  

##### **4.2 唤醒功能验证**
- **休眠唤醒测试**：  
  1. 进入低功耗模式：  
     ```bash
     echo mem > /sys/power/state
     ```  
  2. 触发ATBM6031-X发送唤醒信号（如发送Ping包），确认系统唤醒。  

- **中断信号测量**：  
  用示波器捕获PA15引脚电平，确认`WAKE_HOST_WIFI`信号有效宽度≥100ms（避免短脉冲无法唤醒）。  

---

#### **5. 常见问题解决**
- **SDIO初始化失败**：  
  - 检查设备树中`max-frequency`是否超出模块支持范围（ATBM6031-X通常支持50MHz）。  
  - 测量SDIO_CLK是否输出，确认GPIO复用配置正确。  

- **无法唤醒主机**：  
  - 确认休眠前已启用GPIO唤醒源：`cat /sys/power/wake_lock`。  
  - 测量`WAKE_HOST_WIFI`信号是否在休眠期间保持有效电平（避免电平漂移）。  

---

### **总结**
君正T23通过灵活的外设复用和低功耗管理机制，可高效驱动ATBM6031-X WiFi模块。设计时需重点关注SDIO信号完整性、射频隔离及休眠唤醒流程的软硬件协同。调试阶段优先验证SDIO枚举与中断唤醒功能，再逐步优化射频性能与功耗。