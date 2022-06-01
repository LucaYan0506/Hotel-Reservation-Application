document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #room-types').style.color = 'white';
    load();
})

document.querySelector('#search-bar').addEventListener('keypress', e => {
    if (e.key == 'Enter'){
        start = 1;
        load();
    }
})

document.querySelector('#form-container #id_image').addEventListener('change', () =>{
    const [file] = document.querySelector('#form-container #id_image').files
    if (file) {
        document.querySelector('form img').src =  URL.createObjectURL(file)
    }
})

function show_roomTypesForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_roomTypesForm(){
    location.reload('/admin/room_types/')
}

function create_row(room_type,i){
/*
<tr>
    <th scope="row">{{row.pk}}</th>
    <td>{{row.Title}}</td>
    <td>{{row.Short_Code}}</td>
    <td>
        <button class="btn" style="border:solid 1px gray;">View</button>
        <button class="btn" style="color: #fff; background-color: #007bff; border-color: #007bff;">Edit</button>
        <button class="btn" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">Delete</button>
    </td>
</tr>
*/
    const tr = document.createElement('tr');

    const th = document.createElement('th');
    th.scope = "row";
    th.innerHTML = i;

    const td1 = document.createElement('td');
    td1.innerHTML = room_type.Title;

    const td2 = document.createElement('td');
    td2.innerHTML = room_type.Short_Code;

    const td3 = document.createElement('td');
    td3.innerHTML = `   
    <button class="btn" onclick="view_roomType(${room_type.pk})" style="border:solid 1px gray;">View</button>
    <button class="btn" onclick="edit_roomType(${room_type.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">Edit</button>
    <button class="btn" onclick="delete_roomType(${room_type.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">Delete</button>`;

    tr.append(th);
    tr.append(td1);
    tr.append(td2);
    tr.append(td3);

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
    //show room types
    fetch(`/admin/room_types/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.room_type.forEach(room_type => {
           create_row(room_type,i++);
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
        nextBtn.disabled = start > data.total_room_type;
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
  
function view_roomType(pk){
    show_roomTypesForm();

    fetch(`/admin/room_types/info/?pk=${pk}`)
    .then(response => response.json())
    .then(room_type => {
        document.querySelector('#form-container #id_Title').value = room_type.Title;
        document.querySelector('#form-container #id_Title').disabled = true;

        document.querySelector('#form-container #id_Short_Code').value = room_type.Short_Code;
        document.querySelector('#form-container #id_Short_Code').disabled = true;

        editor.setData(room_type.Description)
        editor.setReadOnly(true);

        document.querySelector('#form-container #id_Base_Occupancy').value = room_type.Base_Occupancy;
        document.querySelector('#form-container #id_Base_Occupancy').disabled = true;

        document.querySelector('#form-container #id_Max_Occupancy').value = room_type.Max_Occupancy;
        document.querySelector('#form-container #id_Max_Occupancy').disabled = true;

        document.querySelector('#form-container #id_Extra_Bed').value = room_type.Extra_Bed;
        document.querySelector('#form-container #id_Extra_Bed').disabled = true;

        document.querySelector('#form-container #id_Kids_Occupancy').value = room_type.Kids_Occupancy;
        document.querySelector('#form-container #id_Kids_Occupancy').disabled = true;

        document.querySelector('#form-container #id_Amenities').value = room_type.Amenities;
        document.querySelector('#form-container #id_Amenities').disabled = true;

        document.querySelector('#form-container #id_Base_Price').value = room_type.Base_Price;
        document.querySelector('#form-container #id_Base_Price').disabled = true;

        document.querySelector('#form-container #id_Additional_Person_Price').value = room_type.Additional_Person_Price;
        document.querySelector('#form-container #id_Additional_Person_Price').disabled = true;

        document.querySelector('#form-container #id_Extra_Bed_Price').value = room_type.Extra_Bed_Price;
        document.querySelector('#form-container #id_Extra_Bed_Price').disabled = true;

        document.querySelector('#form-container #id_image').disabled = true;

        document.querySelector('form img').src = room_type.Image
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

function edit_roomType(pk){
    show_roomTypesForm();

    fetch(`/admin/room_types/info/?pk=${pk}`)
    .then(response => response.json())
    .then(room_type => {
        document.querySelector('#form-container #id_Title').value = room_type.Title;

        document.querySelector('#form-container #id_Short_Code').value = room_type.Short_Code;

        editor.setData(room_type.Description)

        document.querySelector('#form-container #id_Base_Occupancy').value = room_type.Base_Occupancy;

        document.querySelector('#form-container #id_Max_Occupancy').value = room_type.Max_Occupancy;

        document.querySelector('#form-container #id_Extra_Bed').value = room_type.Extra_Bed;

        document.querySelector('#form-container #id_Kids_Occupancy').value = room_type.Kids_Occupancy;

        document.querySelector('#form-container #id_Amenities').value = room_type.Amenities;

        document.querySelector('#form-container #id_Base_Price').value = room_type.Base_Price;

        document.querySelector('#form-container #id_Additional_Person_Price').value = room_type.Additional_Person_Price;

        document.querySelector('#form-container #id_Extra_Bed_Price').value = room_type.Extra_Bed_Price;

        document.querySelector('form img').src = room_type.Image
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/room_types/update/"

}

function delete_roomType(pk){
    if (confirm('Are you sure to delete this Room Type?')){
        fetch()
        window.location.replace(`/admin/room_types/delete/?pk=${pk}`)
    }
}

document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
}

function validation(elem){
    const data = new FormData(elem);
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
    
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
            location.reload('/admin/room_types/')
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