# Course: CS261 - Data Structures
# Student Name: Donald Logan Kiser
# Assignment: A5P1 hash_map UNIT TESTING
# Description: unit tests for hash_map.py

import unittest
from hash_map import HashMap, hash_function_1, hash_function_2

class hashMapTests(unittest.TestCase):
    """
    definte unit tests for hash_map.py
    """
    def test_1(self):
        """
        empty_buckets() example #1
        """
        m = HashMap(100, hash_function_1)
        self.assertEqual(100, m.capacity)
        self.assertEqual(0, m.size)
        self.assertEqual(100, m.empty_buckets())
        m.put('key1', 10)
        self.assertEqual(100, m.capacity)
        self.assertEqual(1, m.size)
        self.assertEqual(99, m.empty_buckets())
        m.put('key2', 20)
        self.assertEqual(100, m.capacity)
        self.assertEqual(2, m.size)
        self.assertEqual(98, m.empty_buckets())
        m.put('key1', 30)
        self.assertEqual(100, m.capacity)
        self.assertEqual(2, m.size)
        self.assertEqual(98, m.empty_buckets())
        m.put('key4', 40)
        self.assertEqual(100, m.capacity)
        self.assertEqual(3, m.size)
        self.assertEqual(97, m.empty_buckets())

    def test_2(self):
        """
        empty_buckets() example #2
        """
        m = HashMap(50, hash_function_1)
        for i in range(150):
            m.put('key' + str(i), i * 100)
            if i % 30 == 0:
                self.assertEqual(50, m.capacity)
                self.assertEqual(i + 1, m.size)
                if i == 0:
                    self.assertEqual(49, m.empty_buckets())
                elif i == 30:
                    self.assertEqual(39, m.empty_buckets())
                elif i == 60:
                    self.assertEqual(36, m.empty_buckets())
                elif i == 90:
                    self.assertEqual(33, m.empty_buckets())
                elif i == 120:
                    self.assertEqual(30, m.empty_buckets())

    def test_3(self):
        """
        table_load() example #1
        """
        m = HashMap(100, hash_function_1)
        self.assertAlmostEqual(0, m.table_load(), 4)
        m.put('key1', 10)
        self.assertAlmostEqual(0.01, m.table_load(), 4)
        m.put('key2', 20)
        self.assertAlmostEqual(0.02, m.table_load(), 4)
        m.put('key1', 30)
        self.assertAlmostEqual(0.02, m.table_load(), 4)

    def test_4(self):
        """
        table_load() example #2
        """
        m = HashMap(50, hash_function_1)
        for i in range(50):
            m.put('key' + str(i), i * 100)
            if i % 10 == 0:
                if i == 0:
                    self.assertEqual(1, m.size)
                    self.assertEqual(50, m.capacity)
                    self.assertAlmostEqual(0.02, m.table_load(), 4)
                elif i == 10:
                    self.assertEqual(11, m.size)
                    self.assertEqual(50, m.capacity)
                    self.assertAlmostEqual(0.22, m.table_load(), 4)
                elif i == 20:
                    self.assertEqual(21, m.size)
                    self.assertEqual(50, m.capacity)
                    self.assertAlmostEqual(0.42, m.table_load(), 4)
                elif i == 30:
                    self.assertEqual(31, m.size)
                    self.assertEqual(50, m.capacity)
                    self.assertAlmostEqual(0.62, m.table_load(), 4)
                elif i == 40:
                    self.assertEqual(41, m.size)
                    self.assertEqual(50, m.capacity)
                    self.assertAlmostEqual(0.82, m.table_load(), 4)

    def test_5(self):
        """
        clear() example #1
        """
        m = HashMap(100, hash_function_1)
        self.assertEqual(0, m.size)
        self.assertEqual(100, m.capacity)
        m.put('key1', 10)
        m.put('key2', 20)
        m.put('key1', 30)
        self.assertEqual(2, m.size)
        self.assertEqual(100, m.capacity)
        m.clear()
        self.assertEqual(0, m.size)
        self.assertEqual(100, m.capacity)

    def test_6(self):
        """
        clear() example #2
        """
        m = HashMap(50, hash_function_1)
        self.assertEqual(0, m.size)
        self.assertEqual(50, m.capacity)
        m.put('key1', 10)
        self.assertEqual(1, m.size)
        self.assertEqual(50, m.capacity)
        m.put('key2', 20)
        self.assertEqual(2, m.size)
        self.assertEqual(50, m.capacity)
        m.resize_table(100)
        self.assertEqual(2, m.size)
        self.assertEqual(100, m.capacity)
        m.clear()
        self.assertEqual(0, m.size)
        self.assertEqual(100, m.capacity)

    def test_7(self):
        """
        put() example #1
        """
        m = HashMap(50, hash_function_1)
        for i in range(150):
            m.put('str' + str(i), i * 100)
            if i % 25 == 24:
                if i == 24:
                    self.assertEqual(39, m.empty_buckets())
                    self.assertAlmostEqual(0.5, m.table_load(), 4)
                    self.assertEqual(25, m.size)
                    self.assertEqual(50, m.capacity)
                elif i == 49:
                    self.assertEqual(37, m.empty_buckets())
                    self.assertAlmostEqual(1.0, m.table_load(), 4)
                    self.assertEqual(50, m.size)
                    self.assertEqual(50, m.capacity)
                elif i == 74:
                    self.assertEqual(35, m.empty_buckets())
                    self.assertAlmostEqual(1.5, m.table_load(), 4)
                    self.assertEqual(75, m.size)
                    self.assertEqual(50, m.capacity)
                elif i == 99:
                    self.assertEqual(32, m.empty_buckets())
                    self.assertAlmostEqual(2.0, m.table_load(), 4)
                    self.assertEqual(100, m.size)
                    self.assertEqual(50, m.capacity)
                elif i == 124:
                    self.assertEqual(30, m.empty_buckets())
                    self.assertAlmostEqual(2.5, m.table_load(), 4)
                    self.assertEqual(125, m.size)
                    self.assertEqual(50, m.capacity)
                elif i == 149:
                    self.assertEqual(30, m.empty_buckets())
                    self.assertAlmostEqual(3.0, m.table_load(), 4)
                    self.assertEqual(150, m.size)
                    self.assertEqual(50, m.capacity)

    def test_8(self):
        """
        put() example #2
        """
        m = HashMap(40, hash_function_2)
        for i in range(50):
            m.put('str' + str(i // 3), i * 100)
            if i % 10 == 9:
                if i == 9:
                    self.assertEqual(36, m.empty_buckets())
                    self.assertAlmostEqual(0.1, m.table_load(), 4)
                    self.assertEqual(4, m.size)
                    self.assertEqual(40, m.capacity)
                elif i == 19:
                    self.assertEqual(33, m.empty_buckets())
                    self.assertAlmostEqual(0.175, m.table_load(), 4)
                    self.assertEqual(7, m.size)
                    self.assertEqual(40, m.capacity)
                elif i == 29:
                    self.assertEqual(30, m.empty_buckets())
                    self.assertAlmostEqual(0.25, m.table_load(), 4)
                    self.assertEqual(10, m.size)
                    self.assertEqual(40, m.capacity)
                elif i == 39:
                    self.assertEqual(27, m.empty_buckets())
                    self.assertAlmostEqual(0.35, m.table_load(), 4)
                    self.assertEqual(14, m.size)
                    self.assertEqual(40, m.capacity)
                elif i == 49:
                    self.assertEqual(25, m.empty_buckets())
                    self.assertAlmostEqual(0.425, m.table_load(), 4)
                    self.assertEqual(17, m.size)
                    self.assertEqual(40, m.capacity)

    def test_9(self):
        """
        contains_key() example #1
        """
        m = HashMap(10, hash_function_1)
        self.assertFalse(m.contains_key('key1'))
        m.put('key1', 10)
        m.put('key2', 20)
        m.put('key3', 30)
        self.assertTrue(m.contains_key('key1'))
        self.assertFalse(m.contains_key('key4'))
        self.assertTrue(m.contains_key('key2'))
        self.assertTrue(m.contains_key('key3'))
        m.remove('key3')
        self.assertFalse(m.contains_key('key3'))

    def test_10(self):
        """
        contains_key() example #2
        """
        m = HashMap(75, hash_function_2)
        keys = [i for i in range(1, 1000, 20)]
        for key in keys:
            m.put(str(key), key * 42)
        self.assertEqual(50, m.size)
        self.assertEqual(75, m.capacity)
        result = True
        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        self.assertTrue(result)

    def test_11(self):
        """
        get() example #1
        """
        m = HashMap(30, hash_function_1)
        self.assertIsNone(m.get('key'))
        m.put('key1', 10)
        self.assertEqual(10, m.get('key1'))

    def test_12(self):
        """
        get() example #2
        """
        m = HashMap(150, hash_function_2)
        for i in range(200, 300, 7):
            m.put(str(i), i * 10)
        self.assertEqual(15, m.size)
        self.assertEqual(150, m.capacity)
        for i in range(200, 300, 21):
            if i == 200:
                self.assertEqual(2000, m.get(str(i)))
                self.assertTrue(m.get(str(i)) == i * 10)
                self.assertIsNone(m.get(str(i + 1)))
                self.assertFalse(m.get(str(i + 1)) == (i + 1) * 10)
            elif i == 221:
                self.assertEqual(2210, m.get(str(i)))
                self.assertTrue(m.get(str(i)) == i * 10)
                self.assertIsNone(m.get(str(i + 1)))
                self.assertFalse(m.get(str(i + 1)) == (i + 1) * 10)
            elif i == 242:
                self.assertEqual(2420, m.get(str(i)))
                self.assertTrue(m.get(str(i)) == i * 10)
                self.assertIsNone(m.get(str(i + 1)))
                self.assertFalse(m.get(str(i + 1)) == (i + 1) * 10)
            elif i == 263:
                self.assertEqual(2630, m.get(str(i)))
                self.assertTrue(m.get(str(i)) == i * 10)
                self.assertIsNone(m.get(str(i + 1)))
                self.assertFalse(m.get(str(i + 1)) == (i + 1) * 10)
            elif i == 284:
                self.assertEqual(2840, m.get(str(i)))
                self.assertTrue(m.get(str(i)) == i * 10)
                self.assertIsNone(m.get(str(i + 1)))
                self.assertFalse(m.get(str(i + 1)) == (i + 1) * 10)

    def test_13(self):
        """
        remove() example #1
        """
        m = HashMap(50, hash_function_1)
        self.assertIsNone(m.get('key1'))
        m.put('key1', 10)
        self.assertEqual(10, m.get('key1'))
        m.remove('key1')
        self.assertIsNone(m.get('key1'))
        m.remove('key4')

    def test_14(self):
        """
        resize() example #1
        """
        m = HashMap(20, hash_function_1)
        m.put('key1', 10)
        self.assertEqual(1, m.size)
        self.assertEqual(20, m.capacity)
        self.assertEqual(10, m.get('key1'))
        self.assertTrue(m.contains_key('key1'))
        m.resize_table(30)
        self.assertEqual(1, m.size)
        self.assertEqual(30, m.capacity)
        self.assertEqual(10, m.get('key1'))
        self.assertTrue(m.contains_key('key1'))

    def test_15(self):
        """
        resize() example #2
        """
        m = HashMap(75, hash_function_2)
        keys = [i for i in range(1, 1000, 13)]
        for key in keys:
            m.put(str(key), key * 42)
        self.assertEqual(77, m.size)
        self.assertEqual(75, m.capacity)

        for capacity in range(111, 1000, 117):
            m.resize_table(capacity)

            m.put('some key', 'some value')
            result = m.contains_key('some key')
            m.remove('some key')

            for key in keys:
                result &= m.contains_key(str(key))
                result &= not m.contains_key(str(key + 1))
            # print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
            if capacity == 111:
                self.assertEqual(111, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(111, m.capacity)
                self.assertEqual(0.69, round(m.table_load(), 2))
            elif capacity == 228:
                self.assertEqual(228, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(228, m.capacity)
                self.assertEqual(0.34, round(m.table_load(), 2))
            elif capacity == 345:
                self.assertEqual(345, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(345, m.capacity)
                self.assertEqual(0.22, round(m.table_load(), 2))
            elif capacity == 462:
                self.assertEqual(462, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(462, m.capacity)
                self.assertEqual(0.17, round(m.table_load(), 2))
            elif capacity == 579:
                self.assertEqual(579, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(579, m.capacity)
                self.assertEqual(0.13, round(m.table_load(), 2))
            elif capacity == 696:
                self.assertEqual(696, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(696, m.capacity)
                self.assertEqual(0.11, round(m.table_load(), 2))
            elif capacity == 813:
                self.assertEqual(813, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(813, m.capacity)
                self.assertEqual(0.09, round(m.table_load(), 2))
            elif capacity == 930:
                self.assertEqual(930, capacity)
                self.assertTrue(result)
                self.assertEqual(77, m.size)
                self.assertEqual(930, m.capacity)
                self.assertEqual(0.08, round(m.table_load(), 2))

    def test_16(self):
        """
        get_keys() example #1
        """
        m = HashMap(10, hash_function_2)
        for i in range(100, 200, 10):
            m.put(str(i), str(i * 10))

        list_0 = ['160', '110', '170', '120', '180', '130', '190', '140', '150', '100']
        da_0 = m.get_keys()
        for i in range(da_0.length()):
            self.assertEqual(list_0[i], da_0.get_at_index(i))

        m.resize_table(1)
        list_1 = ['100', '150', '140', '190', '130', '180', '120', '170', '110', '160']
        da_1 = m.get_keys()
        for i in range(da_1.length()):
            self.assertEqual(list_1[i], da_1.get_at_index(i))

        m.put('200', '2000')
        m.remove('100')
        m.resize_table(2)
        list_2 = ['200', '160', '110', '170', '120', '180', '130', '190', '140', '150']
        da_2 = m.get_keys()
        for i in range(da_2.length()):
            self.assertEqual(list_2[i], da_2.get_at_index(i))


if __name__ == '__main__':
    unittest.main()