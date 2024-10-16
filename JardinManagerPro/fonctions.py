# imports
import string
import random
import datetime
import math
import base64
import os
from geopy.geocoders import Nominatim
from flask import Flask, request, render_template, flash, redirect, session, url_for
from flask_session import Session
from PIL import Image
from datetime import datetime
#from sqlalchemy import bindparam
import sqlite3


#fonction permettant de se connecter à la base de donnée jardinnage
def connectdbjardin():

    db = sqlite3.connect('jardin.db')
    cursor = db.cursor()
    return db, cursor

#Profil

#fonction permettant de se connecter à la base de donnée
def connectDatabase():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    db = sqlite3.connect('profils.db')
    cursor = db.cursor()
    return db, cursor

#fonctions initialisant la base de donnée
def initDB():
    db, cursor = connectDatabase()
    cursor.execute('DROP TABLE IF EXISTS profils')
    
    query = '''
    CREATE TABLE profils 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pseudo TEXT,
        Mail TEXT,
        Mdp TEXT,
        Photo TEXT,
        Ville TEXT
    );
    
    '''
    
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

#LES DONNEES RECUPEREES DANS LA BASE DE DONNE SONT DE LA FORME SUIVANTE : data=[('donne1',),]
#C'EST UNE LISTE DE LISTE !!!!!
#ON A DONC data[0][0] = donne1
#fonction qui récupère l'id
def id_user(pseudo):
    query="""SELECT id FROM profils WHERE Pseudo LIKE ?;"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query,args)
    data = cursor.fetchall()
    db.close
    return int(data[0][0])


#fonction qui vérifie qu'une donnée est déjà dans la liste donnée en entrée
def verif_donnee(donnee,liste):
    for i in range(len(liste)):
        if donnee == liste[i][0]:
            return True
    return False


#fonction qui vérifie si c'est le bon mot de passe
def verif_mdp(pseudo,mdp):
    query = """SELECT Mdp FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    
    if data == []:
        return False
    elif data[0][0] == str(mdp):
        return True
    else :
        return False


#fonction qui vérifie si l'utilisateur a une photo de profil
def verif_photo(pseudo):
    query = """SELECT Photo FROM Profils WHERE Pseudo LIKE ?;"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query,args)
    data = cursor.fetchall()
    db.close()
    
    print(data[0][0])
    if data == []:
        return False
    elif data[0][0] == "1" :
        return True
    else :
        return False
    
    
#fonction gérant la connection
def fct_connection(pseudo, mdp):
    #on récupère la liste de pseudo
    query = """SELECT Pseudo FROM profils"""
    db, cursor = connectDatabase()
    cursor.execute(query)
    liste_pseudo = cursor.fetchall()
    db.close()
    
    #on récupère le mail, la ville, la photo et le mdp associés au pseudo donné en entrée
    query = """SELECT Mail, Mdp, Photo, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    
    #on vérifie que les champs ne sont pas vides
    if pseudo == ("""""") or mdp == ("""""") :
        flash("Veuillez compléter tous les champs !", "error")
        return redirect("/connection")
    
    #on vérifie que le pseudo est déjà dans la base de donnée
    elif verif_donnee(pseudo,liste_pseudo) == False :
        flash("Vous n'êtes pas encore inscrit ! Vérifiez votre pseudo ou inscrivez vous ci-dessous !", "error")
        return redirect("/connection")
    
    #on vérifie que c'est le bon mot de passe
    elif str(mdp) != data[0][1] :
        flash("Mauvais mot de passe !", "error")
        return redirect("/connection")
    
    else :
        session["name"] = pseudo
        flash("Connexion réussie !", "success")
        
        if "previous_url" in session:
            previous_url = session["previous_url"]
            session.pop("previous_url", None)
            if previous_url == "http://127.0.0.1:5454/inscription":
                return redirect("/profil")
            else :
                return redirect(previous_url)


#fonction gérant affichage profil une fois connecté
def fct_profil(pseudo):
    #récupération des données liées au pseudo donné en entrée
    query = """SELECT Mail, Mdp, Photo, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    #on regarde si l'utilisateur possède une photo de profil
    photo = verif_photo(pseudo)
    return render_template("profil.html", items = data, pseudo = pseudo, title="Profil", photo=photo)
    
    
#fonction gérant l'inscription
def fct_inscritpion(pseudo, mail, mdp, conf_mdp, ville):
    #on récupère les pseudos pour vérifier si l'adresse mail ou le pseudo existent déjà dans la database
    query = """SELECT Pseudo FROM Profils WHERE (Pseudo LIKE (?) OR Mail LIKE (?));"""
    args = [pseudo,mail]
    db, cursor = connectDatabase()
    cursor.execute(query,args)
    data = cursor.fetchall()
    db.close()
    
    #il ne faut pas qu'il y ait de pseudo lié au pseudo donné en entrée pour garantir l'unicité
    if data == [] :
        #il faut être sûr que l'utilisateur ne s'est pas trompé lorsqu'il a rentré son mot de passe
        if conf_mdp == mdp:
            #ici on insert une nouvelle ligne dans la base de donnée
            query = """INSERT INTO profils (Pseudo, Mail, Mdp, Photo, Ville) VALUES (?, ?, ?, ?, ?);"""
            args = (pseudo, mail, mdp, False, ville)
            db, cursor = connectDatabase()
            cursor.execute(query, args)
            db.commit()
            db.close()
            flash("Inscription réussie ! Veuillez vous connecter pour accéder à votre profil !", "success")
            return redirect("/connection")
            
        else :
            flash("Les deux mots de passe que vous avez rentrés ne sont pas identiques. Veuillez recommencer !", "error")
            return redirect("/inscription")
    
    else :
        flash("Le pseudo ou le mail que vous avez choisi est déjà utilisé par un autre utilisateur. Veuillez en choisir un nouveau !", "error")
        return redirect("/inscription")
    
    
# fonction pour changer de pseudo,...
def maj_db(pseudo, nouvelle_donnee, donnee_a_changer):
    #on différencie les cas suivant s'il faut changer le mail,...
    if donnee_a_changer == "Pseudo":
        #on récupère la liste des pseudos de la base de donnée afin de garantir l'unicité du nouveau pseudo
        query = """SELECT Pseudo FROM profils"""
        db, cursor = connectDatabase()
        cursor.execute(query)
        liste_pseudo = cursor.fetchall()
        db.close()

        if verif_donnee(nouvelle_donnee,liste_pseudo)==False:
            #mise à jour de la base de donnée
            session["name"] = nouvelle_donnee
            query = """UPDATE profils SET Pseudo = ? WHERE Pseudo LIKE ?;"""
            args = [nouvelle_donnee,pseudo]
            db, cursor = connectDatabase()
            cursor.execute(query,args)
            db.commit()
            db.close()
            flash("Changement de pseudo réussi !", "success")
            #on renomme la photo de profil pour la garder associée au compte si l'utilisateur en possède une :
            if verif_photo(nouvelle_donnee) == True :
                path = f"./static/image/photo_profil/{ pseudo }"
                new_name = f"./static/image/photo_profil/{ nouvelle_donnee }"
                os.rename(path, new_name)

            return redirect("/profil")
        
        else :
            flash("Ce pseudo est déjà utilisé par un autre utilisateur. Veuillez en choisir un autre !", "error")
            return redirect("/maj/pseudo")

    elif donnee_a_changer == "Mail":
        #idem que pour la liste de pseudo
        query = """SELECT Mail FROM profils"""
        db, cursor = connectDatabase()
        cursor.execute(query)
        liste_mail = cursor.fetchall()
        db.close()

        if verif_donnee(nouvelle_donnee,liste_mail) == False:
            #mise a jour de la base de donnée
            query = """UPDATE profils SET Mail = ? WHERE Pseudo LIKE ?;"""
            args = [nouvelle_donnee,pseudo]
            db, cursor = connectDatabase()
            cursor.execute(query,args)
            db.commit()
            db.close()
            flash("Changement de mail réussi !", "success")
            return redirect("/profil")
        
        else :
            flash("Ce mail est déjà utilisé par un autre utilisateur. Veuillez en choisir un autre !","error")
            return redirect("/maj/mail")

    elif donnee_a_changer == "Mdp":
        #mise a jour de la base de donnée
        query = """UPDATE profils SET Mdp = ? WHERE Pseudo LIKE ?;"""
        args = [nouvelle_donnee,pseudo]
        db, cursor = connectDatabase()
        cursor.execute(query,args)
        db.commit()
        db.close()
        flash("Changement de mot de passe réussi !", "success")
        return redirect("/profil")
    
    elif donnee_a_changer == "Ville" :
        #mise a jour de la base de donnée
        query = """UPDATE profils SET Ville = ? WHERE Pseudo LIKE ?;"""
        args = [nouvelle_donnee,pseudo]
        db, cursor = connectDatabase()
        cursor.execute(query,args)
        db.commit()
        db.close()
        flash("Changement de ville réussi !", "success")
        return redirect("/profil")
    
    else :
        #on regarde si l'utilisateur possède déjà une photo
        photo = verif_photo(pseudo)
        if photo == True :
            #on supprime l'ancienne photo
            image_path = f"./static/image/photo_profil/{ pseudo }"
            os.remove(image_path)
        #on ajoute la nouvelle photo à la place
        nouvelle_donnee.save(os.path.join('static/image/photo_profil', pseudo))
        query = """UPDATE profils SET Photo = ? WHERE PSeudo LIKE ?;"""
        args = [True,pseudo]
        db, cursor = connectDatabase()
        cursor.execute(query,args)
        db.commit()
        db.close()
        if photo == True :
            flash("Changement de photo de profil réussi !", "success")
        else :
            flash("Ajout d'une photo de profil réussi !", "success")
        return redirect("/profil")
    
    
# fonction gérant affichage profil public
def fct_profil_public(pseudo):
    #on récupère les données liées au pseudo
    query = """SELECT Mail, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    photo = verif_photo(pseudo)
    
    evenements = liste_evenements(pseudo)
    
    return render_template("profil_public.html", items = data, pseudo = pseudo, title=f"Profil de { pseudo }",photo=photo,evenements=evenements)
    
    
#base de donnéé forum

def connectdbforum():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    dbf = sqlite3.connect('forum.db')
    cursor = dbf.cursor()
    return dbf, cursor

def fct_creersujet(sujet,message,pseudo,date):
    query = """INSERT INTO forum (Sujet,Message,pseudo,date) VALUES (?,?,?,?);"""
    args = [sujet,message,pseudo,date]
    dbf, cursor = connectdbforum()
    cursor.execute(query,args)
    dbf.commit()
    dbf.close()
    return redirect ("/forum")

def fct_creerreponse(sujet,reponse,pseudo,date,message,pseudo1):
    query = """INSERT INTO reponse (Sujet,Reponse,pseudo,date,pseudo1) VALUES (?,?,?,?,?);"""
    args = [sujet,reponse,pseudo,date,pseudo1]
    dbf, cursor = connectdbforum()
    cursor.execute(query,args)
    dbf.commit()
    dbf.close()
    return redirect(url_for('reponsesujet',sujet=sujet,message=message,pseudo1=pseudo1,pseudo=pseudo))

def fct_creeroffre(annonce, prix, localisation, pseudo, date, image,description):
    image_data = image.read()
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    query = """INSERT INTO annonce (Annonce,Prix,Localisation,Pseudo,Date,Image,Description) VALUES (?,?,?,?,?,?,?);"""
    args = [annonce, prix, localisation, pseudo, date, image_b64,description]
    dbf, cursor = connectdbforum()
    cursor.execute(query, args)
    dbf.commit()
    dbf.close()
    
    return redirect(url_for('cabanon'))

def affichertableforum():
    query="""SELECT Sujet,Message,pseudo,date FROM forum;"""
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data=cursor.fetchall()
    dbf.close()

    return render_template("forum.html", listdb=data, title="Jardin Copain")

def affichertableannonce(pseudo):
    query = "SELECT Ville FROM profils WHERE Pseudo = ?"
    args=[pseudo]
    db,cursor=connectDatabase()
    cursor.execute(query,args)
    ville_utilisateur = cursor.fetchone()[0]
    db.close()

    # Récupération des coordonnées de la ville de l'utilisateur
    geolocator = Nominatim(user_agent="my_app")
    localisation = geolocator.geocode(ville_utilisateur)
    lat1, lon1 = localisation.latitude, localisation.longitude

    query = """ SELECT Localisation FROM annonce """
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data = cursor.fetchall()
    dbf.close()

    def distance_haversine(lat1, lon1, lat2, lon2):
        # Convertir les coordonnées en radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        # Calculer la différence entre les latitudes et longitudes
        dlat, dlon = lat2 - lat1, lon2 - lon1
        # Appliquer la formule de Haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        # Rayon de la Terre en kilomètres
        r = 6371
        return c * r

    distances = []
    for ville in data:
        ville_coords = geolocator.geocode(ville[0])
        distance = distance_haversine(localisation.latitude, localisation.longitude, ville_coords.latitude, ville_coords.longitude)
        distances.append(distance)

    #Mettre à jour la table annonce en insérant la distance associée à chaque annonce:
    for i in range(len(distances)):
        query = """ UPDATE annonce SET Distance = ? WHERE id = ?"""
        args = [distances[i], i+1]
        dbf,cursor=connectdbforum()
        cursor.execute(query, args)
        dbf.commit()
        dbf.close()

    # Calcul de la distance entre la ville de l'utilisateur et chaque annonce
    query = """ SELECT Annonce,Prix,Localisation,Pseudo,Date FROM annonce ORDER BY Distance ASC """
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data = cursor.fetchall()
    dbf.close()
    return render_template("cabanon.html", listdb=data, title = "Cabanon")


def affichertableannoncefiltre(prix_min,prix_max,pseudo):
    query = "SELECT Ville FROM profils WHERE Pseudo = ?"
    args=[pseudo]
    db,cursor=connectDatabase()
    cursor.execute(query,args)
    ville_utilisateur = cursor.fetchone()[0]
    db.close()

    # Récupération des coordonnées de la ville de l'utilisateur
    geolocator = Nominatim(user_agent="my_app")
    localisation = geolocator.geocode(ville_utilisateur)
    lat1, lon1 = localisation.latitude, localisation.longitude

    query = """ SELECT Localisation FROM annonce """
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data = cursor.fetchall()
    dbf.close()

    def distance_haversine(lat1, lon1, lat2, lon2):
        # Convertir les coordonnées en radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        # Calculer la différence entre les latitudes et longitudes
        dlat, dlon = lat2 - lat1, lon2 - lon1
        # Appliquer la formule de Haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        # Rayon de la Terre en kilomètres
        r = 6371
        return c * r

    distances = []
    for ville in data:
        ville_coords = geolocator.geocode(ville[0])
        distance = distance_haversine(localisation.latitude, localisation.longitude, ville_coords.latitude, ville_coords.longitude)
        distances.append(distance)

    #Mettre à jour la table annonce en insérant la distance associée à chaque annonce:
    for i in range(len(distances)):
        query = """ UPDATE annonce SET Distance = ? WHERE id = ?"""
        args = [distances[i], i+1]
        dbf,cursor=connectdbforum()
        cursor.execute(query, args)
        dbf.commit()
        dbf.close()

    # Calcul de la distance entre la ville de l'utilisateur et chaque annonce
    query = """ SELECT Annonce,Prix,Localisation,Pseudo,Date FROM annonce WHERE Prix > ? AND Prix < ? ORDER BY Distance ASC """
    args=[prix_min,prix_max]
    dbf,cursor=connectdbforum()
    cursor.execute(query,args)
    data = cursor.fetchall()
    dbf.close()

    return render_template("cabanon.html", listdb=data,prix_min=prix_min,prix_max=prix_max, title = "Cabanon")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#def initdbforum():
#    CREATE TABLE forum( id INTEGER PRIMARY KEY AUTOINCREMENT, Sujet TEXT,Message TEXT, pseudo TEXT,date TEXT);
#def initdbreponseforum():
#    CREATE TABLE reponse( id INTEGER PRIMARY KEY AUTOINCREMENT, Sujet TEXT,Reponse TEXT, pseudo TEXT,date TEXT);
#def initdbannonceforum():
#    CREATE TABLE annonce( id INTEGER PRIMARY KEY AUTOINCREMENT, Annonce TEXT,Prix FLOAT,Localisation TEXT, Pseudo TEXT,Date TEXT);
#Au cas ou



#Calendrier jardin 
#Base de données calendrier
def connectDatabaseCalendrier():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    dbc = sqlite3.connect('calendrier.db')
    cursor = dbc.cursor()
    return dbc, cursor

def initDB_Calendrier():
    dbc, cursor = connectDatabaseCalendrier()
    
    cursor.execute('DROP TABLE IF EXISTS calendrier')
    
    query = '''
    CREATE TABLE calendrier 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        titre TEXT,
        debut TEXT,
        fin TEXT,
        description TEXT,
        participants TEXT
    )
    '''
    cursor.execute(query)
    
    dbc.commit()
    cursor.close()
    dbc.close()

def creer_evenement(donnee):
    user = donnee[0]
    titre = donnee[1]
    debut = donnee[2]
    fin = donnee[3]
    description = donnee[4]
    
    query = """ INSERT INTO calendrier (user, titre, debut, fin, description, participants) VALUES (?,?,?,?,?,?);"""
    args = (user,titre,debut,fin,description,"aucun")
    dbc, cursor = connectDatabaseCalendrier()
    cursor.execute(query,args)
    dbc.commit()
    cursor.close()
    dbc.close()
    
    flash("Votre évènement a bien été créé !", "success")
    return redirect("/jardin")

def liste_evenements(pseudo):
    #on récupère les évènements liés au compte :
    query = """SELECT id, titre, debut, fin, description, participants FROM calendrier WHERE user LIKE ?;"""
    args = [pseudo]
    dbc, cursor = connectDatabaseCalendrier()
    cursor.execute(query, args)
    liste_evenements = cursor.fetchall()
    dbc.close()
    return liste_evenements_triee(liste_evenements)

def inserer(items,liste_triee):
    if liste_triee == []:
        liste_triee.append(items)
    else :
        for j in range (len(liste_triee)) :
                if datetime.strptime(items[2],"%d/%m/%Y") < datetime.strptime(liste_triee[j][2],"%d/%m/%Y"):
                    liste_triee.insert(j,items)
                    return
                elif (datetime.strptime(items[2],"%d/%m/%Y") == datetime.strptime(liste_triee[j][2],"%d/%m/%Y")) and (datetime.strptime(items[3],"%d/%m/%Y") < datetime.strptime(liste_triee[j][2],"%d/%m/%Y")) :
                    liste_triee.insert(j,items)
                    return
                elif (datetime.strptime(items[2],"%d/%m/%Y") == datetime.strptime(liste_triee[j][2],"%d/%m/%Y")) and (datetime.strptime(items[3],"%d/%m/%Y") >= datetime.strptime(liste_triee[j][2],"%d/%m/%Y")) :
                    liste_triee.insert(j+1,items)
                    return
                elif datetime.strptime(items[2],"%d/%m/%Y") > datetime.strptime(liste_triee[j][2],"%d/%m/%Y"):
                    liste_triee.append(items)
                    return

def liste_evenements_triee(liste):
    liste_triee = []
    for items in liste :
        inserer(items,liste_triee)
    
    return liste_triee

def supprimer_evenement(id):
    query = """DELETE FROM calendrier WHERE id == ?;"""
    args = [id]
    dbc, cursor = connectDatabaseCalendrier()
    cursor.execute(query, args)
    dbc.commit()
    dbc.close()

    flash("L'évènement a bien été supprimé !", "success")
    return redirect("/jardin")


def modifier_evenement(liste):
    id = liste[0]
    titre = liste[1]
    debut = liste[2]
    fin = liste[3]
    description = liste[4]
    
    query="""UPDATE calendrier SET titre=?,debut=?,fin=?,description=? WHERE id=?;"""
    args=[titre,debut,fin,description,id]
    dbc, cursor = connectDatabaseCalendrier()
    cursor.execute(query,args)
    dbc.commit()
    dbc.close

    flash("L'évènement a bien été modifié !", "success")
    return redirect("/jardin")

def participer_evenement(id_evenement, pseudo_particiant):
    query="""SELECT participants FROM calendrier WHERE id=?;"""
    args=[id_evenement]
    dbc, cursor = connectDatabaseCalendrier()
    cursor.execute(query,args)
    data = cursor.fetchall()
    dbc.close()
    
    if data[0][0] == "aucun":
        query="""UPDATE calendrier SET participants = ? WHERE id = ?;"""
        args = [pseudo_particiant,id_evenement]
        dbc, cursor = connectDatabaseCalendrier()
        cursor.execute(query,args)
        dbc.commit()
        dbc.close()
    else :
        flash("Il y a déjà un participant !", "error")
    
    query="""SELECT user FROM calendrier WHERE id=?;"""
    args=[id_evenement]
    dbc, cursor = connectDatabaseCalendrier()
    cursor.execute(query,args)
    data = cursor.fetchall()
    dbc.close()
    
    flash("Vous êtes bien inscrit comme participant !", "success")
    return redirect(f"/user/{ data[0][0] }")