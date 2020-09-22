def get_uniformly_distributed_values(amount, min_v, max_v):
    a = min_v
    r = [a]
    step = (max_v - min_v) / (amount - 1)
    for _ in range(1, amount - 1):
        r.append(int(a + step))
        a += step

    r.append(max_v)

    return r


class Program:
    def __init__(self, name, command, index):
        self.name = name
        self.command = command
        self.index = index

    def __repr__(self):
        return self.name
