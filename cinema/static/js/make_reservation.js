const seats = []
const reserving_seats = []
var initialized = false;

const xhttp = new XMLHttpRequest()
xhttp.onload = function() {
    if (initialized) {
        console.log(this.responseText);
        return;
    }
    initialized = true;
    data = JSON.parse(this.responseText);
    console.log(data)
    var seatsTable = document.getElementById("seatsTable_id");
    seatsTable.style.borderSpacing = "5px"
    
    cols = data["cols"]
    nSeats = data["rows"] * cols;
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var tr = null;
    row = -1;
    col = 0;
    for (var i = 0; i < nSeats; i++) {
        if (i % data["cols"] == 0) {
            row++;
            col = 0;
            tr = document.createElement("tr");
            tr.id = "tr" + i + "_id";
            var rowLabel = document.createElement('td');
            rowLabel.innerHTML = letters[row];
            tr.appendChild(rowLabel);
            seatsTable.appendChild(tr);
        }

        var node = document.createElement("td");
        node.id = i + "_id";
        if (data["seats"][letters[row]][col] == null) {
            node.style.backgroundColor = "LightGrey";
            node.style.cursor = "pointer";
            node.onclick = function() { 
                cellClicked(this.id.split("_")[0]);
            };
            seats.push("free");
        }
        else {
            node.style.backgroundColor = "Red";
            seats.push("occupied")
        }
        node.style.width = "30px";
        node.style.height = "20px";
        tr.appendChild(node);
        col++;
    }

    console.log(seats);
}

function cellClicked(node_id) {
    console.log(node_id);
    console.log(seats[node_id]);
    var node = document.getElementById(node_id + "_id");
    if (seats[node_id] === "free") {
        seats[node_id] = "reserving";
        node.style.backgroundColor = "Green";
        reserving_seats.push(node_id);
    }
    else if (seats[node_id] === "reserving") {
        seats[node_id] = "free";
        node.style.backgroundColor = "LightGray"
        i = reserving_seats.indexOf(node_id);
        reserving_seats.splice(i,1);
    }
    else {
        console.log("clicked occupied cell");
    }
}

document.getElementById("reservationForm_id").addEventListener("submit", function (e) {
    e.preventDefault();
    console.log(reserving_seats);
    if (reserving_seats.length === 0) {
        alert("You need to select at least 1 seat");
        return;
    }

    var form = this;
    xhttp.open(form.method.toUpperCase(), form.action);
    const csfr = document.querySelector('[name=csrfmiddlewaretoken]').value;
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.setRequestHeader('X-CSRFToken', csfr);
    xhttp.send(JSON.stringify({"reserving_seats": reserving_seats}))
});

window.onload = function() {
    l = window.location.pathname.split("/");
    id = l[l.length - 2];
    console.log(id);
    xhttp.open("GET", "/movies/screeningseats/" + id);
    xhttp.send();
}