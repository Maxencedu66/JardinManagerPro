# imports
import string
import random
import datetime
from flask import Flask, request, render_template, flash, redirect, session, url_for
from flask_session import Session
from datetime import datetime
import sqlite3
import os

#importation des fonctions créée:
from fonctions import *


# flask app creation
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#def des routes:

#/home (max)
@app.route("/")
def home():
    return render_template("home.html", title = "JardinManagerPro")


#route forum (flo)
@app.route('/forum',methods=['GET','POST'])
def forum():     
    if request.method=='GET':
        return affichertableforum()


@app.route("/creersujet", methods = ["GET","POST"])
def creersujet():
    if request.method == "GET" :
        if  ('name' in session) and (session['name']!=None):
            return render_template("creersujet.html", title = "Créer un sujet")
        else :
            return render_template("connection.html")
    if request.method == "POST" :
        sujet=request.form.get("sujet")
        message=request.form.get("message")
        message=message.replace("\n", "<br>")
        if  ('name' in session) and (session['name']!=None):
            pseudo = session['name']
            date= datetime.now()
            date= date.strftime("%d/%m/%Y %H:%M")
            return fct_creersujet(sujet,message,pseudo,date)
        else :
            return render_template("connection.html", title = "Connexion")

@app.route("/creerreponse", methods = ["GET","POST"])
def creerreponse():
    if request.method == "GET" :
        if  ('name' in session) and (session['name']!=None):
            pseudo1=request.args.get('pseudo1')
            sujet=request.args.get('sujet')
            message=request.args.get('message')
            return render_template("creerreponse.html", pseudo1=pseudo1,sujet=sujet,message=message,title="Créer une réponse")
        else :
            return render_template("connection.html",title = "Connexion")
    if request.method == "POST" :
        sujet=request.form.get('sujet')
        message=request.form.get('message')
        reponse=request.form.get("reponse")
        reponse=reponse.replace("\n", "<br>")
        pseudo1=request.form.get('pseudo1')
        if  ('name' in session) and (session['name']!=None):
            pseudo = session['name']
            date= datetime.now()
            date= date.strftime("%d/%m/%Y %H:%M")
            return fct_creerreponse(sujet,reponse,pseudo,date,message,pseudo1)
        else :
            return render_template("connection.html", title = "Connexion")

@app.route("/creeroffre", methods = ["GET","POST"])
def creeroffre():
    if request.method == "GET" :
        if  ('name' in session) and (session['name']!=None):
            return render_template("creeroffre.html", title = "Créer une offre")
        else :
            return render_template("connection.html", title = "Connexion")
    if request.method == "POST" :
        annonce=request.form.get("annonce")
        localisation=request.form.get("localisation")
        prix=request.form.get("prix")
        image=request.files.get('image')
        description=request.form.get('description')
        description=description.replace("\n", "<br>")
        if  ('name' in session) and (session['name']!=None):
            pseudo = session['name']
            date= datetime.now()
            date= date.strftime("%d/%m/%Y %H:%M")
            return fct_creeroffre(annonce,prix,localisation,pseudo,date,image,description)
        else :
            return render_template("connection.html", title = "Connexion")
            

@app.route("/reponsesujet", methods = ["GET","POST"])
def reponsesujet():
    if request.method == "GET" :
        pseudo1= request.args.get('pseudo')
        sujet = request.args.get('sujet')
        message=request.args.get('message')
        query="""SELECT Reponse,pseudo,date FROM reponse WHERE Sujet=? AND pseudo1=?"""
        args=[sujet,pseudo1]
        dbf,cursor=connectdbforum()
        cursor.execute(query,args)
        data=cursor.fetchall()
        dbf.close()
        return render_template("reponse.html", listdb=data,sujet=sujet,message=message,pseudo1=pseudo1, title = "Réponse")

@app.route("/annonce", methods = ["GET","POST"])
def annonce():
    if request.method == "GET" :
        annonce = request.args.get('annonce')
        pseudo= request.args.get('pseudo')
        query="""SELECT Annonce,Prix,Localisation,Pseudo,Date,Image,Description FROM annonce WHERE Annonce=? AND Pseudo=?"""
        args=[annonce,pseudo]
        dbf,cursor=connectdbforum()
        cursor.execute(query,args)
        data=cursor.fetchall()
        dbf.close()
        return render_template("annonce.html", listdb=data,annonce=annonce,pseudo=pseudo,title="Annonce")

@app.route('/cabanon',methods=['GET','POST'])
def cabanon():     

    if request.method=='GET':
        if  ('name' in session) and (session['name']!=None):
            pseudo=session['name']
            return affichertableannonce(pseudo)
        else :
            return render_template('connection.html')
    if request.method=='POST':
        if  ('name' in session) and (session['name']!=None):
            pseudo=session['name']
            prix_min=request.form.get('prix_min')
            prix_max=request.form.get('prix_max')
            return affichertableannoncefiltre(prix_min,prix_max,pseudo)

#Route du save de jardin
@app.post('/save')
def save():
    try:
        id = id_user(session["name"])
        body = request.json
        garden = body["garden"]
        data = ','.join(str(data) for data in garden) #transforme list en chaine de caractère séparé d'une virgule
        largeur = body["largeur"]
        hauteur = body["hauteur"]
        # Vérifie si une configuration, une largeur et une hauteur existent déjà pour l'id de l'utilisateur
        query = f"""SELECT COUNT(*) FROM jardin WHERE id_user = {id}"""
        db, cursor = connectDatabase()
        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        if result == 0:
            query="""INSERT INTO jardin(configuration, largeur, hauteur, id_user) VALUES (?, ?, ?, ?);"""
            args=[data, largeur, hauteur, id]
            db,cursor=connectDatabase()
            cursor.execute(query,args)
            db.commit()
            db.close()
        else:
            query = """UPDATE jardin SET configuration = ?, largeur = ?, hauteur = ? WHERE id_user = ?;"""
            args=[data, largeur, hauteur, id]
            db,cursor=connectDatabase()
            cursor.execute(query,args)
            db.commit()
            db.close()
        return {'message':'Votre jardin a bien été sauvegardé'}
    except Exception as e:
        return {'message':'erreur de'}

@app.get("/configuration")
def get_configuration():
    try:
        id = id_user(session["name"])
        query = """SELECT configuration, largeur, hauteur FROM jardin WHERE id_user = (?);"""
        args = [id]
        db, cursor = connectDatabase()
        cursor.execute(query,args)
        result = cursor.fetchall()
        configuration = result[0][0]
        print(result)
        largeur = result[0][1]
        hauteur = result[0][2]
        configuration = configuration.split(',')
        db.close()
        return {"configuration": configuration, "largeur": largeur, "hauteur": hauteur}
    except Exception as e:
        return {"message": str(e)}

#Jardin (max et thomas)
@app.route('/jardin', methods = ["GET", "POST"])
def jardin():
    if request.method == "GET":
        evenements = liste_evenements(session["name"])
        return render_template('jardin.html',title="Jardin",evenements=evenements)
    
@app.route("/evenement", methods=["GET", "POST"])
def evenement():
    if request.method == "GET":
        return render_template("creerevenement.html", title="Créer un évènement")
    if request.method == "POST":
        user = session["name"]
        titre = request.form.get("titre")
        debut = request.form.get("debut")
        fin = request.form.get("fin")
        description = request.form.get("description")
        data = [user, titre, debut, fin, description]
        return creer_evenement(data)

@app.route("/supprimerevenement/<int:id>")
def supprimerevenement(id):
    return supprimer_evenement(id)

@app.route("/modifierevenement/<int:id>", methods=["GET", "POST"])
def modifierevenement(id):
    if request.method == "GET":
        return render_template("modifierevenement.html", title="Modifier l'évènement", id=id)
    if request.method == "POST":
        id_user = id
        titre = request.form.get("titre")
        debut = request.form.get("debut")
        fin = request.form.get("fin")
        description = request.form.get("description")
        data = [id_user, titre, debut, fin, description]
        
        return modifier_evenement(data)

@app.route("/participerevenement/<int:id>")
def participerevenement(id):
    pseudo_participant = session["name"]
    id_evenements = id
    return participer_evenement(id_evenements,pseudo_participant)


@app.route('/info')
def info():
    return render_template('info.html',title="Infos")



#gestion  de profil (étienne)

#connexion
@app.route("/connection", methods=["GET","POST"])
def connection():
    if request.method == "GET":
        session["previous_url"] = request.referrer
        return render_template("connection.html", title = "Connexion")
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        mdp = request.form.get("mdp")
        return fct_connection(pseudo, mdp)


#deconnexion
@app.route("/deconnexion")
def deconnexion():
    session["name"] = None
    flash("Déconnexion réussie !", "success")
    return redirect("/")


#profil
@app.route("/profil")
def profil():
    if not session.get("name"):
        return redirect("/connection")
    else :
        pseudo = session.get("name")
        return fct_profil(pseudo)


#inscription
@app.route("/inscription", methods = ["GET","POST"])
def inscription():
    if request.method == "GET" :
        return render_template("inscription_profil.html", title="Inscription")
    if request.method == "POST" :
        pseudo=request.form.get("pseudo")
        mail=request.form.get("mail")
        mdp=request.form.get("mdp")
        #ici on vérifie que l'utilisateur ne s'est pas trompé lorsqu'il rentre son mot de passe pour l'inscription
        conf_mdp=request.form.get("conf_mdp")
        ville=request.form.get("ville")
        
        return fct_inscritpion(pseudo, mail, mdp, conf_mdp, ville)


#mise a jour donnee profil
@app.route("/maj/<string:donnee>", methods = ["GET", "POST"])
def maj(donnee : str):
    if request.method == "GET" :
        #on vérifie si l'utilisateur a déjà une photo ou non pour l'affichage de "maj_photo.html"
        photo = verif_photo(session["name"])
        if photo == True:
            return render_template(f"maj_{ donnee }.html", title = f"Mise à jour de votre { donnee }", photo=photo)
        else :
            return render_template(f"maj_{ donnee }.html", title = f"Ajouter une { donnee }", photo=photo)
    
    if request.method == "POST" :
        pseudo = session.get("name")
        
        #changement pseudo
        if donnee == "pseudo" :
            new_pseudo = request.form.get("new_pseudo")
            return maj_db(pseudo, new_pseudo, "Pseudo")
        
        #changement mail
        elif donnee == "mail" :
            new_mail = request.form.get("new_mail")
            return maj_db(pseudo, new_mail, "Mail")
        
        #changement mdp
        elif donnee == "mdp" :
            ancien_mdp = request.form.get("ancien_mdp")
            
            #ici on vérifie que l'utilisateur a bien saisi son ancien mot de passe pour confirmer le changement
            if verif_mdp(pseudo,ancien_mdp):
                new_mdp = request.form.get("new_mdp")
                return maj_db(pseudo, new_mdp, "Mdp")
            
            else :
                flash("Vous vous êtes trompés dans votre ancien mot de passe !", "error")
                return redirect("/maj/mdp")

        #changement ville
        elif donnee == "ville" :
            new_ville = request.form.get("new_ville")
            return maj_db(pseudo, new_ville, "Ville")
        
        #changement photo
        elif donnee == "photo":
            new_photo = request.files.get("new_photo")
            return maj_db(pseudo, new_photo, "Photo")
        
        
#profil public
@app.route("/user/<string:donnee>")
def user(donnee : str):
    return fct_profil_public(donnee)

#main
if __name__ == "__main__":
    if (False):
        initDB()
    if (False):
        initDBforum()
    if (False):
        initDB_Calendrier()
        
    app.run(debug=1, host='0.0.0.0', port='5454')
