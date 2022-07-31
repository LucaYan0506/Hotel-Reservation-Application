document.addEventListener('DOMContentLoaded', () => {
    if (window.innerWidth < 600){
        document.querySelector('#body').className = '';
        document.querySelector('#menu').className = 'hide-600';
    }
})

document.addEventListener('resize', () => {
    if (window.innerWidth < 600){
        document.querySelector('#body').className = '';
        document.querySelector('#menu').className = 'hide';
    }
    else{
        document.querySelector('#body').className = 'expand';
        document.querySelector('#menu').className = 'show';
    }

        

})

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
    var icon = elem.querySelectorAll('i')[1];
    elem = elem.parentElement.querySelector('#sub-menu');
    elem.parentElement.querySelector('#menu-option').style.background = 'rgb(0,95,112)';

    //if another submenu is open, close it 
    document.querySelectorAll('#sub-menu.show').forEach( el => {
        if (el != elem){
            console.log(el)
            el.parentElement.querySelector('#menu-option').style.background = ''
            el.className = '';
        }
    })

    //get total height of elem
    let sub_memu_height = 0;
    elem.querySelectorAll('li').forEach( x => {
        sub_memu_height += x.clientHeight;
    })

    if (elem.className == "" | elem.className == "hide" ){
        document.documentElement.style.setProperty('--sub-memu-height', sub_memu_height);
        document.documentElement.style.setProperty('--sub-memu-height-curr', elem.clientHeight);
        elem.className = "show";
        icon.innerHTML = "keyboard_arrow_down"
    }
    else{
        document.documentElement.style.setProperty('--sub-memu-height-curr', Math.min(sub_memu_height,elem.clientHeight));
        elem.className = "hide";
        elem.parentElement.querySelector('#menu-option').style.background = ''
        icon.innerHTML = "chevron_left"
    }
}
