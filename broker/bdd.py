from pymongo import MongoClient, cursor
from dotenv import load_dotenv
import os
import datetime

load_dotenv()


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = os.getenv('IDBDD')

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client


client = get_database()

db = client.get_database("surikatt")
appareils = db.get_collection("appareils")
evenements = db.get_collection("evenements")

utilisateurs = db.get_collection("utilisateurs")


def check_apppareil(id):
    return appareils.find_one({'id_appareil': id})


def check_idcarte(idcarte):
    idcarte = idcarte.strip()
    print(f"Check: \"{idcarte}\"")
    return utilisateurs.find_one({'cartes': {
        '$in': [idcarte]
    }})


def recuperer_appareils() -> list:
    return list(appareils.find({}, {"_id": 0}))


def ajout_evenement(id_appareil: str, type: str):
    item_1 = {
        "id_appareil": id_appareil,
        "type": type,
        "date": datetime.datetime.now()
    }
    evenements.insert_one(item_1)


def ajout_utilisateurs(nom_utilisateur: str, ):
    utilisateurs.insert_one({"nom": nom_utilisateur})


def maj_status(id_appareil: str, est_connecte: bool):
    appareils.update_one({"id_appareil": id_appareil}, {
                         "$set": {"connecte": est_connecte}})


def ajout_carte(id_utilisateur: str, idcarte: str):
    utilisateurs.update_one({"_id": id_utilisateur}, {
                            "$push": {"cartes": idcarte}})


def alarme_etat(id_appareil: str, sonne: bool):
    appareils.update_one({"id_appareil": id_appareil},
                         {"$set": {"etat": sonne}})


def recuperer_evenements() -> list:
    return list(evenements.find({}, {"_id": 0}))
