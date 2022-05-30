function show_hideMenu(){
    const elem = document.querySelector('#menu');   
    
    if (elem.className == "" | elem.className == "show" ){
        document.querySelector('#body').className = 'expand';
        elem.className = "hide"; 
    }
    else{
        document.querySelector('#body').className = 'shrink';
        elem.className = "show";
    }
}

function show_hideSubMenu(elem){
    var icon = elem.querySelectorAll('i')[1]
    elem = elem.parentElement.querySelector('#sub-menu')
     
    if (elem.className == "" | elem.className == "hide" ){
        elem.className = "show";
        icon.innerHTML = "keyboard_arrow_down"
    }
    else{
        elem.className = "hide";
        icon.innerHTML = "chevron_left"
    }
}