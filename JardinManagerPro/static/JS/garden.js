let garden = [];

// Gestionnaire d'événement pour la soumission du formulaire
document.getElementById('form').addEventListener('submit', function (event) {
  event.preventDefault(); // Empêche le formulaire de soumettre les données (recharge de la page)

  // Récupération des valeurs de largeur et de hauteur du formulaire
  var width = document.getElementById('width').value;
  var height = document.getElementById('height').value;

  // Vérification de la validité du formulaire
  if (width == '' || height == '') {
    alert('Veuillez remplir tous les champs !'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }
  if (width < 0 || height < 0) {
    alert('Veuillez rentrer des valeurs positives'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }
  if (width == 0 || height == 0) {
    alert('Veuillez rentrer des valeurs non nulles'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }
  if (width > 25 || height > 25) {
    alert('La grille ne peut pas dépasser 25 par 25 !'); // Affichage d'un message d'erreur
    return; // Arrêt de la fonction
  }

  // Suppression du tableau précédemment généré
  var table = document.querySelector('table');
  if (table) {
    table.parentNode.removeChild(table);
  }

  // Création d'un tableau HTML vide
  table = document.createElement('table');

  for (let i = 0; i < height * width; i++) {
    garden.push(null);
  }


  // Création des lignes et des colonnes du tableau
  for (var i = 0; i < height; i++) {
    var row = document.createElement('tr');
    for (var j = 0; j < width; j++) {
      var cell = document.createElement('td');
      cell.innerHTML = ""; // Case vide
      row.appendChild(cell);
    }
    table.appendChild(row);
  }

  // Récupération du div affichage_jardin
  var affichageJardin = document.querySelector('.affichage_jardin');

  // Ajout du tableau dans la div affichage_jardin
  affichageJardin.appendChild(table);


  //affichage button
  document.getElementById('button-container').style.display = 'block';

  // Remise à zéro du menu déroulant
  document.getElementById('vegetable-select').selectedIndex = 0;



  // Ajout d'un gestionnaire d'événement "click" à chaque cellule du tableau
  var cells = document.querySelectorAll('td');
  cells.forEach(function (cell, index) {
    cell.index = index;
    cell.addEventListener('click', function (event) {
      // Récupère le légume sélectionné
      var vegetable = document.getElementById('vegetable-select').value;
      if (vegetable) {
        // Ajoute la classe correspondante à la cellule
        cell.classList.add(vegetable);
        // Ajoute le dégradé de vert à la cellule
        cell.classList.add("vegetable-background")
        garden[index] = vegetable
        console.log(garden)
      } else {
        // Supprime toutes les classes et le background de la cellule cliquée
        cell.className = "";
        cell.classList.remove("vegetable-background");
        garden[cell.index] = null;
      }
    });
  });



  /* Variable qui indique si le mode suppression est activé ou non
  var deleteMode = false;

  // Gestionnaire d'événement pour le bouton "Supprimer case"
  document.getElementById('delete-cell').addEventListener('click', function (event) {
    deleteMode = !deleteMode; // Inverse la valeur de deleteMode
    if (deleteMode) {
      event.target.textContent = 'Annuler suppression'; // Change le texte du bouton en "Annuler suppression"
      // Remise à zéro du menu déroulant
      document.getElementById('vegetable-select').selectedIndex = 0;
    } else {
      event.target.textContent = 'Supprimer case'; // Change le texte du bouton en "Supprimer case"
    }*/
  });

  // Gestionnaire d'événement pour le menu déroulant
  document.getElementById('vegetable-select').addEventListener('change', function (event) {
    // Annule le mode "Supprimer case"
    deleteMode = false;
    document.getElementById('delete-cell').textContent = 'Supprimer case';
  });

  // Gestionnaire d'événement pour chaque cellule du tableau
  var cells = document.querySelectorAll('td');
  cells.forEach(function (cell) {
    cell.addEventListener('click', function (event) {
      if (deleteMode) {
        // Supprime la cellule
        cell.parentNode.removeChild(cell);
        
      }
    });
  });


// Variable globale pour stocker le légume actuellement sélectionné
var currentVegetable = null;

// Gestionnaire d'événement pour le menu déroulant
document.getElementById('vegetable-select').addEventListener('change', function (event) {
  // Mise à jour de currentVegetable avec le nom du légume sélectionné
  currentVegetable = event.target.value;
  var selectedCells = document.querySelectorAll('.selected');

  // Mise à jour du gestionnaire d'événement "click" de chaque cellule
  var cells = document.querySelectorAll('td');
  cells.forEach(function (cell) {
    cell.removeEventListener('click', addVegetableClass);
    cell.addEventListener('click', addVegetableClass);

  });
});


// Récupération de l'élément HTML du bouton "Réinitialiser"
var resetButton = document.getElementById('reset');
// Gestionnaire d'événement pour le bouton "Réinitialiser"
resetButton.addEventListener('click', function () {
  // Suppression du tableau précédemment généré
  var table = document.querySelector('table');
  if (table) {
    table.parentNode.removeChild(table);
  }
  // Réinitialisation de la valeur des champs de formulaire
  document.getElementById('width').value = '';
  document.getElementById('height').value = '';
  // Masquage des boutons
  document.getElementById('button-container').style.display = 'none';
});


// Fonction pour ajouter une classe CSS à une cellule en fonction de currentVegetable
function addVegetableClass(event) {
  // Récupération de la cellule ciblée par l'événement "click"
  var cell = event.target;

  // Suppression de toutes les classes CSS existantes de la cellule
  cell.className = '';

  // Ajout de la classe CSS correspondant à currentVegetable
  cell.classList.add(currentVegetable);

}

// Gestionnaire d'événement pour le bouton "Effacer"
document.querySelector('.delete').addEventListener('click', function() {
  currentVegetable = null; // Remise à null de currentVegetable pour désélectionner le légume actuel

  // Mise à jour du gestionnaire d'événement "click" de chaque cellule
  var cells = document.querySelectorAll('td');
  cells.forEach(function(cell) {
    cell.removeEventListener('click', addVegetableClass);
    cell.addEventListener('click', removeVegetableClass);
  });
    // Remise à zéro du menu déroulant
    document.getElementById('vegetable-select').selectedIndex = 0;
});







// Gestionnaire d'événement pour le bouton "Effacer tout"
document.querySelector('.clear-all').addEventListener('click', function () {
  // Réinitialisation de currentVegetable
  currentVegetable = null;
  // Remise à zéro du menu déroulant
  document.getElementById('vegetable-select').selectedIndex = 0;
  // Suppression de toutes les classes "carrot","tomato",etc des cellules
  var cells = document.querySelectorAll('td');
  cells.forEach(function (cell, index) {
    garden[index] = null

    cell.classList.remove('carrot', 'tomato', 'cerises', 'fraise', 'kiwi', 'melon',
      'peche', 'poire', 'pomme', 'raisin', 'ail', 'aubergine', 'avocat',
      'broccoli', 'cacahuetes', 'chataigne', 'concombre', 'mais',
      'salade', 'oignon', 'patate');
    cell.classList.remove("vegetable-background");
  });
});



// Fonction pour ajouter une classe à la case sur laquelle l'utilisateur clique
function addVegetableClass() {
  this.classList.add(currentVegetable); // Ajout de la classe à la cellule sur laquelle l'utilisateur a cliqué
  this.classList.add("vegetable-background")
}

// Fonction pour effacer la classe de la case sur laquelle l'utilisateur clique
function removeVegetableClass() {
  this.className = ""; // Effacement de la classe de la cellule sur laquelle l'utilisateur a cliqué
}


function addVegetableBackground(cell) {
  // Ajoute la classe "vegetable-background" à la cellule
  cell.classList.add("vegetable-background");
}

//SAUVEGARDER
// Gestionnaire d'événement pour le bouton "Sauvegarder"
document.getElementById('save-file').addEventListener('click', async () => {
  //Nb colonnes et lignes
  const largeur = document.querySelector('tr').children.length
  const hauteur = document.querySelectorAll('tr').length
  // Récupère les données du tableau
  const data = {
    garden: garden,
    largeur: largeur,
    hauteur: hauteur,
  }
  console.log(data);
  const response = await fetch("/save", { method: "POST", headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
  const message = await response.json()
  window.alert(message.message)
});
 

//CHARGER

document.getElementById('load').addEventListener('click', async () => {
  // Récupère les données du tableau
  const response = await fetch("/configuration", { method: "GET"})
  const data = await response.json()
  console.log(data);
  const configuration = data.configuration
  const hauteur = data.hauteur
  const largeur = data.largeur
  const rebuildTable = () => {
    const table = document.createElement('table')
    for (let i = 0; i < hauteur; i++) {
      const row = document.createElement('tr')
      for (let j = 0; j < largeur; j++) {
        const cell = document.createElement('td')
        const index = i * largeur + j
        if (configuration[index] !== 'None') {
          cell.classList.add(configuration[index])
          cell.classList.add('vegetable-background')
        }
        row.appendChild(cell)
      }
      table.appendChild(row)
    }
    return table
  }

  const rebuiltTable = rebuildTable()

  // Récupération du div affichage_jardin
  var affichageJardin = document.querySelector('.affichage_jardin');

  // Suppression du tableau précédemment généré
  var table = document.querySelector('table');
  if (table) {
    table.parentNode.removeChild(table);
  }

  // Ajout du tableau reconstruit dans la div affichage_jardin
  affichageJardin.appendChild(rebuiltTable);
   //affichage button
  document.getElementById('button-container').style.display = 'block';
});

 // Ajout d'un gestionnaire d'événement "click" à chaque cellule du tableau reconstruit
  var cells = document.querySelectorAll('td');
  cells.forEach(function (cell, index) {
    cell.index = index;
    cell.addEventListener('click', function (event) {
      // Récupère le légume sélectionné
      var vegetable = document.getElementById('vegetable-select').value;
      if (vegetable) {
        // Ajoute la classe correspondante à la cellule
        cell.classList.add(vegetable);
        // Ajoute le dégradé de vert à la cellule
        cell.classList.add("vegetable-background")
        garden[index] = vegetable

      } else {
        // Supprime toutes les classes et le background de la cellule cliquée
        cell.className = "";
        cell.classList.remove("vegetable-background");
      }
    });
  
  });




//LIGNE ENTIERE

// Gestionnaire d'événement pour le bouton "Ligne entière"
document.querySelector('.line-button').addEventListener('click', function () {
  // Vérification de la valeur du bouton
  if (this.innerHTML === 'Ligne entière') {
    // Changement de la valeur du bouton et activation du mode "Ligne entière"
    this.innerHTML = 'Annuler';
    document.lineMode = true;
    // Ajout d'un gestionnaire d'événement à chaque ligne du tableau
    var rows = document.querySelectorAll('tr');
    rows.forEach(function (row) {
      row.addEventListener('click', fillRow);
    });
  } else {
    // Changement de la valeur du bouton et désactivation du mode "Ligne entière"
    this.innerHTML = 'Ligne entière';
    document.lineMode = false;

    // Suppression des gestionnaires d'événements ajoutés à chaque ligne du tableau
    var rows = document.querySelectorAll('tr');
    rows.forEach(function (row) {
      row.removeEventListener('click', fillRow);
    });
  }
});

function fillRow() {
  // Récupération de la valeur du menu déroulant
  var vegetable = document.getElementById('vegetable-select').value;
  // Récupération de la largeur de la grille
  var width = document.getElementById('width').value;
  // Récupération de l'index de la ligne dans la grille
  var rowIndex = Array.prototype.indexOf.call(this.parentNode.children, this);
  // Remplissage de chaque cellule de la ligne avec le légume sélectionné
  var cells = this.querySelectorAll('td');
  cells.forEach(function (cell, index) {
    cell.index = index;
    cell.classList.add(vegetable);
    addVegetableBackground(cell);
    // Mise à jour de la valeur de "garden" à l'index correspondant
    garden[rowIndex * width + index] = vegetable;
  }); 
  console.log(garden)
}




//COLONNE ENTIERE

// Gestionnaire d'événement pour le bouton "Colonne entière"
document.querySelector('.colonne-button').addEventListener('click', function () {
  // Vérification de la valeur du bouton
  if (this.innerHTML === 'Colonne entière') {
    // Changement de la valeur du bouton et activation du mode "Colonne entière"
    this.innerHTML = 'Annuler';
    document.columnMode = true;

    // Ajout d'un gestionnaire d'événement à chaque cellule du tableau
    var cells = document.querySelectorAll('td');
    cells.forEach(function (cell) {
      cell.addEventListener('click', fillColumn);
    });
  } else {
    // Changement de la valeur du bouton et désactivation du mode "Colonne entière"
    this.innerHTML = 'Colonne entière';
    document.columnMode = false;

    // Suppression des gestionnaires d'événements ajoutés à chaque cellule du tableau
    var cells = document.querySelectorAll('td');
    cells.forEach(function (cell) {
      cell.removeEventListener('click', fillColumn);
    });
  }
});

function fillColumn() {
  // Récupération de la valeur du menu déroulant
  var vegetable = document.getElementById('vegetable-select').value;
  // Récupération de la largeur de la grille
  var width = document.getElementById('width').value;
  // Récupération de l'index de la colonne dans le tableau garden
  const columnIndex = this.cellIndex;
  // Récupération de toutes les cellules de la colonne
  var cells = document.querySelectorAll('td:nth-of-type(' + (columnIndex + 1) + ')');
  // Remplissage de chaque cellule de la colonne avec le légume sélectionné et mise à jour de "garden"
  cells.forEach(function (cell, index) {
    cell.classList.add(vegetable);
    addVegetableBackground(cell);
    // Mise à jour de la valeur de "garden" à l'index correspondant
    garden[index * width + columnIndex] = vegetable;
  });
  console.log(garden)
}

  


