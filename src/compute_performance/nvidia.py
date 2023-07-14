#!/usr/bin/env python3
from pynvml import *
from dataclasses import dataclass

nvmlInit()

@dataclass
class GpuProcess:
    pid: int
    used_memory: int
    instance_id: int
    compute_instance_id: int


@dataclass
class GpuDevice:
    name: str
    board_id: str
    serial: str
    uuid: str
    index: int
    gpu_usage: int
    memory_usage: int
    memory_total: int
    memory_free: int
    memory_used: int
    encoder_usage: int
    decoder_usage: int
    graphics_processes: list
    compute_processes: list
    power_usage: int
    temperature: int

@dataclass
class GpuSystem:
    cuda_version: str
    driver_version: str
    gpu_count: int
    gpus: list

# Information fetchers
class GpuDeviceFetcher:
    def __init__(self, index):
        self.index = index
        self.h = nvmlDeviceGetHandleByIndex(self.index)
        self.name = str(nvmlDeviceGetName(self.h))
        self.board_id = str(nvmlDeviceGetBoardId(self.h))
        self.serial = str(nvmlDeviceGetSerial(self.h))
        self.uuid = str(nvmlDeviceGetUUID(self.h))

    def fetch(self):
        _usage = nvmlDeviceGetUtilizationRates(self.h)
        _meminfo = nvmlDeviceGetMemoryInfo(self.h)
        _encoder_usage = nvmlDeviceGetEncoderUtilization(self.h)
        _decoder_usage = nvmlDeviceGetDecoderUtilization(self.h)
        _graphics_processes = nvmlDeviceGetGraphicsRunningProcesses(self.h)
        _compute_processes = nvmlDeviceGetComputeRunningProcesses(self.h)
        _power_usage = nvmlDeviceGetPowerUsage(self.h)
        _gpu_temperature = nvmlDeviceGetTemperature(
            self.h, NVML_TEMPERATURE_GPU)

        return GpuDevice(
            name=self.name,
            board_id=self.board_id,
            serial=self.serial,
            uuid=self.uuid,
            index=self.index,
            gpu_usage=_usage.gpu,
            memory_usage=_usage.memory,
            memory_total=_meminfo.total,
            memory_free=_meminfo.free,
            memory_used=_meminfo.used,
            encoder_usage=_encoder_usage[0],
            decoder_usage=_decoder_usage[0],
            graphics_processes=[GpuProcess(pid=process.pid, used_memory=process.usedGpuMemory, instance_id=process.gpuInstanceId,
                                           compute_instance_id=process.computeInstanceId) for process in _graphics_processes],
            compute_processes=[GpuProcess(pid=process.pid, used_memory=process.usedGpuMemory, instance_id=process.gpuInstanceId,
                                           compute_instance_id=process.computeInstanceId) for process in _compute_processes],
            power_usage=_power_usage,
            temperature=_gpu_temperature
        )

class GpuSystemFetcher:
    def __init__(self):
        nvmlInit()
        self.cuda_version = str(nvmlSystemGetCudaDriverVersion())
        self.driver_version = str(nvmlSystemGetDriverVersion())
        self.device_count = nvmlDeviceGetCount()
        
        self.gpu_fetchers = [GpuDeviceFetcher(idx) for idx in range(self.device_count)]

    def fetch(self):
        return GpuSystem(
            cuda_version=self.cuda_version,
            driver_version=self.driver_version,
            gpu_count=self.device_count,
            gpus=[gpu.fetch() for gpu in self.gpu_fetchers]
        )
    
    def close(self):
        nvmlShutdown()


def main():
    gsf = GpuSystemFetcher()
    print(gsf.fetch())

if __name__ == '__main__':
    main()
    nvmlShutdown()
