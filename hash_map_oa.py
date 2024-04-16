# Name: John Burtsche
# OSU Email: burtschj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 6/9/2023
# Description: Implements a Hashmap class that uses a dynamic array described as buckets to hashmap different items based on there key. This class implements multiple Hashmap methods including put, empty_buckets, table_load, etc. Further descriptions can be found within the methods below.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    def quadprob(self, index, j):
        """
        Helper function for helping to find the
        index when quadratic probing
        """

        newindex = (index+j*j)%self._capacity

        return newindex


    def put(self, key: str, value: object) -> None:
        """
        This method takes a key and a value
        and uses it to store them in the correct
        location within the hashmap. It does this
        by first detemining if the table needs to be
        resized due to the load factor. Then uses
        a series of if statements to determine where
        to put the vaiable. If the place is taken...
        quadratic probing takes place to find the next
        index
        """

        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        j=0

        hash = self._hash_function(key)

        index = hash% self._capacity

        initialindex= index

        bucket = self._buckets.get_at_index(index)

        entry = HashEntry(key, value)


        if self.contains_key(key) == True:
            for index in range (0,self._capacity):
                if self._buckets.get_at_index(index) != None:
                    if self._buckets.get_at_index(index).key == key:
                        if self._buckets.get_at_index(index).is_tombstone is True:
                            self._size = self._size + 1
                        self._buckets.set_at_index(index, entry)

                        self._buckets.get_at_index(index).is_tombstone = False

                        return


        if bucket != None:

            while self._buckets.get_at_index(index) != None:
                if self._buckets.get_at_index(index).is_tombstone is True:
                    self._buckets.set_at_index(index, entry)
                    self._size= self._size+1
                    self._buckets.get_at_index(index).is_tombstone= False
                    return

                j=j+1
                index = self.quadprob(initialindex,j)
                if index> self._capacity-1:
                    index = 0

            self._buckets.set_at_index(index, entry)
            self._size = self._size + 1


        if bucket == None:
            self._buckets.set_at_index(index, entry)
            self._size = self._size + 1



    def table_load(self) -> float:
        """
        Determines the table load using
        get_size and capacity. It then
        returns this value.
        """

        num = self.get_size() / self._capacity

        return num


    def empty_buckets(self) -> int:
        """
        Determines the amount of empty buckets
        by using a for loop that cycles through the
        hashmap. It then returns this value.
        """

        num= 0
        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index) == None:
                num= num+1

        return num


    def resize_table(self, new_capacity: int) -> None:
        """
        This method takes the new capacity and
        returns a table resized to the proper size.
        If the capacity is< size then it returns nothing.
        It does this by using the get keys and values method
        to get an array of all the non-tombstone values
        and then uses put to place them in their correct
        location in a new dynamic array appended to the
        correct capacity
        """

        cap = new_capacity
        hold = self._capacity
        values = self.get_keys_and_values()

        variables = values.length()

        if new_capacity < self._size:
            return

        if self._is_prime(new_capacity) is False:
            cap = self._next_prime(new_capacity)

        self._buckets = DynamicArray()
        self._capacity = cap
        self._size = 0

        for i in range (cap):
            self._buckets.append(None)

        for index in range (variables):
            contents = values[index]
            self.put(contents[0], contents[1])



    def get(self, key: str) -> object:
        """
        Takes the inputed key and
        cycles through all the values
        until it reaches the key. If
        the key is not found or it is
        a tombstone it returns None. Otherwise
        it returns the value
        """

        for index in range(0, self._capacity):
            if self._buckets.get_at_index(index) != None:
                if self._buckets.get_at_index(index).key == key:
                    num = self._buckets.get_at_index(index).value
                    if self._buckets.get_at_index(index).is_tombstone ==True:
                        return None

                    return num

        return None


    def contains_key(self, key: str) -> bool:
        """
        Takes the key and returns True
        if the for loop finds it or false
        if it is not within the hashmap.
        """

        for index in range(0, self._capacity):
            if self._buckets.get_at_index(index) != None:
                if self._buckets.get_at_index(index).key == key:

                    return True

        return False


    def remove(self, key: str) -> None:
        """
        Takes the key and finds the index
        that it is within using a for loop. Then
        it sets the tombstone to true and reduces the
        size of the hashmap
        """


        for index in range(0, self._capacity):
            if self._buckets.get_at_index(index) != None:
                if self._buckets.get_at_index(index).key == key:
                    if self._buckets.get_at_index(index).is_tombstone is False:
                        self._buckets.get_at_index(index).is_tombstone = True
                        self._size = self._size-1



    def clear(self) -> None:
        """
        Clears the array by setting any value
        that is not none to none using a for loop. Then
        it returns this hashmap with size 0 and the
        same capacity
        """

        num = self._capacity
        for index in range(0, self._capacity):
            if self._buckets.get_at_index(index) != None:
                self._buckets.set_at_index(index,None)

        self._size = 0
        self._capacity = num


    def get_keys_and_values(self) -> DynamicArray:
        """
        Fills a blank array with all the indexes that
        contain keys and values as long as the tombstone
        is set to false. It then returns this array.
        """

        blank = DynamicArray()

        for index in range (0, self._capacity):
            if self._buckets.get_at_index(index) != None:
                keys = self._buckets.get_at_index(index).key
                value = self._buckets.get_at_index(index).value

                if self._buckets.get_at_index(index).is_tombstone is False:
                    blank.append((keys, value))

        return blank


    def __iter__(self):
        """
        sets self._index to 0 and returns it
        """

        self._index = 0

        return self


    def __next__(self):
        """
        Goes to the next filled index and
        returns that value as long as it is not a tombstone.
        If it reaches the end of the array a dynamic array
        exception stops the iteration
        """

        try:

            while self._buckets.get_at_index(self._index) is None:
                self._index= self._index+1
                if self._buckets.get_at_index(self._index) is not None:
                    if self._buckets.get_at_index(self._index).is_tombstone is True:
                        self._index =self._index+1



            if self._buckets.get_at_index(self._index) is not None:

                    value = self._buckets.get_at_index(self._index)
                    self._index= self._index+1
                    return value


        except DynamicArrayException:
            raise StopIteration







# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    m.put('key313', 1000)
    m.put('key232', 1000)
    m.put('key174', 1000)
    m.put('key582', 1000)
    m.put('key618', 1000)
    m.put('key485', 1000)
    m.put('key953', 1000)
    m.put('key681', 1000)
    m.put('key718', 1000)
    m.put('key858', 1000)
    m.put('key684', 1000)
    m.put('key961', 1000)
    m.put('key889', 1000)
    m.put('key387', 1000)
    m.put('key961', 1000)
    m.remove('key961')
    m.put('key961', 1000)


    print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('str14', 1400)
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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)

    m.put('key5',20)
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
