#include <linux/module.h>
#include <linux/types.h>
#include <linux/fs.h>
#include <linux/errno.h>
#include <linux/init.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

#define DEMO_NAME "my_demo_dev"
int dev1_registers[5];
int dev2_registers[5];
struct cdev cdev; 
dev_t devno;

/*文件打开函数*/
int demodrv_open(struct inode *inode, struct file *file) {
    /*获取次设备号*/
    int num = MINOR(inode->i_rdev);
    if (num == 0) {
        file->private_data = dev1_registers;
    }
    else if(num == 1)
        file->private_data = dev2_registers;
    else
        return -ENODEV;  //无效的次设备号
    return 0; 
}

/*文件释放函数*/
int demodrv_release(struct inode *inode, struct file *file)
{
    return 0;
}

/*读函数*/
static ssize_t demodrv_read(struct file *file, char __user *buf, size_t size, loff_t *ppos)
{
    unsigned long p = *ppos;
    unsigned int count = size;
    int ret = 0;
    int *register_addr = file->private_data; /*获取设备的寄存器基地址*/

    /*判断读位置是否有效*/
    if (p >= 5 * sizeof(int)) {
        return 0;
    }
    if (count > 5 * sizeof(int) - p) {
        count = 5 * sizeof(int) - p;
    }
        

  /*读数据到用户空间*/
    if (copy_to_user(buf, register_addr + p, count)) {
        ret = -EFAULT;
    } else {
        *ppos += count;
        ret = count;
    }
    
    return ret;
}

/*写函数*/
static ssize_t demodrv_write(struct file *file, const char __user *buf, size_t size, loff_t *ppos)
{
    unsigned long p =  *ppos;
    unsigned int count = size;
    int ret = 0;
    int *register_addr = file->private_data; /*获取设备的寄存器地址*/
  
    /*分析和获取有效的写长度*/
    if (p >= 5*sizeof(int))
        return 0;
    
    if (count > 5 * sizeof(int) - p)
        count = 5 * sizeof(int) - p;
    
    /*从用户空间写入数据*/
    if (copy_from_user(register_addr + p, buf, count))
        ret = -EFAULT;
    else
    {
        *ppos += count;
        ret = count;
    }
    return ret;
}
/*文件操作结构体*/
static const struct file_operations demodrv_fops =
{
    .open = demodrv_open,    
    .read = demodrv_read,
    .write = demodrv_write,
    .release = demodrv_release,
};

/*设备驱动模块加载函数*/
static int demodrv_init(void)
{
    /*初始化cdev结构*/
    cdev_init(&cdev, &demodrv_fops);
  
    /* 注册字符设备 */
    alloc_chrdev_region(&devno, 0, 2, DEMO_NAME );
    
    cdev_add(&cdev, devno, 2);
    printk("char device created, name %s, dev number %d\n", DEMO_NAME, devno);
    return 0;
}

/*模块卸载函数*/
static void demodrv_exit(void)
{
    cdev_del(&cdev);   /*注销设备*/
    unregister_chrdev_region(devno, 2); /*释放设备号*/
}

MODULE_LICENSE("GPL");

module_init(demodrv_init);
module_exit(demodrv_exit);

