document.getElementById("imcForm").addEventListener("submit", function(e) {
    e.preventDefault(); // Empêche le rechargement de la page

    const username = document.getElementById("username").value;
    const poids = parseFloat(document.getElementById("weight").value);
    const taille = parseFloat(document.getElementById("height").value);
    
    console.log("username:", username);
    console.log(taille,poids,username);

    if (poids > 0 && taille > 0) {
        fetch("__API_URL__/imc", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ weight: poids, height: taille, username: username })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("result").innerHTML = 
                    `<p style="color:red;">${data.error}</p>`;
            } else {
                if(username !== ""){
                    document.getElementById("result").innerHTML = 
                    `<p><strong>${username}</strong>, votre IMC est : <strong>${data.imc.toFixed(2)}</strong></p>
                     <p>Interprétation : ${data.category}</p>`;
                }
                else{
                    document.getElementById("result").innerHTML = 
                    `<p>Votre IMC est : <strong>${data.imc.toFixed(2)}</strong></p>
                     <p>Interprétation : ${data.category}</p>`;
                }
                
            }
            loadHistory();
            document.getElementById("result").style.display = "block";
        })
        .catch(err => {
            document.getElementById("result").innerHTML = 
                `<p style="color:red;">Erreur serveur : ${err}</p>`;
            document.getElementById("result").style.display = "block";
        });
    } else {
        document.getElementById("result").innerHTML = 
            "<p style='color:red;'>Veuillez entrer des valeurs valides.</p>";
        document.getElementById("result").style.display = "block";
    }
});


// Fonction pour charger l'historique
function loadHistory() {
  fetch("__API_URL__/imc")
    .then(response => response.json())
    .then(data => {
      const historyBody = document.getElementById("historyBody");
      historyBody.innerHTML = ""; // reset tableau

      if (data.length === 0) {
        historyBody.innerHTML = "<tr><td colspan='4'>Aucun calcul enregistré</td></tr>";
      } else {
        data.forEach(entry => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${entry.username}</td>
            <td>${entry.weight}</td>
            <td>${(entry.height / 100).toFixed(2)}</td>
            <td>${entry.imc}</td>
          `;
          historyBody.appendChild(row);
        });
      }

      document.getElementById("historyTable").style.display = "table";
    })
    .catch(err => {
      console.error("Erreur lors du chargement de l'historique :", err);
    });
}

// Bouton pour charger l'historique
document.getElementById("loadHistory").addEventListener("click", loadHistory);
