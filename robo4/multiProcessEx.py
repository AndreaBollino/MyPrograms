import multiprocessing

# Define a function to perform the task
def calculate_square(number):
    result = number * number
    return result

# Define a function for parallel processing
def parallel_processing(numbers, pool_size):
    # Create a multiprocessing pool
    pool = multiprocessing.Pool(pool_size)

    # Use the map function to distribute the work to the pool of processes
    results = pool.map(calculate_square, numbers)

    # Close the pool and wait for all tasks to complete
    pool.close()
    pool.join()

    return results

if __name__ == "__main__":
    # Define the list of numbers to calculate squares
    numbers_to_square = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Specify the number of processes to use (adjust according to your CPU cores)
    pool_size = multiprocessing.cpu_count()

    # Perform the parallel processing
    results = parallel_processing(numbers_to_square, pool_size)

    # Print the results
    print("Original numbers:", numbers_to_square)
    print("Squared numbers:", results)