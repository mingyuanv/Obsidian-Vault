export ARCH=arm64#设置平台架构
export CROSS_COMPILE=/home/topeet/Linux/rk356x_linux/prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-
#交叉编译器前缀
obj-m += ds18b20.o    #此处要和你的驱动源文件同名
KDIR :=/home/topeet/Linux/rk356x_linux/kernel    #这里是你的内核目录                                                                                                                            
PWD ?= $(shell pwd)
all:
	make -C $(KDIR) M=$(PWD) modules    #make操作
clean:
	make -C $(KDIR) M=$(PWD) clean    #make clean操作
