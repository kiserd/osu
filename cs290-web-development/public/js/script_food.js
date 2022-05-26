// upon DOM content successfully loading, call function to bind buttons
document.addEventListener('DOMContentLoaded', bindButtons);

function bindButtons() {
    document.getElementById("unpurchasedTbody").addEventListener('click', markPurchased);
    document.getElementById("addButton").addEventListener('click', addToList);
}

buildTbody();

// build tbody of shopping list
function buildTbody() {
    var unpurchasedRows = getUnpurchased();
    var myTbody = document.getElementById("unpurchasedTbody");
    for (var i = 0; i < unpurchasedRows.length; i++) {
        var newRow = document.createElement("tr");
        var col = 0;
        for (key in unpurchasedRows[i]) {
            newData = document.createElement("td");
            newData.textContent = unpurchasedRows[i][key];
            if (col == 0 || col == 4) {
                newData.className = "d-none";
            }
            newRow.appendChild(newData);
            col++;
        }
        newData = document.createElement("td");
        newButton = document.createElement("button");
        newButton.textContent = "Mark Purchased";
        newButton.className = "btn btn-primary";
        newData.appendChild(newButton);
        newRow.appendChild(newData);
        myTbody.appendChild(newRow);
    }
}

function addToList(event) {
    var name = document.getElementById("nameSelect").value;
    var qty = document.getElementById("qtySelect").value;
    var req = new XMLHttpRequest();
    var resource = '/insert?name=' + name + "&qty=" + qty;
    req.open('GET', resource, false);
    req.addEventListener('load', () => {
        if (req.status >= 200 && req.status < 400) {
            console.log(req.responseText);
        }
        else {
            console.log("Error in network request: " + req.statusText);
        }
    });
    req.send(null);
    document.getElementById("unpurchasedTbody").innerHTML = "";
    buildTbody();
    event.preventDefault();
}

function markPurchased(event) {
    console.log("mark purchased entered");
    let target = event.target;
    console.log(target.tagName);
    if (target.tagName != "BUTTON") {
        return;
    }
    var id = getIDFromButton(target);
    sendMarkPurchased(id);
}

function getIDFromButton(button) {
    var targetRow = button.parentNode.parentNode;
    var targetCell = targetRow.firstChild;
    var id = targetCell.textContent;
    return id;
}

function sendMarkPurchased(id) {
    var req = new XMLHttpRequest();
    var resource = 'markPurchased?id=' + id; 
    req.open('GET', resource, false);
    req.addEventListener('load', () => {
        if (req.status >= 200 && req.status < 400) {
            console.log(req.responseText);
        }
        else {
            console.log("Error in network request: " + req.statusText);
        }
    });
    req.send(null);
    document.getElementById("unpurchasedTbody").innerHTML = "";
    buildTbody();
}

function getUnpurchased() {
    return_var = [];
    var req = new XMLHttpRequest();
    req.open('GET', '/getUnpurchased', false);
    req.addEventListener('load', () => {
        if (req.status >= 200 && req.status < 400) {
            var response_0 = req.responseText;
            var response_json = JSON.parse(req.responseText);
            for (var i = 0; i < response_json.length; i++) {
                closureMaker = function(x) {
                    return_var.push(response_json[x]);
                }
                closureMaker(i);
            }
        }
        else {
            console.log("Error in network request: " + req.statusText);
        }
    });
    req.send(null);
    return return_var;
}
