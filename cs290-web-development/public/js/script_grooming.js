document.addEventListener('DOMContentLoaded', bindButton);

function bindButton(){
    document.getElementById('groomingSubmit').addEventListener('click', submitGroomingInfo);
}

function submitGroomingInfo(event){
    var pup = null;
    if (document.getElementById("zeekRadio").checked) {
        pup = "Zeek";
    }
    else if (document.getElementById("nellRadio").checked) {
        pup = "Nellie";
    }
    var payload = {Dog:null, Service:null, Email:null};
    payload.Dog = pup;
    payload.Service = document.getElementById('Service').value;
    payload.Email = document.getElementById('E-mail').value;
    var req = new XMLHttpRequest();
    req.open('POST', 'http://flip3.engr.oregonstate.edu:6032/grooming', true);
    req.setRequestHeader('Content-Type', 'application/json');
    req.addEventListener('load', () => {
        if (req.status >= 200 && req.status < 400) {
            var response = JSON.parse(req.responseText);
            document.getElementById("dogDisplay").textContent = "Dog: " + response["Dog"];
            document.getElementById("serviceDisplay").textContent = "Service: " + response["Service"];
            document.getElementById("emailDisplay").textContent = "E-mail: " + response["Email"];
        }
        else {
            console.log("Error in network request: " + req.statusText);
        }
    });
    req.send(JSON.stringify(payload));
    event.preventDefault();
}