# Course: CS261 - Data Structures
# Assignment: A5P1 hash map
# Student: Donald Logan Kiser
# Description:  implementation of a hash map data structure


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        DESCRIPTION:    clears contents of HashMap
        INPUT:          NA
        RETURN:         NA
        """
        # iterate through HashMap.buckets and replace current LL with empty LL
        for index in range(self.capacity):
            self.buckets.set_at_index(index, LinkedList())

        # update size property to zero
        self.size = 0


    def get(self, key: str) -> object:
        """
        DESCRIPTION:    returns value associated with given key
        INPUT:          key to search for and return value associated with
        RETURN:         value associated with key argument
        """
        # pass key through hash function to find appropriate index in DA
        hash_val = self.hash_function(key)
        da_index = hash_val % self.capacity

        # handle case where HashMap is empty
        if self.buckets.length() == 0:
            return False

        # reference target LL with convenient variable
        target_ll = self.buckets.get_at_index(da_index)

        # handle case where key does not exist in LL
        if target_ll.contains(key) is None:
            return None

        # handle case where key does exist within the LL
        if target_ll.contains(key) is not None:
            return target_ll.contains(key).value


    def put(self, key: str, value: object) -> None:
        """
        DESCRIPTION:    updates the key/value pair in the HashMap
        INPUT:          a key and value to be added to HashMap
        RETURN:         NA
        """
        # pass key through hash function to find appropriate index in DA
        hash_val = self.hash_function(key)
        da_index = hash_val % self.capacity

        # handle case where key already exists in LL
        if self.buckets.get_at_index(da_index).contains(key) is not None:
            self.buckets.get_at_index(da_index).remove(key)
            self.buckets.get_at_index(da_index).insert(key, value)
            return

        # handle case where key does NOT exist in LL
        if self.buckets.get_at_index(da_index).contains(key) is None:
            self.buckets.get_at_index(da_index).insert(key, value)
            self.size += 1


    def remove(self, key: str) -> None:
        """
        DESCRIPTION:    removes given key/value from HashMap
        INPUT:          key to be removed
        RETURN:         NA
        """
        # pass key through hash function to find appropriate index in DA
        hash_val = self.hash_function(key)
        da_index = hash_val % self.capacity

        # remove SLNode containing key if one exists
        if self.buckets.get_at_index(da_index).remove(key):
            # update HashMap.size if node removal was successful
            self.size -= 1


    def contains_key(self, key: str) -> bool:
        """
        DESCRIPTION:    Indicates whether a key exists in the HashMap
        INPUT:          key to check
        RETURN:         boolean indication of whether key exists in the HashMap
        """
        # pass key through hash function to find appropriate index in DA
        hash_val = self.hash_function(key)
        da_index = hash_val % self.capacity

        # handle case where HashMap is empty
        if self.buckets.length() == 0:
            return False

        # reference target LL with convenient variable
        current_ll = self.buckets.get_at_index(da_index)

        # handle case where key does not exists in target LL
        if current_ll.contains(key) is None:
            return False

        # handle case where key exists in target LL
        if current_ll.contains(key) is not None:
            return True


    def empty_buckets(self) -> int:
        """
        DESCRIPTION:    returns number of empty buckets in hash table
        INPUT:          NA
        RETURN:         integer indication of the number of empty buckets
        """
        # iterate through HashMap.buckets DA and count empty LinkedLists
        count = 0
        for index in range(self.buckets.length()):
            if self.buckets.get_at_index(index).length() == 0:
                count += 1
        return count


    def table_load(self) -> float:
        """
        DESCRIPTION:    returns the current HashMap table load factor
        INPUT:          NA
        RETURN:         float indication of HashMap table load factor
        """
        return float(self.size / self.capacity)


    def resize_table(self, new_capacity: int) -> None:
        """
        DESCRIPTION:    changes the capacity of the HashMap table
        INPUT:          new capacity of HashMap
        RETURN:         NA
        """
        # handle case where new_capacity < 1
        if new_capacity < 1:
            return

        # construct new HashMap DA skeleton with new capacity
        new_da = DynamicArray()
        for _ in range(new_capacity):
            new_da.append(LinkedList())

        # iterate through original DA
        for index in range(self.capacity):
            # iterate through LL located at index
            current_ll = self.buckets.get_at_index(index)
            # re-hash keys and populate new_da with re-hashed nodes
            for node in current_ll:
                hash_val = self.hash_function(node.key)
                new_da_index = hash_val % new_capacity
                new_da.get_at_index(new_da_index).insert(node.key, node.value)

        # replace HashMap.buckets w/ new_da and update HashMap.capacity
        self.buckets = new_da
        self.capacity = new_capacity


    def get_keys(self) -> DynamicArray:
        """
        DESCRIPTION:    returns a DA containing all keys from the HashMap
        INPUT:          NA
        RETURN:         DA containing all keys from the HashMap
        """
        # reference return DynamicArray with a convenient variable
        return_da = DynamicArray()

        # iterate through HashMap DA and LL while appending keys to return_da
        for index in range(self.capacity):
            current_ll = self.buckets.get_at_index(index)
            for node in current_ll:
                return_da.append(node.key)

        return return_da