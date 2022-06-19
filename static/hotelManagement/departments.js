document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hr-management #menu-option'))
    document.querySelector('.menu-option-container#hr-management #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hr-management #sub-menu #departments').style.color = 'white';
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


function show_departmentsForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_departmentsForm(){
    location.reload('/admin/departments/')
}

function create_row(departments,i){
    const tr = document.createElement('tr');

    const th = document.createElement('th');
    th.scope = "row";
    th.innerHTML = i;

    const td1 = document.createElement('td');
    td1.innerHTML = departments.name;

    const td2 = document.createElement('td');
    td2.innerHTML = `   
    <button class="btn" onclick="view_departments(${departments.pk})" style="border:solid 1px gray;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
        View
    </button>
    <button class="btn" onclick="edit_departments(${departments.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
        Edit
    </button>
    <button class="btn" onclick="delete_departments(${departments.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 2px;">delete</i>
        Delete
    </button>`;

    tr.append(th);
    tr.append(td1);
    tr.append(td2);

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
    //show departments
    fetch(`/admin/departments/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.departments.forEach(departments => {
           create_row(departments,i++);
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
        nextBtn.disabled = start > data.total_departments;
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
  

function view_departments(pk){
    show_departmentsForm();

    fetch(`/admin/departments/info/?pk=${pk}`)
    .then(response => response.json())
    .then(departments => {
        document.querySelector('#form-container #id_name').value = departments.name;
        document.querySelector('#form-container #id_name').disabled = true;

        document.querySelector('#form-container #id_active').checked = departments.active;
        document.querySelector('#form-container #id_active').disabled = true;

        editor.setData(departments.description)
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

function edit_departments(pk){
    show_departmentsForm();

    fetch(`/admin/departments/info/?pk=${pk}`)
    .then(response => response.json())
    .then(departments => {
        document.querySelector('#form-container #id_name').value = departments.name;

        document.querySelector('#form-container #id_active').checked = departments.active;

        editor.setData(departments.description)

        document.querySelector('#form-container img').src = departments.image;
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/departments/update/"

}

function delete_departments(pk){
    if (confirm('Are you sure to delete this departments?')){
        fetch()
        window.location.replace(`/admin/departments/delete/?pk=${pk}`)
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
            location.reload('/admin/departments/')
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