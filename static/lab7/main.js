function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
            
            // Ячейка с названиями (русское + оригинальное)
            let tdTitles = document.createElement('td');
            let titleContainer = document.createElement('div');
            titleContainer.className = 'title-container';
            
            let russianTitle = document.createElement('div');
            russianTitle.className = 'russian-title';
            russianTitle.innerText = films[i].title_ru;
            
            let originalTitle = document.createElement('div');
            originalTitle.className = 'original-title';

            if (films[i].title && films[i].title !== films[i].title_ru) {
                originalTitle.innerText = `(${films[i].title})`;
            }
            
            titleContainer.appendChild(russianTitle);
            titleContainer.appendChild(originalTitle);
            tdTitles.appendChild(titleContainer);
            
            let tdYear = document.createElement('td');
            tdYear.innerText = films[i].year;
            
            let tdActions = document.createElement('td');
            
            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };
            
            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };
            
            tdActions.append(editButton);
            tdActions.append(delButton);
            
            tr.append(tdTitles);  
            tr.append(tdYear);    
            tr.append(tdActions); 
            
            tbody.append(tr);
        }
    })
}

// Остальные функции остаются без изменений...
function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function () {
        fillFilmList();
    });
}

function showModal() {
    document.getElementById('description-error').innerText = "";
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = "";
    document.getElementById('title').value = "";
    document.getElementById('title_ru').value = "";
    document.getElementById('year').value = "";
    document.getElementById('description').value = "";
    document.getElementById('description-error').innerText = "";
    showModal();
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        document.getElementById('description-error').innerText = "";
        showModal();
    });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };
    
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.description)
            document.getElementById('description-error').innerText = errors.description;
        if(errors.title_ru)
            document.getElementById('description-error').innerText = errors.title_ru;
    });
}