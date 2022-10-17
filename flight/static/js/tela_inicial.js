const id_funcao = localStorage.getItem('post');

if(id_funcao == 1) {
    document.getElementById("flight-monitor").style.visibility="hidden";
    document.getElementById("flight-monitor").style.position="absolute";

    document.getElementById("flight-report").style.visibility="hidden";
    document.getElementById("flight-report").style.position="absolute";
}

if(id_funcao == 2) {
    document.getElementById("flight-manegement").style.visibility="hidden";
    document.getElementById("flight-manegement").style.position="absolute";

    document.getElementById("flight-report").style.visibility="hidden";
    document.getElementById("flight-report").style.position="absolute";
}

if(id_funcao == 3) {
    document.getElementById("flight-monitor").style.visibility="hidden";
    document.getElementById("flight-monitor").style.position="absolute";

    document.getElementById("flight-manegement").style.visibility="hidden";
    document.getElementById("flight-manegement").style.position="absolute";
}