document.addEventListener('keydown', function(e) {
    if(e.key == "Enter"){
      document.getElementById("btn-logar").click();
    }
});

function validaSenha(){
    $("#txt_senha").hide();
    $("#btn-cadastro").attr("disabled",true); 
    if($("#confirma_senha").val() != ''){
        $("#txt_senha").show();
        $("#txt_senha").html("As senhas não conferem!");
        $("#txt_senha").css("color","#f97d7d");
        $("#btn-cadastro").attr("disabled",true);
        if($("#confirma_senha").val() == $("#senha_cadastro").val()){
            $("#txt_senha").html("As senhas conferem");
            $("#txt_senha").css("color","#82ff82");
            $("#btn-cadastro").attr("disabled",false);
        }
    }
}

function validarUsuarioExistente(){
    var retorno_funcao;
    const objectData = {
        acao : 'validarUsuarioExistente',
        login : $("#usuario_cadastro").val(),
    }

    $.ajax({
            url: "controller.cgi",
            data: objectData,
            dataType: "json",
            type: "post",
            async: false,
            success: function(result)  {
                const retorno = result.retorno;
                if (retorno.length > 0) {
                  retorno_funcao = false;
                } else {
                  retorno_funcao = true;
                }
            },
    })
    return retorno_funcao;
}

$("#btn-cadastro").on("click", async function(e){
    if($("#usuario_cadastro").val() == ''){
        alert("Digite o login!");
        return false;
    }

    if($("#senha_cadastro").val() == ''){
        alert("Digite a senha!");
        return false;     
    }

    if($("#confirma_senha").val() == ''){
        alert("Digite a confirmação de senha!");
        return false;
    }

    if(!validarUsuarioExistente()){
        alert("Usuário ja existente! tente inserir outro");
        return false;
    }
    const objectData = {
        acao: 'cadastrarUsuario',
        login: $("#usuario_cadastro").val(),
        senha: $("#senha_cadastro").val(),
    }
    await $.ajax({
        url: "controller.cgi",
        data: objectData,
        type: "post",
        dataType : "json",
        success: function(result){
            alert(result.msg);
            if(result.status != "Sucesso"){
                return false;   
            }else{
                setTimeout(location.reload(), 1500);
            }
        },
    })
})

$("#btn-logar").on("click", async function(e){
    if($("#usuario").val() == ''){
        alert("Digite o login!");
        return false;
    }

    if($("#senha").val() == ''){
        alert("Digite a senha!");
        return false;     
    }
    const objectData = {
        acao: 'logarUsuario',
        login: $("#usuario").val(),
        senha: $("#senha").val(),
    }
    await $.ajax({
        url: "controller.cgi",
        data: objectData,
        type: "post",
        dataType : "json",
        success: function(result){
            if(result.retorno > 0){
                inserirLocalStorage($("#usuario").val());
            }else{
                alert("Login inválido! Tente novamente.");
            }
        },
    })
})

function removeAcento(text,campo)
{       

    var semAcento = text.normalize('NFD').replace(/[\u0300-\u036f]/g, "");

    $(campo).val(semAcento);
}

function inserirLocalStorage(usuario) {
    $.ajax({
      url: "controller.cgi",
      data: { acao: "validarUsuarioExistente", login: usuario },
      dataType: "json",
      type: "get",
      success: (result) => {
        const retorno = result.retorno;
       
        if (retorno.length > 0) {
           
          for (usuario of retorno) {
            const { id, login, permissoes, senha } = usuario;
            let codificado_login = Criptografa(login);
            let codificado_id = Criptografa(id);
            let codificado_permissoes = Criptografa(permissoes);
            let codificado_senha = Criptografa(senha);

            localStorage.setItem("usuario", codificado_login);
            localStorage.setItem("id", codificado_id);
            localStorage.setItem("permissoes", codificado_permissoes);
            localStorage.setItem("senha", codificado_senha);
            window.location.href = "http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/index.cgi";
          }
        }
      },
    });
}

function Criptografa(dados){
	var mensx="";
	var l;
	var i;
	var j=0;
	var ch;
	ch = "assbdFbdpdPdpfPdAAdpeoseslsQQEcDDldiVVkadiedkdkLLnm";
	for (i=0;i<dados.length; i++){
		j++;
		l=(Asc(dados.substr(i,1))+(Asc(ch.substr(j,1))));
		if (j==50){
			j=1;
		}
		if (l>255){
			l-=256;
		}
		mensx+=(Chr(l));
	}
	return mensx;
}

function Descriptografa(dados){
	var mensx="";
	var l;
	var i;
	var j=0;
	var ch;
	ch = "assbdFbdpdPdpfPdAAdpeoseslsQQEcDDldiVVkadiedkdkLLnm";
	for (i=0; i<dados.length;i++){
		j++;
		l=(Asc(dados.substr(i,1))-(Asc(ch.substr(j,1))));
		if (j==50){
			j=1;
		}
		if (l<0){
			l+=256;
		}
		mensx+=(Chr(l));
	}
	return mensx;
}

function Asc(String){
	return String.charCodeAt(0);
}
function Chr(AsciiNum){
	return String.fromCharCode(AsciiNum)
}