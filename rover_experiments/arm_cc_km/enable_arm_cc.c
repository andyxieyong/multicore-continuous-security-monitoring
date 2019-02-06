#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Enable ARM cycle counter registers");
MODULE_VERSION("0.01");
MODULE_AUTHOR("MONOWAR HASAN");

// https://matthewarcus.wordpress.com/2018/01/27/using-the-cycle-counter-registers-on-the-raspberry-pi-3/

void enable_ccr(void *info) {
  // Set the User Enable register, bit 0
  asm volatile ("mcr p15, 0, %0, c9, c14, 0" :: "r" (1));
  // Enable all counters in the PNMC control-register
  asm volatile ("mcr p15, 0, %0, c9, c12, 0\t\n" :: "r"(1));
  // Enable cycle counter specifically
  // bit 31: enable cycle counter
  // bits 0-3: enable performance counters 0-3
  asm volatile ("mcr p15, 0, %0, c9, c12, 1\t\n" :: "r"(0x80000000));
}

static int __init enable_arm_cc_init(void){
   // printk(KERN_INFO "Hello, world.\n");
   // Each cpu has its own set of registers
   on_each_cpu(enable_ccr,NULL,0);
   printk (KERN_INFO "ARM cycle counter registers enabled!\n");
   return 0;
}

static void __exit enable_arm_cc_exit(void){
   printk(KERN_INFO "ARM CCR unloaded!\n");
}

module_init(enable_arm_cc_init);
module_exit(enable_arm_cc_exit);
