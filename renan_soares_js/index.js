//FUNÇÃO PARA DESLOGAR APÓS UM TEMPO DE INATIVIDADE
seg = 0;
document.addEventListener("mousemove", function(){  
  seg = 0;
});

setInterval(function(){ 
  seg = seg + 1; 
  if(seg == 600){
    alert("Deslogado por inatividade!");
    window.location.href = "http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/login.cgi";
    localStorage.removeItem("usuario");
    localStorage.removeItem("id");
    localStorage.removeItem("permissoes");
    localStorage.removeItem("senha");
  }
   
}, 1000);

//AO INICIAR A TELA
$(document).ready(function(){
    $("#data_nasc").mask("99/99/9999");
    $("#tel1").mask("(99) 9999-9999");
    $("#tel2").mask("(99) 99999-9999");
    $("#cpf").mask("999.999.999-99");
    $("#rg").mask("99.999.999-9");
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const permissoes = Descriptografa(localStorage.getItem("permissoes"));
    const senha = Descriptografa(localStorage.getItem("senha"));

    validarUsuarioExistente(usuario_acesso,senha);

    $("#botaoPerfil").hide();
    if(permissoes == 1){
        $(".container").css("background-image", "linear-gradient(10deg, rgb(253, 101, 0), rgb(72 38 255), rgb(0 0 0))");
        $("#foto").css("width","77%");
        $(".menu").css("background", "#202020");
        $(".box").css("background", "#202020");
        $(".box").css("box-shadow","3px 0px 9px white");
        $(".modal-content").css("box-shadow","2px 4px 15px white");
        $("#foto2").attr("src","http://manager.qa.kabumdev.com.br/conteudo/js/informatica/renan_soares/logo-kabum-adm2.jpeg");
        $("#foto2").css("border-radius","114px");
        $("#foto2").css("width","10%");
        $(".modal-content").css("background","linear-gradient(to right,#000000, #182370)");
        $("#botaoPerfil").show();
    }
    $("#usuario_logado").html(usuario_acesso);
    if (!usuario_acesso) {
        window.location.href =
        "http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/login.cgi";    
    }
    ConsultaCliente();
});

document.addEventListener('keydown', function(e) {
    if(e.key == "Enter"){
        ConsultaCliente();
    }
});

// INÍCIO FUNÇÕES REFERENTE AO CLIENTE
async function ConsultaCliente(){
    const permissao = Descriptografa(localStorage.getItem("permissoes"));
    const id_usuario = Descriptografa(localStorage.getItem("id"));
    const $divLoading = $("#div-loading");
    const $divNadaEncontrado = $("#div-nada-encontrado");
    var campo = $("#campo").val();
    var ativo_inativo ;
    var cor_thead;
    valor = $("#valor").val();
    if(campo == 'ativo'){
        valor = $("#ativos_inativos").val();
    }

    if(campo == 'data_nascimento'){
        valor = valor.split('/').reverse().join('-');
    }
    await $.ajax({
        url: 'controller.cgi',
        data: {acao: 'listarClientes',campo:campo,valor:valor,permissoes:permissao,id_usuario:id_usuario},
        dataType: 'json',
        method: 'POST',
        beforeSend: () => $divLoading.show(),
        complete: () => $divLoading.hide(),
        success: result => {
            const retorno = result.retorno;
            if(retorno.length > 0){
                $divNadaEncontrado.hide();
                let htmlTable = ``;
                    if(permissao == 1){
                        cor_thead = '#202020';
                    }else{
                        cor_thead = '#0267B5';
                    }
                    htmlTable += `                    
                    <table class="table" id="tabela_consulta_cliente">
                        <thead class="thead_cliente" style="position: sticky;top: 0;background: ${cor_thead};">
                            <tr>
                                <th>Ativar/Desativar</th>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>RG</th>
                                <th>Email</th>
                                <th>Telefone</th>
                                <th>Telefone 2</th>
                                <th>Data de Nascimento</th>
                                <th>Opções</th>
                            </tr>
                        </thead>
                        `;
                var i = 0;
                for(cliente of retorno){
                    const {codigo,nome,cpf,rg,email,telefone1,telefone2,data_nascimento,ativo,contador_endereco} = cliente;
                    var cont = i % 2;
                    var cor = '';
                    var telefone1_novo = '';
                    var telefone2_novo = '';

                    cor = '#ffffff;';
                    if(cont == 0){
                        cor = '#b3b7bb;';
                    }

                    telefone1_novo = telefone1;
                    if(telefone1 == ''){
                        telefone1_novo = '-----------------';
                    }
                    telefone2_novo = telefone2;
                    if(telefone2 == ''){
                        telefone2_novo = '-----------------';
                    }
                    ativo_inativo = 1;
                    if(ativo == 1){
                        ativo_inativo = 0;
                    }

                    
                    let data = data_nascimento.split('-').reverse().join('/');
                    htmlTable += `
                        <tr  style="background:`+cor+`;color:black;">
                            <td>
                            ${
                                permissao == 1 ?
                                ativo == 1 ? 
                                '<button id="btn-editar-ativo" class="btn btn-sm btn-danger" onclick="ativar_desativar_clientes('+ativo_inativo+','+codigo+')" style="margin-top: 5px;width:80px;" data-ativo="0" >Desativar</button>' 
                                : 
                                '<button id="btn-editar-ativo" class="btn btn-sm btn-success" onclick="ativar_desativar_clientes('+ativo_inativo+','+codigo+')" style="margin-top: 5px;width:80px;" data-ativo="1">Ativar</button>'
                                : ativo == 1 ? 
                                '<label style="color:#009f00">Ativado</label>' 
                                : 
                                '<label style="color:#ff1b1b">Desativado</label>'
                            }
                            </td>
                            <td id="nome">${nome}</td>
                            <td id="cpf">${mascara('cpf',cpf)}</td>
                            <td id="rg">${mascara('rg',rg)}</td>
                            <td id="email">${email}</td>
                            <td style="width:11%" id="telefone1">${mascara('tel1',telefone1_novo)}</td>
                            <td style="width:11%" id="telefone2">${mascara('tel2',telefone2_novo)}</td>
                            <td id="data_nascimento">${data}</td>
                            <td>
                                <button id="btn-editar-dados" data-keyboard="false" data-backdrop="static" onclick="exibirDadosCliente(${codigo})"  data-toggle="modal" data-target="#myModalEditar" style="margin-top: 5px;width:80px;  background: #d78d00;color:white" class="btn btn-sm btn-default" data-codigocliente="${codigo}">Editar</button>
                                <button id="btn-listar" data-keyboard="false" data-backdrop="static" onclick="ListarEnderecosCliente(${codigo})" data-toggle="modal" data-target="#myModalEndereco" style="margin-top: 5px;  background: #4470f4;color:white;width:95px;" class="btn btn-sm btn-default">Endereços <span style="background: red;border-radius: 10px;padding: 5px;font-weight: bold; class="cont_endereco">${contador_endereco}</span></button>
                            </td>
                        </tr>
                    `;
                    i++;
                }
                    htmlTable += `</table>`;
                $("#exibe_consulta").html(htmlTable);
            }else{
                $divNadaEncontrado.show();
                $("#exibe_consulta").html("");
            }
        }
    })
}

async function ativar_desativar_clientes(ativo_inativo,id_cliente){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);

    if(confirm("Deseja realizar a alteração?")){
        await $.ajax({
            url: `controller.cgi`,
            method: 'POST',
            data: { acao: 'desativar_ativar',
                    ativo_inativo: ativo_inativo,
                    id_cliente :id_cliente},
            success: (response) => {
                alert(response.msg);
                setTimeout(location.reload(), 1500);           
            }
        });
    }
}


async function exibirDadosCliente(id_cliente){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    const permissao = Descriptografa(localStorage.getItem("permissoes"));
    validarUsuarioExistente(usuario_acesso,senha);

    $("#tabela-editar").hide();
    const $divLoading = $("#div-loading-editar");
    const objectData = {
        acao :  'listarClientes',
        id_cliente : id_cliente,
        possuiId : 't',
        permissoes:permissao,
        id_usuario:usuario_acesso
    };
    await $.ajax({
        url: `controller.cgi`,
        method: 'POST',
        data: objectData,
        complete: () => $divLoading.hide(),
        beforeSend: () => $divLoading.show(),
        success: (result) => {   
            const retorno = result.retorno;
            $("#data_nasc_editar").unmask();
            $("#tel1_editar").unmask();
            $("#tel2_editar").unmask();
            $("#cpf_editar").unmask();
            $("#rg_editar").unmask();
            if(retorno.length > 0){
                for(cliente of retorno){
                    const {codigo,nome,cpf,rg,email,telefone1,telefone2,data_nascimento,ativo} = cliente;
                    let data = data_nascimento.split('-').reverse().join('/');
                    $("#nome_editar").val(nome);
                    $("#email_editar").val(email);
                    $("#tel1_editar").val(telefone1);
                    $("#tel2_editar").val(telefone2);
                    $("#data_nasc_editar").val(data);
                    $("#cpf_editar").val(cpf);
                    $("#rg_editar").val(rg);
                    $("#id_cliente_alterar").val(codigo);
                }
                $("#data_nasc_editar").mask("99/99/9999");
                $("#tel1_editar").mask("(99) 9999-9999");
                $("#tel2_editar").mask("(99) 99999-9999");
                $("#cpf_editar").mask("999.999.999-99");
                $("#rg_editar").mask("99.999.999-9");
                $("#tabela-editar").show();
            }
        }
    });  
}

$("#form_modal_cadastrar").on("submit",async function(e){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    

    var data_nascimento = $("#data_nasc").val();
    let data = data_nascimento.split('/').reverse().join('-');
    var check;
    e.preventDefault();   
    const $form      = $(this);
    const $btnSubmit = $form.find('#bt-salvar');
    const id_usuario = Descriptografa(localStorage.getItem("id"));
    
    check = 'f';
    if ($('#habilita_cadastro_endereco').is(':checked')) {
        if($("#logradouro_cadastro").val() == ''){
            alert("Digite um logradouro!");
            return false;
        }

        if($("#numero_cadastro").val() == ''){
            alert("Digite um número!");
            return false;
        }

        if($("#cep_cadastro").val() == ''){
            alert("Digite um CEP!");
            return false;
        }

        if($("#bairro_cadastro").val() == ''){
            alert("Digite um bairro!");
            return false;
        }

        if($("#estado_cadastro").val() == ''){
            alert("Selecione um estado!");
            return false;
        }

        if($("#cidade_cadastro").val() == ''){
            alert("Selecione uma cidade!");
            return false;
        }
        check = 't';
    }

    if(!validaTelefone($("#tel1").val())){
        alert("Digite um telefone válido!");
        return false;
    }

    if(!validaCelular($("#tel2").val())){
        alert("Digite um celular válido!");
        return false;
    }
    $("#tel1").unmask();
    $("#tel2").unmask();
    $("#cpf").unmask();
    $("#rg").unmask();
    validarUsuarioExistente(usuario_acesso,senha);
    $btnSubmit.text('Aguarde...').attr('disabled', true);
    try {
        const formData = new FormData($form[0]);
        formData.append('data_nasc_mascara',data);
        formData.append('cidade_cadastro',$("#cidade_cadastro").val());
        formData.append('estado_cadastro',$("#estado_cadastro").val());
        formData.append('acao', 'salvar_cliente');
        formData.append('id_usuario', id_usuario);
        formData.append('habilita_cadastro_endereco', check);
        const result = await $.ajax({
            type: 'post',
            url: 'controller.cgi',
            data: formData,
            dataType: 'json',
            contentType: false, 
            processData: false,
        });     
        alert(result.msg);


        if(result.status != "Sucesso"){
            $btnSubmit.text('Cadastrar').attr('disabled',false);
            return false;
        }
        setTimeout(location.reload(), 1500);  
    } catch (e){
        alert('Ocorreu algum erro, tente novamente.');
    }
});



$("#form-modal-editar").on("submit", async function(e){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);

    var data_nascimento = $("#data_nasc_editar").val();
    let data = data_nascimento.split('/').reverse().join('-');
    e.preventDefault();
    const $form      = $(this);
    const $btnSubmit = $form.find('#bt-alterar');

    if(!validaTelefone($("#tel1_editar").val())){
        alert("Digite um telefone válido!");
        return false;
    }

    if(!validaCelular($("#tel2_editar").val())){
        alert("Digite um celular válido!");
        return false;
    }

    $("#tel1_editar").unmask();
    $("#tel2_editar").unmask();
    $("#cpf_editar").unmask();
    $("#rg_editar").unmask();

    $btnSubmit.text('Aguarde...').attr('disabled', true);
    try {
        const formData = new FormData($form[0]);
        const $btn             = $("#tabela_consulta_cliente").find('#btn-editar-dados');
        const codigoCliente = $btn.data('codigocliente');
        formData.append('data_nasc',data);
        formData.append('id_cliente',$("#id_cliente_alterar").val());
        formData.append('acao', 'alterar_cliente');
        const result = await $.ajax({
            type: 'post',
            url: 'controller.cgi',
            data: formData,
            dataType: 'json',
            contentType: false, 
            processData: false,
        });     
        alert(result.msg);
        if(result.status != "Sucesso"){
            $btnSubmit.text('Alterar').attr('disabled',false);
            return false;  
        }
        setTimeout(location.reload(), 1500);          
    } catch (e){
        alert('Ocorreu algum erro, tente novamente.');
    } 
});
// FIM FUNÇÕES REFERENTE AO CLIENTE

//INÍCIO FUNÇÕES REFERENTE AO USUÁRIO
async function ListarUsuarios(){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    const $divLoading = $("#div-loading-usuario");
    const objectData = {
        acao: 'listarUsuarios',
    }
    await $.ajax({
        url: 'controller.cgi',
        data: objectData,
        dataType: 'json',
        method: 'POST',
        beforeSend: () => $divLoading.show(),
        complete: () => $divLoading.hide(),
        success: result => {
            const retorno = result.retorno;
            if(retorno.length > 0){
                let htmlTable = ``;
                    htmlTable += `                    
                    <table class="table" style="text-align:center;" id="tabela_consulta_usuario">
                        <thead>
                            <tr>
                                <th>Login</th>
                                <th>Tipo de Perfil</th>
                                <th>Opções</th>
                            </tr>
                        </thead>
                        <tbody>
                        </tbody>`;
                var i = 0;
                for(usuario of retorno){
                    const {id,login,permissoes} = usuario;
                    var cont = i % 2;
                    var select_usuario = '' ;
                    var select_adm = '' ;
                    var cor;

                    cor = '#ffffff;';
                    if(cont == 0){
                        cor = '#b3b7bb;';
                    }

                    if(permissoes == 1){
                        select_adm = 'selected';
                    }else{
                        select_usuario = 'selected';
                    }
                    htmlTable += `
                        <tr style="background:`+cor+` color:black;">

                            <td id="login">${login}</td>
                            <td id="usuario">
                                <select class="forms-select" id="usuario_select_${id}" name="usuario_select">
                                <option ${select_usuario} value="0">Usuário</option>
                                <option ${select_adm} value="1">Administrador Master</option>
                                </select>
                            </td>
                            <td>
                                <input type="button" value="Alterar" id="botao_editar_usuario" onclick="alterarUsuario(${id},'${login}')" style="margin-top: 5px;width:80px;  background: #d78d00;color:white" class="btn btn-sm btn-default">
                                <button id="btn-remove-usuario"  style="margin-top: 5px; background: #d9534f;color:white;width:80px;" onclick="removerPerfil(${id})" class="btn btn-sm btn-default">Remover</button>
                            </td>

                        </tr>
                    `;
                    i++;
                }
                htmlTable += `</table>`;
                $("#exibe_usuario").html(htmlTable);
            }else{
                $("#exibe_usuario").html("");
            }
        }
    })
}

async function removerPerfil(codigo_perfil){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    if(confirm("Deseja excluir o perfil?")){   
        await $.ajax({
            url: `controller.cgi`,
            method: 'POST',
            data: { acao: 'excluir_perfil',
            codigo_perfil :codigo_perfil},
            success: (response) => {        
                alert(response.msg);
                ListarUsuarios();          
            }
        });
    }
}

async function alterarUsuario(id_usuario,login){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    if(confirm("Deseja alterar as informações de " + login + " ?")){
        const id_usuario_localStorage = Descriptografa(localStorage.getItem("id"));
        const objectData = {
            acao: 'editarUsuario',
            tipo_usuario : $("#usuario_select_"+id_usuario).val(),
            id_usuario : id_usuario,
        }
        await $.ajax({
            url: 'controller.cgi',
            data: objectData,
            dataType: 'json',
            method: 'POST',
            success: result => {
                alert(result.msg);
                if(result.status != 'Sucesso'){
                    return false;
                }
                if(id_usuario_localStorage == id_usuario){
                    localStorage.removeItem("permissoes");
                    localStorage.setItem("permissoes",Criptografa($("#usuario_select_"+id_usuario).val()));
                    setTimeout(location.reload(), 1500);           
                }
                ListarUsuarios();
            }
        })
    }
}
//FIM FUNÇÕES REFERENTE AO USUÁRIO

// INÍCIO FUNÇÕES REFERENTE AO ENDEREÇO
async function ListarEnderecosCliente(id_cliente){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    const $divLoading = $("#div-loading-endereco");
    const permissao = Descriptografa(localStorage.getItem("permissoes"));
    const objectData = {
        acao: 'listarEnderecosCliente',
        id_cliente : id_cliente,
    }
    await $.ajax({
        url: 'controller.cgi',
        data: objectData,
        dataType: 'json',
        method: 'POST',
        beforeSend: () => $divLoading.show(),
        complete: () => $divLoading.hide(),
        success: result => {
            const retorno = result.retorno;
            if(retorno.length > 0){
                $("#exibe_endereco").css("overflow","auto");
                $("#exibe_endereco").css("height", "auto");  
                if(retorno.length > 3){
                    $("#exibe_endereco").css("overflow","scroll");
                    $("#exibe_endereco").css("height", "215px");    
                }
                let htmlTable = ``;
                    htmlTable += `                    
                    <table class="table" style="text-align:center;" id="tabela_consulta_endereco">
                        <thead>
                            <tr>
                                <th>Ativar/Desativar</th>
                                <th>Logradouro</th>
                                <th>Número</th>
                                <th>Bairro</th>
                                <th>CEP</th>
                                <th>Cidade</th>
                                <th>Estado</th>
                                <th>Opções</th>
                            </tr>
                        </thead>
                        <tbody>
                        </tbody>`;
                var i = 0;
                for(endereco of retorno){
                    const {id,logradouro,numero,bairro,cep,cidade,estado,codigo_cliente,ativo} = endereco;
                    var cont = i % 2;
                    cor = '#ffffff;';
                    if(cont == 0){
                        cor = '#b3b7bb;';
                    }

                    ativo_inativo = 1;
                    if(ativo == 1){
                        ativo_inativo = 0;
                    }
                    var display = '';
                    if(permissao == 0){
                        display = "display:none;";
                    }
                    htmlTable += `
                        <tr style="background:`+cor+` color:black;">
                            <td>
                            ${
                                permissao == 1 ? 
                                ativo == 1 ? 
                                '<button id="btn-editar-ativo" class="btn btn-sm btn-danger" onclick="ativar_desativar_endereco('+ativo_inativo+','+id+','+codigo_cliente+')" style="margin-top: 5px;width:80px;" data-ativo="0" >Desativar</button>' 
                                : 
                                '<button id="btn-editar-ativo" class="btn btn-sm btn-success" onclick="ativar_desativar_endereco('+ativo_inativo+','+id+','+codigo_cliente+')" style="margin-top: 5px;width:80px;" data-ativo="1">Ativar</button>'
                                : ativo == 1 ? '<label style="color:#009f00">Ativado</label>' 
                                : 
                                '<label style="text-align:center;color:#ff1b1b">Desativado</label>'
                            }
                            </td>
                            <td id="logradouros">${logradouro}</td>
                            <td id="numeros">${numero}</td>
                            <td id="bairros">${bairro}</td>
                            <td id="ceps">${cep}</td>
                            <td style="width:11%" id="cidade_lista">${cidade}</td>
                            <td style="width:11%" id="estado_lista">${estado}</td>
                            <td>
                                <button id="btn-editar-dados-endereco" data-keyboard="false" data-backdrop="static" onclick="exibirDadosEndereco(${id})"  data-toggle="modal" data-target="#myModalEditarEndereco" style="margin-top: 5px;width:80px;  background: #d78d00;color:white" class="btn btn-sm btn-default" data-codigoendereco="${id}">Editar</button>
                                <button id="btn-remove-endereco"  style="margin-top: 5px;${display}  background: #d9534f;color:white;width:80px;" onclick="removeEndereco(${id},${codigo_cliente},${ativo})" class="btn btn-sm btn-default">Remover</button>
                                <input type="hidden" id="btn-codigo-cliente" value="${id_cliente}">
                            </td>
                        </tr>
                    `;
                    i++;
                }
                htmlTable += `</table>`;
                $("#exibe_endereco").html(htmlTable);
            }else{
                $("#exibe_endereco").css("overflow","auto");
                $("#exibe_endereco").css("height", "auto");
                $("#exibe_endereco").html("<input type='hidden' id='btn-codigo-cliente' value='"+id_cliente+"'>");
            }
        }
    })
}

async function removeEndereco(codigo_endereco,id_cliente,ativo){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    if(ativo == 1){
    if(!verificaEndereco(id_cliente)){
        alert("Não é possível excluir o email principal!");
        return false;
    }
    }

    if(confirm("Deseja excluir o endereço?")){   
        await $.ajax({
            url: `controller.cgi`,
            method: 'POST',
            data: { acao: 'excluir_endereco',
                codigo_endereco :codigo_endereco},
            success: (response) => {
            
                alert(response.msg);
                ListarEnderecosCliente(id_cliente);            
            }
        });
    }
}

$("#bt-salvar-endereco").on("click", async function(){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    const codigoCliente = $("#btn-codigo-cliente").val(); 
    const objectData = {
        acao : 'inserir_endereco',
        logradouro : $("#tabela-endereco").find('#logradouro').val(),
        numero : $("#tabela-endereco").find("#numero").val(),
        bairro : $("#tabela-endereco").find("#bairro").val(),
        cep : $("#tabela-endereco").find("#cep").val(),
        id_cliente : codigoCliente,
        cidade : $("#tabela-endereco").find("#cidade").val(),
        estado : $("#tabela-endereco").find("#estado").val(),
    }

    if($("#tabela-endereco").find('#logradouro').val() == ''){
        alert("Digite o logradouro!");
        return false;
    }

    if($("#tabela-endereco").find('#bairro').val() == ''){
        alert("Digite o bairro!");
        return false;
    }

    if($("#tabela-endereco").find('#numero').val() == ''){
        alert("Digite o número!");
        return false;
    }

    if($("#tabela-endereco").find('#cep').val() == ''){
        alert("Digite o CEP!");
        return false;
    }

    if($("#tabela-endereco").find('#estado').val() == ''){
        alert("Selecione o estado!");
        return false;
    }

    if($("#tabela-endereco").find('#cidade').val() == ''){
        alert("Digite a cidade!");
        return false;
    }
    validarUsuarioExistente(usuario_acesso,senha);
    try{
        const result = await $.ajax({
            url: 'controller.cgi',
            data: objectData,
            dataType: 'json',
            method: 'POST'
        }); 
        alert(result.msg);
        if(result.status = "Sucesso"){
            ListarEnderecosCliente(codigoCliente);
        }
    }catch(e){
        alert('Oops! Ocorreu algum erro, tente novamente mais tarde.');
    }  
    $("#tabela-endereco").find('#logradouro').val("");
    $("#tabela-endereco").find("#numero").val("");
    $("#tabela-endereco").find("#bairro").val("");
    $("#tabela-endereco").find("#cep").val("");
    $("#tabela-endereco").find("#estado").val("");
    $("#tabela-endereco").find("#cidade").val("");
});


async function salvaEnderecoCliente(logradouro,numero,cep,bairro,estado,cidade,id_cliente){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    const objectData = {
        acao : 'inserir_endereco',
        logradouro : logradouro,
        numero : numero,
        bairro : bairro,
        cep : cep,
        id_cliente : id_cliente,
        cidade : cidade,
        estado : estado,
    }

    try{
        const result = await $.ajax({
            url: 'controller.cgi',
            data: objectData,
            dataType: 'json',
            method: 'POST'
        }); 
        alert(result.msg);
    }catch(e){
        alert('Oops! Ocorreu algum erro, tente novamente mais tarde.');
    }  
}

async function ativar_desativar_endereco(ativo_inativo,id_endereco,id_cliente){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    if(ativo_inativo == 0){
        if(!verificaEndereco(id_cliente)){
            alert("Não é possível desativar o email principal!");
            return false;
        }
    }

    if(confirm("Deseja realizar a alteração?")){
        await $.ajax({
            url: `controller.cgi`,
            method: 'POST',
            data: { acao: 'desativar_ativar',
                    ativo_inativo: ativo_inativo,
                    id_endereco :id_endereco,
                    tabela: 'endereco'},
            success: (response) => {    
                alert(response.msg);
                ListarEnderecosCliente(id_cliente);             
            }
        });
    }
}
function verificaEndereco(id_cliente){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    var retorno_funcao;
    const objectData = {
        acao : 'validarEndereco',
        id_cliente : id_cliente,
    }

    $.ajax({
            url: "controller.cgi",
            data: objectData,
            dataType: "json",
            type: "post",
            async: false,
            success: function(result)  {
                retorno_funcao = true;
                if (result.retorno == 1) {
                  retorno_funcao = false;
                } 
            },
    })
    return retorno_funcao;

}
async function exibirDadosEndereco(id_endereco){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    $("#tabela-editar-endereco").hide();
    const $divLoading = $("#div-loading-editar-endereco");
    const objectData = {
        acao :  'listarEnderecosCliente',
        id_endereco : id_endereco,
        possuiId : 't'
    };
    await $.ajax({
        url: `controller.cgi`,
        method: 'POST',
        data: objectData,
        complete: () => $divLoading.hide(),
        beforeSend: () => $divLoading.show(),
        success: (result) => {   
            const retorno = result.retorno;
            if(retorno.length > 0){
                for(endereco of retorno){
                    const {logradouro,numero,bairro,cep,cidade,estado,codigo_cliente} = endereco;
                    $("#logradouro_editar").val(logradouro);
                    $("#numero_editar").val(numero);
                    buscaCidadesEditar(estado);
                    $("#cidade_editar").val(cidade);
                    $("#bairro_editar").val(bairro);
                    $("#estado_editar").val(estado);
                    $("#cep_editar").val(cep);
                    $("#id_cliente_endereco_alterar").val(codigo_cliente)
                }
                $("#tabela-editar-endereco").show();
            }
        }
    });  
}

$("#form-modal-editar-endereco").on("submit", async function(e){
    const usuario_acesso = Descriptografa(localStorage.getItem("usuario"));
    const senha = Descriptografa(localStorage.getItem("senha"));
    validarUsuarioExistente(usuario_acesso,senha);
    e.preventDefault();
    const $form      = $(this);
    const $btnSubmit = $form.find('#bt-alterar');
    $btnSubmit.text('Aguarde...').attr('disabled', true);
    try {
        const formData = new FormData($form[0]);
        const $btn2             = $("#myModalEndereco").find('#btn-editar-dados-endereco');
        const codigoEndereco = $btn2.data('codigoendereco');
        formData.append('id_endereco',codigoEndereco);
        formData.append('acao', 'alterar_endereco');
        const result = await $.ajax({
            type: 'post',
            url: 'controller.cgi',
            data: formData,
            dataType: 'json',
            contentType: false, 
            processData: false,
        });     
        alert(result.msg);
        if(result.status != "Sucesso"){
            $btnSubmit.text('Alterar').attr('disabled',false);
            return false;

        }
        $("#myModalEditarEndereco").modal("hide");
        ListarEnderecosCliente($("#id_cliente_endereco_alterar").val());  
    } catch (e){
        alert('Ocorreu algum erro, tente novamente.');
    } 
});
//FIM FUNÇÕES REFERENTE AO ENDEREÇO

//INÍCIO FUNÇÕES REFERENTE AO LOGIN
function validarUsuarioExistente(usuario,senha){

        var retorno_funcao;
        const objectData = {
            acao: 'logarUsuario',
            login: usuario,
            senha: senha,
        }
    
        $.ajax({
                url: "controller.cgi",
                data: objectData,
                dataType: "json",
                type: "post",
                async: false,
                success: function(result)  {
                    const retorno = result.retorno;

                    if (retorno == 0 ) {
                        localStorage.removeItem("usuario");
                        localStorage.removeItem("id");
                        localStorage.removeItem("permissoes");
                        localStorage.removeItem("senha");
                        window.location.href =
                        "http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/login.cgi";   
                    }
                },
        })
       
}

//FIM FUNÇÕES REFERENTE AO LOGIN

//OUTRAS FUNÇÕES
function showModal(){
    $("#myModal3").css("display","block");
    document.body.style.overflow = 'hidden';
}

$("#data_nasc").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#cpf").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#rg").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#numero").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#numero_editar").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#numero_cadastro").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#cep").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#cep_editar").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#cep_cadastro").keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
        return false;
    }
});

$("#nome").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#nome_editar").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#logradouro").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#logradouro_editar").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#bairro").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#bairro_editar").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#logradouro_cadastro").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#logradouro_cadastro").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

$("#bairro_cadastro").keypress(function (e){
    var char = String.fromCharCode(e.keyCode);
    var pattern = '[a-zA-Z0-9 ]';
      if (char.match(pattern)) {
        return true;
    }else{
        return false;
    }
});

function altera(){
    $("#valor").val("");
    $("#valor").focus();

    $("#ativos_inativos").hide();  
    if($("#campo").val() == 'ativo'){
        $("#ativos_inativos").show();
    }

    $("#valor").show();
    if($("#campo").val() == ""){
        $("#valor").hide();
    }else if ($("#campo").val() == 'ativo'){
        $("#valor").hide();
    }

    $("#valor").unmask();
    if($("#campo").val() == 'data_nascimento'){
        $("#valor").mask("99/99/9999");
    }

    $("#valor").keypress(function (e) {
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)){
            return false;
        }
    });

    if($("#campo").val() == 'nome'){    
        $('#valor').unbind("keypress");
    }else if($("#campo").val() == 'email'){
        $('#valor').unbind("keypress");
    }
}

function logout(){
    window.location.href = "http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/login.cgi";
    localStorage.removeItem("usuario");
    localStorage.removeItem("id");
    localStorage.removeItem("permissoes");
    localStorage.removeItem("senha");
}

function mascara(campo,value){
    value = value.replace(/\D/g,"");
    if(campo == 'cpf'){
        value=value.replace(/(\d{3})(\d)/,"$1.$2")
        value=value.replace(/(\d{3})(\d)/,"$1.$2")
        value=value.replace(/(\d{3})(\d{1,2})$/,"$1-$2")
    }

    if(campo == 'rg'){
        value=value.replace(/(\d{2})(\d)/,"$1.$2")
        value=value.replace(/(\d{3})(\d)/,"$1.$2")
        value=value.replace(/(\d{3})(\d{1,2})$/,"$1-$2")
        value=value.replace(/(\d{1})(\d{1,2})$/,"$1-$2") 
    }
    
    if(campo == 'tel1'){ 
        value = value.replace(/^(\d{2})(\d)/g,"($1) $2");
        value = value.replace(/(\d)(\d{4})$/,"$1-$2");  
    }

    if(campo == 'tel2'){
        value = value.replace(/^(\d{2})(\d)/g,"($1) $2");
        value = value.replace(/(\d)(\d{5})$/,"$1-$2");  
    }
    return value;
}
function habilitaCamposEndereco(){
    $("#logradouro_cadastro").val('');
    $("#numero_cadastro").val('');
    $("#bairro_cadastro").val('');
    $("#cep_cadastro").val('');
    $("#estado_cadastro").val('');
    $("#cidade_cadastro").val('');
    $("#cadastro_endereco").hide();
    if ($('#habilita_cadastro_endereco').is(':checked')) {
        $("#cadastro_endereco").show();
    }
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

function validaTelefone(valor){

    valor = valor.replace("(", "");
    valor = valor.replace(")", "");
    valor = valor.replace("-", "");
    valor = valor.replace(" ", "").trim();
    if(valor.length != 10){
        return false;
    }
    return true;
}

function validaCelular(valor){

    valor = valor.replace("(", "");
    valor = valor.replace(")", "");
    valor = valor.replace("-", "");
    valor = valor.replace(" ", "").trim();
    if(valor.length != 11){
        return false;
    }
    return true;
}

//FUNÇÃO PARA SETAR O RETORNO DOS CAMPOS VIACEP
function buscaCep(valor,logradouro,bairro,estado,cidade,busca){
    if(valor.length == 8){
        $.ajax({
                url: "https://viacep.com.br/ws/"+valor+"/json/?callback=?",
                dataType: "json",
                success: function(result)  {
                    if(result.logradouro){
                        $("#"+logradouro).val(result.logradouro);
                        $("#"+bairro).val(result.bairro);
                    if(busca == 'cadastrar'){
                        buscaCidadesCadastro(result.uf);
                    }else if(busca == 'editar'){
                        buscaCidadesEditar(result.uf);
                    }else{
                        buscaCidades(result.uf);
                    } 
                        $("#"+estado).val(result.uf);
                        $("#"+cidade).val(result.localidade);
                    }else{
                        alert("CEP INVÁLIDO");
                        $("#"+logradouro).val('');
                        $("#"+bairro).val('');
                        $("#"+estado).val('');
                        $("#"+cidade).val('');
                    }

                },
        })
    }else{
        alert("CEP menor que 8 dígitos!");
        $("#"+logradouro).val('');
        $("#"+bairro).val('');
        $("#"+estado).val('');
        $("#"+cidade).val('');
        
    }
}
