import time
def dummy_func(num):
    print(num)
    for i in range(num):
        print("Print: %d" % (i))
        time.sleep(1)
if __name__ == '__main__':
    dummy_func(1000)
