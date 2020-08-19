import csv

from Package import Package


class Hash:

    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    # Big O Notation -> Constant O(1)
    # hash function to get bucket number for key
    # function subtracts 1 from package number to obtain bucket (package ids unique and no collision)
    def hash_func(self, key):
        bucket_num = int(key) - 1
        return bucket_num

    # Big O Notation -> Linear O(N)
    def insert_into_table(self, package_id, package):
        """
        Insert package into hash table based on key
            'bucket_num' for [package id, package] is determined using the hash function using the package_id as the key
                - hash_func()
            Due to the use of dictionaries being prohibited the hash table is implemented with a 2D list. The outer list
                represent's the hash table's buckets and the inner is the package_id and package stored together
                as a 'key-value' pair
            *Package_id (key) is stored with package in the event that a package collision occurs and the correct key needs
                to be used to retrieve package (Not needed for this iteration of the solution due to the absence of collisions but
                it is implemented to so that additional hash table functionality can be easy built on top of current solution)
            If package's 'bucket_number' + 1 > size of hash table then the hash table needs to resized because there is no
                bucket for the package to be stored
                New size is 'bucket_number' + 1 because the hash function stores the package at index which is equal to
                package_id - 1
                ex. id 25 at index/bucket 24 , id 40 at index/bucket 39
                To store package with id 41 the package needs to be stored at index 40. The list has index values of 0-39
                so the table needs to resized to 41 (40(bucket_number) + 1) which has index values of 0-40 to create bucket
            *Hash table is able to self_adjust (increase in size) by creating a new list with the size set to be able to add
                the package without collision to the bucket_number assigned from the hash function - hash_func()
        """
        bucket_num = self.hash_func(int(package_id))
        key = package_id
        value = package
        key_value_pair = [key, value]

        if bucket_num + 1 > len(self.table):

            # create new hash table with a a size that allows for package to be stored at bucket_number from hash_func()
            new_size = bucket_num + 1
            new_table = [None] * new_size

            for x in range(len(self.table)):
                item = self.table[x]
                index = x
                new_table[index] = item

            # set hash class table to the new table
            self.table = new_table

        self.table[bucket_num] = key_value_pair

    # Big O Notation -> Constant O(1)
    # get package based on key value
    # use hash_func to retrieve package from hash table
    def get_from_table(self, key):
        location_in_list = self.hash_func(key)
        return self.table[location_in_list][1]

    # Big O Notation -> Quadratic O(N^2)
    # read package file, create package and insert into hash table
    def create_package_list(self, filename):
        with open(filename) as p_file:
            reader = csv.reader(p_file)

            for row in reader:
                package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                self.insert_into_table(int(package.ID), package)



