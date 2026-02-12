---
title: 
aliases: 
tags: 
description:
---


# 备注(声明)：

![RK3568（linux学习）/rk3568芯片开发/linux外设驱动开发（未）/assets/第二十三期 ADC/file-20250810171741867.png](assets/第二十三期%20ADC/file-20250810171741867.png)

·
# 一、基础知识

## ADC基础知识
### 1 、什么是 ADC - 模拟值转数字值
[“1.ADC基础知识”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#1.ADC基础知识&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={30EC0FEB-CCB0-4B9F-91B8-DF5D3CA7B7EA}&object-id={45367CE8-B9AA-46B5-8F33-FB9373DCC9DA}&12)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F1.ADC%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%7C30EC0FEB-CCB0-4B9F-91B8-DF5D3CA7B7EA%2F%29&wdpartid=%7b1AF52A68-53E6-4B8D-B0CC-3A64CE94F4BF%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 2 、ADC的分辨率的计算
[“1.ADC基础知识”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#1.ADC基础知识&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={30EC0FEB-CCB0-4B9F-91B8-DF5D3CA7B7EA}&object-id={45367CE8-B9AA-46B5-8F33-FB9373DCC9DA}&2A)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F1.ADC%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%7C30EC0FEB-CCB0-4B9F-91B8-DF5D3CA7B7EA%2F%29&wdpartid=%7b1AF52A68-53E6-4B8D-B0CC-3A64CE94F4BF%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 3 、其他概念
[“1.ADC基础知识”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#1.ADC基础知识&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={30EC0FEB-CCB0-4B9F-91B8-DF5D3CA7B7EA}&object-id={45367CE8-B9AA-46B5-8F33-FB9373DCC9DA}&65)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F1.ADC%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%7C30EC0FEB-CCB0-4B9F-91B8-DF5D3CA7B7EA%2F%29&wdpartid=%7b1AF52A68-53E6-4B8D-B0CC-3A64CE94F4BF%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 4 、





## iTOP-RK3568开发板ADC接口介绍
### 1 、6通道10位SAR-ADC （逐次逼近型）
[“2.iTOP-RK3568开发板ADC接口介绍”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#2.iTOP-RK3568开发板ADC接口介绍&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={58BFCF77-2C11-4199-A8AB-135238EF6FA9}&object-id={7100173E-39C3-422C-9D31-79E16C116244}&30)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F2.iTOP-RK3568%E5%BC%80%E5%8F%91%E6%9D%BFADC%E6%8E%A5%E5%8F%A3%E4%BB%8B%E7%BB%8D%7C58BFCF77-2C11-4199-A8AB-135238EF6FA9%2F%29&wdpartid=%7b94AC88AE-8720-4A67-9161-C2BC71BE42E6%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

-  **硬件引脚原理图**
[“2.iTOP-RK3568开发板ADC接口介绍”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#2.iTOP-RK3568开发板ADC接口介绍&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={58BFCF77-2C11-4199-A8AB-135238EF6FA9}&object-id={7100173E-39C3-422C-9D31-79E16C116244}&81)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F2.iTOP-RK3568%E5%BC%80%E5%8F%91%E6%9D%BFADC%E6%8E%A5%E5%8F%A3%E4%BB%8B%E7%BB%8D%7C58BFCF77-2C11-4199-A8AB-135238EF6FA9%2F%29&wdpartid=%7b94AC88AE-8720-4A67-9161-C2BC71BE42E6%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))
### 2 、2通道TS-ADC
[那这里呢他的第零路是监测这个CPU第一路啊](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#2.iTOP-RK3568开发板ADC接口介绍&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={58BFCF77-2C11-4199-A8AB-135238EF6FA9}&object-id={7100173E-39C3-422C-9D31-79E16C116244}&59)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F2.iTOP-RK3568%E5%BC%80%E5%8F%91%E6%9D%BFADC%E6%8E%A5%E5%8F%A3%E4%BB%8B%E7%BB%8D%7C58BFCF77-2C11-4199-A8AB-135238EF6FA9%2F%29&wdpartid=%7b94AC88AE-8720-4A67-9161-C2BC71BE42E6%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 3 、ADC接口的复用情况
[“2.iTOP-RK3568开发板ADC接口介绍”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#2.iTOP-RK3568开发板ADC接口介绍&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={58BFCF77-2C11-4199-A8AB-135238EF6FA9}&object-id={7100173E-39C3-422C-9D31-79E16C116244}&9C)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F2.iTOP-RK3568%E5%BC%80%E5%8F%91%E6%9D%BFADC%E6%8E%A5%E5%8F%A3%E4%BB%8B%E7%BB%8D%7C58BFCF77-2C11-4199-A8AB-135238EF6FA9%2F%29&wdpartid=%7b94AC88AE-8720-4A67-9161-C2BC71BE42E6%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 4 、ADC接口在开发板上实际位置
[“2.iTOP-RK3568开发板ADC接口介绍”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#2.iTOP-RK3568开发板ADC接口介绍&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={58BFCF77-2C11-4199-A8AB-135238EF6FA9}&object-id={7100173E-39C3-422C-9D31-79E16C116244}&A7)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F2.iTOP-RK3568%E5%BC%80%E5%8F%91%E6%9D%BFADC%E6%8E%A5%E5%8F%A3%E4%BB%8B%E7%BB%8D%7C58BFCF77-2C11-4199-A8AB-135238EF6FA9%2F%29&wdpartid=%7b94AC88AE-8720-4A67-9161-C2BC71BE42E6%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 5、



## 逐次逼近型ADC工作原理(了解)
### 1 、逐次逼近型 ADC工作原理框图
[“3.逐次逼近型ADC工作原理(了解)”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#3.逐次逼近型ADC工作原理\(了解\)&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={385BA348-F38E-4849-8FB1-336373A317F4}&object-id={C057EC4E-649B-46D8-B9F3-4055F33F75E2}&12)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F3.%E9%80%90%E6%AC%A1%E9%80%BC%E8%BF%91%E5%9E%8BADC%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86%28%E4%BA%86%E8%A7%A3%5C%29%7C385BA348-F38E-4849-8FB1-336373A317F4%2F%29&wdpartid=%7bDFF27FAC-FCA0-4F7E-AD07-5F17F05D3E83%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 2 、举例 - 5 位逐次逼近型 ADC


### 3 、




# 二、如何把ADC用起来

## ADC子系统框图
### 1 、框架图
![RK3568（linux学习）/rk3568芯片开发/linux外设驱动开发（未）/assets/第二十三期 ADC/file-20250810171742100.png](assets/第二十三期%20ADC/file-20250810171742100.png)

### 2 、


## 通过sysfs接口操作ADC
### 1 、adc设备在sysfs系统中的位置
[“5.通过sysfs接口操作ADC（1）”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#5.通过sysfs接口操作ADC（1）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={67864D5F-B799-457C-8F39-B2A831550FB5}&object-id={03CF2A35-F18B-445A-A8FB-284A89FA8800}&15)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F5.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%881%EF%BC%89%7C67864D5F-B799-457C-8F39-B2A831550FB5%2F%29&wdpartid=%7bE536C135-E16E-493C-8D49-39DA39E09D83%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 2 、用cat命令读取通道
[“5.通过sysfs接口操作ADC（1）”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#5.通过sysfs接口操作ADC（1）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={67864D5F-B799-457C-8F39-B2A831550FB5}&object-id={03CF2A35-F18B-445A-A8FB-284A89FA8800}&15)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F5.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%881%EF%BC%89%7C67864D5F-B799-457C-8F39-B2A831550FB5%2F%29&wdpartid=%7bE536C135-E16E-493C-8D49-39DA39E09D83%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

- 1 cat in_voltage7_raw

### 3 、通道值换算成电压
[开发板这里我什么都不接](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#5.通过sysfs接口操作ADC（1）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={67864D5F-B799-457C-8F39-B2A831550FB5}&object-id={03CF2A35-F18B-445A-A8FB-284A89FA8800}&3E)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F5.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%881%EF%BC%89%7C67864D5F-B799-457C-8F39-B2A831550FB5%2F%29&wdpartid=%7bE536C135-E16E-493C-8D49-39DA39E09D83%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

- 1 1.8v/1024  乘通道值
### 4 、査看 CPU 和 GPU 的温度的操作
[开发板这里我什么都不接](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#5.通过sysfs接口操作ADC（1）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={67864D5F-B799-457C-8F39-B2A831550FB5}&object-id={03CF2A35-F18B-445A-A8FB-284A89FA8800}&3E)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F5.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%881%EF%BC%89%7C67864D5F-B799-457C-8F39-B2A831550FB5%2F%29&wdpartid=%7bE536C135-E16E-493C-8D49-39DA39E09D83%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 5、ADC的八个通道对应的属性文件
[这样的属性文件呢](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#5.通过sysfs接口操作ADC（1）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={67864D5F-B799-457C-8F39-B2A831550FB5}&object-id={03CF2A35-F18B-445A-A8FB-284A89FA8800}&33)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F5.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%881%EF%BC%89%7C67864D5F-B799-457C-8F39-B2A831550FB5%2F%29&wdpartid=%7bE536C135-E16E-493C-8D49-39DA39E09D83%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 6、





## 编写应用程序通过sysfs接口操作ADC
### 1 、代码编写
[#include <stdio.h>    // 引入标准输入输出库](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#6.通过sysfs接口操作ADC（2）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={F642510F-C8BB-4B6F-820A-08A8BD14CFBC}&object-id={B4C8A947-2960-4F1B-9AF0-CF6CEFE9BBFF}&10)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F6.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%882%EF%BC%89%7CF642510F-C8BB-4B6F-820A-08A8BD14CFBC%2F%29&wdpartid=%7b6096B32A-7D22-4C2A-90A9-424F1AB6290C%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

> [!note] 关键代码
>     //  "r" 表示以只读模式打开文件。
>     fp = fopen("/sys/bus/iio/devices/iio:device0/in_voltage4_raw", "r");
> 
>     // 从打开的文件中读取一个整数值到 scale 变量中
>     fscanf(fp, "%d", &scale);


### 2 、实验操作及现象
[“6.通过sysfs接口操作ADC（2）”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#6.通过sysfs接口操作ADC（2）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={F642510F-C8BB-4B6F-820A-08A8BD14CFBC}&object-id={FBCCBED3-112D-48CC-9409-79696431B153}&36)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F6.%E9%80%9A%E8%BF%87sysfs%E6%8E%A5%E5%8F%A3%E6%93%8D%E4%BD%9CADC%EF%BC%882%EF%BC%89%7CF642510F-C8BB-4B6F-820A-08A8BD14CFBC%2F%29&wdpartid=%7b6096B32A-7D22-4C2A-90A9-424F1AB6290C%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))


### 3 、


## 编写ADC驱动程序（未完）
### 1 、驱动代码编写（通过IIO子系统）
[#include <linux/module.h>](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#8.编写ADC驱动程序（2）&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={F2D51B9B-504C-4E06-9840-BC0E1B9076D6}&object-id={A4499B8D-35BE-4A94-B551-120DF6CB2893}&E)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F8.%E7%BC%96%E5%86%99ADC%E9%A9%B1%E5%8A%A8%E7%A8%8B%E5%BA%8F%EF%BC%882%EF%BC%89%7CF2D51B9B-504C-4E06-9840-BC0E1B9076D6%2F%29&wdpartid=%7bC12E804C-0F8F-463C-818C-5AA9A3F69DB9%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

> [!关键代码]
> // 设备树匹配表，用于匹配具体的硬件设备
> const struct of_device_id adc_driver_match[] = {
>     {.compatible = "myadc"},
>     {},
> };
> 
> struct miscdevice adc_misc_dev = {
>     .minor = MISC_DYNAMIC_MINOR,
>     .name = "adc",		//在/dev下生成设备节点/dev/adc    
>     .fops = &adc_misc_fops,
> };
> 
>     // 获取与设备树兼容的ADC通道
>     adc_chan = iio_channel_get(&(pdev->dev), NULL);
> 
>    // 读取指定ADC通道的原始值到scale变量中
>    iio_read_channel_raw(adc_chan, &scale);
> 


### 2 、应用测试程序的编写
[#include <stdio.h>      // 标准输入输出库，提供如printf、fprintf等函数的声明](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#9.编写ADC驱动程序（3）-应用程序&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={120CDA17-6190-4CBF-BC5B-D59557E82763}&object-id={3A6ED828-61FB-49C5-8110-42F6F7C8F999}&2D)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F9.%E7%BC%96%E5%86%99ADC%E9%A9%B1%E5%8A%A8%E7%A8%8B%E5%BA%8F%EF%BC%883%EF%BC%89-%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F%7C120CDA17-6190-4CBF-BC5B-D59557E82763%2F%29&wdpartid=%7b701E89E8-BE39-4A08-8376-2C9CC6AD5C20%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

> [!note] 关键代码
> `// 定义自定义的ioctl命令CMD_READ_SCALE，用于向设备发送特定指令并读取数据`
> `#define CMD_READ_SCALE _IOR('A', 1, int)    // 'A'是魔数，1是序号，int表示数据类型`
> 
>     // 尝试以读写模式打开/dev/adc设备文件
>     fd = open("/dev/adc", O_RDWR);
> 
>     // 使用ioctl发送CMD_READ_SCALE命令给设备，并将返回值存储在scale变量中
>     ioctl(fd, CMD_READ_SCALE, &scale);
> 


### 3 、实验操作及现象
[“9.编写ADC驱动程序（3）-应用程序”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/第二十三期_ADC.one#9.编写ADC驱动程序（3）-应用程序&section-id={313A2954-EFE2-4A38-9EBF-B63CAFC74968}&page-id={120CDA17-6190-4CBF-BC5B-D59557E82763}&object-id={17255284-5AD2-4F90-9593-2559F6E858DE}&12)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E6%9C%9F_ADC.one%7C313A2954-EFE2-4A38-9EBF-B63CAFC74968%2F9.%E7%BC%96%E5%86%99ADC%E9%A9%B1%E5%8A%A8%E7%A8%8B%E5%BA%8F%EF%BC%883%EF%BC%89-%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F%7C120CDA17-6190-4CBF-BC5B-D59557E82763%2F%29&wdpartid=%7b701E89E8-BE39-4A08-8376-2C9CC6AD5C20%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s1eaed7aadd0b4f5f9f2756f1d3af9f7d))

### 4 、

### 5、


### 6、


### 7、


### 8、


## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


