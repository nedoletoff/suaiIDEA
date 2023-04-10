import matplotlib.pyplot as plt


def Berlekamp_Massey_algorithm(sequence):
    N = len(sequence)
    s = sequence[:]

    for k in range(N):
        if s[k] == 1:
            break
    f = {k + 1, 0}
    l = k + 1

    g = {0}
    a = k
    b = 0

    for n in range(k + 1, N):
        d = 0
        for ele in f:
            d ^= s[ele + n - l]

        if d == 0:
            b += 1
        else:
            if 2 * l > n:
                f ^= set([a - b + ele for ele in g])
                b += 1
            else:
                temp = f.copy()
                f = set([b - a + ele for ele in f]) ^ g
                l = n + 1 - l
                g = temp
                a = b
                b = n - l + 1

    def print_poly(polynomial):
        result = ''
        lis = sorted(polynomial, reverse=True)
        for i in lis:
            if i == 0:
                result += '1'
            else:
                result += 'x^%s' % str(i)

            if i != lis[-1]:
                result += ' + '

        return result

    return print_poly(f), l


def read_sequence() -> list:
    text = ''
    with open('sequence.txt', 'r') as f:
        for line in f:
            text += line
    sequence = text.split(', ')
    sequence.pop(-1)
    sequence = [int(i) for i in sequence]
    return sequence


def get_symbols(num, sequence):
    symbols = sequence[:num]
    return symbols


def draw_plot(linear_list: list, lenght_list: list):
    plt.plot(lenght_list, linear_list)
    plt.plot(lenght_list, lenght_list, 'r')
    plt.xlabel('Length of sequence')
    plt.ylabel('Linear complexity')
    plt.title('Linear complexity')
    plt.savefig('plot.png')
    plt.show()


if __name__ == '__main__':
    seq = read_sequence()
    linear_list = []
    for i in range(1, len(seq) + 1):
        # print(get_symbols(i, seq))
        poly, linear = Berlekamp_Massey_algorithm(get_symbols(i, seq))
        print(f"Length: {i}")
        print(f"Polynomial: {poly}")
        print(f"Linear: {linear}\n")
        linear_list.append(linear)
    draw_plot(linear_list, list(range(1, len(seq) + 1)))
