.global _start
.text
# evecve(filename, arg, env)
# %rax保存系统调用号，%rdi保存第一个参数，%rsi保存第二个参数
_start:
    lea data(%rip), %rdi
    movq $59, %rax
    xor %rsi, %rsi
    xor %rdx, %rdx
    syscall

data:
    .asciz "/bin/sh"
