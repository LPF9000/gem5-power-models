# gem5-power-models
Gem5 Power Modelling


NOTE: ARM DVFS modelling

 There are some additional modifications required in configs/example/arm/devices.py. 

[...]
self.clk_domain = SrcClockDomain(clock=cpu_clock,
                                 voltage_domain=self.voltage_domain,
                                 domain_id=system.numCpuClusters())
[...]