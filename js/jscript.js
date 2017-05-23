/* Open when someone clicks on the span element */
function openNav() {
    document.getElementById("myNav").style.display = "block";
    document.getElementById("myNav").style.zIndex = "1";
    document.getElementById("myNav").style.height = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("myNav").style.display = "none";
    document.getElementById("myNav").style.zIndex = "-1";
    document.getElementById("myNav").style.height = "0%";
}

/* Toggle when someone clicks on the span element */
function toggleAddComment() {
    var x = document.getElementById("addComm");
    if (x.style.display == 'block')
    {
        x.style.display = 'none'
    }
    else
    {
        x.style.display = 'block'
    }
}

function openComNav(comId) {
    document.getElementById(comId).style.display = "block";
    document.getElementById(comId).style.zIndex = "1";
    document.getElementById(comId).style.height = "100%";
}

function closeComNav(comId) {
    document.getElementById(comId).style.display = "none";
    document.getElementById(comId).style.zIndex = "-1";
    document.getElementById(comId).style.height = "0%";
}

function openEditCom(comId) {
    document.getElementById(comId).style.display = "block";
    document.getElementById(comId).style.zIndex = "1";
    document.getElementById(comId).style.height = "100%";
}

function closeEditCom(comId, comOriginalContent) {
    document.getElementById(comId).style.display = "none";
    document.getElementById(comId).style.zIndex = "-1";
    document.getElementById(comId).style.height = "0%";
    document.getElementById(comId + "textarea").value = comOriginalContent;
}

function updateComTextarea(comUpdatedTextId) {
    var comTextToUpdate = document.getElementById(comUpdatedTextId).value;
    return comTextToUpdate
}