function get_user_list() {
    console.log("test");
    let userNameList = document.getElementById("userNameList");
    let req = new XMLHttpRequest();
    req.open("GET", `/get_user_list/${roomName}/${adminName}/`, true); // roomName, adminName initialized in the html files
    req.onload = function() {
        let json_msg = JSON.parse(req.responseText);
        console.log(json_msg);
        let json_msg_length = json_msg["userList"].length;
        let msg = "";
        for(let i=0; i<json_msg_length; ++i) {
            msg = msg + `
            <li class="listItem">${json_msg["userList"][i]}<br>
            </li><br> 
            `
        }
        userNameList.insertAdjacentHTML("beforeend", msg);
    }
    req.send();
}

get_user_list();