MODULE_NAME := demodrv

obj-m := $(MODULE_NAME).o

all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(shell pwd) ccflags-y=$(ccflags-y) modules

clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(shell pwd) clean

