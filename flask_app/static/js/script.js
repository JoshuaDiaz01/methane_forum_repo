
// fetch("https://global-warming.org/api/methane-api")
fetch("/api/thought/new")
    .then(response => response.json() )
    .then(data => {
        console.log(data)
        //do something with data below
    })
    .catch(err => console.log(err) ) //see errors that happen

fetch("/api/thought/<int:id>/edit")
    .then(response => response.json() )
    .then(data => {
        console.log(data)
        //do something with data below
    })
    .catch(err => console.log(err) ) //see errors that happen


fetch("/api/thought/<int:id>")
    .then(response => response.json())
    .then(data => {
        console.log(data)
        //do something with data below
    })
    .catch(err => console.log(err) ) //see errors that happen


fetch("https://global-warming.org/api/methane-api")
    .then(response => response.json())
    .then(data => console.log(data))//do something with data below
    .catch(err => console.log(err) ) //see errors that happen

