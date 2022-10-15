function updateNavItems() {
    let navbarItems = document.getElementsByClassName("navItem");
    navbarItems[1].innerHTML = "";
    navbarItems[1].innerHTML = "LOGOUT";
    navbarItems[1].href = "/logout/";

    navbarItems[2].innerHTML = "";
    navbarItems[2].innerHTML = navItemUserName; //navItemUserName is initialized in the html files
    navbarItems[2].href = "#";
}

updateNavItems();