# 定义交叉编译器路径
CC=/usr/local/arm64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-gcc/usr/local/arm64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-gcc

# 生成可执行文件 app
app: gps.o uart.o main.o
	$(CC) -o app gps.o uart.o main.o

# 编译 gps 模块
gps.o: gps.c gps.h
	$(CC) -c gps.c

# 编译 uart 模块
uart.o: uart.c
	$(CC) -c uart.c 

# 编译主程序入口 main 模块
main.o: uart.o gps.o gps.h
	$(CC) -c gps.c uart.c main.c

# 清除编译生成的目标文件和可执行文件
clean:
	rm -f app *.o
