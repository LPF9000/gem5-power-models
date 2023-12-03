# gem5-power-models
Gem5 Power Modelling


------------------------------------------------------
How to install cross-tool ng for compiling ARM files:
------------------------------------------------------
sudo apt-get install -y autoconf automake bison flex gawk libtool libncurses5-dev make patch python3 texinfo unzip help2man libtool-bin
clone crosstool-ng repository
cd crosstool-ng
./bootstrap
./configure --prefix=home/USERNAME/opt/crosstool-ng
make
sudo make install
export PATH="home/USERNAME/opt/crosstool-ng/bin:$PATH"

add export PATH="/home/USERNAME/opt/crosstool-ng/bin:$PATH" to bash.rc in home
ct-ng version
ct-ng menuconfig -> target arm

ct-ng arm-unknown-linux-uclibcgnueabi
ct-ng build

** TAKES A LONG ASS TIME**

Set bash RC to uclibcgnueabi bin folder

------------------------------------------------------
Command for compiling ARM
------------------------------------------------------
arm-unknown-linux-uclibcgnueabi-gcc -O0 -ggdb3 -std=c99 -static -o hello_n hello_n.c


------------------------------------------------------
Building/running terminal window for full-system
------------------------------------------------------
cd gem5/util/term
gcc  -o m5term term.c
sudo install -o root -m 555 m5term /usr/local/bin
./m5term <host> <port> (example: ./m5term localhost 3456)

------------------------------------------------------
Commands for building architecture:
------------------------------------------------------


***new stuff:***

*** find loopback device ***
losetup -f

sudo losetup -o 65536 /dev/loop17 ubuntu-18.04-arm64-docker.img


*** mount the disk ***
sudo mount -o loop,offset=65536 ubuntu-18.04-arm64-docker.img /mnt/mydrive


*** copy binaries to folder ***
sudo cp -r /path/to/arm/folder/with/binaries /mnt/mydrive/home/

*** Set permissions for binaries***
sudo chmod +x hello_n

*** if running the files doesn't works - setting up chroot bin/bash***
sudo apt-get install qemu-user-static
sudo cp /usr/bin/qemu-aarch64-static /mnt/mydrive/usr/bin/
sudo chroot /mnt/mydrive /bin/bash
export LANG=C
export LC_ALL=C


*** Unmount drive ***
sudo umount  /home/lpf9000/gem5/gem5/ubuntu-18.04-arm64-docker.img

** cleanup loopback device **
losetup -d /dev/loop17


*** Main Build Script ***

build/ARM/gem5.opt --debug-flag=Printf --debug-flag=Terminal gem5-power-models/src/fs_power.py --kernel /home/lpf9000/gem5/gem5/aarch-system-20220707/binaries/vmlinux.arm64 --disk /home/lpf9000/gem5/gem5/ubuntu-18.04-arm64-docker.img --bootloader /home/lpf9000/gem5/gem5/aarch-system-20220707/binaries/boot.arm64 --caches





https://www.gem5.org/documentation/general_docs/fullsystem/m5term
or
telnet localhost 3456

***old stuff:***

build/ARM/gem5.opt gem5-power-models/src/two_level.py --arch ARM --l1i_assoc=4 --l1i_size=4kB --binary hello_n
build/X86/gem5.opt gem5-power-models/src/two_level.py --arch x86 --l1i_assoc=4 --l1i_size=4kB --binary hello_n


------------------------------------------------------
MISC if you need it
------------------------------------------------------



NOTE: ARM DVFS modelling

 There are some additional modifications required in configs/example/arm/devices.py. 

[...]
self.clk_domain = SrcClockDomain(clock=cpu_clock,
                                 voltage_domain=self.voltage_domain,
                                 domain_id=system.numCpuClusters())
[...]