function get_room_list() {
    let roomList = document.getElementById("userRoomList");
    let req = new XMLHttpRequest();
    req.open("GET", "/get_room_list/", true);
    req.onload = function() {
        let json_msg = JSON.parse(req.responseText);
        let json_msg_length = json_msg["roomList"].length;
        console.log(json_msg);
        let msg = "";
        for(let i=0; i<json_msg_length; ++i) {
            msg = msg + `
            <li class="listItem">${json_msg["roomList"][i]}<br>
                Admin: ${json_msg["adminList"][i]}<br>
                <a href="/room/${json_msg["roomList"][i]}/${json_msg["adminList"][i]}/">Enter</a>
            </li><br> 
            `;
        }
        roomList.insertAdjacentHTML("beforeend", msg);
    }
    req.send();
}

get_room_list();