function search(event) {
    if(event.keyCode == 13) {
        var searchTerm = document.getElementById('search-field').value;
        var colors = {
            'black':document.getElementById('search-black').checked ? 1 : 0,
            'blue':document.getElementById('search-blue').checked ? 1 : 0,
            'green':document.getElementById('search-green').checked ? 1 : 0,
            'red':document.getElementById('search-red').checked ? 1 : 0,
            'white':document.getElementById('search-white').checked ? 1 : 0
        }
        window.location.href = '/results?term='+searchTerm+'&colors='+JSON.stringify(colors);
    }
}