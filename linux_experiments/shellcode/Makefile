all: shellcode64 shellcode64_test
	@echo "############NOTE############"
	@echo "1. Default output is 64bit shellcode, for 32bit shellcode please type \"make shellcode\"."
	@echo "2. shellcode64.elf can be executed directly, while shellcode64 is just the raw binary machine code used to inject intto other programs."
	@echo "3. shellcode_test.c is used to test the shellcode64."
	@echo "4. binary2char.py is a python script used to convert a binary file to a c char array."

shellcode64_test: shellcode64_test.c
	gcc -z execstack $^ -o $@

shellcode64: shellcode64.S
	gcc -nostdlib $^ -o shellcode64.elf
	objcopy -O binary -j .text shellcode64.elf $@
	@echo "##########64bit shellcode#########"
	@python3 ./binary2char.py $@

shellcode: shellcode.S
	gcc -m32 -nostdlib $^ -o shellcode.elf
	objcopy -O binary -j .text shellcode.elf $@
	@echo "##########32bit shellcode########"
	@python3 binary2char.py $@

.PHNOY: clean
clean:
	-rm -f shellcode.elf shellcode shellcode64.elf shellcode64 shellcode64_test
