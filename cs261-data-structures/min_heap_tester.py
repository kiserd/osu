# Course: CS261 - Data Structures
# Student Name: Donald Logan Kiser
# Assignment: A5P2 min_heap UNIT TESTING
# Description: unit tests for min_heap.py

# Import pre-written DynamicArray and LinkedList classes
from a5_include import *

import unittest
from min_heap import MinHeap, MinHeapException

class minHeapTests(unittest.TestCase):
    """
    definte unit tests for min_heap.py
    """
    def test_1(self):
        """
        add() example #1
        """
        h = MinHeap()
        self.assertTrue(h.is_empty())
        for value in range(300, 200, -15):
            h.add(value)
            if value == 300:
                list = [300]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 285:
                list = [285, 300]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 270:
                list = [270, 300, 285]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 255:
                list = [255, 270, 285, 300]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 240:
                list = [240, 255, 285, 300, 270]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 225:
                list = [225, 255, 240, 300, 270, 285]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 210:
                list = [210, 255, 225, 300, 270, 285, 240]
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))

    def test_2(self):
        """
        add() example #2
        """
        h = MinHeap(['fish', 'bird'])
        list = ['bird', 'fish']
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
            h.add(value)
            if value == 'monkey':
                list = ['bird', 'fish', 'monkey']
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 'zebra':
                list = ['bird', 'fish', 'monkey', 'zebra']
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 'zebra':
                list = ['bird', 'elephant', 'monkey', 'zebra', 'fish']
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 'zebra':
                list = ['bird', 'elephant', 'horse', 'zebra', 'fish', 'monkey']
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))
            elif value == 'zebra':
                list = ['bear', 'elephant', 'bird', 'zebra', 'fish', 'monkey', 'horse']
                for i in range(h.heap.length()):
                    self.assertEqual(list[i], h.heap.get_at_index(i))

    def test_3(self):
        """
        get_min() example #1
        """
        h = MinHeap(['fish', 'bird'])
        list = ['bird', 'fish']
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual('bird', h.get_min())
        self.assertEqual('bird', h.get_min())

    def test_4(self):
        """
        remove_min() example #1
        """
        h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
        list = [1, 3, 2, 5, 6, 8, 4, 10, 7, 9]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(1, h.remove_min())
        list = [2, 3, 4, 5, 6, 8, 9, 10, 7]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(2, h.remove_min())
        list = [3, 5, 4, 7, 6, 8, 9, 10]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(3, h.remove_min())
        list = [4, 5, 8, 7, 6, 10, 9]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(4, h.remove_min())
        list = [5, 6, 8, 7, 9, 10]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(5, h.remove_min())
        list = [6, 7, 8, 10, 9]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(6, h.remove_min())
        list = [7, 9, 8, 10]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(7, h.remove_min())
        list = [8, 9, 10]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(8, h.remove_min())
        list = [9, 10]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(9, h.remove_min())
        list = [10]
        for i in range(h.heap.length()):
            self.assertEqual(list[i], h.heap.get_at_index(i))
        self.assertEqual(10, h.remove_min())

    def test_5(self):
        """
        build_heap() example #1
        """
        da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
        h = MinHeap(['zebra', 'apple'])

        list_0 = ['apple', 'zebra']
        for i in range(h.heap.length()):
            self.assertEqual(list_0[i], h.heap.get_at_index(i))

        h.build_heap(da)
        list_0 = [6, 20, 100, 200, 90, 150, 300]
        for i in range(h.heap.length()):
            self.assertEqual(list_0[i], h.heap.get_at_index(i))

        da.set_at_index(0, 500)
        list_0 = [500, 20, 6, 200, 90, 150, 300]
        for i in range(da.length()):
            self.assertEqual(list_0[i], da.get_at_index(i))

        list_0 = [6, 20, 100, 200, 90, 150, 300]
        for i in range(h.heap.length()):
            self.assertEqual(list_0[i], h.heap.get_at_index(i))

        h.build_heap(da)
        list_0 = [6, 20, 150, 200, 90, 500, 300]
        for i in range(h.heap.length()):
            self.assertEqual(list_0[i], h.heap.get_at_index(i))

if __name__ == '__main__':
    unittest.main()