from PiCore import Pi, Processor, Sensors
from time import perf_counter

s_time: float = perf_counter()

pi = Pi()
cpu = Processor()
sensors = Sensors()

print(f"\n Pi model : {pi.pi_model()}")
print(f" Serial number : {pi.serial_number()}")


print(f"\n Name : {cpu.name()}")
print(f" Arch : {cpu.archeticture()}")
print(f" Family : {cpu.family()}")
print(f" Stepping : {cpu.stepping()}")
print(f" Cores : {cpu.cores_count()}")
print(f" Threads : {cpu.cores_count(logical=True)}\n")

print(f" l1i : {cpu.l1i_cache_size()}")
print(f" l1d : {cpu.l1d_cache_size()}")
print(f" l2 : {cpu.l2_cache_size()}")
print(f" l3 : {cpu.l3_cache_size()}\n")

print(f" Max speed : {cpu.max_clock_speed(aliased=False)}")
print(f" Min speed : {cpu.base_clock_speed(aliased=False)}")
print(f" Voltage : {cpu.voltage()} v")
print(f" Release date : {cpu.release_date()}\n")

print(f" Is Overclocked : {cpu.is_overclock()}")
print(f" Is Force Turbo : {cpu.is_force_turbo()}\n")
print(f" CPU Flags : {cpu.flags()}\n")


# Get the finished time
print(f"\nFinished in : {perf_counter() - s_time:.5f} s\n")