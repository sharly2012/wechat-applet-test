import time


def run_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(func.__name__ + " took: " + str(end_time - start_time) + "seconds")
        return result

    return wrapper


@run_time
def multiplication():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print("%s * %s = %s" % (j, i, i * j), end=" ")
        print()


if __name__ == '__main__':
    multiplication()
