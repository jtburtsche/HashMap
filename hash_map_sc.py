# Name: John Burtsche
# OSU Email: burtschj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 6/9/2023
# Description: Implements a Hashmap class that uses a dynamic array described as buckets and a linked list to hashmap different items based on there key. This class implements multiple Hashmap methods including put, empty_buckets, table_load, etc. Further descriptions can be found within the methods below.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method takes a key and a value
        and uses it to store them in the correct
        location within the hashmap. It does this
        by first detemining if the table needs to be
        resized due to the load factor. Then uses
        a series of if statements to determine where
        to put the vaiable. If the key is in the
        map already it replaces it or it inserts it
        using insert.
        """

        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)

        index = hash% self._capacity

        bucket = self._buckets.get_at_index(index)

        check = bucket.contains(key)


        if check != None:
            check.value = value

        if check == None:
            bucket.insert(key, value)
            self._size = self._size + 1



    def empty_buckets(self) -> int:
        """
        Determines the amount of empty buckets
        by using a for loop that cycles through the
        hashmap. It then returns this value.
        """

        num= 0
        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index)._head == None:

                num = num+1


        return num


    def table_load(self) -> float:
        """
        Determines the table load using
        get_size and capacity. It then
        returns this value.
        """

        num = self.get_size() / self._capacity

        return num


    def clear(self) -> None:
        """
        Clears the array by setting any value
        that is not none to an empty
        linked list using a for loop. Then
        it returns this hashmap with size 0 and the
        same capacity
        """

        num = self._capacity
        for index in range(0, self._capacity):
            if self._buckets.get_at_index(index)._head != None:
                self._buckets.set_at_index(index, LinkedList())


        self._size = 0
        self._capacity = num



    def resize_table(self, new_capacity: int) -> None:
        """
        This method takes the new capacity and
        returns a table resized to the proper size.
        If the capacity is< 1 then it returns nothing.
        It does this by using the get keys and values method
        to get an array of all the keys and values
        and then uses put to place them in their correct
        location in a new dynamic array appended to the
        correct capacity. Returns self
        """

        cap = new_capacity
        hold = self._capacity
        values = self.get_keys_and_values()

        variables = values.length()


        if new_capacity< 1:
            return

        if self._is_prime(new_capacity) == False:
            cap =self._next_prime(new_capacity)



        self._buckets = DynamicArray()
        self._capacity = cap
        self._size = 0


        for i in range (cap):
            self._buckets.append(LinkedList())

        for index in range (variables):
            hey = values[index]
            self.put(hey[0], hey[1])



    def get(self, key: str):
        """
        Takes the inputed key and
        cycles through all the values
        until it reaches the key. If
        the key is not found or it returns None.
        Otherwise
        it returns the value
        """

        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index).contains(key) !=None:
                value = self._buckets.get_at_index(index).contains(key)
                num = value.value
                return num


    def contains_key(self, key: str) -> bool:
        """
        Takes the key and returns True
        if the for loop finds it or false
        if it is not within the hashmap.
        """

        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index).contains(key) !=None:
                return True

        return False


    def remove(self, key: str) -> None:
        """
        Takes the key and finds it within
        the buckets. If it is found it removes
        it using .remove from a6_include. It then
        returns self
        """

        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index).contains(key) !=None:
                self._buckets.get_at_index(index).remove(key)
                self._size = self._size - 1



    def get_keys_and_values(self) -> DynamicArray:
        """
        Fills a blank array with all the indexes that
        contain keys and values.
        It goes through every node in the linked list
        using a while loop.
        It then returns this array.
        """

        blank = DynamicArray()

        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index)._head !=None:
                node = self._buckets.get_at_index(index)._head
                while node != None:
                    hold = node
                    key = node.key
                    value = node.value
                    blank.append((key, value))

                    node = node.next

        return blank



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This takes a dynamic array and
    finds the mode as well as the frequency.
    It does this by first creating a hashmap
    and then using the key provided by the dynamic
    array and setting the value equal to how many
    were previously of the same key +1. It then
    returns the item(s) with the highest value
    in an array.
    """


    map = HashMap()
    self = map




    key = da.get_at_index(0)
    value = 1

    hash = self._hash_function(key)

    index = hash % self._capacity

    bucket = self._buckets.get_at_index(index)

    check = bucket.contains(key)

    bucket.insert(key, value)
    self._size = self._size + 1




    hold = DynamicArray()
    hold.append(da.get_at_index(0))
    count = 1



    for index in range(1, da.length()):
        key= da.get_at_index(index)
        value = 0



        hash = self._hash_function(key)

        mapindex = hash% self._capacity

        bucket = self._buckets.get_at_index(mapindex)

        check = bucket.contains(key)


        if check != None:
            check.value = check.value+1

            if check.value == count:
                hold.append(da.get_at_index(index))


            if check.value> count:
                hold = DynamicArray()
                hold.append(da.get_at_index(index))
                count = check.value


        if check == None:


            value = value+1
            bucket.insert(key, value)
            self._size = self._size + 1

            if value == count:
                hold.append(da.get_at_index(index))


    return (hold, count)



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
