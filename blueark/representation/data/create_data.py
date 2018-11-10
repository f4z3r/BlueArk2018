import sys
import random


def create_file(cols, rows, fn, template, a, b):
    with open(fn, 'w') as f:
        f.write(','.join(template + str(i) for i in range(cols)))
        f.write('\n')
        f.write('\n'.join(','.join(str(random.randint(a, b))
                                   for _ in range(cols)) for _ in range(rows)))


def main():
    dp = 24
    create_file(5, dp, 'fake_tanks.txt', 'Tank ', 30, 90)
    create_file(5, dp, 'fake_pipes.txt', 'Pipe ', 80, 160)
    create_file(5, dp, 'fake_consumers.txt', 'Consumer ', 20, 80)
    create_file(5, dp, 'fake_power.txt', 'Generator ', 10, 60)


if __name__ == '__main__':
    main()
