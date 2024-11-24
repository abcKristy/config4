import struct
import argparse
import csv


class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file

    def assemble(self):
        with open(self.input_file, 'r') as infile, open(self.output_file, 'wb') as outfile, open(self.log_file, 'w',
                                                                                                 newline='') as logfile:
            csv_writer = csv.writer(logfile)
            # Записываем заголовок в CSV-файл
            csv_writer.writerow(["A", "B", "C", "D", "E", "F"])

            for line in infile:
                if line.startswith("#"):  # Пропускаем комментарии
                    continue
                if not line.strip():  # Пропускаем пустые строки
                    continue

                parts = line.strip().split()
                parsed_parts = list(map(int, parts))
                if len(parts) < 6:
                    parsed_parts += [0] * (6 - len(parts))  # Дополняем недостающие элементы нулями

                # Упаковка команд в бинарный формат
                command = struct.pack("BBBBBB", *parsed_parts)
                outfile.write(command)

                # Запись в CSV
                csv_writer.writerow(parsed_parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="путь к входному файлу")
    parser.add_argument("output_file", help="путь к выходному файлу")
    parser.add_argument("--log_file", help="путь к файлу-логу")

    args = parser.parse_args()

    assembler = Assembler(args.input_file, args.output_file, args.log_file)
    assembler.assemble()