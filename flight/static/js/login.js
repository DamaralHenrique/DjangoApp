var LOGINS = [
    {
        id: "funcionario",
        name: "Arthur",
        password: "qwer",
        post: 1,
    },
    {
        id: "gerente",
        name: "Juliano",
        password: "qwer",
        post: 2,
    },
    {
        id: "operador",
        name: "Milenha",
        password: "qwer",
        post: 3,
    },

]

function login(){
    var id = document.getElementById('IdInput');
    var password = document.getElementById('PasswordInput');
    var name = "";
    var post = 0;
    var valid_login = false;
    LOGINS.forEach(element => {
        if(element.id == id.value && element.password == password.value){
            valid_login = true;
            name = element.name;
            post = element.post;
        }
    });

	if(valid_login){
        const url = "http://" + window.location.href.split('/')[2] + "/home";
        const nextState = { name, post };
        const nextTitle = "home";
        window.history.pushState(nextState, nextTitle, url);
    }else{
        alert("Credenciais inválidas");
    }
}