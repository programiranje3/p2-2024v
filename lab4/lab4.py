from functools import reduce


def compute_product(*numbers, squared=False):
    # Option 1
    # prod = 1
    # for number in numbers:
    #     prod *= number if not squared else number**2
    # return prod
    # Option 2
    return reduce(lambda a, b: a*b, [number if not squared else number**2 for number in numbers])


def select_strings(*strings, threshold=3):
    # Option 1
    # selection = []
    # for s in strings:
    #     if s[0].lower() == s[-1].lower() and len(set(s)) > threshold:
    #         selection.append(s)
    # return selection
    # Option 2
    # return [s for s in strings if s[0].lower() == s[-1].lower() and len(set(s)) > threshold]
    # Option 3
    return list(filter(lambda s: s[0].lower() == s[-1].lower() and len(set(s)) > threshold, strings))



def process_product_orders(orders, discount=None, shipping=10):

    def compute_total_price(q, item_price):
        tot_price = q * item_price
        tot_price *= (100 - discount)/100 if discount else 1
        tot_price += shipping if tot_price < 100 else 0
        return tot_price

    # Option 1
    # processed_orders = []
    # for order_id, _, quantity, price_per_item in orders:
    #     tot_price = compute_total_price(quantity, price_per_item)
    #     processed_orders.append((order_id, tot_price))
    # return processed_orders
    # Option 2
    # return { order_id:compute_total_price(quantity, price_per_item)
    #         for order_id, _, quantity, price_per_item in orders}
    # Option 3
    return dict(map(lambda order: (order[0], compute_total_price(order[2], order[3])), orders))




import functools
from time import perf_counter

def timer(func):
    @functools.wraps(func)	 # čuva identitet funkcije nakon što je dekorisana
    def wrapper_timer(*args, **kwargs):

        start_time = perf_counter()

        value = func(*args, **kwargs)

        duration = perf_counter() - start_time
        print(f"The execution time of the {func.__name__} function is {duration:.4f}")

        return value
    return wrapper_timer


@timer
def compute_sum_loop(n):
    s = 0
    for x in range(1, n+1):
        s += sum(range(x+1))
    return s

@timer
def compute_sum_lc(n):
    return sum([sum(range(1, x+1)) for x in range(1, n+1)])

@timer
def compute_sum_mr(n):
    mapped = map(lambda x: sum(range(1, x+1)), range(1, n+1))
    return reduce(lambda a,b: a + b, mapped)


@timer
def mean_median_diff(n, k, iterations=10):
    from random import randint
    from statistics import mean, median

    m_mdn_diff = []
    for _ in range(iterations):
        l = [randint(1, k) for _ in range(n)]
        m_mdn_diff.append(abs(mean(l) - median(l)))
    print("Mean - median differences: " + ', '.join([f'{i:.4f}' for i in m_mdn_diff]))
    print(f"Average mean / median difference: {mean(m_mdn_diff):.4f}")





def standardiser(func):
    @functools.wraps(func)
    def wrapper_stadardiser(*args, **kwargs):

        if all([isinstance(a, (int, float)) for a in args]):
            from statistics import mean, stdev
            m = mean(args)
            sd = stdev(args)
            args = [(a-m)/sd for a in args]
        else:
            print(f"Not all positional arguments are numbers; skipping standardisation")

        print(f"Calling function: {func.__name__}, with the following arguments:")
        if args:
            print("\t-args:" + ", ".join([f'{a:.4f}' for a in args]))
        if kwargs:
            print("\t-kwargs:" + ", ".join([f'{arg}={val}' for arg, val in kwargs.items()]))

        value = func(*args, **kwargs)

        return round(value, 4)
    return wrapper_stadardiser



@standardiser
def sum_of_sums(*numbers, n=10):
    # Option 1
    # s = 0
    # for x in numbers:
    #     s += sum([x**i for i in range(n+1)])
    # return s
    # Option 2
    # return sum([sum([x**i for i in range(n+1)]) for x in numbers])
    # Option 3
    mapping = map(lambda x: sum([x**i for i in range(n+1)]), numbers)
    return reduce(lambda a, b: a+b, mapping)



if __name__ == '__main__':

    pass

    # Task 1
    # print(compute_product(1,-4,13,2))
    # print(compute_product(1, -4, 13, 2, squared=True))
    # print()
    # # Calling the compute_product function with a list
    # num_list = [2, 7, -11, 9, 24, -3]
    # # This is NOT a way to make the call:
    # print("Calling the function by passing a list as the argument")
    # print(compute_product(num_list))
    # print()
    # # instead, this is how it should be done (the * operator is 'unpacking' the list):
    # print("Calling the function by passing an UNPACKED list as the argument")
    # print(compute_product(*num_list))
    # print()

    # Task 2
    # str_list = ['yellowy', 'Bob', 'lovely', 'Yesterday', 'too']
    # print(select_strings(*str_list))
    # print()

    # Task 3
    # orders = [("34587", "Learning Python, Mark Lutz", 4, 40.95),
    #           ("98762", "Programming Python, Mark Lutz", 5, 56.80),
    #           ("77226", "Head First Python, Paul Barry", 3, 32.95),
    #           ("88112", "Einführung in Python3, Bernd Klein", 3, 24.99)]
    #
    # print(process_product_orders(orders))
    # print()
    # print("The same orders with discount of 10%")
    # print(process_product_orders(orders, discount=10))
    # print()

    # Task 4.1
    # print(compute_sum_loop(10000))
    # print()
    # print(compute_sum_lc(10000))
    # print()
    # print(compute_sum_mr(10000))

    # Task 4.2
    # mean_median_diff(100, 250, iterations=20)
    # print()

    # Task 5.1
    # print(sum_of_sums(1,3,5,7,9,11,13, n=7))

