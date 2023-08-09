async function loadIntoSelect(url, select) {
    let response = await fetch(url);
    let data = await response.json();
    console.log(data);
    let option;
    Object.keys(data).forEach(function (key) {
        console.log(key, data[key])
        option = document.createElement('option');
        option.text = key;
        select.add(option);
    });
}

loadIntoSelect("http://hamster.nax.lol:8201/charge-codes", document.getElementById('shorthand'));
