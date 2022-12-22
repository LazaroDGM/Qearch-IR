const listButtoms = document.querySelectorAll(".bar .list li");
// const searchBarInput = document.getElementById("input[type='text']");
const searchBarInput = document.querySelector("#searchBar");
const searchBarContainer = document.querySelector("#searchBarContainer");
// const searchBarSimulator = document.querySelector("#searchBarSimulator");
const searchBarIcon = document.querySelector("#searchBarContainer .icon");
const searchBarIconSvg = document.querySelector("#searchBarContainer .icon svg");
const resultsGrid = document.querySelector("#resultsGrid");

let result_docs = [];
const console_log = console.log.bind(console);
const docs_per_page = 12

listButtoms.forEach(item => {
    item.onclick = function () {
        var selected_buttom = document.querySelector(".bar .list li.selected");
        if (selected_buttom != null) selected_buttom.classList.remove('selected');
        item.classList.add('selected');
    }
});

searchBarInput.addEventListener('focus', (event) => {

    searchBarIcon.classList.add("searching");
    event.target.style.padding = "10px";
    event.target.style.paddingLeft = "40px";
    // searchBarSimulator.style.height = '70px';
});
searchBarInput.addEventListener('blur', (event) => {
    // event.target.style.background = 'white';
    searchBarIcon.classList.remove('searching')
    event.target.style.padding = "5px";
    event.target.style.paddingLeft = "40px";
    // searchBarSimulator.style.height = '60px';
});
searchBarInput.addEventListener('input', (event) =>{
    // event.target.value = 'K'.fontcolor("white");
    
})
searchBarInput.addEventListener("keydown", (e) => {
    if(e.key == "Enter"){
        const query = searchBarInput.value;
        const page = 0;
        // FetchDataFromServer(0, query == "" ? "texts" : query);
        console.log(`query: ${query}`);
    }
});


// document.addEventListener('DOMContentLoaded', ()=>{
//     var results = document.querySelectorAll(".result")
//     results.forEach(item=>{
//         item.onclick = function(){
//             document.querySelector('#docIndexTitle').value = 
//         }
//     });
// })