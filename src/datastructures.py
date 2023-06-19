
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [
            {
                "first_name": "John",
                "id": self._generateId(),
                "age": 36,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "first_name": "Jane",
                "id": self._generateId(),
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "first_name": "Jimmy",
                "id": self._generateId(),
                "age": 8,
                "lucky_numbers": [1]
            }
        ]

    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member["id"] = self._generateId()
        self._members.append(member)

    def delete_member(self, id):
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return

        raise Exception("Member not found")

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member

        raise Exception("Member not found")

    def get_all_members(self):
        return self._members

app = FamilyStructure("Doe")
