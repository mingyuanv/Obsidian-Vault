#Makefile文件
#platform_driver.c 对应的.o文件的名称。名称要保持一致。	
obj-m += platform_driver.o	#platform_device.c对应.o文件的名称。名称要保持一致。
KDIR :=/home/topeet/Linux/rk356x_linux/kernel    #内核源码所在虚拟机ubuntu的实际路径
PWD ?= $(shell pwd)
all:
	make -C $(KDIR) M=$(PWD) modules    #make操作
clean:
	make -C $(KDIR) M=$(PWD) clean    #make clean操作

