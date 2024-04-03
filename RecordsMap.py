class LocalRecord:
    def __init__(self, pos, max=None, min=None, precision = 0): 
        """initalizes a local record with pos/max/min/precision"""
        lat = round(pos[0], precision)
        long = round(pos[1], precision)
        self.pos = (lat, long)
        self.max = max
        self.min = min
        self.precision = precision

    def add_report(self, temp): 
        """updates the max/min temperature"""
        if self.max == None:
            self.max = temp

        if self.min == None:
            self.min = temp

        elif self.max < temp:
            self.max = temp

        elif self.min > temp:
            self.min = temp

    def __eq__(self, other): 
        """checks the positional equality of the record"""
        if self.pos == other.pos:
            return True
        else:
            return False

    def __hash__(self): 
        """creates a hash value for the record based on its position"""
        return (hash(self.pos))

    def __repr__(self):
        """returns the record in an appropriate format"""
        return f"Record(pos={self.pos}, max={self.max}, min={self.min}"

class RecordsMap:
    def __init__(self): 
        """initializes an empty list of local records"""
        self._n_buckets = 9            
        self._len = 0                   
        self._L = [[] for i in range(self._n_buckets)]  

    def __len__(self): 
        """the number of key:value pairs stored in recordmaps"""
        return self._len
    
    def find_bucket(self, pos):
        """returns the bucket location (index) in which a hashed position should go"""
        return hash(pos) % self._n_buckets

    def add_report(self, pos, temp): 
        """updates max and min temps for given pos. 2 inputs --> pos tuple, and float"""
        check_rec = LocalRecord(pos)
        index = self.find_bucket(pos)
        
        if pos in self:
            for record in self._L[index]:
                if record == check_rec:
                    record.add_report(temp)

        else:
            new_record = LocalRecord(pos, temp, temp)
            self._L[index].append(new_record)
            self._len += 1

        if (len(self) >= self._n_buckets*2):
            self._rehash(self._n_buckets*2)

    def __getitem__(self, pos): 
        """returns (min, max) temps at position: pos. Raise keyerror if not in mapping"""
        index = self.find_bucket(pos)
        re = LocalRecord(pos)

        for record in self._L[index]:
            if record == re:
                return (record.min, record.max)
        raise KeyError (f"No records for position: {pos}.")
  
    def __contains__(self, pos):
        """returns true or false depending on whether the key is in recordmaps"""
        index = self.find_bucket(pos)

        record = LocalRecord(pos)

        if record in self._L[index]:
            return True
        return False

    def _rehash(self, m_new): 
        """rehash to optimize code by creating new buckets as to not 'overflow' each bucket when there is an influx in entries"""
        self._n_buckets = m_new
        new_L = [[] for i in range(self._n_buckets)] 

        for bucket in self._L:
            for record in bucket:
                new_i = self.find_bucket(record)
                new_L[new_i].append(record)

        self._L = new_L
