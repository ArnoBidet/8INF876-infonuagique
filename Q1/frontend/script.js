document.getElementById("imcForm").addEventListener("submit", function(e) {
    e.preventDefault(); // Empêche le rechargement de la page

    const username = document.getElementById("username").value;
    const poids = parseFloat(document.getElementById("weight").value);
    const taille = parseFloat(document.getElementById("height").value);
    
    console.log("username:", username);
    console.log(taille,poids,username);

    if (poids > 0 && taille > 0) {
        fetch("http://localhost:3000/imc", {
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
