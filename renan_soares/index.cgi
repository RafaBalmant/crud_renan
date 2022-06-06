#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser set_message);

$BASEAPP = $ENV{HTTP_BASEAPP};
require $BASEAPP."/GLOBAL/cgi-local/modulos/kernel/000.cgi";

my $cgi = new CGI->new();

print $cgi->header();

cookie("ler");

if (!$cookie_manager_usuario) { redirecionar("$path_cgi/login/login.cgi", '2'); exit; }

print << "HTML";

<!DOCTYPE html>
    <html lang="Pt-br">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
        <title>Área Usuário</title> 
        <link rel="stylesheet" href="$path_conteudo/css/libs/font-awesome.min.css" />
        <link rel="stylesheet" href="$path_conteudo/css/libs/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="$path_conteudo/css/plugin/toastr.min.css"  />
        <link rel="stylesheet" type="text/css" href="$path_conteudo/css/spinkit/spinkit.min.css" />
        <link rel="stylesheet" type="text/css" href="$path_conteudo/css/plugin/jquery-ui-auto.css"  />
        <style>
            .container{
                width: 100%;
                height: auto;
                background-image: linear-gradient(10deg, #2f00ff,#fd6500 , #F9FAFB  );
                display: flex;
                /*flex-direction: row;
                justify-content: center;
                align-items: center;*/
            }
            .btn-sm{
                font-weight:600;
            }
            .box{
                background: #0267B5;
                border-radius: 15px;
                width: 100%;
                padding:16px;
                height: auto;
                color:white;
                margin-top:20px;
                box-shadow: 5px 3px 5px black;
            }
            body{
                margin:0;
                font-family:Roboto;
            }
            .menu{
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: space-around;
                flex: 1 1 0%;
                height: 9rem;
                background: #0267B5;
            }
            .titulo{
                color: white;
            }
            .box > div{
                display: inline-block;
                padding: 20px;
                width: 41%;
            }
            .box > div > input{
                width: 100%;
                padding: 10px;
                height: 80px;
                cursor:pointer;
                font-size: 20px;
                color:white;
                font-weight: bold;
                background-image: linear-gradient(to right,#FD7726, #0267B5);
            }

            .box > div > input:hover{
                opacity:0.7;   
                background-image: linear-gradient(#0267B5,#FD7726,);       
                -webkit-transition: all 200ms ease-in;
                -ms-transition: all 200ms ease-in;
                -moz-transition: all 200ms ease-in;
                transition: all 200ms ease-in;
            }
            .img{
                text-align: center;
                width:100%;
                margin-left: 50px;
                margin-right: 50px;
                margin-top:10px\!important;
            }
            .img > img{
                padding: 10px;
   
                
            }
            .modal {
                left:-150px;
                
            }

            .modal-title-nome {
                font-weight:bold;
            }

            .modal-content {
                width: 750px;
                top:150px;
                border-radius: 35px;
                box-shadow: 6px 6px 8px black;
            }

            \@media only screen and (max-width:1270px){
                .modal-content{
                    width:750px\!important;
                }
                
            }
            \@media only screen and (max-width:1051px){
                .img{
                    margin:0;
                }
                .btn-consulta{
                    width:20%\!important;
                }
                .box{
                    height:auto;
                }
                .container{
                    height:auto;
                }
                .p_menu{
                    width:80%\!important;
                }
                \#imagem-login{
                    width:7%\!important;
                }
            }
            \@media only screen and (max-width:768px){
                .modal-content{
                    width:70%\!important;
                    left: 143px\!important;
                    padding:15px\!important;
                }
                .modal-body fieldset{
                    padding:12px\!important;
                }

                .cidade{
                        width: 100%\!important;
                }

            }
            \@media only screen and (max-width:676px){
                \#imagem-login{
                    width:15%\!important;
                }
                \#imagem-logout{
                    width:9%\!important;
                }
            }
            \@media only screen and (max-width:467px){
                .btn-consulta{
                    width:30%\!important;
                }
                \#foto2{
                    width:35%\!important;
                }

            }
            
            \@media only screen and (max-width:366px){
                .btn-consulta{
                    width:40%\!important;
                }
                .a-foto{
                    width: 42%;
                    margin-left: 0px\!important;
                }


                \#foto{
                    width: 98%;
                }
            }
            .tabela{
                width:100%;
            }
            .coluna{
                width:50%
            }
            .forms{
                width:96%;
                margin: 0 auto;
                padding: 10px;
                border: none;
                margin-bottom: 10px;
                border-radius: 50px;
                color:black;
            }
            .modal-body fieldset{
                border: 1px solid #fff;
                padding:45px;
            }
            .modal-body legend{
                width: 27%;
                border:none;
                color:white;
            }
            .modal-body-consulta{
                overflow:auto;
                height:400px;
            }
            .modal-content-consulta{
                width:1000px;
                height: 610;
            }
            .btn-consulta{
                padding: 10px;
                width: 11%;
                background: linear-gradient(to right,#FD7726, #7000DF);;
                border: none;
                border-radius: 20px;
                cursor:pointer;
            }
            .btn-consulta:hover{
                opacity:0.9;   
                -webkit-transition: all 200ms ease-in;
                -ms-transition: all 200ms ease-in;
                -moz-transition: all 200ms ease-in;
                transition: all 200ms ease-in;
            }
            .forms-select{
                border-radius: 15px;
                padding: 9px;
                background: white;
                color: black;
                border: 1px solid;
                cursor: pointer;
            }
            .table > thead > tr >  th{
                text-align:center;
            }
            .menu > img{
                width: 7%;
            }
            .menu-div{
                background: #0267B5;
            }
            .label_login{
                margin: 0;
            }
            .texto_login{
                font-size: 24px;
                color: white;
                text-decoration: underline;
                margin: 0;
                cursor: pointer;
                margin-right: 7%;
            }
            \#imagem-logout{
                width:2%;
                margin-right: 5px;
            }
        </style>
    </head>

    <body>
        <div class="menu-div">
        <header class="menu">
            <a class="a-foto" style="margin-left: 9%;" href="http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/index.cgi" target="_blank"><img id="foto" src="$path_conteudo/js/informatica/renan_soares/logo-kabum-adm.png"></a>
            <div class="menu" style="justify-content:end!important;height: auto;text-align: right;display: inline-flex;width: 100%;">    
            <p class="p_menu"  style="color:white;margin:0;"><img style="width: 5%;" id="imagem-login" src="https://cdn1.iconfinder.com/data/icons/outlinies-basic/9/user-512.png"> <label style="text-transform:uppercase;margin-right:30px;" class="label_login" id="usuario_logado"></label></p> 
            <img  id="imagem-logout" src="https://cdn4.iconfinder.com/data/icons/liberty/46/Logout-256.png"><h3 class="texto_login " onclick="logout()">Sair</h3>
        </div>
        </header>
        </div>
        <div class="container">
            <div class="img">
                <a href="http://manager.qa.kabumdev.com.br/cgi-local/informatica/renan_soares/index.cgi" target="_blank"><img id="foto2" src="$path_conteudo/js/informatica/renan_soares/logo_kabum.png"></a>
                <div class="box">
                    <fieldset>
                    <legend style="color:white;font-weight:bold"> Área de Consulta </legend>
                        <div style="text-align:left">
                            <label for="campo"> Filtro </label><br>
                            <select id="campo"onchange="altera();"class="forms-select" name="campo">
                                <option value="">--Selecione--</option>
                                <option value="nome">Nome</option>
                                <option value="cpf">CPF</option>
                                <option value="rg">RG</option>
                                <option value="email">Email</option>
                                <option value="telefone1">Telefone</option>
                                <option value="telefone2">Telefone 2</option>
                                <option value="data_nascimento">Data de Nascimento</option>
                                <option value="ativo">Ativos/Inativos</option>
                            </select>
                                <select class="forms-select" style="display:none" id="ativos_inativos" name="ativos_inativos">
                                <option value="">Todos</option>
                                <option value="1">Ativos</option>
                                <option value="0">Inativos</option>
                            </select>
                            <input type="text" class="forms" style="width:26%;display:none"  id="valor" name="valor">
                            <input type="button" class="btn-consulta"  id="btn_pesquisar" onclick="ConsultaCliente();" value="Filtrar">
                            <input type="button" class="btn-consulta"  value="Cadastrar" id="botaoCadastro" name="botaoCadastro" data-keyboard="false" data-backdrop="static" type="btn btn-danger" data-toggle="modal" data-target="#myModal12345">
                            <input type="button" class="btn-consulta" style="display:none"  value="Editar Perfis" onclick="ListarUsuarios()"; id="botaoPerfil" name="botaoPerfil" data-keyboard="false" data-backdrop="static" type="btn btn-danger" data-toggle="modal" data-target="#myModalEditarUsuario">
                        </div>
                        <div class="row" id="div-loading">
                            <div class="col-md-12"><h2 class="text-center">Aguarde...</h2></div>
                        </div>
                        
                        <div class="row" id="div-nada-encontrado" style="display:none">
                            <div class="col-md-12"><h2 class="text-center">Nenhum Resultado Encontrado</h2></div>
                        </div>
                        <div class="row" id="exibe_consulta" style="height: 619px;overflow: auto;">
                        </div>
                    </fieldset>
                </div>
            </div>
        </div>
        
      	<!-- Modal Cadastro -->
		<div class="modal fade" id="myModal12345" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <form id="form_modal_cadastrar"> 
                <div class="modal-dialog modal-dialog-centered">
                <!-- Modal content-->
                <div class="modal-content" style="background: linear-gradient(to right,#FD7726, #0267B5);color:white">
                    <div class="modal-header">
                    <h5 class="modal-title" id="modal-title-nome">Cadastro de Clientes</h5>
                    </div>
                    <div class="modal-body">  
                        <fieldset>
                        <legend> Área de Cadastro </legend>
                            <table class="tabela" id="tabela_cadastro_cliente">
                                <tr> 
                                    <td class="coluna" >
                                        <label for="nome"> Nome </label><br>
                                        <input class="forms" required placeholder="Nome" id="nome" name="nome" type="text">
                                    </td>
                                    <td class="coluna" >
                                        <label for="email"> Email </label><br>
                                        <input class="forms" required id="email" placeholder="Email" name="email" type="email">
                                    </td>
                                </tr>
                                <tr>
                                    <td class="coluna">
                                        <label for="tel1"> Telefone </label><br>
                                        <input class="forms" required id="tel1" placeholder="Telefone" onblur="teste(this.value)" name="tel1" type="text">
                                    </td>
                                    <td class="coluna">
                                        <label for="tel2"> Telefone 2 </label><br>
                                        <input class="forms" required id="tel2" placeholder="Telefone 2" name="tel2" type="text">
                                    </td>
                                </tr>
                            </table>
                            <table>
                                <tr>
                                    <td class="coluna" style="width:36%">
                                        <label for="rg"> RG </label><br>
                                        <input class="forms" required id="rg" placeholder="RG" name="rg" type="text">
                                    </td>
                                    <td class="coluna" style="width:36%">
                                        <label for="cpf"> CPF </label><br>
                                        <input class="forms" id="cpf" placeholder="CPF" name="cpf" required type="text">
                                    </td>
                                    <td class="coluna" style="width:36%">
                                        <label for="data_nacimento"> Data de Nascimento </label><br>
                                        <input class="forms" id="data_nasc" required  name="data_nasc" type="text">
                                    </td>
                                </tr>
                                <tr>
                                    <td class="coluna" style="width:36%">
                                        <input type="checkbox" onclick="habilitaCamposEndereco()" id="habilita_cadastro_endereco" value="t"><label for="cad_end">Cadastrar Endereço</label>
                                    </td>
                                </tr>
                            </table>
                            <table id="cadastro_endereco" style="display:none">
                            <tr>
                                <td class="coluna" style="width:36%" >
                                    <label for="logradouro"> Logradouro </label><br>
                                    <input class="forms" placeholder="Logradouro" id="logradouro_cadastro" name="logradouro_cadastro" type="text">
                                </td>
                                <td class="coluna" style="width:36%" >
                                    <label for="numero"> Número </label><br>
                                    <input class="forms" id="numero_cadastro" placeholder="Número" name="numero_cadastro" type="text">
                                </td>
                                <td class="coluna" style="width:36%" >
                                    <label for="bairro"> Bairro </label><br>
                                    <input class="forms" id="bairro_cadastro" placeholder="Bairro" name="bairro_cadastro" type="text">
                                </td>
                            </tr>
                            <tr>
                                <td class="coluna" style="width:36%">
                                    <label for="cep"> CEP </label><br>
                                    <input class="forms" id="cep_cadastro" maxlength="8" onblur="buscaCep(this.value,'logradouro_cadastro','bairro_cadastro','estado_cadastro','cidade_cadastro','cadastrar')" placeholder="CEP" name="cep_cadastro" type="text">
                                </td>
                                <td class="coluna" style="width:36%">
                                    <label for="estado"> Estado</label><br>
                                    <select style="width:96%" class="forms-select" id="estado_cadastro" onchange="buscaCidadesCadastro(this.value)">
                                        <option value="">Selecione o Estado</option>
                                        <option value="AC">Acre</option>
                                        <option value="AL">Alagoas</option>
                                        <option value="AM">Amazonas</option> 
                                        <option value="AP">Amapá</option> 
                                        <option value="BA">Bahia</option> 
                                        <option value="CE">Ceará</option> 
                                        <option value="DF">Distrito Federal</option> 
                                        <option value="ES">Espírito Santo</option> 
                                        <option value="GO">Goiás</option> 
                                        <option value="MA">Maranhão</option> 
                                        <option value="MT">Mato Grosso</option> 
                                        <option value="MS">Mato Grosso do Sul</option> 
                                        <option value="MG">Minas Gerais</option> 
                                        <option value="PA">Pará</option> 
                                        <option value="PB">Paraíba</option> 
                                        <option value="PR">Paraná</option> 
                                        <option value="PE">Pernambuco</option> 
                                        <option value="PI">Piauí</option> 
                                        <option value="RJ">Rio de Janeiro</option> 
                                        <option value="RN">Rio Grande do Norte</option> 
                                        <option value="RO">Rondônia</option> 
                                        <option value="RS">Rio Grande do Sul</option> 
                                        <option value="RR">Roraima</option> 
                                        <option value="SC">Santa Catarina</option> 
                                        <option value="SE">Sergipe</option> 
                                        <option value="SP">São Paulo</option> 
                                        <option value="TO">Tocantins</option> 
                                    </select>
                                </td>
                                <td class="coluna" style="width:36%">
                                    <label for="cidade"> Cidade</label><br>
                                    <select style="width:100%" class="forms-select cidade" id="cidade_cadastro">
                                    </select>
                                </td>
                            </tr>
                        </table>
                        </fieldset>                
                    </div>
                    <div class="modal-footer">
                    <button type="submit" class="btn btn-primary" id="bt-salvar">Cadastrar</button>
                    <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
                    </div>
                </div>
                </div>
            </form>
		</div>
	<!-- Modal Cadastro End -->

        <!-- Modal Editar -->
		<div class="modal fade" id="myModalEditar" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">,
            <form id="form-modal-editar">
			<div class="modal-dialog modal-dialog-centered">

			  <!-- Modal content-->
			  <div class="modal-content modal-content-consulta" style="background: linear-gradient(to right,#FD7726, #0267B5);color:white">
				<div class="modal-header">
				  <h5 class="modal-title" id="modal-title-nome">Editar Cliente</h5>
				</div>
				<div class="modal-body modal-body-consulta">    
                    <div class="row" id="div-loading-editar">
                        <div class="col-md-12"><h2 class="text-center">Aguarde...</h2></div>
                    </div>            
                    <fieldset id="tabela-editar" style="display:none">
                    <legend> Área de Edição </legend>
                        <table class="tabela" >
                            <tr>
                                <td class="coluna" >
                                    <label for="nome"> Nome </label><br>
                                    <input class="forms" required placeholder="Nome" id="nome_editar" name="nome_editar" type="text">
                                    <input   id="id_cliente_alterar" name="id_cliente_alterar" type="hidden">
                                </td>
                                <td class="coluna" >
                                    <label for="email"> Email </label><br>
                                    <input class="forms" required id="email_editar" placeholder="Email" name="email_editar" type="email">
                                </td>
                            </tr>
                            <tr>
                                <td class="coluna" >
                                    <label for="tel1"> Telefone </label><br>
                                    <input class="forms" required id="tel1_editar" placeholder="Telefone" name="tel1_editar" type="text">
                                </td>
                                <td class="coluna">
                                    <label for="tel2"> Telefone 2 </label><br>
                                    <input class="forms" required id="tel2_editar"  placeholder="Telefone 2" name="tel2_editar" type="text">
                                </td>
                            </tr>
                        </table>
                        <table>
                            <tr>
                                <td class="coluna" style="width:36%">
                                    <label for="rg"> RG </label><br>
                                    <input class="forms" required id="rg_editar" placeholder="RG" name="rg_editar" type="text">
                                </td>
                                <td class="coluna" style="width:36%">
                                    <label for="cpf"> CPF </label><br>
                                    <input class="forms" required id="cpf_editar" placeholder="CPF" name="cpf_editar" type="text">
                                </td>
                                <td class="coluna" style="width:36%">
                                    <label for="data_nacimento"> Data de Nascimento </label><br>
                                    <input class="forms" required id="data_nasc_editar"  name="data_nasc_editar" type="text">
                                </td>
                            </tr>
                        </table>
                    </fieldset>
				</div>
				<div class="modal-footer">
                    <button type="submit" id="bt-alterar" class="btn btn-primary">Alterar</button>
				  <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
				</div>
			  </div>
			</div>
            </form>
		</div>
	<!-- Modal Editar End -->

            <!-- Modal Endereços -->
		<div class="modal fade" id="myModalEndereco" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">,
            <!--<form id="form-modal-endereco">-->
			<div class="modal-dialog modal-dialog-centered">

			  <!-- Modal content-->
			  <div class="modal-content modal-content-consulta" style="left: -89px;background:linear-gradient(to right,#FD7726, #0267B5);color:white">
				<div class="modal-header">
				  <h5 class="modal-title" id="modal-title-nome">Editar Endereços</h5>
				</div>
				<div class="modal-body ">       
                    <div class="row" style="display:none" id="div-loading-endereco">
                        <div class="col-md-12"><h2 class="text-center">Aguarde...</h2></div>
                        <input   id="id_cliente_endereco_alterar" name="id_cliente_endereco_alterar" type="hidden">
                    </div>
                    <div class="row" id="exibe_endereco">
                    </div>
                    <fieldset id="tabela-endereco">
                    <legend> Área de Cadastro </legend>
                        <table class="tabela" >
                            <tr>
                                <td class="coluna" >
                                    <label for="logradouro"> Logradouro </label><br>
                                    <input class="forms" placeholder="Logradouro" id="logradouro" name="logradouro" type="text">
                                </td>
                                <td class="coluna" >
                                    <label for="numero"> Número </label><br>
                                    <input class="forms" id="numero" placeholder="Número" name="numero" type="text">
                                </td>
                            </tr>
                            <tr>
                                <td class="coluna" >
                                    <label for="bairro"> Bairro </label><br>
                                    <input class="forms" id="bairro" placeholder="Bairro" name="bairro" type="text">
                                </td>
                                <td class="coluna">
                                    <label for="cep"> CEP </label><br>
                                    <input class="forms" id="cep" maxlength="8" onblur="buscaCep(this.value,'logradouro','bairro','estado','cidade','')"  placeholder="CEP" name="cep" type="text">
                                </td>
                            </tr>
                            <tr>
                                <td class="coluna">
                                    <label for="estado"> Estado</label><br>
                                    <select class="forms-select" id="estado" onchange="buscaCidades(this.value)">
                                        <option value="">Selecione o Estado</option>
                                        <option value="AC">Acre</option>
                                        <option value="AL">Alagoas</option>
                                        <option value="AM">Amazonas</option> 
                                        <option value="AP">Amapá</option> 
                                        <option value="BA">Bahia</option> 
                                        <option value="CE">Ceará</option> 
                                        <option value="DF">Distrito Federal</option> 
                                        <option value="ES">Espírito Santo</option> 
                                        <option value="GO">Goiás</option> 
                                        <option value="MA">Maranhão</option> 
                                        <option value="MT">Mato Grosso</option> 
                                        <option value="MS">Mato Grosso do Sul</option> 
                                        <option value="MG">Minas Gerais</option> 
                                        <option value="PA">Pará</option> 
                                        <option value="PB">Paraíba</option> 
                                        <option value="PR">Paraná</option> 
                                        <option value="PE">Pernambuco</option> 
                                        <option value="PI">Piauí</option> 
                                        <option value="RJ">Rio de Janeiro</option> 
                                        <option value="RN">Rio Grande do Norte</option> 
                                        <option value="RO">Rondônia</option> 
                                        <option value="RS">Rio Grande do Sul</option> 
                                        <option value="RR">Roraima</option> 
                                        <option value="SC">Santa Catarina</option> 
                                        <option value="SE">Sergipe</option> 
                                        <option value="SP">São Paulo</option> 
                                        <option value="TO">Tocantins</option> 
                                    </select>
                                </td>
                                <td>
                                    <label for="cidade"> Cidade</label><br>
                                    <select style="width:50%" class="forms-select cidade" id="cidade">
                                    </select>
                                </td>
                            </tr>
                        </table>
                    </fieldset>
				</div>
				<div class="modal-footer">
                    <button type="submit" id="bt-salvar-endereco" class="btn btn-primary">Salvar</button>
				  <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
				</div>
			  </div>

			</div>
            <!--</form>-->
		</div>
	<!-- Modal Endereços End -->

        <!-- Modal Editar Endereços -->
		<div class="modal fade"  id="myModalEditarEndereco"  role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <form id="form-modal-editar-endereco">
			<div class="modal-dialog modal-dialog-centered">

			  <!-- Modal content-->
			  <div class="modal-content modal-content-consulta" style="background: linear-gradient(to right,#FD7726, #0267B5);color:white">
				<div class="modal-header">
				  <h5 class="modal-title" id="modal-title-nome">Editar Endereço</h5>
				</div>
				<div class="modal-body ">  
                    <div class="row" style="display:none" id="div-loading-editar-endereco">
                        <div class="col-md-12"><h2 class="text-center">Aguarde...</h2></div>
                    </div>
                    <fieldset id="tabela-editar-endereco">
                    <legend> Área de Edição </legend>
                        <table class="tabela" >
                            <tr>
                                <td class="coluna" >
                                    <label for="logradouro"> Logradouro </label><br>
                                    <input class="forms" placeholder="Logradouro" id="logradouro_editar" name="logradouro_editar" type="text">
                                </td>
                                <td class="coluna" >
                                    <label for="numero"> Número </label><br>
                                    <input class="forms" id="numero_editar" placeholder="Número" name="numero_editar" type="text">
                                </td>
                            </tr>
                            <tr>
                                <td class="coluna" >
                                    <label for="bairro"> Bairro </label><br>
                                    <input class="forms" id="bairro_editar" placeholder="Bairro" name="bairro_editar" type="text">
                                </td>
                                <td class="coluna">
                                    <label for="cep"> CEP </label><br>
                                    <input class="forms" id="cep_editar" maxlength="8" onblur="buscaCep(this.value,'logradouro_editar','bairro_editar','estado_editar','cidade_editar','editar')"  placeholder="CEP" name="cep_editar" type="text">
                                </td>
                            </tr>
                            <tr>
                                <td class="coluna">
                                    <label for="estado"> Estado</label><br>
                                    <select class="forms-select" id="estado_editar" name="estado_editar" onchange="buscaCidadesEditar(this.value)">
                                        <option value="">Selecione o Estado</option>
                                        <option value="AC">Acre</option>
                                        <option value="AL">Alagoas</option>
                                        <option value="AM">Amazonas</option> 
                                        <option value="AP">Amapá</option> 
                                        <option value="BA">Bahia</option> 
                                        <option value="CE">Ceará</option> 
                                        <option value="DF">Distrito Federal</option> 
                                        <option value="ES">Espírito Santo</option> 
                                        <option value="GO">Goiás</option> 
                                        <option value="MA">Maranhão</option> 
                                        <option value="MT">Mato Grosso</option> 
                                        <option value="MS">Mato Grosso do Sul</option> 
                                        <option value="MG">Minas Gerais</option> 
                                        <option value="PA">Pará</option> 
                                        <option value="PB">Paraíba</option> 
                                        <option value="PR">Paraná</option> 
                                        <option value="PE">Pernambuco</option> 
                                        <option value="PI">Piauí</option> 
                                        <option value="RJ">Rio de Janeiro</option> 
                                        <option value="RN">Rio Grande do Norte</option> 
                                        <option value="RO">Rondônia</option> 
                                        <option value="RS">Rio Grande do Sul</option> 
                                        <option value="RR">Roraima</option> 
                                        <option value="SC">Santa Catarina</option> 
                                        <option value="SE">Sergipe</option> 
                                        <option value="SP">São Paulo</option> 
                                        <option value="TO">Tocantins</option> 
                                    </select>
                                </td>
                                <td>
                                    <label for="cidade"> Cidade</label><br>
                                    <select style="width:50%" class="forms-select cidade" name="cidade_editar" id="cidade_editar">
                                    </select>
                                </td>
                            </tr>
                        </table>
                    </fieldset>                       
				</div>
				<div class="modal-footer">
                    <button type="submit" id="bt-editar-endereco" class="btn btn-primary">Salvar</button>
				    <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
				</div>
			  </div>
			</div>
            </form>
		</div>
	<!-- Modal Editar Endereços End -->

            <!-- Modal Perfis -->
		<div class="modal fade" id="myModalEditarUsuario"  role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
			<div class="modal-dialog modal-dialog-centered">

			  <!-- Modal content-->
			  <div class="modal-content modal-content-consulta" style="background: linear-gradient(to right,#FD7726, #0267B5);color:white">
				<div class="modal-header">
				  <h5 class="modal-title" id="modal-title-nome">Editar Perfil</h5>
				</div>
				<div class="modal-body ">  
                    <div class="row" style="display:none" id="div-loading-usuario">
                        <div class="col-md-12"><h2 class="text-center">Aguarde...</h2></div>
                    </div>                 
                     <div class="row"style="overflow-x: auto;height: 515px;"id="exibe_usuario">
				</div>
				<div class="modal-footer">
				    <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
				</div>
			  </div>
			</div>
		</div>
	<!-- Modal  Perfis End -->
    
        <script type="text/javascript" src='$path_conteudo/js/jquery.min.js'></script>
        <script type="text/javascript" src='$path_conteudo/js/jquery.mask.min.js'></script>
        <script type="text/javascript" src="$path_conteudo/js/libs/bootstrap/bootstrap.min.js"></script>
        <script type="text/javascript" src="$path_conteudo/js/plugin/toastr.min.js"></script>
        <script type="text/javascript" src="$path_conteudo/js/plugin/toastr.global.js"></script>
        <!--Caminho do seu JS-->
        <script src='$path_conteudo/js/informatica/renan_soares/index.js'></script>
        <script src='$path_conteudo/js/informatica/renan_soares/estados_cidades.js'></script>
    </body>
</html>

HTML

1;