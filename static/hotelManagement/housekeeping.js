let start = 1;

document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #rooms').style.color = 'white';

    //if room_id is known, then apply this filter 
    if (room_id != 'None'){
        document.querySelector('select#id_room').selectedIndex = room_id
        document.querySelectorAll('#custom-select-container')[1].querySelector(`input[value="${room_id}"]`).click();
    }

    load();
})

document.querySelector('.btn#search').addEventListener('click', e =>{
    start = 1;
    load();
})

document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
};


function show_housekeepingForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_housekeepingForm(){
    document.querySelector('#table-container').style.display = 'block';   
    document.querySelector('#form-container').style.display = 'none';   
}

function create_row(housekeeping,i){
/*
<tr>
    <th scope="row">{{row.pk}}</th>
    <td>{{row.Title}}</td>
    <td>{{row.Short_Code}}</td>
    <td>
        <button class="btn" onclick="view_housekeeping(1)" style="border:solid 1px gray;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
            View
        </button>
        <button class="btn" onclick="edit_housekeeping(1)" style="color: #fff; background-color: #007bff; border-color: #007bff;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
            Edit
        </button>
        <button class="btn" onclick="delete_housekeeping(1)" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 2px;">delete</i>
            Delete
        </button>
    </td>
</tr>
*/
    const tr = document.createElement('tr');

    const th = document.createElement('th');
    th.scope = "row";
    th.innerHTML = i;

    const td0 = document.createElement('td');
    td0.innerHTML = housekeeping.room.value;

    const td1 = document.createElement('td');
    td1.innerHTML = housekeeping.housekeeping_status.value;

    const td2 = document.createElement('td');
    td2.innerHTML = housekeeping.assigned_to.value;

    const td3 = document.createElement('td');
    td3.innerHTML = `   
    <button class="btn" onclick="view_housekeeping(${housekeeping.pk})" style="border:solid 1px gray;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
        View
    </button>
    <button class="btn" onclick="edit_housekeeping(${housekeeping.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
        Edit
    </button>
    <button class="btn" onclick="delete_housekeeping(${housekeeping.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 2px;">delete</i>
        Delete
    </button>`;

    tr.append(th);
    tr.append(td0);
    tr.append(td1);
    tr.append(td2);
    tr.append(td3);

    document.querySelector('.table tbody').append(tr);
}

function load(){
    let quantity = parseInt(document.querySelector('select#entries').value);

    //clear table
    if (document.querySelectorAll('.table tbody *') != [])
        document.querySelectorAll('.table tbody *').forEach(element => {
            element.remove();
        });

    //clear btn-container
    if (document.querySelector('#btn-container'))
        document.querySelector('#btn-container').remove()
    let end = start + quantity - 1;
    
    //check if there are filters to apply
    let filter = "";
    document.querySelectorAll('#custom-select-container #sub-menu').forEach( elem => {
        if (parseInt(elem.getAttribute('data-selected-item')) > 0){
            if (filter == "")
                filter = "True";
            filter += `&${elem.parentElement.getAttribute('data-name')}=`
            elem.querySelectorAll('input[type="checkbox"').forEach(checkbox => {
                if (checkbox.checked){
                    filter += checkbox.value + ",";
                }
            })
        }
    })

    //show housekeeping
    fetch(`/admin/room/housekeeping/info/?start=${start}&end=${end}&filter=${filter}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.housekeeping.forEach(housekeeping => {
           create_row(housekeeping,i++);
        });

        //increasing start
        start+= quantity;

        //add next/previous button
        const btn_container = document.createElement('div');
        btn_container.id = "btn-container";
        document.querySelector('.table').parentElement.append(btn_container);
        
        const previousBtn = document.createElement('button');
        previousBtn.innerHTML = 'previous';
        previousBtn.id = 'previous';
        previousBtn.className = 'btn btn-outline-secondary';
        previousBtn.onclick = () => {
            start -= quantity * 2;
            load();
            
        }
        previousBtn.disabled = start - quantity <= quantity;
        btn_container.append(previousBtn);
      
        const nextBtn = document.createElement('button');
        nextBtn.innerHTML = 'next';
        nextBtn.className = 'btn btn-outline-secondary';
        nextBtn.id = 'next';
        nextBtn.onclick = () => {
            load();
        }
        nextBtn.disabled = start > data.total_housekeeping;
        btn_container.append(nextBtn);

        const div_clear = document.createElement('div');
        div_clear.style.clear = "both";
        btn_container.append(div_clear);
    })

}

function view_housekeeping(pk){
    show_housekeepingForm();

    fetch(`/admin/room/housekeeping/info/?pk=${pk}`)
    .then(response => response.json())
    .then(housekeeping => {
        document.querySelector('#form-container #id_room').selectedIndex = housekeeping.room.pk
        document.querySelector('#form-container #id_room').disabled = true;

        document.querySelector('#form-container #id_housekeeping_status').selectedIndex = housekeeping.housekeeping_status.pk
        document.querySelector('#form-container #id_housekeeping_status').disabled = true;

        document.querySelector('#form-container #id_assign_to').selectedIndex = housekeeping.assigned_to.pk
        document.querySelector('#form-container #id_assign_to').disabled = true;  
    })
    
    document.querySelectorAll('.btn').forEach(x => {x.style.display = 'none'})

    const a = document.createElement('button')
    a.className = 'btn'
    a.style=`
        margin: 0 auto;
        display: block;
        width: 50%;
        margin: 0 auto;
        display: block;
        background-color: #dc3545; 
        border-color: #dc3545;
        color: white;`
    a.innerHTML = 'Close'
    a.onclick = () =>{
        location.reload();
    }
    document.querySelector('#form-container').append(a)
}

function edit_housekeeping(pk){
    show_housekeepingForm();
    
    fetch(`/admin/room/housekeeping/info?pk=${pk}`)
    .then(response => response.json())
    .then(housekeeping => {
        document.querySelector('#form-container #id_room').selectedIndex = housekeeping.room.pk

        document.querySelector('#form-container #id_housekeeping_status').selectedIndex = housekeeping.housekeeping_status.pk

        document.querySelector('#form-container #id_assign_to').selectedIndex = housekeeping.assigned_to.pk
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    input.type = 'hidden';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/room/housekeeping/update/"

}

function delete_housekeeping(pk){
    if (confirm('Are you sure to delete this housekeeping?')){
        fetch()
        window.location.replace(`/admin/room/housekeeping/delete/?pk=${pk}`)
    }
}

function validation(elem){
    const data = new FormData(elem);

    fetch(elem.action,{
        method: 'POST',
        header: {
            'Content-Type': "multipart/form-data",
        },
        body: data,
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(message => {
        if (message.Result == 'Succeed')
            location.reload()
        else{
            alert(message.Result)

            document.querySelectorAll('label br').forEach(x => x.remove());
            document.querySelectorAll('label b').forEach(x => x.remove());

            const error =JSON.parse(message.error);
            for (const [key, value] of Object.entries(error)) {
                if (!document.querySelector(`label[for="id_${key}"] b`))
                    document.querySelector(`label[for="id_${key}"]`).innerHTML += `<br> <b style='color:red'> ${value[0]['message']}</b>`
            }
        }
    })
    return false;
}

document.querySelectorAll('#sub-menu input[type=checkbox').forEach(elem => {
    elem.onclick = () => {
        const parent = elem.parentElement.parentElement;
        let n_item = parseInt(parent.getAttribute('data-selected-item'));
        if (elem.checked)
            parent.setAttribute('data-selected-item', ++n_item);
        else
            parent.setAttribute('data-selected-item', --n_item);

        if (n_item > 0){
            parent.parentElement.style.background = "#057642"
            parent.parentElement.style.color = "white"
            parent.parentElement.querySelector('i').style.color = "white"
        }else{
            parent.parentElement.style.background = ""
            parent.parentElement.style.color = ""
            parent.parentElement.querySelector('i').style.color = "black"
        }
    }
})

document.addEventListener('click',(e) => { 
    document.querySelectorAll('.custom-select').forEach(elem => {
        if (elem != e.target && elem != e.target.parentElement && !elem.parentElement.contains(e.target))
            elem.parentElement.querySelector('#sub-menu').className = 'fade-in'
    })
})

function show_hide_sub_menu(elem){
    let subMenu = elem.parentElement.querySelector('#sub-menu')

    if (subMenu.className == 'fade-out'){
        subMenu.className = 'fade-in';
        setTimeout(() => {
            subMenu.style.display = 'none';
        },500)

    }
    else{
        subMenu.style.display = 'flex';
        subMenu.className = 'fade-out';         
    }

}