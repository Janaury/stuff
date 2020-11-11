# where to find the system call table?

You can find system call function prototypes in linux source directory at `include/linux/syscalls.h`

You can find x86 arch system call numbers in linux source directory at `arch/x86/entry/syscalls/syscall_64.tbl` for 64bit kernel and `syscall_32.tbl` for 32bit kernel.

Besides, you can find x86 arch syscall numbers in a general linux distribution(e.g. ubunut) at `/usr/include/x86_64-linux-gnu/asm/unistd_64.h` for 64bit kernel
and `unistd_32.h` for 32bit kernel.