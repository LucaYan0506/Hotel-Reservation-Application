document.addEventListener('DOMContentLoaded', () =>{   
    show_hideSubMenu(document.querySelector('.menu-option-container#hotel-configuration #menu-option'))
    document.querySelector('.menu-option-container#hotel-configuration #menu-option').style.background = 'rgb(0,95,112)';
    document.querySelector('.menu-option-container#hotel-configuration #sub-menu #price-manager').style.color = 'white';
    load();
})

document.querySelector('#search-bar').addEventListener('keypress', e => {
    if (e.key == 'Enter'){
        start = 1;
        load();
    }
})

function show_priceManagerForm(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_priceManagerForm(){
    if (typeof myWindow !== 'undefined')
        myWindow.close();
    location.reload();
}

function create_row(price_Manager,i){
    const tr = document.createElement('tr');

    const th = document.createElement('th');
    th.scope = "row";
    th.innerHTML = i;

    const td1 = document.createElement('td');
    td1.innerHTML = price_Manager.title;

    const td2 = document.createElement('td');
    td2.innerHTML = `£${price_Manager.mon}`;

    const td3 = document.createElement('td');
    td3.innerHTML = `£${price_Manager.tue}`;

    const td4 = document.createElement('td');
    td4.innerHTML = `£${price_Manager.wed}`;

    const td5 = document.createElement('td');
    td5.innerHTML = `£${price_Manager.thu}`;

    const td6 = document.createElement('td');
    td6.innerHTML = `£${price_Manager.fri}`;

    const td7 = document.createElement('td');
    td7.innerHTML = `£${price_Manager.sat}`;

    const td8 = document.createElement('td');
    td8.innerHTML = `£${price_Manager.sun}`;

    const td9 = document.createElement('td');
    td9.innerHTML = `   
    <button class="btn" onclick="edit_priceManager(${price_Manager.pk},'${price_Manager.type}')" style="color: #fff; background-color: #007bff; border-color: #007bff;">
        <i class="material-icons" style="vertical-align: text-top;font-size: 1rem;padding-right: 5px;">edit</i>
        Edit
    </button>`;

    tr.append(th);
    tr.append(td1);
    tr.append(td2);
    tr.append(td3);
    tr.append(td4);
    tr.append(td5);
    tr.append(td6);
    tr.append(td7);
    tr.append(td8);
    tr.append(td9);

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
    //show prices
    fetch(`/admin/priceManager/info/?start=${start}&end=${end}&contain=${contain}`)
    .then(response => response.json())
    .then(data =>{
        let i = start;
        data.price_Manager.forEach(price_Manager => {
           create_row(price_Manager,i++);
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
        nextBtn.disabled = start > data.total_price_Manager;
        btn_container.append(nextBtn);

        const div_clear = document.createElement('div');
        div_clear.style.clear = "both";
        btn_container.append(div_clear);
    })

}

function edit_priceManager(pk,type){
    show_priceManagerForm();

    fetch(`/admin/priceManager/info/?pk=${pk}&type=${type}`)
    .then(response => response.json())
    .then(price_Manager => {
        document.querySelector('#form-container h3').innerHTML = price_Manager.title
        document.querySelector('input#id_mon').value = price_Manager.mon;
        document.querySelector('input#id_tue').value = price_Manager.tue;
        document.querySelector('input#id_wed').value = price_Manager.wed;
        document.querySelector('input#id_thu').value = price_Manager.thu;
        document.querySelector('input#id_fri').value = price_Manager.fri;
        document.querySelector('input#id_sat').value = price_Manager.sat;
        document.querySelector('input#id_sun').value = price_Manager.sun;
    })

    const input = document.createElement('input');
    input.value = pk;
    input.type = "hidden"
    input.id = 'id_pk';
    input.name = 'pk';
    const input2 = document.createElement('input');
    input2.value = type;
    input2.type = "hidden"
    input2.id = 'id_type';
    input2.name = 'type';
    document.querySelector('form').append(input);
    document.querySelector('form').append(input2);
    document.querySelector('form').action = "/admin/priceManager/update/"

}


document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
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
            location.reload('/admin/priceManager/')
        else{
            alert(message.Result)
        }
    })

    return false;
}