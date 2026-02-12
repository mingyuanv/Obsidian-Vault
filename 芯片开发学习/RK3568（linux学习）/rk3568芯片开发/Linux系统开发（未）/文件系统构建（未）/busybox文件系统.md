# 备注：
busybox它就有一个特点，它非常的<span style="background:#b1ffff">灵活</span>，
也就是说我们需要<span style="background:#affad1">配置哪些功能</span>，我们自己去<span style="background:#affad1">按照自己的需求去配置就可以了</span>。
这节课给大家讲的，它实际上是一个<span style="background:#b1ffff">标准的模板。</span>

# 1.构建根文件系统
[02-使用busybox构建文件系统](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#02-使用busybox构建文件系统&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={5779686D-DDAB-4D7A-AA46-866721B28873}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F02-%E4%BD%BF%E7%94%A8busybox%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%7C5779686D-DDAB-4D7A-AA46-866721B28873%2F%29))
## 1.1解压busybox源码
[解压busybox源码](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#02-使用busybox构建文件系统&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={5779686D-DDAB-4D7A-AA46-866721B28873}&object-id={3753CA09-2B9E-4320-99C7-7F7CB83B3E18}&14)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F02-%E4%BD%BF%E7%94%A8busybox%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%7C5779686D-DDAB-4D7A-AA46-866721B28873%2F%29))
## 1.2初始化好make menuconfig图形化界面。 
[初始化好make menuconfig图形化界面。](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#02-使用busybox构建文件系统&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={5779686D-DDAB-4D7A-AA46-866721B28873}&object-id={3753CA09-2B9E-4320-99C7-7F7CB83B3E18}&23)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F02-%E4%BD%BF%E7%94%A8busybox%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%7C5779686D-DDAB-4D7A-AA46-866721B28873%2F%29))

配置<span style="background:#affad1">交叉编译器</span>和<span style="background:#affad1">linux命令</span>。
## 1.3Busybox支持中文
[Busybox支持中文](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#02-使用busybox构建文件系统&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={5779686D-DDAB-4D7A-AA46-866721B28873}&object-id={3753CA09-2B9E-4320-99C7-7F7CB83B3E18}&2D)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F02-%E4%BD%BF%E7%94%A8busybox%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%7C5779686D-DDAB-4D7A-AA46-866721B28873%2F%29))

## 1.4编译构建根文件系统
[编译构建根文件系统](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#02-使用busybox构建文件系统&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={5779686D-DDAB-4D7A-AA46-866721B28873}&object-id={3753CA09-2B9E-4320-99C7-7F7CB83B3E18}&37)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F02-%E4%BD%BF%E7%94%A8busybox%E6%9E%84%E5%BB%BA%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%7C5779686D-DDAB-4D7A-AA46-866721B28873%2F%29))

# 2.完善busybox文件系统
 [03-完善busybox文件系统](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#03-完善busybox文件系统&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={8A14BC2E-A8E4-4D75-B18C-D676EC7FAC90}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F03-%E5%AE%8C%E5%96%84busybox%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%7C8A14BC2E-A8E4-4D75-B18C-D676EC7FAC90%2F%29))

# 3.打包busybox文件系统
[04-打包busybox文件系统_以RK3568为例](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#04-打包busybox文件系统_以RK3568为例&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={DFD0C5C7-4745-41FD-9973-B1D54E0032D0}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F04-%E6%89%93%E5%8C%85busybox%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F_%E4%BB%A5RK3568%E4%B8%BA%E4%BE%8B%7CDFD0C5C7-4745-41FD-9973-B1D54E0032D0%2F%29))

# 4.给busybox文件系统增加功能-以QT库为例（移植QT）

## 4.1 编译QT库
[05-给busybox文件系统增加功能-以QT库为例（移植QT）](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#05-给busybox文件系统增加功能-以QT库为例（移植QT）&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={20F783B6-E83A-4F78-AF06-4D80015B3578}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F05-%E7%BB%99busybox%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E5%A2%9E%E5%8A%A0%E5%8A%9F%E8%83%BD-%E4%BB%A5QT%E5%BA%93%E4%B8%BA%E4%BE%8B%EF%BC%88%E7%A7%BB%E6%A4%8DQT%EF%BC%89%7C20F783B6-E83A-4F78-AF06-4D80015B3578%2F%29))
## 4.2 将编译好的QT库部署在busybox文件系统上
[06-将编译好的QT库部署在busybox文件系统上](onenote:https://d.docs.live.net/52d4b76bb0ffcf51/Documents/\(RK3568\)Linux驱动开发/文件系统构建_基于RK3568.one#06-将编译好的QT库部署在busybox文件系统上&section-id={D274A68A-A696-4F4A-B6FE-98047B597794}&page-id={CD638453-5937-40ED-8B91-17133C027214}&end)  ([Web 视图](https://onedrive.live.com/view.aspx?resid=52D4B76BB0FFCF51%21se8c325913f784bf694d429e5ee2ab2be&id=documents&wd=target%28%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%9E%84%E5%BB%BA_%E5%9F%BA%E4%BA%8ERK3568.one%7CD274A68A-A696-4F4A-B6FE-98047B597794%2F06-%E5%B0%86%E7%BC%96%E8%AF%91%E5%A5%BD%E7%9A%84QT%E5%BA%93%E9%83%A8%E7%BD%B2%E5%9C%A8busybox%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E4%B8%8A%7CCD638453-5937-40ED-8B91-17133C027214%2F%29))


# 2、手册指导

## Busybox 制作最小文件系统
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/16.开发板学习教程/文件系统构建手册_rk3568_v1.1.pdf#page=16&selection=17,0,25,8&color=important|文件系统构建手册_rk3568_v1.1, p.16]]
> > 第 2 章 Busybox 制作最小文件系统
> 
> 



## 最小文件系统移植 QT 库
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/16.开发板学习教程/文件系统构建手册_rk3568_v1.1.pdf#page=44&selection=17,0,27,1&color=important|文件系统构建手册_rk3568_v1.1, p.44]]
> > 第 3 章最小文件系统移植 QT 库
> 
> 


## 系统移植常用工具（ssh等）
> [!PDF|important] [[芯片开发学习/RK3568（linux学习）/linux开发资料库/rk3568迅为开发pdf/16.开发板学习教程/文件系统构建手册_rk3568_v1.1.pdf#page=57&selection=17,0,25,6&color=important|文件系统构建手册_rk3568_v1.1, p.57]]
> > 第 4 章 QT 系统移植工具
> 
> 



## 











