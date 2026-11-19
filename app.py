 
from flask import Flask, jsonify, request
class NumberStore:

    def __init__(self):
        self._numbers = []
    def reset(self):
        self._numbers.clear()
    def add(self, number):
        if (not isinstance(number, int) or isinstance (number,bool)):
            raise TypeError("Csak egesz szam adhato meg")
        else:
            self._numbers.append(number)
    def total(self):
        return sum(self._numbers)

def create_app():
    app=Flask(__name__)
    store=NumberStore()
    @app.post("/numbers")
    def add_number():
         data = request.get_json(silent=True)
         if not isinstance(data, dict) or "number" not in data:
             return jsonify({"error": "Hiányzó 'number' mező."}), 400
         try:
             store.add(data["number"])
         except TypeError as exc:
            return jsonify({"error": str(exc)}), 400
         return jsonify({"number": data["number"]}), 201
    @app.get("/sum")
    def get_sum():
        return jsonify({"sum": store.total()}), 200
    @app.post("/reset")
    def reset():
        store.reset()
        return jsonify({"message": "A tároló kiürítve."}), 200
    return app

    
if __name__ == "__main__":
    create_app().run(debug=True)
