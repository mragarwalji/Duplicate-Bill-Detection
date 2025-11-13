import hashlib
import datetime
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists("uploads"):
    os.makedirs("uploads")


# ---------- BILL CLASS ----------
class Bill:
    def __init__(self, amount, date, file_path):
        self.amount = amount
        self.date = date
        self.file_path = file_path
        self.hash = self._calculate_hash()

    def _calculate_hash(self):
        try:
            with open(self.file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None

    def to_dict(self):
        return {
            "amount": self.amount,
            "date": str(self.date),
            "hash": self.hash
        }


# --------- DUPLICATE FINDER ----------
class DuplicateBillFinder:
    def __init__(self):
        self.bill_hashes = set()

    def add_bill(self, amount, date_str, file_path):

        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        bill = Bill(amount, date, file_path)

        if bill.hash in self.bill_hashes:
            return False, bill.hash  # Duplicate

        self.bill_hashes.add(bill.hash)
        return True, bill.hash


finder = DuplicateBillFinder()


# --------- API ENDPOINT TO UPLOAD BILL ----------
@app.route("/upload", methods=["POST"])
def upload_bill():

    amount = request.form.get("amount")
    date = request.form.get("date")
    file = request.files.get("bill")

    if not amount or not date or not file:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    amount = int(amount)

    # Save uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Detect duplicate
    success, file_hash = finder.add_bill(amount, date, file_path)

    if success:
        return jsonify({
            "status": "success",
            "message": "Bill added successfully!",
            "hash": file_hash
        }), 200

    else:
        return jsonify({
            "status": "duplicate",
            "message": "Duplicate bill detected!",
            "hash": file_hash
        }), 200


# ---------- SERVE FRONTEND ----------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
    