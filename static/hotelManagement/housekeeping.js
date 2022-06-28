document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #housekeeping-status').style.color = 'white';
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

document.querySelector('#form-container #id_image').addEventListener('change', () =>{
    const [file] = document.querySelector('#form-container #id_image').files
    if (file) {
        document.querySelector('form img').src =  URL.createObjectURL(file)
    }
})


function show_housekeepingForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_housekeepingForm(){
    location.reload('/admin/housekeeping/')
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

    const td1 = document.createElement('td');
    td1.innerHTML = housekeeping.name;


    const td2 = document.createElement('td');
    if (housekeeping.active)
        td2.innerHTML = 'Active';
    else
        td2.innerHTML = 'Inactive';

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
    //show housekeeping
    fetch(`/admin/housekeeping/info/?start=${start}&end=${end}&contain=${contain}`)
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

// The instanceReady event is fired when an instance of CKEditor 4 has finished
// its initialization.
CKEDITOR.on('instanceReady', function(ev) {
    editor = ev.editor;

    });
  

function view_housekeeping(pk){
    show_housekeepingForm();

    fetch(`/admin/housekeeping/info/?pk=${pk}`)
    .then(response => response.json())
    .then(housekeeping => {
        document.querySelector('#form-container #id_name').value = housekeeping.name;
        document.querySelector('#form-container #id_name').disabled = true;

        document.querySelector('#form-container #id_active').checked = housekeeping.active;
        document.querySelector('#form-container #id_active').disabled = true;

        editor.setData(housekeeping.description)
        editor.setReadOnly(true);

        document.querySelector('#form-container img').src = housekeeping.image;
        document.querySelector('#form-container #id_image').disabled = true;
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

    fetch(`/admin/housekeeping/info/?pk=${pk}`)
    .then(response => response.json())
    .then(housekeeping => {
        document.querySelector('#form-container #id_name').value = housekeeping.name;

        document.querySelector('#form-container #id_active').checked = housekeeping.active;

        editor.setData(housekeeping.description)

        document.querySelector('#form-container img').src = housekeeping.image;
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/housekeeping/update/"

}

function delete_housekeeping(pk){
    if (confirm('Are you sure to delete this housekeeping?')){
        fetch()
        window.location.replace(`/admin/housekeeping/delete/?pk=${pk}`)
    }
}



function validation(elem){
    const data = new FormData(elem);
    data.append('Description', editor.getData())
    
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
            location.reload('/admin/housekeeping/')
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