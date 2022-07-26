document.addEventListener('DOMContentLoaded',() => {
    opener.document.querySelectorAll('#id_image option').forEach(elem => {
        document.querySelector(`div[data-image_pk="${elem.value}"]`).click();
    })
    const option = document.createElement('option');
    option.innerHTML = "create a new folder";
    option.value = -1;
    document.querySelector('form #id_folder').append(option);
})

document.querySelector('form #id_folder').onchange = e => {
    if (e.target.value == '-1'){
        let folder_name = prompt("Please enter the name of the new folder", "new folder");
        document.querySelector('option[value="-1"]').innerHTML = folder_name;
    }
}

document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
}

document.querySelector('#folder').onchange = (e) => {
    window.location.href = `#${e.target.value}`;
}

document.querySelector('#folder').onfocus = (e) => {
    e.target.selectedIndex = -1;
}

document.querySelectorAll('.images div').forEach(elem => {
    elem.onclick = (e) => {
        if (e.target.tagName == 'BUTTON')
            return;
        if (elem.dataset.selected == 'false'){
            elem.style.background = "#3d3d3d";
            elem.querySelector('figure').style.background = "#3d3d3d";
            elem.querySelector('span').style.color = "#fff";
            elem.querySelector('img').style.opacity = "0.2";
            elem.dataset.selected = 'true';
        }else{
            elem.style.background = "";
            elem.querySelector('figure').style.background = "";
            elem.querySelector('img').style.opacity = "";
            elem.querySelector('span').style.color = "";
            elem.dataset.selected = 'false';  
        }

    }
})

function post_value(){
    opener.document.querySelector('#id_image').innerHTML = "";

    document.querySelectorAll('.images div').forEach(elem => {
        if (elem.dataset.selected == 'true'){
            const img = document.createElement('option');
            img.innerText = elem.querySelector('span').innerText;
            img.value = elem.dataset.image_pk;
            opener.document.querySelector('#id_image').append(img);
        }
    })

    self.close();
}

function show_Form(){
    document.querySelector('#table-container').style.display = 'none';   
    document.querySelector('#form-container').style.display = 'block';   
}

function hide_Form(){
    location.reload();
}

function validation(elem){
    const data = new FormData(elem);
    if (document.querySelector('form select').value = '-1'){
        data.append('folder_name',document.querySelector('option[value="-1"]').innerHTML)
    }
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

function deleteImage(pk){
    if (confirm("Are you sure to delete this image?"))
        location.href = `/admin/image/delete?pk=${pk}`;
}