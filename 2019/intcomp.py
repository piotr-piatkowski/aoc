import sys
import inspect
import queue
from collections import defaultdict
from threading import Thread

class BaseInstruction:

    def __init__(self, comp, ip=None):
        self.comp = comp
        if ip is None:
            ip = comp.ip
        n = comp.memory[ip]
        self.params = [self.comp.memory[ip+1+i] for i in range(self.PARAMS_NUM)]
        pm_str = str(n)[-3::-1] + '0' * self.PARAMS_NUM
        self.param_modes = [pm_str[i] for i in range(self.PARAMS_NUM)]

    def __repr__(self):
        params = ', '.join([f"{self.params[i]}@{self.param_modes[i]}"
                for i in range(self.PARAMS_NUM)])
        return f"{self.__class__.__name__}(params={params})"

    def get_param(self, n):
        pm = self.param_modes[n]
        if pm == '0':
            return self.comp.memory[self.params[n]]
        elif pm == '1':
            return self.params[n]
        elif pm == '2':
            return self.comp.memory[self.params[n] + self.comp.rbo]
        else:
            raise Exception(f"Unknown param mode {pm}")

    def set_param(self, n, v):
        pm = self.param_modes[n]
        if pm == '0':
            self.comp.memory[self.params[n]] = v
        elif pm == '1':
            raise Exception("Immediate mode not supported for set")
        elif pm == '2':
            self.comp.memory[self.params[n] + self.comp.rbo] = v
        else:
            raise Exception(f"Unknown param mode {pm}")


class StopInstruction(BaseInstruction):
    OPCODE = 99
    PARAMS_NUM = 0

    def execute(self):
        raise StopIteration()


class BaseMathInstruction(BaseInstruction):
    PARAMS_NUM = 3

    def calculate(self, a, b):
        raise NotImplementedError()

    def execute(self):
        a = self.get_param(0)
        b = self.get_param(1)
        self.set_param(2, self.calculate(a, b))


class AddInstruction(BaseMathInstruction):
    OPCODE = 1

    def calculate(self, a, b):
        return a + b


class MulInstruction(BaseMathInstruction):
    OPCODE = 2

    def calculate(self, a, b):
        return a * b


class ReadInstruction(BaseInstruction):
    OPCODE = 3
    PARAMS_NUM = 1

    def execute(self):
        while self.comp.running:
            try:
                v = self.comp.input.get(timeout=0.1)
                break
            except queue.Empty:
                pass
        self.set_param(0, v)


class WriteInstruction(BaseInstruction):
    OPCODE = 4
    PARAMS_NUM = 1

    def execute(self):
        self.comp.output.put(self.get_param(0))


class JumpIfTrueInstruction(BaseInstruction):
    OPCODE = 5
    PARAMS_NUM = 2

    def execute(self):
        if self.get_param(0) != 0:
            self.comp.jump(self.get_param(1))


class JumpIfFalseInstruction(BaseInstruction):
    OPCODE = 6
    PARAMS_NUM = 2

    def execute(self):
        if self.get_param(0) == 0:
            self.comp.jump(self.get_param(1))


class LessThanInstruction(BaseInstruction):
    OPCODE = 7
    PARAMS_NUM = 3

    def execute(self):
        if self.get_param(0) < self.get_param(1):
            self.set_param(2, 1)
        else:
            self.set_param(2, 0)


class EqualsInstruction(BaseInstruction):
    OPCODE = 8
    PARAMS_NUM = 3

    def execute(self):
        if self.get_param(0) == self.get_param(1):
            self.set_param(2, 1)
        else:
            self.set_param(2, 0)


class AdjustRBOInstruction(BaseInstruction):
    OPCODE = 9
    PARAMS_NUM = 1

    def execute(self):
        self.comp.rbo += self.get_param(0)


# Register all Instruction classes keyed by opcode
op_to_class = {cls.OPCODE: cls
    for name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass)
    if issubclass(cls, BaseInstruction) and not name.startswith('Base')
}


class Computer:
    def __init__(self, memory):
        self.memory = defaultdict(int)
        for i, m in enumerate(memory):
            self.memory[i] = m
        self.input = queue.Queue()
        self.output = queue.Queue()
        self.rbo = 0
        self.running = False
        self.jump_done = False

    def _instruction_from_ip(self):
        opcode = self.memory[self.ip] % 100

        if opcode in op_to_class:
            return op_to_class[opcode](self)
        else:
            raise Exception(f"Instruction not found at ip={self.ip}: {opcode}")

    def jump(self, addr):
        self.ip = addr
        self.jump_done = True

    def run(self):
        self.running = True
        self.ip = 0
        while self.running:
            try:
                ins = self._instruction_from_ip()
                #print(f"ip={self.ip}, executing {ins}")
                self.jump_done = False
                ins.execute()
                if not self.jump_done:
                    self.ip += ins.PARAMS_NUM + 1
            except StopIteration:
                self.running = False

    def start(self):
        self.worker = Thread(target=self.run)
        self.worker.start()

    def stop(self):
        self.running = False
        self.worker.join()

