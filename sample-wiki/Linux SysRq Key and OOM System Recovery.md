---
title:       Linux Magic SysRq Key and OOM
lable:       
description: Command for recovering frozen Linux machine using the SysRq keybinding.
keywords:    
---

## Overview

Unlike MacOSX and Microsoft Windows NT, the Linux kernel and consequentely, Linux distributions still have an OOM - Out-Of-Memory bug, which freezes the computer and makes it unresponsive when almost all memory is used. This issue is annoying as even the keyboard becomes unresponsive and key combination similar to Windows' Ctrl+Al+Del for invoking a process manager does not work. 

For many users, the solution is a forced system reboot. However, it may lead to data loss, data corruption and loss of productivity. An alternative to system reboot is the Linux's kernel **magic SysReq** key combination, which is available in Linux kenels compiled with CONFIG_MAGIC_SYSREQ option enabled. Nowadays, most Linux distributions are shipped with a kenel using this option enabled.In order to be use SysReq keyboard shortcut for system recovery, it is necessary to enable it either temporarily or permanently by editing the appropriate configuration file.
 
## SysRq Settings

### Check whether SysRq status

To check whether SysRq is eanabled, run 

```sh
$ cat /proc/sys/kernel/sysrq
1
```

if the output is 0, then sysrq is disabled, otherwise sysrq is enabled. All sysrq functions are only enabled when this pseudo-file, created by the Linux kernel, is set to 1. 

### Set SySrq Value without reboot

Enable all SysRq options/functions.

```sh
$ sudo sysctl kernel.sysrq=1
```

All SysRq options can be enabled by setting the pseudo-file (a kernel interface) using the command.

```sh
$ echo 1 | sudo tee /proc/sys/kernel/sysrq
```

### Persist SysRq Value on Reboot

Create backup of the configuration file.

```sh
$ sudo cp /etc/sysctl.d/99-sysctl.conf -v /etc/sysctl.d/99-sysctl.conf.back
```

Override the file 99-sysctl.conf with the line `kernel.sysrq = 1`. 

```sh
$ echo "kernel.sysrq = 1" | sudo tee /etc/sysctl.d/99-sysctl.conf
```


## Commands

SysRq key-combination provide the following commands.

- b – reboots the computer
- e – ask all processes to terminate gracefully
- f – to get rid of an [Out Of Memory condition](https://en.wikipedia.org/wiki/Out_of_memory "Out Of Memory Condition") via oom\_kills
- i – to kill all processes immediately except init
- k – to kill absolutely all processes, including X
- m – to output the current memory information
- o – to shut down the computer
- r – very useful, to take the keyboard out of the X server control
- s – to sync data from all mounted devices (avoid data loss in case of violent reboot)
- t – to display a list of the current tasks
- u – to remount all file system in read-only mode
 

### Unfreeze Computer in OOM 

Unfreeze computer in OOM (Out-Of-Memory) by terminating memory hogging processes.

+ **SysRq + Alt + f** 

### Safe System Reboot

Safe system reboot with graceful termination of processes for avoiding data loss and file system damage.

+ **Alt + SysRq + reisub**

This keybinding peforms the following sequence of operations.

- (r) - Take the keyboard from X
- (e) - Ask all programs to end gently
- (i) Kill the one who did not
- (s) - Save the data from the cache to the hard drive
- (u) - Remounts the file systems
- (b) - Reboot

reisub meneumonic: 

  + opposite of "busier"
  + "[R]aising an [E]lephant is so [U]tterly [B]oring"
## See 

+ *Linux Magic System Request Key Hacks*, Kernel\.org
  + https://www.kernel.org/doc/html/latest/admin-guide/sysrq.html
+ *How to enable all SysRq functions on Linux*, Linux Config (2020)
  + https://linuxconfig.org/how-to-enable-all-sysrq-functions-on-linux 
+ *Understanding the SysRq Key – The Magic Key To Control Linux*, MakeTechEasier (2012)
  + https://www.maketecheasier.com/the-usage-of-sysrq-key-in-linux/ 
+ *What is /proc/sysrq-trigger in linux and how to use sysrq kernel feature ?*
  + https://ngelinux.com/what-is-proc-sysrq-trigger-in-linux-and-how-to-use-sysrq-kernel-feature/
+ *Use the Magic SysRq Key on Linux to Fix Frozen X Servers, Cleanly Reboot, and Run Other Low-Level Commands*, Chris Hoffman, How-To Geek (2012)
  + https://www.howtogeek.com/119127/use-the-magic-sysrq-key-on-linux-to-fix-frozen-x-servers-cleanly-reboot-and-run-other-low-level-commands/    