
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/kallsyms.h> // needed by kallsyms_lookup_name
#include <linux/init.h> // needed by macro __init & __exit
#include <linux/err.h>	// IS_ERR/ERR_PTR/PTR_ERR
#include <linux/types.h> //data type definition
#include <asm/unistd.h>


// store unexported sysbol
// syscall table
static unsigned long* syscall_table = NULL;
static long (*sys_open)(const char __user *filename,
				int flags, umode_t mode);
static long (*sys_openat)(int dfd, const char __user *filename, int flags,
			   umode_t mode);	
static long (*sys_unlink)(const char __user *pathname);
static long (*sys_unlinkat)(int dfd, const char __user * pathname, int flag);

static long (*sys_mkdir)(const char __user *filename, umode_t mode);

static int init_unexported_symbol(void)
{
	if (syscall_table == NULL) {
		syscall_table = (unsigned long*)kallsyms_lookup_name("sys_call_table");
		if (IS_ERR(syscall_table)) {
			printk(KERN_INFO "fail to find syscall_table\n");
			return -1;
		}
		printk(KERN_INFO "find sys_call_table:%016x\n", syscall_table);
	}
	return 0;
}

// syscall implementation
static asmlinkage long fake_open(const char __user *filename,
				int flags, umode_t mode)
{
	printk("call open, filename %s, flags %x\n", filename, flags);
	return sys_open(filename, flags, mode);
}

static asmlinkage long fake_openat(int dfd, const char __user *filename, int flags,
			   umode_t mode)
{
	//printk("call openat, filename %s, flags %x\n", filename, flags);
	return sys_openat(dfd, filename, flags, mode);
}

static asmlinkage long fake_unlink(const char __user *pathname)
{
	printk("call unlink, filename %s\n", pathname);
	return sys_unlink(pathname);
}

static asmlinkage long fake_unlinkat(int dfd, const char __user * pathname, int flag)
{
	printk("call unlinkat, filename %s\n", pathname);
	return sys_unlinkat(dfd, pathname, flag);
}

static asmlinkage long fake_mkdir(const char __user *filename, umode_t mode)
{
	printk("call mkdir, filename %s\n", filename);
	return sys_mkdir(filename, mode);
}



// 更改cr0调整内存保护策略
static void set_wp(int enable)
{
	if (enable == 1) {
		asm volatile(
			"pushq %rax\n"
			"movq %cr0, %rax\n"
			"orl $0x10000, %eax\n"
			"movq %rax, %cr0\n"
			"popq %rax\n"
		);
	} else {
		asm volatile(
			"pushq %rax\n"
			"movq %cr0, %rax\n"
			"andl $0xfffeffff, %eax\n"
			"movq %rax, %cr0\n"
			"popq %rax\n"
		);
	}
}


static void modify_syscall(void) {
	sys_open = syscall_table[__NR_open];
	sys_openat = syscall_table[__NR_openat];
	sys_unlinkat = syscall_table[__NR_unlinkat];
	sys_unlink = syscall_table[__NR_unlink];
	sys_mkdir = syscall_table[__NR_mkdir];

	set_wp(0);
	syscall_table[__NR_open] = fake_open;
	syscall_table[__NR_openat] = fake_openat;
	syscall_table[__NR_unlink] = fake_unlink;
	syscall_table[__NR_unlinkat] = fake_unlinkat;
	syscall_table[__NR_mkdir] = fake_mkdir;
	set_wp(1);
}

static void recover_syscall(void) {
	set_wp(0);
	syscall_table[__NR_open] = sys_open;
	syscall_table[__NR_openat] = sys_openat;
	syscall_table[__NR_unlink] = sys_unlink;
	syscall_table[__NR_unlinkat] = sys_unlinkat;
	syscall_table[__NR_mkdir] = sys_mkdir;
	set_wp(1);
}

// init & exit
static int __init syscall_modify_init(void) 
{
	int ret = 0;
	ret = init_unexported_symbol();
	if (ret != 0) {
		ret = -1;
		printk("fail to load syscall table\n");
		goto out;
	}

 	modify_syscall();
	printk("syscall table modified\n");
	
	out:
	return ret;
}

static void __exit syscall_modify_exit(void)
{
	recover_syscall();
	printk("syscall table recovered\n");
}

module_init(syscall_modify_init);
module_exit(syscall_modify_exit);
MODULE_LICENSE("GPL");
