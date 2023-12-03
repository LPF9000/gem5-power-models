# gem5-power-models
Gem5 Power Modelling

## How to install cross-tool ng for compiling ARM files:

```bash
sudo apt-get install -y autoconf automake bison flex gawk libtool libncurses5-dev make patch python3 texinfo unzip help2man libtool-bin
clone crosstool-ng repository
cd crosstool-ng
./bootstrap
./configure --prefix=home/USERNAME/opt/crosstool-ng
make
sudo make install
export PATH="home/USERNAME/opt/crosstool-ng/bin:$PATH"
```
### add export PATH="/home/USERNAME/opt/crosstool-ng/bin:$PATH" to bash.rc in home
```bash
ct-ng version
```
### Target ARM in menuconfig
```bash
ct-ng menuconfig
```
### Build
```bash
ct-ng arm-unknown-linux-uclibcgnueabi
ct-ng build
```
**TAKES A Very Long TIME**

Set bash RC to uclibcgnueabi bin folder

## Command for compiling ARM

```bash
arm-unknown-linux-uclibcgnueabi-gcc -O0 -ggdb3 -std=c99 -static -o hello_n hello_n.c
```

## Building/running terminal window for full-system

*First download the kernel, bootloader, and disk image:*
https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries

### Commands for building architecture:

#### Find loopback device
```bash
losetup -f

sudo losetup -o 65536 /dev/loop17 ubuntu-18.04-arm64-docker.img
```
#### Mount the disk
```bash
sudo mount -o loop,offset=65536 ubuntu-18.04-arm64-docker.img /mnt/mydrive
```

#### Copy Binaries to Folder
```bash
sudo cp -r /path/to/arm/folder/with/binaries /mnt/mydrive/home/
```

#### Set permissions for binaries
```bash
sudo chmod +x hello_n
```
*Continue for rest of binaries...*

**If running the files doesn't works - setting up chroot bin/bash**

*Can also compile to mounted drive using this method*
```bash
sudo apt-get install qemu-user-static
sudo cp /usr/bin/qemu-aarch64-static /mnt/mydrive/usr/bin/
sudo chroot /mnt/mydrive /bin/bash
export LANG=C
export LC_ALL=C
bash

#### Unmount Drive
```bash
sudo umount  /home/lpf9000/gem5/gem5/ubuntu-18.04-arm64-docker.img
```

#### Cleanup Loopback Devices
```bash
losetup -d /dev/loop17
```

## Main Build Script
```bash
build/ARM/gem5.opt --debug-flag=Printf --debug-flag=Terminal gem5-power-models/src/fs_power.py --kernel /home/lpf9000/gem5/gem5/aarch-system-20220707/binaries/vmlinux.arm64 --disk /home/lpf9000/gem5/gem5/ubuntu-18.04-arm64-docker.img --bootloader /home/lpf9000/gem5/gem5/aarch-system-20220707/binaries/boot.arm64 --caches --dvfs
```

https://www.gem5.org/documentation/general_docs/fullsystem/m5term

```bash
cd gem5/util/term
gcc  -o m5term term.c
sudo install -o root -m 555 m5term /usr/local/bin
```
./m5term <host> <port>
```bash
./m5term localhost 3456
```
or
telnet localhost 3456

## ARM DVFS Modeling

**NOTE:** *There are some additional modifications required in configs/example/arm/devices.py.*
```python
[...]
self.clk_domain = SrcClockDomain(clock=cpu_clock,
                                 voltage_domain=self.voltage_domain,
                                 domain_id=system.numCpuClusters())
[...]
```
