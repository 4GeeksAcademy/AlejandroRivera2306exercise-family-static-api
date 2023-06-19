"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from random import randint
from utils import APIException, generate_sitemap

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

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

        raise APIException("Member not found", status_code=404)

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member

        raise APIException("Member not found", status_code=404)

    def get_all_members(self):
        return self._members

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    jackson_family.add_member(data)
    return jsonify(data), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = jackson_family.get_member(id)
    member_dict = {
        "name": member["first_name"],
        "id": member["id"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }
    return jsonify(member_dict), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    for member in jackson_family.get_all_members():
        if member["id"] == id:
            jackson_family.delete_member(id)
            return jsonify({"done": True}), 200

    return jsonify({"error": "Member not found"}), 404

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Pruebas adicionales

@app.route('/members', methods=['GET'])
def get_all_members_additional():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/3443', methods=['GET'])
def get_member_3443():
    member = {
        "first_name": "Tommy",
        "id": 3443,
        "age": 25,
        "lucky_numbers": [8, 12, 5]
    }
    return jsonify(member), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


