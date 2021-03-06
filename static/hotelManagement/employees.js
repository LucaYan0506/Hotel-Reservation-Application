document.addEventListener('DOMContentLoaded', () =>{
    show_hideSubMenu(document.querySelector('.menu-option-container#hr-management #menu-option'))
    document.querySelector('.menu-option-container#hr-management #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hr-management #sub-menu #employees').style.color = 'white';
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

//user-permission
document.querySelectorAll('.user-permission li').forEach(el => {
    el.onclick = () => {li_click(el)};
})

function li_click(el){
    if (el.parentElement.parentElement.id == 'group-1'){
        const newEl = document.createElement('li');
        newEl.innerHTML = el.innerHTML;
        newEl.value = el.value;
        newEl.onclick = () => {li_click(newEl)};
        el.parentElement.removeChild(el);
        document.querySelector('#group-2 ul').appendChild(newEl);
    }else{
        const newEl = document.createElement('li');
        newEl.innerHTML = el.innerHTML;
        newEl.value = el.value;
        newEl.onclick = () => {li_click(newEl)};
        el.parentElement.removeChild(el);
        document.querySelector('#group-1 ul').appendChild(newEl);
    }
}

function show_employeesForm(){
    document.querySelector('#form-container #id_pk').style.display = "none";
    document.querySelector('label[for="id_pk"').style.display = "none";
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_employeesForm(){
    document.querySelector('#table-container').style.display = 'block';   
    document.querySelector('#form-container').style.display = 'none';   
}

function create_row(employees,i){
/*
<tr>
    <th scope="row">{{row.pk}}</th>
    <td>{{row.Title}}</td>
    <td>{{row.Short_Code}}</td>
    <td>
        <button class="btn" onclick="view_employees(1)" style="border:solid 1px gray;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
            View
        </button>
        <button class="btn" onclick="edit_employees(1)" style="color: #fff; background-color: #007bff; border-color: #007bff;">
            <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
            Edit
        </button>
        <button class="btn" onclick="delete_employees(1)" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
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
    td1.innerHTML = employees.username;

    const td2 = document.createElement('td');
    td2.innerHTML = employees.position.name;

    const td3 = document.createElement('td');
    td3.innerHTML = employees.pk;

    const td4 = document.createElement('td');
    td4.innerHTML = `   
    <button class="btn" onclick="view_employees(${employees.pk})" style="border:solid 1px gray;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
        View
    </button>
    <button class="btn" onclick="edit_employees(${employees.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
        Edit
    </button>
    <button class="btn" onclick="delete_employees(${employees.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
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
    //show employees
    fetch(`/admin/employees/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.employees.forEach(employees => {
           create_row(employees,i++);
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
        nextBtn.disabled = start > data.total_employees;
        btn_container.append(nextBtn);

        const div_clear = document.createElement('div');
        div_clear.style.clear = "both";
        btn_container.append(div_clear);
    })

}


function view_employees(pk){
    show_employeesForm();

    fetch(`/admin/employees/info/?pk=${pk}`)
    .then(response => response.json())
    .then(employees => {
        document.querySelector('#form-container #id_pk').style.display = "";
        document.querySelector('label[for="id_pk"').style.display = "";
        document.querySelector('#form-container #id_pk').value = employees.pk;
        document.querySelector('#form-container #id_pk').disabled = true;

        document.querySelector('#form-container #id_title').value = employees.title;
        document.querySelector('#form-container #id_title').disabled = true;
        
        document.querySelector('#form-container #id_gender').value = employees.gender;
        document.querySelector('#form-container #id_gender').disabled = true;
        
        document.querySelector('#form-container #id_first_name').value = employees.first_name;
        document.querySelector('#form-container #id_first_name').disabled = true;
        
        document.querySelector('#form-container #id_last_name').value = employees.last_name;
        document.querySelector('#form-container #id_last_name').disabled = true;
        
        document.querySelector('#form-container #id_username').value = employees.username;
        document.querySelector('#form-container #id_username').disabled = true;
        
        document.querySelector('#form-container #id_email').value = employees.email;
        document.querySelector('#form-container #id_email').disabled = true;
        
        document.querySelector('#form-container #id_password').value = '********************';
        document.querySelector('#form-container #id_password').disabled = true;
        
        document.querySelector('#form-container #id_confirm_password').value = '********************';
        document.querySelector('#form-container #id_confirm_password').disabled = true;

        document.querySelector('#form-container #id_date_of_birth').value = employees.date_of_birth;
        document.querySelector('#form-container #id_date_of_birth').disabled = true;
        
        document.querySelector('#form-container #id_country_calling_code').value = employees.country_calling_code;
        document.querySelector('#form-container #id_country_calling_code').disabled = true;

        document.querySelector('#form-container #id_phone_number').value = employees.phone_number;
        document.querySelector('#form-container #id_phone_number').disabled = true;

        document.querySelector('#form-container #id_department').value = employees.department.pk;
        document.querySelector('#form-container #id_department').disabled = true;

        document.querySelector('#form-container #id_position').value = employees.position.pk;
        document.querySelector('#form-container #id_position').disabled = true;

        document.querySelector('#form-container #id_country').value = employees.country;
        document.querySelector('#form-container #id_country').disabled = true;

        document.querySelector('#form-container #id_city').value = employees.city;
        document.querySelector('#form-container #id_city').disabled = true;

        document.querySelector('#form-container #id_address').value = employees.address;
        document.querySelector('#form-container #id_address').disabled = true;

        document.querySelector('#form-container img').src = employees.image;
        document.querySelector('#form-container #id_image').disabled = true;

        document.querySelector('#form-container .user-permission#group-1').style = 'pointer-events: none;'
        document.querySelector('#form-container .user-permission#group-2').style = 'pointer-events: none;'
        employees.user_permission.forEach(x => {
            document.querySelector(`#form-container .user-permission#group-1 ul li[value="${x.pk}"]`).click();
        })
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

function edit_employees(pk){
    show_employeesForm();

    fetch(`/admin/employees/info/?pk=${pk}`)
    .then(response => response.json())
    .then(employees => {
        document.querySelector('#form-container #id_pk').style.display = "";
        document.querySelector('label[for="id_pk"').style.display = "";
        document.querySelector('#form-container #id_pk').value = employees.pk;
        document.querySelector('#form-container #id_pk').disabled = true;

        document.querySelector('#form-container #id_title').value = employees.title;
        
        document.querySelector('#form-container #id_gender').value = employees.gender;
        
        document.querySelector('#form-container #id_first_name').value = employees.first_name;
        
        document.querySelector('#form-container #id_last_name').value = employees.last_name;
        
        document.querySelector('#form-container #id_username').value = employees.username;
        
        document.querySelector('#form-container #id_email').value = employees.email;
        
        document.querySelector('#form-container #id_password').value = '********************';
        document.querySelector('#form-container #id_password').disabled = true;
        
        document.querySelector('#form-container #id_confirm_password').value = '********************';
        document.querySelector('#form-container #id_confirm_password').disabled = true;

        document.querySelector('#form-container #id_date_of_birth').value = employees.date_of_birth;
        
        document.querySelector('#form-container #id_country_calling_code').value = employees.country_calling_code;

        document.querySelector('#form-container #id_phone_number').value = employees.phone_number;

        document.querySelector('#form-container #id_department').value = employees.department.pk;

        document.querySelector('#form-container #id_position').value = employees.position.pk;

        document.querySelector('#form-container #id_country').value = employees.country;

        document.querySelector('#form-container #id_city').value = employees.city;

        document.querySelector('#form-container #id_address').value = employees.address;

        document.querySelector('#form-container img').src = employees.image;

        employees.user_permission.forEach(x => {
            document.querySelector(`#form-container .user-permission#group-1 ul li[value="${x.pk}"]`).click();
        })
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/employees/update/"

}

function delete_employees(pk){
    if (confirm('Are you sure to delete this employees?')){
        fetch()
        window.location.replace(`/admin/employees/delete/?pk=${pk}`)
    }
}

function validation(elem){  
    const data = new FormData(elem);
    let list = '';
    document.querySelectorAll('#form-container .user-permission#group-2 ul li').forEach(x => {
        list += x.value;
    })
    data.append('user_permission',list)

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
            location.reload('/admin/employees/')
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