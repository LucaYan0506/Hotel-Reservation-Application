document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #rooms').style.color = 'white';
    load();
})

document.querySelector('#search-bar').addEventListener('keypress', e => {
    if (e.key == 'Enter'){
        start = 1;
        load();
    }
});

document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
};


function show_roomForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_roomForm(){
    location.reload('/admin/room/')
}

function create_row(room,i){
/*
<tr>
    <th scope="row">{{row.pk}}</th>
    <td>{{row.Title}}</td>
    <td>{{row.Short_Code}}</td>
    <td>
        <button class="btn" onclick="view_room(1)" style="border:solid 1px gray;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
            View
        </button>
        <button class="btn" onclick="edit_room(1)" style="color: #fff; background-color: #007bff; border-color: #007bff;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
            Edit
        </button>
        <button class="btn" onclick="delete_room(1)" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
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

    const td1 = document.createElement('td');
    td1.innerHTML = room.room_number;


    const td2 = document.createElement('td');
    td2.innerHTML = room.room_type;
   
    const td3 = document.createElement('td');
    td3.innerHTML = room.floor;

    const td4 = document.createElement('td');
    td4.innerHTML = `   
    <button class="btn" onclick="alert('working in progress')" style="background-color: #00b0ee; border-color: #00b0ee;color:white">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: white;padding-right: 2px;">home</i>
        Housekeeping
    </button>
    <button class="btn" onclick="edit_room(${room.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
        Edit
    </button>
    <button class="btn" onclick="delete_room(${room.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 2px;">delete</i>
        Delete
    </button>`;

    tr.append(th);
    tr.append(td1);
    tr.append(td2);
    tr.append(td3);
    tr.append(td4);

    document.querySelector('.table tbody').append(tr);
}

let start = 1;

function load(){
    let quantity = parseInt(document.querySelector('select').value);

    //clear table
    if (document.querySelectorAll('.table tbody *') != [])
        document.querySelectorAll('.table tbody *').forEach(element => {
            element.remove();
        });

    //clear btn-container
    if (document.querySelector('#btn-container'))
        document.querySelector('#btn-container').remove()
    let end = start + quantity - 1;
    let contain = document.querySelector('#search-bar').value;
    //show room
    fetch(`/admin/room/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.room.forEach(room => {
           create_row(room,i++);
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
        nextBtn.disabled = start > data.total_room;
        btn_container.append(nextBtn);

        const div_clear = document.createElement('div');
        div_clear.style.clear = "both";
        btn_container.append(div_clear);
    })

}

// The instanceReady event is fired when an instance of CKEditor 4 has finished
// its initialization.
CKEDITOR.on('instanceReady', function(ev) {
    editor = ev.editor;

    });
  
function edit_room(pk){
    show_roomForm();

    fetch(`/admin/room/info/?pk=${pk}`)
    .then(response => response.json())
    .then(room => {
        document.querySelector(`#form-container #id_room_type option[value='${room.room_type_pk}']`).selected = true;

        document.querySelector(`#form-container #id_floor option[value='${room.floor_pk}']`).selected = true;

        document.querySelector('#form-container #id_room_number').value = room.room_number;
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/room/update/"

}

function delete_room(pk){
    if (confirm('Are you sure to delete this room?')){
        fetch()
        window.location.replace(`/admin/room/delete/?pk=${pk}`)
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
            location.reload('/admin/room/')
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