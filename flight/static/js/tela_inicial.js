const state = window.history.state;

alert(state);

if(state.post == 1) {
    document.getElementById("flight-monitor").style.visibility="hidden";
    document.getElementById("flight-monitor").style.position="absolute";

    document.getElementById("flight-report").style.visibility="hidden";
    document.getElementById("flight-report").style.position="absolute";
}

if(state.post == 2) {
    document.getElementById("flight-manegement").style.visibility="hidden";
    document.getElementById("flight-manegement").style.position="absolute";

    document.getElementById("flight-report").style.visibility="hidden";
    document.getElementById("flight-report").style.position="absolute";
}

if(state.post == 3) {
    document.getElementById("flight-monitor").style.visibility="hidden";
    document.getElementById("flight-monitor").style.position="absolute";

    document.getElementById("flight-manegement").style.visibility="hidden";
    document.getElementById("flight-manegement").style.position="absolute";
}