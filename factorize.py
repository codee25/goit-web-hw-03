import time
from multiprocessing import Pool, cpu_count


def factorize_sync(*numbers):
    result = []
    for number in numbers:
        divisors = [i for i in range(1, number + 1) if number % i == 0]
        result.append(divisors)
    return result


def factorize_single(n):
    return [i for i in range(1, n + 1) if n % i == 0]


def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(factorize_single, numbers)
    return result


def test_factorize():
    a, b, c, d = factorize_sync(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]
    print("Sync test passed!")
    a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]
    print("Parallel test passed!")


def main():
    numbers = [128, 255, 99999, 10651060]
    print(f"CPU count: {cpu_count()}")
    start = time.time()
    factorize_sync(*numbers)
    print(f"Sync time: {time.time() - start:.3f} s")
    start = time.time()
    factorize_parallel(*numbers)
    print(f"Parallel time: {time.time() - start:.3f} s")


if __name__ == "__main__":
    test_factorize()
    main()
