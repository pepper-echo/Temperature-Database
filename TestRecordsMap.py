import unittest, random
from RecordsMap import LocalRecord, RecordsMap

class TestLocalRecord(unittest.TestCase):
    def test_init(self):
        """Checks if the record was initialized correctly"""
        # initialized w/ position and max/min/precision
        p1 = LocalRecord((random.uniform(-90,90), random.uniform(-180,180)), 130, 30, 4)
        self.assertGreaterEqual(p1.pos, (-90, -180)) 
        self.assertLessEqual(p1.pos, (90, 180)) 
        self.assertEqual(p1.max, 130)
        self.assertEqual(p1.min, 30)
        self.assertEqual(p1.precision, 4)

        # initialized only w/ position
        p2 = LocalRecord((random.uniform(-90,90), random.uniform(-180,180)))
        self.assertGreaterEqual(p2.pos, (-90, -180)) 
        self.assertLessEqual(p2.pos, (90, 180)) 
        self.assertEqual(p2.max, None)
        self.assertEqual(p2.min, None)
        self.assertEqual(p2.precision, 0)

    def test_hash(self):
        """checks if the hash method returns a hash based on a record's position"""
        p1 = LocalRecord((random.uniform(-90,90), random.uniform(-180,180)))
        self.assertEqual(hash(p1), hash(p1.pos)) # make sure the hash method is taking the hash of the positions

    def test_eq(self):
        """checks if 2 records are for the same position"""
        p1 = LocalRecord((random.uniform(-90,-1), random.uniform(-180,-1))) # only negative latitudes and longitudes
        p2 = p1 
        p3 = LocalRecord((random.uniform(0,90), random.uniform(0,180))) # only positive latitudes and longitudes
        self.assertTrue(p1.__eq__(p2)) # p1 == p2
        self.assertFalse(p1.__eq__(p3)) # p1 != p3

    def test_add_report(self):
        """Checks if the min/max were updated properly"""
        p1 = LocalRecord((random.uniform(-90,90), random.uniform(-180,180)))
        p2 = LocalRecord(p1.pos)
        p3 = LocalRecord(p1.pos)
        # Checks if the base initialized values can get updated properly
        p1.add_report(90)
        p2.add_report(90)
        p3.add_report(30)
            # p1 == p2 
        self.assertEqual(p1.max, p2.max)
        self.assertEqual(p1.min, p2.min)
            # p1 != p3 
        self.assertNotEqual(p1.max, p3.max)
        self.assertNotEqual(p1.min, p3.min)

        # Checks if the updated values are correct with established max/min temps
        p4 = LocalRecord((random.uniform(-90,90), random.uniform(-180,180), 120, -20))
        p4.add_report(300)
        self.assertEqual(p4.max, 300)
        p4.add_report(-30)
        self.assertEqual(p4.min, -30)
        

class TestRecordsMap(unittest.TestCase):
    def test_add_one_report(self):
        """Tests whether a max/min temperature is correctly updated for a specific location. Remember to test len, get, contains, and add_report"""
        rm = RecordsMap()
        
        # Test len
        self.assertEqual(rm.__len__(), 0)
        # Test add_report
        p1 = (random.uniform(-90,90), random.uniform(-180,180)) # random latitude-longitude -- (tuple)
        t1 = random.uniform(-128,134) # random temperature to (potentially) update records -- (float)
        t2 = -150
        t3 = 150
        rm.add_report(p1, t1)
        # Test len
        self.assertEqual(rm.__len__(), 1)
        # Test get
        self.assertEqual(rm.__getitem__(p1), (t1, t1))
        # Test contains
        self.assertTrue(rm.__contains__(p1))

        # Test functionality of add_report's updates
        rm.add_report(p1, t2)
        rm.add_report(p1, t3)
        # Test get
        self.assertEqual(rm.__getitem__(p1), (t2, t3))
        
        
        

    def test_add_many_reports(self):
        """Tests whether the max/min temperature is correctly updated for a multitude of locations. Remember to test len, get, contains, and add_report"""
        rm = RecordsMap()
        # points and temperatures
        p1 = (random.uniform(-90,90), random.uniform(-180,180)) # The min and max latitude and longitude values
        p2 = (random.uniform(-90,90), random.uniform(-180,180))
        p3 = (random.uniform(-90,90), random.uniform(-180,180))
        t1 = random.uniform(-128,134) # currently the lowest and highest temperatures recorded worldwide
        t2 = random.uniform(-128,134)
        t3 = random.uniform(-128,134)
        t4 = -150 # arbitrary point that demonstrates updating the min temperature of a record 
        t5 = 150 # arbitrary point that demonstrates updating the max temperature of a record 

        # Test add_reports
        rm.add_report(p1, t1)
        rm.add_report(p2, t2)
        rm.add_report(p3, t3)
        # Test len
        self.assertEqual(len(rm), 3)
        # Test get
        self.assertEqual(rm[p1], (t1, t1))
        self.assertEqual(rm[p2], (t2, t2))
        self.assertEqual(rm[p3], (t3, t3))
        # Test contains
        self.assertTrue(p1 in rm)
        self.assertTrue(p3 in rm)

        # Test the functionality of updating records 
        rm.add_report(p1, t4)
        rm.add_report(p1, t5)
        # Test len
        self.assertEqual(len(rm), 3)
        # Test get
        self.assertEqual(rm[p1], (t4, t5))
        
unittest.main()