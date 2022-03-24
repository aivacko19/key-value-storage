# key-value-storage

A redis-like storage implemented in Python

## Step 1

System contains following commands:
- GET \<key>
- SET \<key> \<value>
- UNSET \<key>
- NUMEQUALTO \<value>
- END

Each command is implemented as a class which inherits class Command and implement `def run(self, *args)` method. If there are any fixed arguments inside the 'run' method, they will be considered required and the system will print a proper message in case they are missing from the input.

Chosen structure for the storage is a hash table (python dict) since the complexity for inserting, lookup and removal are O(1), and the commands supported will not require to have sorted values or to traverse the values. 

On the other hand, command NUMEQUALTO needs to know the total number of a specific value. In order to avoid traversing all values and counting them we need to keep a structure (hash table) that will maintain a number for each value the storage contains and allow NUMEQUALTO to have prepared number for each value with complexity of O(1). This will require additional operations inside insert (SET) and remove (UNSET) commands, nevertheless they will remain O(1).

HashTableStorage encapsulates the two structures we described and contains methods for the above actions.
