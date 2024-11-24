import csv
import struct
import argparse

def byteswap_64bit(value):
    if value < 0 or value > 0xFFFFFFFFFFFFFFFF:
        return -1 #Handle negative numbers or numbers >64bits as needed.

    bytes_list = value.to_bytes(8, 'big') #Ensure 8 bytes using big endian.
    swapped_bytes = bytes_list[::-1]
    swapped_value = int.from_bytes(swapped_bytes, 'big')
    return swapped_value

def byteswap_int(value):
    return ((value & 0xFF) << 24) | ((value & 0xFF00) << 8) | \
           ((value >> 8) & 0xFF00) | ((value >> 24) & 0xFF)


class Interpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory = [0] * 256  #Increased memory size if needed.
        self.memory_range = memory_range

    def run(self):
        with open(self.binary_file, 'rb') as file:
            while command := file.read(6):
                args = struct.unpack("BBBBBB", command)
                self.execute_command(args)

        # Запись результата в формате CSV
        with open(self.result_file, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["address", "value"])  # Заголовки столбцов
            for i in range(*self.memory_range):
                csv_writer.writerow([i, self.memory[i]])

    def execute_command(self, args):
        opcode, op1, op2, op3, op4, op5 = args

        match opcode:
            case 98:
                self.memory[op2] = op1
            case 19:
                address = self.memory[op2] + op3
                self.memory[op1] = self.memory[address]
            case 5:
                address = self.memory[op1]
                self.memory[address] = self.memory[op2]
            case 22:
                # Унарная операция bswap()
                operand_address = op2  # Адрес операнда (поле C)
                result_address = op1  # Адрес результата (поле B)
                operand = self.memory[operand_address]
                result = byteswap_64bit(operand)
                self.memory[result_address] = result
            case _:
                raise ValueError(f"Unknown opcode: {opcode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="путь к входному файлу")
    parser.add_argument("output_file", help="путь к выходному файлу")
    parser.add_argument("--memory_range", nargs=2, type=int, help="диапазон памяти для вывода результата")

    args = parser.parse_args()

    interpreter = Interpreter(args.input_file, args.output_file, tuple(args.memory_range))
    interpreter.run()