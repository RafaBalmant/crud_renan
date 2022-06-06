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
    <html lang="pt-br" >
    <head>
        

        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <title>Área Usuário</title> 
        <link rel="stylesheet" href="$path_conteudo/css/libs/font-awesome.min.css" />
        <link rel="stylesheet" href="$path_conteudo/css/libs/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="$path_conteudo/css/plugin/toastr.min.css"  />
        <link rel="stylesheet" type="text/css" href="$path_conteudo/css/spinkit/spinkit.min.css" />
        <link rel="stylesheet" type="text/css" href="$path_conteudo/css/plugin/jquery-ui-auto.css"  />

        <style>
            .container{
                display: flex;
                flex-flow: row wrap;
                justify-content: center;
                height: 88vh;
                width:100%;
                background-image: linear-gradient(10deg, #2f00ff,#fd6500 , #F9FAFB  );
            }
            .box{
                background:#0267B5;
                height: 55rem;
                padding: 1rem;
                display:flex;
                margin-top: 3rem;
                box-shadow: 2rem 3rem 2rem -2rem #00000094;
                border-radius: 6rem;
            }
            .img{
                text-align:center;
                width:50%;
            }
            .img > img{
                margin-top: 1rem;
            }
            body{
                margin:0;
                background:#0267B5;
                color:white;
                font-family:Roboto;
            }
            .menu{
                width: 100%;
                display: flex;
                align-items: center;
                align-items: center;
                justify-content: space-between;
                flex: 1 1 0%;
                max-width: 90rem;
                margin: 0rem auto;
                width: 100%;
                padding: 6rem 0rem;
                height: 0rem;
                background: #0267B5; 
            }
            .forms{
                width:96%;
                margin: 0 auto;
                padding: 2rem;
                border: none;
                margin-bottom: 4rem;
                border-radius: 13rem;
                color:black;
            }

            .box > section{
                display: flex;
                flex: 1 1 0%;
                flex-direction: column;
            }
            .borda{
                border-right: 0.3rem solid #fff;
                }
            .menu > img{
                width: 15%;
            }
            .menu-div{
                background: #0267B5;
            }
            .btn-consulta{
                padding: 2rem;
                width: 65%;
                background: linear-gradient(to right,#FD7726, #7000DF);
                border: none;
                border-radius: 5rem;
                cursor:pointer;
                margin: 0 auto;
                font-size: 2rem;
                font-weight:bold;
            }
            .btn-consulta:hover{
                opacity:0.9;   
                -webkit-transition: all 200ms ease-in;
                -ms-transition: all 200ms ease-in;
                -moz-transition: all 200ms ease-in;
                transition: all 200ms ease-in;
            }
            label{
                text-shadow:0rem 0rem 1rem black;
            }
            \@media only screen and (max-width: 1280px) {
                .container{
                    justify-content:flex-start;
                }
                .img{
                    width: 100%;
                }
                .btn-consulta {
                    width:70%;
                }
                .img > img{
                    width: 25%;
                }
                .btn-consulta{
                    font-size: 1.5rem;
                    padding:1rem;
                }
                .box{
                    height: 41rem;
                }
                .forms{
                    padding:1rem;
                    margin-bottom: 1rem;
                }

            }
            \@media only screen and (max-width: 600px) {
                .forms{
                    padding:1rem;
                    margin-bottom: 1rem;
                }
                .img > img{
                    width:35%;
                    
                }
                .btn-consulta{
                    font-size: 1.5rem;
                    padding:1rem;
                }
                .box{
                    height: 41rem;
                }
                .menu > img{
                    width: 35%;
                }
            }

            \@media only screen and (max-width: 890px) {
                .menu > img{
                    width: 35%!important;
                } 
            }


        </style>
    </head>

    <body>
        <div class="menu-div">
        <header class="menu">
            <img src="$path_conteudo/js/informatica/renan_soares/kabum-logo-2.png">
            <div>
            </div>
        </header>
        </div>
        <div class="container">
            <div class="img">
                <img src="$path_conteudo/js/informatica/renan_soares/logo_kabum.png">
                <div class="box">
                    <section class="borda">
                    <h3> Tenho um cadastro </h3>
                    <label for="login">Login</label>
                    <input type="text" class="forms" onkeyup="removeAcento(this.value,this)" id="usuario" name="usuario">
                    <label for="senha">Senha</label>
                    <input type="password" class="forms" id="senha" name="senha"> 
                    <input type="button" class="btn-consulta"    id="btn-logar"  value="Logar">
                    </section>

                    <section>
                    <form id="form-cadastro-usuario">
                    <h3> Não tenho um cadastro </h3>
                    <label for="login">Login</label>
                    <input type="text" class="forms" id="usuario_cadastro" onkeyup="removeAcento(this.value,this)" name="usuario_cadastro">
                    <label for="senha">Senha</label>
                    <input type="password" onblur="validaSenha();" class="forms" id="senha_cadastro" name="senha_cadastro"> 
                    <p style="display:none;font-weight:bold" id="txt_senha"></p>
                    <label for="confirma_senha">Confirmar Senha</label>
                    <input type="password" onblur="validaSenha();" class="forms" id="confirma_senha" name="confirma_senha"> 
                    <input type="button" class="btn-consulta" disabled   id="btn-cadastro"  value="Cadastrar-se">
                    </form>
                    </section>
                </div>
            </div>
        </div>
        <script type="text/javascript" src='$path_conteudo/js/jquery.min.js'></script>
        <script type="text/javascript" src='$path_conteudo/js/jquery.mask.min.js'></script>
        <script type="text/javascript" src="$path_conteudo/js/libs/bootstrap/bootstrap.min.js"></script>
        <script type="text/javascript" src="$path_conteudo/js/plugin/toastr.min.js"></script>
        <script type="text/javascript" src="$path_conteudo/js/plugin/toastr.global.js"></script>
        <!--Caminho do seu JS-->
        <script src='$path_conteudo/js/informatica/renan_soares/login.js'></script>
    </body>
</html>

HTML

1;