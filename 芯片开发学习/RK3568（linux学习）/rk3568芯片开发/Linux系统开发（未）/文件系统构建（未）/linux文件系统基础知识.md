---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---
# 备注(声明)：



# 一、基础知识

## 什么是文件系统、根文件系统以及如何构 建
### 1 、Linux系统组成
[“01-什么是文件系统、根文件系统以及如何构 建”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#01-什么是文件系统、根文件系统以及如何构%20建&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={4240E827-573C-4D9A-9487-4DDFE4AA6D67}&object-id={A8463CA2-F4D9-46B7-AC06-573FAF9C4529}&12)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F01-%E4%BB%80%E4%B9%88%E6%98%AF%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E3%80%81%E6%A0%B9%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E6%9E%84%20%E5%BB%BA%7C4240E827-573C-4D9A-9487-4DDFE4AA6D67%2F%29&wdpartid=%7b5740D650-2452-4A5F-8C44-1816E66D154E%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s3210484a72894f69a6a7a2deed6a881c))


### 2 、什么是文件系统? - 组织和管理文件的一个系统
[“01-什么是文件系统、根文件系统以及如何构 建”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#01-什么是文件系统、根文件系统以及如何构%20建&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={4240E827-573C-4D9A-9487-4DDFE4AA6D67}&object-id={A8463CA2-F4D9-46B7-AC06-573FAF9C4529}&2A)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F01-%E4%BB%80%E4%B9%88%E6%98%AF%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E3%80%81%E6%A0%B9%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E6%9E%84%20%E5%BB%BA%7C4240E827-573C-4D9A-9487-4DDFE4AA6D67%2F%29&wdpartid=%7b5740D650-2452-4A5F-8C44-1816E66D154E%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s3210484a72894f69a6a7a2deed6a881c))

### 3 、什么是根文件系统呢?
[“01-什么是文件系统、根文件系统以及如何构 建”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#01-什么是文件系统、根文件系统以及如何构%20建&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={4240E827-573C-4D9A-9487-4DDFE4AA6D67}&object-id={A8463CA2-F4D9-46B7-AC06-573FAF9C4529}&34)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F01-%E4%BB%80%E4%B9%88%E6%98%AF%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E3%80%81%E6%A0%B9%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E6%9E%84%20%E5%BB%BA%7C4240E827-573C-4D9A-9487-4DDFE4AA6D67%2F%29&wdpartid=%7b5740D650-2452-4A5F-8C44-1816E66D154E%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s3210484a72894f69a6a7a2deed6a881c))

### 4 、根文件系统目录功能介绍
[“01-什么是文件系统、根文件系统以及如何构 建”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#01-什么是文件系统、根文件系统以及如何构%20建&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={4240E827-573C-4D9A-9487-4DDFE4AA6D67}&object-id={A8463CA2-F4D9-46B7-AC06-573FAF9C4529}&41)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F01-%E4%BB%80%E4%B9%88%E6%98%AF%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E3%80%81%E6%A0%B9%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E6%9E%84%20%E5%BB%BA%7C4240E827-573C-4D9A-9487-4DDFE4AA6D67%2F%29&wdpartid=%7b5740D650-2452-4A5F-8C44-1816E66D154E%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s3210484a72894f69a6a7a2deed6a881c))

### 5、根文件系统制作工具 - buzybox等
[“01-什么是文件系统、根文件系统以及如何构 建”页上的图片](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#01-什么是文件系统、根文件系统以及如何构%20建&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={4240E827-573C-4D9A-9487-4DDFE4AA6D67}&object-id={F899A125-4B5E-4A6E-8FCB-54BACE4981AD}&3E)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F01-%E4%BB%80%E4%B9%88%E6%98%AF%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E3%80%81%E6%A0%B9%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E6%9E%84%20%E5%BB%BA%7C4240E827-573C-4D9A-9487-4DDFE4AA6D67%2F%29&wdpartid=%7b5740D650-2452-4A5F-8C44-1816E66D154E%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s3210484a72894f69a6a7a2deed6a881c))

- 1 但是呢如果你做项目，这个build root是非常合适的，因为它非常的简单
### 6、




## RK3568 Linux系统下的目录结构
[RK3568 Linux系统下的目录结构](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/自主思考学习.one#RK3568%20Linux系统下的目录结构&section-id={144DA372-ACEC-4771-B0D4-C902A97035BF}&page-id={71BFA610-614F-4A5A-9186-B97F3BA2107F}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E8%87%AA%E4%B8%BB%E6%80%9D%E8%80%83%E5%AD%A6%E4%B9%A0.one%7C144DA372-ACEC-4771-B0D4-C902A97035BF%2FRK3568%20Linux%E7%B3%BB%E7%BB%9F%E4%B8%8B%E7%9A%84%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84%7C71BFA610-614F-4A5A-9186-B97F3BA2107F%2F%29&wdpartid=%7b8EC3E862-711E-0B86-0A7C-BC657A305D3B%7d%7b1%7d&wdsectionfileid=52D4B76BB0FFCF51!s8771e5dd69b243b8b8759e7aa53e7997))


##  Linux 文件系统简介（手册）
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/16.开发板学习教程/文件系统构建手册_rk3568_v1.1.pdf#page=11&selection=17,0,25,6&color=important|文件系统构建手册_rk3568_v1.1, p.11]]
> > 第 1 章 Linux 文件系统简介
> 
> 

### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、




# 二、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


# 三、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


# 四、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


# 五、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


