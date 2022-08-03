document.addEventListener('DOMContentLoaded', () =>{
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #coupon-management').style.color = 'white';
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    load();
})

document.querySelector('#add-image').onclick = () => {
    myWindow = window.open(`http://${location.host}/admin/image/`,'popUpWindow','height=500,width=400,left=100,top=100');
};

document.querySelector('#search-bar').addEventListener('keypress', e => {
    if (e.key == 'Enter'){
        start = 1;
        load();
    }
});

document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
};

//li of user, room-type and hall-type
document.querySelectorAll('.options li').forEach(el => {
    el.onclick = () => {li_click(el)};
})

function li_click(el){
    let parentclassName = el.parentElement.parentElement.className;
    let className = "";

    parentclassName.split(' ').forEach(el => {
        className += `.${el}`;
    })
    
    if (el.parentElement.parentElement.id == 'group-1'){
        const newEl = document.createElement('li');
        newEl.innerHTML = el.innerHTML;
        newEl.value = el.value;
        newEl.onclick = () => {li_click(newEl)};
        el.parentElement.removeChild(el);

        document.querySelector(`${className}#group-2 ul`).appendChild(newEl);
    }else{
        const newEl = document.createElement('li');
        newEl.innerHTML = el.innerHTML;
        newEl.value = el.value;
        newEl.onclick = () => {li_click(newEl)};
        el.parentElement.removeChild(el);

        document.querySelector(`${className}#group-1 ul`).appendChild(newEl);
    }
}

function show_couponForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_couponForm(){
    if (typeof myWindow !== 'undefined')
        myWindow.close();
    location.reload();
}

function create_row(coupon,i){
    const tr = document.createElement('tr');

    const th = document.createElement('th');
    th.scope = "row";
    th.innerHTML = i;

    const td1 = document.createElement('td');
    td1.innerHTML = coupon.title;


    const td2 = document.createElement('td');
    if (coupon.active)
        td2.innerHTML = 'Active';
    else
        td2.innerHTML = 'Inactive';

    const td3 = document.createElement('td');
    td3.innerHTML = `   
    <button class="btn" onclick="view_coupon(${coupon.pk})" style="border:solid 1px gray;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;color: black;padding-right: 2px;">remove_red_eye</i>
        View
    </button>
    <button class="btn" onclick="edit_coupon(${coupon.pk})" style="color: #fff; background-color: #007bff; border-color: #007bff;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
        Edit
    </button>
    <button class="btn" onclick="delete_coupon(${coupon.pk})" style="color: #fff; background-color: #dc3545; border-color: #dc3545;">
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
    //show coupon
    fetch(`/admin/coupon/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.coupon.forEach(coupon => {
           create_row(coupon,i++);
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
        nextBtn.disabled = start > data.total_coupon;
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
  

function view_coupon(pk){
    show_couponForm();

    fetch(`/admin/coupon/info/?pk=${pk}`)
    .then(response => response.json())
    .then(coupon => {
        document.querySelector('#form-container #id_title').value = coupon.title;
        document.querySelector('#form-container #id_title').disabled = true;

        editor.setData(coupon.description)
        editor.setReadOnly(true);

        document.querySelector('#form-container #id_start_datetime').value = coupon.start_datetime.substring(0,16);
        document.querySelector('#form-container #id_start_datetime').disabled = true;

        document.querySelector('#form-container #id_end_datetime').value = coupon.end_datetime.substring(0,16);
        document.querySelector('#form-container #id_end_datetime').disabled = true;

        document.querySelector('#form-container #id_coupon_code').value = coupon.coupon_code;
        document.querySelector('#form-container #id_coupon_code').disabled = true;

        document.querySelector('#form-container #id_coupon_type').value = coupon.coupon_type;
        document.querySelector('#form-container #id_coupon_type').disabled = true;

        document.querySelector('#form-container #id_coupon_value').value = coupon.coupon_value;
        document.querySelector('#form-container #id_coupon_value').disabled = true;

        document.querySelector('#form-container #id_minimum_amount').value = coupon.minimum_amount;
        document.querySelector('#form-container #id_minimum_amount').disabled = true;

        document.querySelector('#form-container #id_valid_only_once').checked = coupon.valid_only_once;
        document.querySelector('#form-container #id_valid_only_once').disabled = true;

        coupon.image.forEach(image => {
            const option = document.createElement('option');
            option.value = image.pk;
            option.innerHTML = image.name;
            document.querySelector('form #id_image').append(option);
        })

        document.querySelector('#form-container .customer#group-1').style = 'pointer-events: none;'
        document.querySelector('#form-container .customer#group-2').style = 'pointer-events: none;'
        coupon.customer.forEach(x => {
            document.querySelector(`#form-container .customer#group-1 ul li[value="${x.pk}"]`).click();
        })

        document.querySelector('#form-container .room-type#group-1').style = 'pointer-events: none;'
        document.querySelector('#form-container .room-type#group-2').style = 'pointer-events: none;'
        coupon.room_type.forEach(x => {
            document.querySelector(`#form-container .room-type#group-1 ul li[value="${x.pk}"]`).click();
        })

        document.querySelector('#form-container .hall-type#group-1').style = 'pointer-events: none;'
        document.querySelector('#form-container .hall-type#group-2').style = 'pointer-events: none;'
        coupon.hall_type.forEach(x => {
            document.querySelector(`#form-container .hall-type#group-1 ul li[value="${x.pk}"]`).click();
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

function edit_coupon(pk){
    show_couponForm();

    fetch(`/admin/coupon/info/?pk=${pk}`)
    .then(response => response.json())
    .then(coupon => {
        document.querySelector('#form-container #id_title').value = coupon.title;

        editor.setData(coupon.description)

        document.querySelector('#form-container #id_start_datetime').value = coupon.start_datetime.substring(0,16);

        document.querySelector('#form-container #id_end_datetime').value = coupon.end_datetime.substring(0,16);

        document.querySelector('#form-container #id_coupon_code').value = coupon.coupon_code;

        document.querySelector('#form-container #id_coupon_type').value = coupon.coupon_type;

        document.querySelector('#form-container #id_coupon_value').value = coupon.coupon_value;

        document.querySelector('#form-container #id_minimum_amount').value = coupon.minimum_amount;

        document.querySelector('#form-container #id_valid_only_once').checked = coupon.valid_only_once;

        coupon.image.forEach(image => {
            const option = document.createElement('option');
            option.value = image.pk;
            option.innerHTML = image.name;
            document.querySelector('form #id_image').append(option);
        })

        coupon.customer.forEach(x => {
            document.querySelector(`#form-container .customer#group-1 ul li[value="${x.pk}"]`).click();
        })

        coupon.room_type.forEach(x => {
            document.querySelector(`#form-container .room-type#group-1 ul li[value="${x.pk}"]`).click();
        })

        coupon.hall_type.forEach(x => {
            document.querySelector(`#form-container .hall-type#group-1 ul li[value="${x.pk}"]`).click();
        })
    })

    const input = document.querySelector('input');
    input.value = pk;
    input.style.display = 'none';
    input.id = 'id_pk';
    input.name = 'pk';
    document.querySelector('form').append(input);
    document.querySelector('form').action = "/admin/coupon/update/"

}

function delete_coupon(pk){
    if (confirm('Are you sure to delete this coupon?')){
        fetch()
        window.location.replace(`/admin/coupon/delete/?pk=${pk}`)
    }
}



function validation(elem){
    const data = new FormData(elem);
    data.append('description', editor.getData())
    document.querySelectorAll('#id_image option').forEach(elem =>{
        data.append('image', parseInt(elem.value));
    });

    document.querySelectorAll('#form-container #group-2 ul li').forEach(el => {
        let parentclassName = el.parentElement.parentElement.className.split(' ')[1]
        data.append(parentclassName, el.value)
    })

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
            location.reload('/admin/coupon/')
        else{
            alert(message.Result)
            document.querySelectorAll('label br').forEach(x => x.remove());
            document.querySelectorAll('label b').forEach(x => x.remove());

            const error =JSON.parse(message.error);
            for (const [key, value] of Object.entries(error)) {
                console.log(key);
                console.log(value);
                if (!document.querySelector(`label[for="id_${key}"] b`))
                    document.querySelector(`label[for="id_${key}"]`).innerHTML += `<br> <b style='color:red'> ${value[0]['message']}</b>`
            }
        }
    })
    return false;
}