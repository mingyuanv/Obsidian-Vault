
# 第一章 安装虚拟机 VMware 软件

虚拟机的软件有几种：Vmware Workstation（收费软件），Virtualbox（免费软件）。我们使用Vmware Workstation 作为虚拟机工具。Vmware Workstation 可以在 vmware 的官网下载：https://www.vmware.com/products/workstation- pro/workstation- pro- evaluation.html，当前最新版本是Vmware Workstation 16 Pro，下载Windows 版本，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/0659736d6fc98862f68e59bcefe8023b11ee184059fbcc5cac1baefdde7b94d9.jpg)

在光盘资料里面提供了该软件，路径为“iTOP- 3568 开发板02_【iTOP- RK3568 开发板】开发资料\01_iTOP- 3568 开发板Vmware 软件安装包\01- VMware 软件VMware- workstation- full- 16.2.1- 18811642. exe”。双击VMware- workstation- full- 16.2.1- 18811642. exe进入安装界面，如图所示：

![](assets/Linux入门篇（ubuntu基础知识）/ccb8703d4eb0556322d5aeceb176d7f35a68296fd613f3f139194308bdedc3a3.jpg)

然后点击上图中的“下一步”按钮，进入下图所示界面：

![](assets/Linux入门篇（ubuntu基础知识）/a57c333ad98057e9bfdb918437bb86d83e595dce29643fe78c1ee450eb3d9a06.jpg)

然后选中上图中的“我接受许可协议中的条款”，继续选择“下一步”按钮，进入下图所示界面：

![](assets/Linux入门篇（ubuntu基础知识）/069339386dd7555f40d76c7213cb05203b1126672d17e35b8ee20b3604f2a735.jpg)

根据实际需要可以在上图红色箭头所示的地方更改安装路径，选择好按住哪个路径，点击上图中的“下一步”按钮，进入下图界面：

![](assets/Linux入门篇（ubuntu基础知识）/289d9c0fc19dcdaee2df3fa2e08caea1feb9ede7578c945bb6cbf4febf4793d8.jpg)

在上图界面中，取消红色方框内的两个复选框，然后点击“下一步”按钮，然后进入下图所示界面：

![](assets/Linux入门篇（ubuntu基础知识）/f07c199a7b1332639e996d2df8260791ee697c856d73c9e21a6fc859c4cfcbdb.jpg)

然后选中上图中红色方框内的两个复选框，确保安装完成后，在桌面和开始菜单里面有VMware图标，然后点击上图中的“下一步”按钮，进入下图所示界面：

![](assets/Linux入门篇（ubuntu基础知识）/9b33b40889a3c1e16f4afa9a86daa319486657c0a95b8ff50e4c35284e8ee379.jpg)

经过前面几步的操作，已经设置好了安装参数，点击上图中的“安装”按钮开始安装VMware，安装过程如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/b4e2fc37024b6d1759ef5e57a9e93b6462614ce54728b233b95fa80be5f1b2ad.jpg)

安装完成会显示如下界面：

![](assets/Linux入门篇（ubuntu基础知识）/9e72edd75fe60e24781739439fc5541d1cb14eea59f2c0d4e0596a91886933c3.jpg)

然后点击上图中的“完成”按钮，完成VMware虚拟机的安装，将会在桌面生成VMwareWorkstation Pro的图标，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/238e315b9eeb6104b1188d973cde15c8ec235d53a42932e58538f9e92a3c3fbf.jpg)

接下来双击上图中的图标，打开 VMware 软件。第一次打开软件会提示输入许可证密钥 VMware 是付费软件，如果您购买了 VMware 会有一串许可证密钥，如果没有购买，可以选择“我希望试用 VMware Workstation 1630 天”选项，然后点击“继续”按钮，然后点击“完成”按钮，打开 VMware 的界面如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/014abf2f25aa7f8125358f04801b1ca0a7feb7b502e67f1729bdd25cd13bfaea.jpg)

至此，虚拟机 VMware 的安装就完成了。

# 第二章 获取并安装Ubuntu操作系统

首先打开VMware虚拟机软件，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/768b1f1191ea275b76e5cfba64bd97ed728f169de358564557c377385775aaad.jpg)

点击菜单栏中的文件，选择第一个“新建虚拟机”，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/7a4ec0b44cd2622359c94092874b56d375aec22b990067fa10522858e807f745.jpg)

会弹出“新建虚拟机向导”界面，使用自定义类型来进行虚拟机配置，然后点击下一步，如下图所示，

![](assets/Linux入门篇（ubuntu基础知识）/f5c9ac0b74e5bf62b5e8bbfa20deb20245e252dca45ac294fcc86fdd86e96d22.jpg)

随后选择硬件兼容性，直接选择默认的 16.2. x 即可，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/f4ce95bc574d43987efa7137d12def61b9f5f73fb96c68643ac2db53fe46b553.jpg)

随后选择安装程序光盘映像文件，映像文件存放路径为“iTOP- 3568 开发板\02_【iTOP- RK3568 开发板】开发资料\03_iTOP- 3568 开发板原始 Ubuntu18.04 虚拟机镜像”路径下，下载之后，点击浏览对其进行选择，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/d15f65e55f95a2005255eb3c3e9228dabe9f1e5e7e62ee0a2016839f86a4d6c9.jpg)

随后输入 ubuntu 虚拟机的全名、用户名以及密码，在这里都设置为了“topeet”，迅为提供搭建好的虚拟机密码也是 topeet，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/200b765dedf7850eb0adcc31b1c092af0174dfef52d7f72a1eada818d1be1d39.jpg)

随后设置虚拟机名称（使用默认不修改也可以），然后确定虚拟机安装位置，最后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/63e38b56362d510e03d7b8699e58d88c50f6e1d37f08cfa11d3c0d27c8116189.jpg)

随后设置处理器数量，这里根据自己电脑的配置来进行设置，内核总数越高，虚拟机的性能越高，编译源码的速度越快，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/4a56226411cab669fa9f7b1fed98027397dd8e6c0ef34c980a70841cdbea6dbd.jpg)

随后设置虚拟机的内存大小，推荐16G内存大小以上，在这里作者设置了32G，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/74c8734244be6cdadbdea0874884e4fe4018242f5ff6a322de3d98116b5a3d71.jpg)

随后选择网络类型为桥接模式（可以保证主机和虚拟机在相同的网段下），然后点击下一步，如下图所示

![](assets/Linux入门篇（ubuntu基础知识）/138e0bef15f56985e4892bd46f13610784ab29de5a9efa1ad140a9994119097b.jpg)

随后的IO控制器类型和磁盘类型根据推荐来选择即可，最后的选择磁盘页面要选择第一个“创建新虚拟磁盘”，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/2ba987b55c8e798426bdc08c65bec6c66bdce8a93997bd6c8f6f2a994ebef540.jpg)

随后来到磁盘容量大小确定界面，如果只是编译 Linux 源码只需要给定 300G 即可，而如果想要编译安卓则需要给定 600G 大小的空间，作者这里给定 600G（这里要注意，给 300G 并不是该虚拟机直接就是 300G 了，只是最大容量是 300G 而已），然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/879ce65b47f53d81a13f4d42e6dd297d8599cd3a101dfdf0e12a3ad7b9f8e8f8.jpg)

然后指定磁盘文件名称，使用默认的即可，然后点击下一步，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/d5d45b4c2b067c647a99fc1a566c7312831701402f84cd2b4b7358645ccbca35.jpg)

最后点击完成按钮来开始 ubuntu 虚拟机的正式安装，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/2e58c4a5bd9d75b72981a700722c3adcc4b178495c28eccd6e1ab8fb3ce3081f.jpg)

等待虚拟机安装完毕，大概 5 分钟左右（与自身虚拟机配置有关），安装完成进入系统如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/f65399d387dac630150d689b111687e90acc836dc1ac9b03a5bc73b12796c2a3.jpg)

至此，Ubuntu 虚拟机的安装就完成了。

# 第三章 Ubuntu 系统介绍

## 3.1 Ubuntu 操作系统的介绍

Ubuntu 是 Linux 发行版之一，它和 Linux 的关系是包含与被包含的关系，即 Ubuntu 是包含在 linux 里面的。常见的操作系统有 Windows、Linux、iOS 还有 Android。

## 3.2 linux 发行版种类

> 除了 Ubuntu，Linux 的**发行版还有 Radhat、Centos、Debian、openwrt** 等。

之所以选择 Ubuntu，是因为 Ubuntu 有着良好的图形界面和非常强大的 ape- get 功能，学习和开发一般都使用 Ubuntu。

## 3.3 常见的 ubuntu 分类

> Ubuntu 的种类有很多，从外观上分，可以分为有界面的 ubuntu 和没有界面的 ubuntu。没有界面的 ubuntu 叫做 ubuntu- core，有界面的 ubuntu 叫做 ubuntu- desktop，两种 ubuntu 的主要区别在于有没有显示界面。有界面的 ubuntu 主要在 X86 的机器上运行，而 RK3568 也有足够的性能来运行有界面 ubuntu 系统。

> 有界面的 ubuntu 由 ubuntu- core 和第三方桌面组成的。根据第三方桌面种类不同，组成了不同类型的 ubuntu。以前一小节搭建的 ubuntu 为例，它由 ubuntu- core 加上 gnome 第三方桌面组成。除了 gnome 还有 kde 等比较常见的第三方桌面，kde 桌面加 ubuntu 组成了 kubuntu。除了 kde 另一个常见的第三方桌面为 lxde，lxde 桌面加文件系统就组成了 ubuntu，lubuntu 是一个轻量级的 ubuntu，可以在性能低的设备中运行。

下面来简单认识一下这三个 ubuntu，首先是最常见的 
### gnome 桌面的 ubuntu：

![](assets/Linux入门篇（ubuntu基础知识）/3404dd9e3df7042db9a63c8df2b005e7b9f4ec01bfa06aaca4bec859d523e228.jpg)

然后看一下
### kubuntu，它的图标由小齿轮组成：

![](assets/Linux入门篇（ubuntu基础知识）/8cb4f94186e6867996ce873ddd888211faaf4986240e9485db7c5cae79710dee.jpg)




# 第六章 Vim 编辑器的使用

## 6.1 vim 简介

vim 编辑器最初是 vi 编辑器，vi 编辑器是 Unix 系统最初的编辑器。允许查看文件内容和在文件中移动、插入、编辑和替换文本。后来开发人员对它做了一些改进。并重命名为 vim。

## 6.2 学习 vim 的理由

因为几乎任何一个发行版都有 vi/vim 编辑器，在嵌入式 linux 上，通常也会集成 vim 编辑器，所以说 vim 编辑器大部分的版本都是支持的，所以就要学习 vim。

## 6.3 vi 和 vim 的关系

> **vim 是 vi 的加强版**，vi 的命令基本全部可以在 vim 上使用，而且比 vi 使用起来更加容易。因为这两个是一样的，所以在后面的学习中，不对 vim 和 vi 加以区分。

## 6.4 打开 vim 编辑器

打开控制台，输入以下命令

- 1 vi test.c

这里的文件名为 test.c，这样就打开了文本编辑器。如果打开的文件不存在，它会新建一个文件，而文件存在，会直接打开，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/36b59edaa7cfb4cb621442242ac6ebccd888489c764b4158d69e2c1601d3c79f.jpg)

## 6.5 vim 编辑器有三种模式

第一种模式是
### 一般模式
在打开 vi 编辑器之后，所处的模式就是一般模式，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/687508509a72cefa5382ee03bd89e6dd01b9f0c979357da6b0b5141c27b5f33e.jpg)

第二种模式是
### 编辑模式
> 进入文件之后，**点击字母 i 会切换到编辑模式**，可以看到左下角出现了 INSERT，就证明当前所处的模式为编辑模式，在编辑模式下，可以对内容进行编辑。

![](assets/Linux入门篇（ubuntu基础知识）/48393f2265f96f9d079ad587b3b686cf1915b11e46913f17780270a7ce7a7efc.jpg)

> **点击 ESC 按键可以从编辑模式退到一般模式**，退出之后左下角的 INSERT 会消失如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/6693675956bc419934a10d40a15c22db7270bb6c78571c504f41127f286c5a86.jpg)

第三种是
### 命令行模式
> 在一般模式**点击冒号按钮**就会切换到命令行模式。左下角出现冒号后，所处状态就是命令行模式。

![](assets/Linux入门篇（ubuntu基础知识）/6132b79199e78e542e421e09a088f2ed03125c8b2cfc2bd01a27e2a68da7e075.jpg)

#### 在命令行模式下输入命令

- 1 set number

- 2 即可显示行号

![](assets/Linux入门篇（ubuntu基础知识）/74781a8178ccff770c6a2a3f8247d41ee6513feea2a84560eac3bbe8084ce88b.jpg)


## 6.6 vim 编辑器移动光标

> 在vim编辑器中，由于没有图形界面，所以不能通过鼠标来移动光标，光标的移动是通过**上下左右按键**来实现的，如果使用的键盘是小键盘，没有上下左右按键，可以使用键盘上的HJKLM按键来完成光标的移动。每个按键对应的功能如下图所示：

<table><tr><td>按键</td><td>对应的功能</td></tr><tr><td>K</td><td>向上移动</td></tr><tr><td>J</td><td>向下移动</td></tr><tr><td>H</td><td>向左移动</td></tr><tr><td>L</td><td>向右移动</td></tr></table>

## 6.7 vim 编辑器支持快速定位
### 一般模式使用ngg
- 2 以移动光标到第3行为例子，则输入3gg。

<table><tr><td>按键</td><td>对应的功能</td></tr><tr><td>gg</td><td>将光标定位到第一行</td></tr><tr><td>G</td><td>将光标定位到最后一行</td></tr><tr><td>ngg</td><td>将光标定位到第n行</td></tr></table>

## 6.8 vim 编辑器的文本的复制和粘贴

下面讲解linux中文本的复制和粘贴操作。

> 首先是`单行内容的复制`，将光标移动到要复制内容的行首，然后按字母**y**，接着把光标移动到要粘贴的地方，按ESC**回到一般模式，点击字母p**来进行复制。

> 如果要`复制多行内容`，先将光标移动到要复制内容的行首，然后按字母**v**，左下角会出现VISUAL，然后使用键盘的上下左右按键选择要复制的文本，选择完成之后，按字母**Y**进行文本的复制，如下图所示：
> > 复制完成之后，先按ESC回到一般模式，把光标移动到想要粘贴的位置，然后按字母**p**进行粘贴，粘贴完成如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/56c50b62aa6285bc637f4662070f4a0d6fb29b791459e2009ddf202afbb30216.jpg)

![](assets/Linux入门篇（ubuntu基础知识）/4f5bfbd5a50762ec73eb11dddfbc0ef537a8c1a380d21dedb72f26548ee3344b.jpg)

## 6.9 vim 编辑器使用快捷键来复制

<table><tr><td>按键</td><td>对应的功能</td></tr><tr><td>yy</td><td>复制当前行</td></tr><tr><td>nyy</td><td>复制当前行下的n行</td></tr></table>

![](assets/Linux入门篇（ubuntu基础知识）/0f1b400798171e0b8f4fb65bf7bdf19c1006db623ddcc22e7b97c06ab8a73e0e.jpg)


![](assets/Linux入门篇（ubuntu基础知识）/184f4db82636cdc3fa9988a2b656d4e97f1c7ba5288d95890e95bd38153e37b6.jpg)

> 注：在 windows 上使用的复制粘贴命令分为“ctrl+c”“ctrl+v”，而在 ubuntu 中除了上面两个小节所讲述的方法，在 ubuntu 中使用鼠标进行内容的框选，然后使用复制**命令“ctrl+shift+c”，最后输入“ctrl+shift+v”快捷键也可以进行粘贴**。可以亲自去尝试一下。

## 6.10 vim 编辑器的删除

<table><tr><td>按键</td><td>对应的功能</td></tr><tr><td>dd</td><td>删除光标所在行</td></tr><tr><td>ndd</td><td>删除n行</td></tr><tr><td>n1,n2d</td><td>删除指定范围的行</td></tr></table>

dd 命令是删除光标所在行内容，以删除第八行为例，在一般模式下，将光标移动到第八行，然后双击 d，那么第 8 行就被删掉了。如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/e11b256652782baaa6ea61b5bb76cc764b61c140bada3b4ed74ff386e1bb5eb0.jpg)

同样可以使用 ndd 命令来删除多行，比如删除第 9 到 11 行内容，可以直接将光标移动到第九行，输入命令 3dd，则这 3 行内容就被删掉了，如下图所示。

![](assets/Linux入门篇（ubuntu基础知识）/07c0d3eb5dbd281bb4fbedbae93a8cfff9f182a1510abcc56b969d73ec33ed2c.jpg)

也可以删除指定范围行的内容，命令格式为 n1,n2d，该命令需要在命令行模式下输入。以删除第 1 行到第 6 行的内容为例，首先点击“冒号”进入命令行模式，然后输入 1,6d，然后输入回车，这样 1- 6 行就全被删掉了。如下图所示。

![](assets/Linux入门篇（ubuntu基础知识）/f2dbfe2c9a7b032565334cb7188d1b98ec9c6d66876f364881da882852aa02ba.jpg)

## 6.11vim编辑器的撤销

在一般模式下，输入字母u来撤销之前的内容，进行内容的回退。反撤销是ctrl+r。注意撤销和反撤销都是一般模式下进行的，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/87641bd242fc0513d0910e707dc8ce8cbb53027eae07c89f4a3203822f4b7748.jpg)

## 6.12vim编辑器的查找

在ubuntu的vim编辑器中，查找命令是通过／或者？来实现的。以查找“da"内容为例，现首先进到了命令行模式，点击字符""并输入da。输入完成之后敲击回车，就会找到"da"了，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/43fda53b2e463abb2d4035d10ec1cb6d42653e54bcd0b2a6ca35445c154d0136.jpg)

查找完成之后点击字母“n”, 回向下查找内容, 而“/”和“？”查找的区别在于, “/”为向下进行查找内容, 而“？”向上进行内容的查找。

## 6.13vim编辑器的替换

替换命令的格式为%s/old/new/g。以“xunwei”替换成“dianzi”内容为例子, 首先进入到命令行模式, 输入: %s

/xunwei/dianzi/g，然后点击回车进行内容的确定，可以发现内容已经进行了替换，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/e01675b2e1b2dc7703a6bd9eea2fcf4671016a5f1fad7c95edb5c8ba7b122145.jpg)

## 6.14 vim 编辑器的保存

q！:强行退出wq：保存退出q：退出没有编辑过的文本

直接输入冒号进到命令行模式，如果想要保存退出，直接输入 wq，然后回车，这样就保存退出了。如下图所示。

![](assets/Linux入门篇（ubuntu基础知识）/5ccdedfa44812c3edf3f463b3f6f8ec6b9dacf34609792b554cb05751a58b036.jpg)

然后打开 test.c 的文件，可以看到之前修改的内容没有发生改变，如果想修改完之后但不进行保存，比如删掉当前行，然后输入冒号，进入命令模式，输入 q! 就会退出，然后再次打开文本，可以看到删掉的东西并没有保存，即之前的操作没有被保存。如下图所示。

![](assets/Linux入门篇（ubuntu基础知识）/8aa4ace59d17ffd11c923dbed8efa90817ea4f0f98a1220168db7e8d8f6636bc.jpg)

如果想直接退出，即只是浏览了文件中的内容，但并没有对文件进行编辑，直接输入：进入命令行模式，然后输入 q 可以直接退出，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/504b53de7c9859961e85f2afc90a1398a15096cea4da90ec88816e12a7714f19.jpg)

保存退出之后，vim 编辑器会自动保存 test.c 文件，而之前是没有 test.c 文件的。如下图所示。

![](assets/Linux入门篇（ubuntu基础知识）/a11c057091b3307517916dceb9d825197eb0e19998964a6932b941f87a9675e2.jpg)

vi 加上要创建文件的名字，然后保存之后，文件会自动被创建。我们以创建一个名为 test4. c 的文件为例子，输入“vi test4. c”命令，之前路径下是没有 test4. c 文件的，那么 vim 编辑器会先创建这个文件，然后再打开，保存退出对当前路径进行查看，可以看到 test4. c 文件已经被创建了，如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/2751dd4b23a54596f061592ced3e4fbaf1e9b92345cb25ea58a316cb9408199e.jpg)

## 6.15 vim 编辑器文件的对比

vimdiff file1 file2 file3

vim 编辑器可以进行文件的对比，使用的命令为 vimdiff，使用以下命令对比 test.c 和 test4. c 文件，如下图所示：

vimdiff test.c test4. c

![](assets/Linux入门篇（ubuntu基础知识）/7d4f5ea63613a7e34d5f18eb8870a8f582f3b5cf82c0c9fd68b451fbc75e8088.jpg)

大部分情况是两个文件的对比，该命令也可以进行两个以上文件的对比，在这里添加一个 test3. c，如下图所示。

vimdiff test.c test4. c test3. c

![](assets/Linux入门篇（ubuntu基础知识）/cc44c6f79a122993614ce2883878f93021d95a808ec5d6809afee64f255d9143.jpg)

对于 vim 编辑器就先介绍到这里。


# 第八章 相对路径和绝对路径

## 8.1 绝对路径

> 绝对路径有一个特点，它是**从最顶层开始的**，在 linux 中，最顶层为根目录，所以绝对路径都是从根目录开始。为了便于理解，举个现实中的例子，比如作者现在的位置在北京海淀区，那么用绝对路径表示作者当前所处的位置要如何表示呢，绝对路径都是从根目录开始的，这里假设最顶层是地球，那么/地球/中国/北京市/海淀区/复兴路/100 号，就是作者所处位置的绝对路径。

## 8.2 相对路径

> 同样 opt 也是一个相对路径，相对路径它同样有个特点，一般都是**以 . 开头或者 ./ 开头**。这样说仍比较抽象，同样举个现实中的例子，比如说作者当前的位置是在北京，那么用相对位置来表示作者现在具体的位置表示：./海淀区/复兴路/100 号，这个路径就是相对路径，./ 可以去掉写成：海淀区/复兴路/100 号，也是没有问题的，也就是说在使用 cd 命令的时候，直接加上相对于当前路径的文件夹的名字就可以了。

# 第九章 家目录和根目录概念

## 9.1根目录

## 9.2家目录

> 用**～**表示家目录，使用以下命令进入家用户目录



# 第十二章 权限管理

## 12.1 linux 权限管理

### Ubuntu 的用户分为三类：
>  1 root（超级用户）  2 系统初次创建的用户表，比如 topeet  3 安装完系统之后创建的用户


### 以 topeet 信息为例子进行讲解：
- 2 用户的信息全部被保存在 /etc/passwd 文件里面。

> 40 gdm:x:121:125:Gnome Display Manager:/var/lib/gdm3:/bin/false  
> 41 topeet:x:1000:1000:topeet,,,:/home/topeet:/bin/bash  
> 42 sshd:x:122:65534::/ran/sshd:/usr/sbin/nologin

> 1. 用户名 topeet: 在用户登录时使用。介于 1 和 32 个字符的长度。
> 
> 2. **密码 x**: 一个 x 字符表明加密的密码存储在 /etc/shadow 文件。请注意,您需要使用 passwd 命令计算散列密码输入 CLI 或存储/更新密码的哈希 /etc/shadow 文件。
> 
> 3. 用户 ID (UID) 1000: 每个用户必须指定的用户 ID (UID)。UID 0(零) 用于根和 UID 1-99 是留给其他预定义的账户。进一步的 UID 100-999 保留系统管理和系统账户/组。
> 
> 4. 组 ID (GID) 1000: 主组 IDX存储在所属文件
> 
> 5. 用户 ID 信息 topeet: 注释字段。
> 
> 6. 主目录 /home/topeet: 绝对路径的日录用户登录时将在。
> 
> 7. 命令/壳 /bin/bash。

## 12.2 Ubuntu 的文件权限

### 读权限 r，写权限 w，执行权限 x：

![](assets/Linux入门篇（ubuntu基础知识）/f488274a4714a7b4ba5a4356605d16834b6fffb6c9fe8ecb6ad6c7c6ba70a01c.jpg)

> 9个英文字符划分成三组，每三个字母为一组，以test.c的权限为例进行讲解。第一组：rw- 文件拥有者的权限topeet用户对test.c有rw权限，没有执行权限。第二组：rw- 文件拥有者所在用户组的权限与topeet文件拥有者所在topeet组的用户可以读写，但是不能执行。
> 第三组：r- - 其他用户的权限，不与文件拥有者在同一个组的用户权限是只能读，不能写和执行。

![](assets/Linux入门篇（ubuntu基础知识）/45d068aa0de2997bb4534a8a916843d8fb5a8d3618cf7702d25a872785515aa4.jpg)

第三列：topeet代表文件拥有者第四列：topeet文件拥有者所在的组文件的
### 权限使用二进制来表示

<table><tr><td>字母</td><td>二进制</td><td>十进制</td></tr><tr><td>r</td><td>100</td><td>4</td></tr><tr><td>w</td><td>010</td><td>2</td></tr><tr><td>x</td><td>001</td><td>1</td></tr></table>

> 因为每个文件的权限是由9位来表示的，每3位为一组，这样就可以组合成8种不同的情况，如下表所示：

<table><tr><td></td><td>权限</td><td>二进制</td><td>十进制</td></tr><tr><td>第一种组合</td><td>---</td><td>000</td><td>0</td></tr><tr><td>第二种组合</td><td>--x</td><td>001</td><td>1</td></tr><tr><td>第三种组合</td><td>r--</td><td>100</td><td>4</td></tr><tr><td>第四种组合</td><td>-w-</td><td>010</td><td>2</td></tr><tr><td>第五种组合</td><td>-wx</td><td>011</td><td>3</td></tr><tr><td>第六种组合</td><td>rx-x</td><td>101</td><td>5</td></tr><tr><td>第七种组合</td><td>rw-</td><td>110</td><td>6</td></tr><tr><td>第八种组合</td><td>rwx</td><td>111</td><td>7</td></tr></table>


## 12.3 chmod 命令：修改文件或者文件夹的权限

- 1 chmod 参数 权限 文件名


- 2 chmod 777 test.c
使用以下命令赋予 test.c 文件一个 777 的权限
root@ubuntu:/home/topeet# chmod 777 test.c root@ubuntu:/home/topeet# ls - l test.c - rwxrwxrwx 1 topeet topeet 0 May 24 22:06 test.c root@ubuntu:/home/topeet#

# 第十三章 连接档概念

## 13.1 Linux下的连接档种类

Linux下的连接档有两个种类。一种类似于win电脑的快捷方式，称为软连接，软连接也可以叫做符号链接。另一种是通过文件系统的inode连接来产生的，类似于win电脑的复制，但是不产生新的文件，称为硬连接。硬连接也可以称作为实体连接。

## 13.2 inode简介：索引节点

- 1 内核会给每一个新创建的文件分配一个索引节点，这个索引节点就是inode。
> inode用来存放文件信息，每个文件都会占用一个inode，并且这个inode号是唯一的，可以把inode简单的理解为一个**指针，它永远指向本文本的具体存储位置**，文件的属性保存在inode里，系统是通过inode而不是文件名来定义每一个文件的。当系统要访问文件时，inode就会被复制到内存，从而实现文件的快速访问。

- 2 使用“ls - i”命令可以看到inode号。如下图所示：

> root@ubuntu:/home/topeet#`ls - i `
> 17563715 Desktop 
>` 17563941 test `
> 17563900 test.c 

## 13.3硬连接介绍

> 硬连接是一个新的链接到某个inode号码的记录。这个链接指向inode，系统并不给他从新分配inode。也就是说会有多个文件对应同一个inode，如果**两个文件的inode一样，那么这两个文件就是完全一样的**。
> 可以用ln命令来。

### 建立硬连接
- 1 ln 源文件 目标文件

> 常用**参数- f，强制创建**，无论目标文件是否存在都要创建连接。

- 2 ln testl.c test2. c

![](assets/Linux入门篇（ubuntu基础知识）/95b949f03a7190bc0071d89488655f60e27fda1e5cd5bda7cbaa8bcb84dcde7c.jpg)

### 分析硬连接deinode号

- 2 然后使用“ls - i”命令查看 inode 信息如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/533e73e8a6560d45f465c428ea3b811f24ab9d7dc5e1ee016903fc6144f84ac5.jpg)

> 可以发现 test1. c 和 test2. c 他们的 inode 号码都是 17563943。因为 **inode 号一样，所有这个两个文件的权限和属性也是一摸一样的**，也是 test1. c 和 test2. c 是两个完全一样的文件。如下图所示：

![](assets/Linux入门篇（ubuntu基础知识）/7a34a37a9b3dd9cf6577501f9389f541c63c7ce3d4c3f6c8e4c75c6329f9b4da.jpg)

> 上图中的**数字 2，这个代表的是有 2 个档名链接到了这个 inode 号**。使用以下命令再创建一个硬连接。则会发现连接数从 2 变成了 3 如下图所示：

## 13.4 硬连接的优缺点

### 优点：

> 第一方便，虽然**类似于 win 的复制，但通常不占用实际空间**。而且不管是修改 test1. c 或者是修改 test2. c 还是 test3. c，只要修改一个，文件就会被同时修改。

> 第二是安全，防止误删除。**即使删除了 test1. c、test2. c、test3. c 中的任意一个，还可以通过其他连接来访问文件**，可以利用硬连接这个特点来做文件的**备份**。


### 缺点：

> 第一，只能在同一个文件系统才可以创建硬连接（因为不同的文件系统管理方式不同），甚至有的文件系统没有索引号，它不是索引文件系统。哪怕他有索引号，两个文件系统的索引号含义不一定是相同的，即使它的索引号相同，但是不同的文件系统中也有可能使用该 inode 的其他文件，这样就会发生冲突，所以说**只能在同一个文件系统中才能创建硬连接**。

> 第二，**目录之间不能创建硬连**接（太复杂，现在还不支持）。如果说将根目录下的 etc 用硬连接创建一个硬连接的目录，那么不只是我们的文件要被创建，这个文件下面所有的文件名都要创建一个硬连接，这样呢就会给工作环境造成一个很大的工作量，而且非常的复杂，所以现在还不支持。

## 13.5 软连接介绍：类似于 win 上的快捷方式

- 1 ln - s  源文件 目标文件
> - s 为创建一个软连接。**源文件必须使用绝对路径**，不能使用相对路径。

- 2 ln - s /home/topeet/test1. c test4. c

![](assets/Linux入门篇（ubuntu基础知识）/ac7323ab99f41ae8fb785bb8f37feb3c5739753d80f3aef84b2aedecd184a87b.jpg)

> 上图中可以发现 test1. c 和 test4. c 的 inode 号是不一样的，所以这两个文件是完全独立的，**软连接就是创立了一个新的文件，当访问这个链接文件的时候，系统就会发现他是一个链接文件，然后读取链接文件找到真正要访问的文件**。

> 类似于 win 上的快捷方式，如果删掉源文件 test3. c，那么 test1. c 就不能打开了，如下图所示（红色背景代表无效。）：

![](assets/Linux入门篇（ubuntu基础知识）/2ef8898dbb1085f55432b2a10b0302b7dabf007f2d9ce74b8635d43fe0eb9281.jpg)

软连接虽然没有硬连接安全，但是限制少，所以使用范围广泛

### ubuntu系统中各个文件的颜色含义  

<table><tr><td>颜色</td><td>对应的文件含义</td></tr><tr><td>蓝色</td><td>文件夹，ls -l 或 II 时可以看到权限部分的第 1 个字母是 d</td></tr><tr><td>红色</td><td>压缩文件</td></tr><tr><td>绿色</td><td>可执行文件</td></tr><tr><td>白色</td><td>文本文件</td></tr><tr><td>红色闪烁</td><td>错误的符号链接</td></tr><tr><td>淡蓝色</td><td>符号链接</td></tr><tr><td>黄色</td><td>设备文件</td></tr><tr><td>灰色</td><td>其他文件</td></tr></table>

# 第十四章 目录结构讲解

## 14.1linux目录结构

> Linux整个文件系统是**以“／”目录开始**，根目录是最顶层，前面在讲解根目录和家目录概念的时候已经提到了。它下边包括众多的目录，这些目录又称为子目录，子目录下边又包含更多的目录，形成了一个像树一样的结构，可以把它想像成一个倒挂的树，就是从树根开始往下，它的枝叶是一支一支的。


## 14.2 linux 文件层次标准（FHS）

> FHS 定义了两层规范：
> 第一层是 / 目录下面文件夹要存放的文件，比如说
>  /etc 下面就应该放配置文件，
>  bin 或 sbin 下边就应该放可执行文件。
>第二层规范是针对 linux 下 /usr 和 /var 这两个目录的子目录来定义的。
>比如 /usr/share 下面就应该放共享数据文件，

> FHS 仅仅**给出了最上层项目录以及子层 /usr 和 share 要存放的数据**，在其他的子目录层，就可以随意的来配置了，

## 14.3 linux 根目录下

### 各个文件的规定如下：

![](assets/Linux入门篇（ubuntu基础知识）/435fcc9cc00e0a7410983f525bba847d128d9e5395c2d47d07338fa72aeb4db2.jpg)

<table><tr><td>文件名称</td><td>各个文件的规定</td></tr><tr><td>bin</td><td>系统启动时需要的可执行命令，大部分普通用户只有可执行权限没有读写权限，只有root用户有读写权限，</td></tr><tr><td>boot</td><td>用来存放BootLoader相关文件，千万不要乱动，否则无法进入系统。</td></tr><tr><td>cdrom</td><td>光盘目录</td></tr><tr><td>dev</td><td>设备驱动文件夹</td></tr><tr><td>etc</td><td>系统配置文件夹，这个文件夹的权限很高，只有root用户才可以修改这个文件夹</td></tr><tr><td>home</td><td>家目录，普通用户都有一个以自己名字命名的文件夹存放在这个目录里面</td></tr><tr><td>lib</td><td>各种程序所需要的库文件和系统可以正常运行的支持文件都存放在这个文件夹里面</td></tr><tr><td>lib64:</td><td>64位支持库</td></tr><tr><td>media:</td><td>用来存放媒体信息的文件</td></tr><tr><td>mnt</td><td>可以把设备挂载在这个文件夹下，比如U盘，</td></tr><tr><td>opt</td><td>可以用来存放第三方文件</td></tr><tr><td>proc</td><td>用来存放系统信息和进程信息</td></tr><tr><td>root</td><td>root用户的家目录</td></tr><tr><td>run</td><td>保存了系统从最开始到现在的系统信息</td></tr><tr><td>sbin</td><td>存放系统管理员的可执行命令，里面也是二进制文件</td></tr><tr><td>snap</td><td>snap应用程序框架的程序文件</td></tr><tr><td>srv</td><td>用来存放系统存储服务相关数据</td></tr><tr><td>sys</td><td>系统的设备和文件层次信息</td></tr><tr><td>temp</td><td>存放临时文件</td></tr><tr><td>usr</td><td>存放和用户有关的文件</td></tr><tr><td>var</td><td>存放一直在变化的文件</td></tr></table>

> 这个就是在FHS规范的建议下，linux根目录下各个文件的规定。**尽管FHS这个不是强制的标准，但是作为一个开发人员，还是要遵守这个标准的**，比如说后面自己定义了一个命令，就要把这个命令放到bin文件下，不然别人接手你的项目就容易出现混乱。

# 第十五章 文件系统的讲解

## 15.1文件系统的概念

> 操作系统中**负责管理和存储文件系统的软件**称为文件系统。

## 15.2文件系统的作用

Linux系统必须要挂载一个文件系统，如果系统不能从指定的设备挂载，系统就会出错。

## 15.3、linux常见文件系统类型

> 在linux系统中常见的文件系统类型分别为**ext3、ext4、proc文件系统和sysfs文件系统**。ext3文件系统是从ext2发展过来的，而且完全兼容ext2文件系统，并且比ext2要小，要可靠。

> ext4文件系统是在ext3的基础上改进的，并且ext4文件系统在性能和可靠性上都要比3的表现更好，而且功能也非常的丰富，并且**ext4完全兼容ext3**，ext3只支持32000个子目录，但是**ext4支持无限数量的子目录**，所以比3更优秀。

> `Proc文件系统`，这个文件系统是linux系统中特殊的文件系统，实际上**只存在于内存中，是一个伪文件系统**，该文件系统**是内核和内核模块用来向进程发送消息的机制**。

## 15.4ubuntu文件系统类型

### df- T命令来打印文件系统的类型

Filesystem显示该文件系统的分区，会将所有的设备名称进行打印，如下图所示

<table><tr><td colspan="7">root@ubuntu:/home/topeet# df -T</td></tr><tr><td>Filesystem</td><td>Type</td><td>1K-blocks</td><td>Used</td><td>Available</td><td>Use%</td><td>Mounted on</td></tr><tr><td>udev</td><td>devtmpfs</td><td>16461592</td><td>0</td><td>16461592</td><td>0%</td><td>dev</td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>3285304</td><td>2212</td><td>3283092</td><td>1%</td><td>run</td></tr><tr><td>dev/sda1</td><td>ext4</td><td>618220704</td><td>9715756</td><td>577031388</td><td>2%</td><td>/</td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>16426520</td><td>0</td><td>16426520</td><td>0%</td><td>dev/shm</td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>5120</td><td>4</td><td>5116</td><td>1%</td><td>run/lock</td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>16426520</td><td>0</td><td>16426520</td><td>0%</td><td>sys/fs/cgroup</td></tr></table>

> **/dev/sda1是ubuntu的主分区**，Type是文件系统的类型。所以ubuntu的主分区的文件类型就是ext4。ext4上边的**tmpfs是虚拟内存文件系统**。618220704这串数字代表的是内存的总和，1k代表单位。

> ext4和ext3它是日志型的文件系统，要比传统型的文件系统安全，因为它可以用独立内容的日志来跟踪磁盘内容的变化，Used 是已经使用的空间大小，Available 这一列是剩余空间大小，Use% 是磁盘使用率。最后一个 **Mounted on 是磁盘挂载的目录**，这里 /dev/sda1 就挂载到了 / 目录上面。


### df - Th：以更容易读的方式进行显示

<table><tr><td colspan="8">root@ubuntu: /home/topeet# df -Th</td></tr><tr><td>Filesystem</td><td>Type</td><td>Size</td><td>Used</td><td>Fail</td><td>Use%</td><td>Mounted</td><td>on</td></tr><tr><td>udev</td><td>devtmpfs</td><td>16G</td><td>0</td><td>16G</td><td>0%</td><td>dev</td><td></td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>3.2G</td><td>2.2M</td><td>3.2G</td><td>1%</td><td>run</td><td></td></tr><tr><td>dev/sda1</td><td>ext4</td><td>590G</td><td>9.3G</td><td>551G</td><td>2%</td><td>run</td><td></td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>16G</td><td>0</td><td>16G</td><td>0%</td><td>dev/shm</td><td></td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>5.0M</td><td>2.0K</td><td>5.0M</td><td>1%</td><td>run/tock</td><td></td></tr><tr><td>tmpfs</td><td>tmpfs</td><td>16G</td><td>0</td><td>16G</td><td>0%</td><td>sys/fs/cgroup</td><td></td></tr></table>

> 第三列就变成了 Size，**将 kb 单位转换成了 G**，这样看起来就更加容易理解了。

> 如果不想看文件系统的内容，就可以不加 T 参数，**直接输入“df - h”命令，这样就能看到一个磁盘的使用状况。**


# 第十八章 第一个命令的编写

## 18.1 命令的概念

> **命令就是可执行程序**。比如说输入“ls - al”命令，ls 就是可执行程序的名字。- al 就是要传递进去的参数。

## 18.2 定义自己的命令


> 根目录下的**bin文件是专门存放可执行文件的**，使用以下命令将commond可执行性文件拷贝到根目录下bin文件夹中，如下图所示：


> **也可以把存放commond这个可执行文件的路径加到PATH这个变量里面去**，先使用以下命令将bin目录下的commond可执行文件删掉，如下图所示：
```shell
export PATH=/home/topeet/test:/$PATH
```




