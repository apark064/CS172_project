
function getInputValue(){
    let seed_url; // = prompt("what is the seed_url?");
    let query; // = prompt("Query: ");

    seed_url = document.getElementById("input_url").value;
    query = document.getElementById("input_query").value;

    console.log(seed_url)
    console.log(query)
}




//var h1 = document.createElement('h1');
//var h2 = document.createElement('h2');

//textSeed = document.createTextNode('seed_URL: ' + seed_url)
//textQuery = document.createTextNode('Query: ' + query)

//h1.setAttribute('id', 'seed');
//h1.appendChild(textSeed)
//document.getElementById('flex-box-result').appendChild(h1)
// pass seed_url
// pass query