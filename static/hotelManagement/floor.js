document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #floors').style.color = 'white';
    load();
})

document.querySelector('#search-bar').addEventListener('keypress', e => {
    if (e.key == 'Enter'){
        start = 1;
        load();
    }
})

function show_floorForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_floorForm(){
    location.reload('/admin/floor/')
}

function create_row(floor,i){
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
    td1.innerHTML = floor.Name;

    const td2 = document.createElement('td');
    td2.innerHTML = floor.Number;

    const td3 = document.createElement('td');
    if (floor.Active)
        td3.innerHTML = 'Active';
    else
        td3.innerHTML = 'Inactive';

    const td4 = document.createElement('td');
    td4.innerHTML = `   
    <button class="btn" onclick="view_floor(${floor.pk})" style="border:solid 1px gray;">View</button>
    <button class="btn" onclick="edit_floor(${floor.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">Edit</button>
    <button class="btn" onclick="delete_floor(${floor.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">Delete</button>`;

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
    //show floor
    fetch(`/admin/floor/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.floor.forEach(floor => {
           create_row(floor,i++);
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
        nextBtn.disabled = start > data.total_floor;
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
  

function view_floor(pk){
    show_floorForm();

    fetch(`/admin/floor/info/?pk=${pk}`)
    .then(response => response.json())
    .then(floor => {
        document.querySelector('#form-container #id_Name').value = floor.Name;
        document.querySelector('#form-container #id_Name').disabled = true;

        document.querySelector('#form-container #id_Number').value = floor.Number;
        document.querySelector('#form-container #id_Number').disabled = true;

        document.querySelector('#form-container #id_Active').checked = floor.Active;
        document.querySelector('#form-container #id_Active').disabled = true;

        editor.setData(floor.Description)
        editor.setReadOnly(true);

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

function edit_floor(pk){
    show_floorForm();

    fetch(`/admin/floor/info/?pk=${pk}`)
    .then(response => response.json())
    .then(floor => {
        document.querySelector('#form-container #id_Name').value = floor.Name;

        document.querySelector('#form-container #id_Number').value = floor.Number;

        document.querySelector('#form-container #id_Active').checked = floor.Active;

        editor.setData(floor.Description)
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/floor/update/"

}

function delete_floor(pk){
    if (confirm('Are you sure to delete this floor?')){
        fetch()
        window.location.replace(`/admin/floor/delete/?pk=${pk}`)
    }
}



function validation(elem){
    const data = new URLSearchParams(new FormData(elem));
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
    fetch(elem.action,{
        method: 'POST',
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