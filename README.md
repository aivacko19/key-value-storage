# key-value-storage

A redis-like storage implemented in Python

## Step 1

__Command__         | __Description__
--                  | --
GET \<key>          | Get value for specified key
SET \<key> \<value> | Add key-value entry
UNSET \<key>        | Remove key-value entry
NUMEQUALTO \<value> | Get number of entries with specified value
END                 | Exit program

Each command is implemented as a class which inherits class Command and implement `def run(self, *args)` method. If there are any fixed arguments inside the 'run' method, they will be considered required and the system will print a proper message in case they are missing from the input.

Chosen structure for the storage is a hash table (python dict) since the complexity for inserting, lookup and removal are O(1), and the commands supported will not require to have sorted values or to traverse the values. 

On the other hand, command NUMEQUALTO needs to know the total number of a specific value. In order to avoid traversing all values and counting them we need to keep a structure (hash table) that will maintain a number for each value the storage contains and allow NUMEQUALTO to have prepared number for each value with complexity of O(1). This will require additional operations inside insert (SET) and remove (UNSET) commands, nevertheless they will remain O(1).

Storage encapsulates the two structures we described and contains methods for the above actions.

## Step 2

__Command__ | __Description__
--          | --
BEGIN       | Start transaction
COMMIT      | Preserve changes
ROLLBACK    | Reset changes

Next version of the system contains additional commands for transaction management. The changes required to change the structure of our initial version of the system. Namely, we created two different Managers (BaseManager, TransactionManager), one for each state of the storage. We suppose that before starting a transaction the system will behave same as it was described initially, so this behaviour will be handeled by the BaseManager. When a transaction starts, BaseManager is replaced by TransactionManager which will handle the additional behaviour. We also suppose that starting the transaction after it has already been started will have no effect.

TransactionManager inherits BaseManager and it has additional structures: a stage and a unset tracker, that help with change tracking. Stage will contain all entries that are either new or need to replace old ones, and the unset tracker will track which entries need to be deleted. There is also a stage value counter that will contain the difference between staging and actual counter so it can sum them up when fetching the NUMEQUALTO during transaction.

When the transaction commit, the data from the stage will be entered in the actuall storage and the entries in the unset tracker will be removed from it. Then TransactionManager will be replaced again with the BaseManager. In case of rollback, TransactionManager will just be imidiatelly replaced without saving any changes.

The Big-O of the actions during the transaction will remain the same as it was, although it will have more overhead due to additional checks. However, COMMIT will have complexity of O(n) since it is traversing the stage and unset tracker and updating each entry individually.

Note: Design of the code is influenced by OO paradigm due to experience of working with Java, and it might not be to a high degree Pythonic :)
