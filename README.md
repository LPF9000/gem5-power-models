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

## Output Graphs

### Big Cluster Dynamic Power
#### Default Settings
![system bigCluster_dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/db44d204-3f63-4e03-a0e8-cd8dad60c98e)

#### Double Cache Associativity
![system bigCluster_dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/8b7493e2-4544-400e-ae75-aa45fa1039a0)

#### Doubled Cache Size
![system bigCluster_dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/217bc2bd-331f-47cd-8167-a267e9b8e9e1)

### Big Cluster PM0 (Power On) Dynamic Power
#### Default Settings
![system bigCluster_pm0 dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/53092544-0255-4582-aad5-5af670b8c07d)

#### Double Cache Associativity
![system bigCluster_pm0 dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/80257749-3a5a-403a-96a3-340353f9104b)

#### Doubled Cache Size
![system bigCluster_pm0 dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/050c1c75-af18-4689-9f6c-55bf32bd7b97)

### Big Cluster Static Power
#### Default Settings
![system bigCluster_staticPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/f38ac7bd-50f0-4257-a256-13163b0294ea)

#### Double Cache Associativity
![system bigCluster_staticPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/a63ce10b-511c-459b-aba4-30684dda2ee1)

#### Doubled Cache Size
![system bigCluster_staticPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/57808cb9-cf1a-4d18-8afa-ff6001d312a0)

### Little Dynamic Power
#### Default Settings
![system littleCluster_dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/d16aae34-3e3b-47be-b251-f02e1fd5f0d3)


#### Double Cache Associativity
![system littleCluster_dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/4523dcf4-d886-40a4-b28a-26a7a0994fe8)

#### Doubled Cache Size
![system littleCluster_dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/b85da5ff-1df7-43f4-939a-3939d5e5a072)

### Little Cluster PM0 (Power On) Dynamic Power
#### Default Settings
![system littleCluster_pm0 dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/4e88bf24-b724-43e1-9299-8e6152501169)


#### Double Cache Associativity
![system littleCluster_pm0 dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/0aa7e21c-0788-41dc-a0ef-aac2a006dc5c)

#### Doubled Cache Size
![system littleCluster_pm0 dynamicPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/ea7f97f9-a6f9-47d0-ba7c-cbb4afc32bd7)

### Little Cluster Static Power
#### Default Settings
![system littleCluster_staticPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/e2a9d39f-6749-46bb-b691-a4fe71794d02)


#### Double Cache Associativity
![system littleCluster_staticPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/f23913e1-2ef8-4081-a3f4-8210a192769f)

#### Doubled Cache Size
![system littleCluster_staticPower_graph](https://github.com/LPF9000/gem5-power-models/assets/56581520/37c2e3c9-8936-4f89-962e-7acfa3602a96)
