from flask import request, jsonify
from config import app, db
from models import Contact





@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))#With a lambda function we map each object to its json representation
    return jsonify({"contacts": json_contacts})#Mettiamo tutto in un pyhton dictionary e lo restituiamo come json usando il comando jsonify


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
                  jsonify({"Message": "ou must include a first name, a last name and an email"})
                , 400                       
                )
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)

    try:
        db.session.add(new_contact)
        db.session.commit()

    except Exception as e:
        return (jsonify({"message":str(e)}), 400)
    
    return (jsonify({"messagee": "User created"}), 201)

@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return (jsonify({"message":"User not found"}), 404)

    data = request.json

    contact.first_name = data.get("firstName", contact.first_name)#La get con questa sintassi restituisce o quello che cerchiamo o quello che abbiamo passato come default, è di fatto una getOrDefault in java
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "Usr updated"}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message":"User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message":"User deleted"}), 200

'''
Queste due righe di codice servono a runnare l'app 
solo se si esegue il file main.py, 
quando in python infatti si importa qualcosa
il viene eseguito, se importassimo main da qualche parte
con queste due righe di codice evitiamo che parta l'app'''

if __name__ == "__main__": ##Queste due righe di codice servono a runnare l'app solo se si esegue il file main.py, quando in python infatti si impor
    
    with app.app_context():
        db.create_all()#If not created create the db model classes
    
    app.run(debug=True)
