#!/usr/bin/perl
BEGIN {
    $BASEAPP = $ENV{HTTP_BASEAPP};
    push @INC, "$BASEAPP/GLOBAL/cgi-local/module/";
}
use v5.10;
use JSON;
use Data::Dumper;
use DateTime;
use CGI;
use CGI::Carp qw(fatalsToBrowser set_message);
use Encode qw(decode encode);
use Library::V1::Format::Encoding::SimpleEncoding;
require $BASEAPP."/GLOBAL/cgi-local/modulos/kernel/000.cgi";



my $json = JSON->new();
my $acao = form('acao');

print $query->header("application/json");

#Funções CLIENTES

sub listarClientes {

    mysqlr('open');
    my ($campo , $valor , $permissoes, $id_usuario, $possuiId , $id_cliente) = @_;
    my $condicao = ($campo eq "" ) ? "" : " AND $campo = ? ";
    $condicao = ($valor eq "") ? "" : "$condicao";

    if($campo eq 'data_nascimento'){     
        $condicao = " AND data_nascimento = ?";
    }
    if($campo eq "nome" || $campo eq "email" ){
        $condicao =" AND $campo LIKE concat('%', ?, '%') ";
    }
    if($valor eq ""){
        $condicao = "";
    }
    my $condicao2 = ($permissoes == 0) ? " AND id_login = $id_usuario" : ""; 
    my $condicao3 = ($possuiId eq 't') ? " AND cc.codigo = ?" : "";
    #query que será executada
    my $sql = "
        SELECT cc.codigo,
        cc.nome,
        cc.cpf,
        cc.rg,
        cc.email,
        cc.telefone1,
        cc.telefone2,
        cc.data_nascimento,
        cc.ativo,
        cc.id_login,
        (SELECT COUNT(0) FROM crud_enderecos ce WHERE  ce.codigo_cliente = cc.codigo) AS contador_endereco
        FROM crud_clientes1 cc 
        WHERE 1=1
        $condicao
        $condicao2
        $condicao3
        ORDER BY codigo DESC
        ";

    my $sth = $conexaor->prepare($sql);

    if($possuiId eq 't'){
        $sth->execute($id_cliente);
    }else{
        if($campo eq "" || $valor eq ""){
            $sth->execute();    
        }else{
            $sth->execute($valor);
        }
    }

    mysqlr('close');  
    return $sth->fetchall_arrayref({});
}

sub desativar_ativar{

    mysql('open');
    my ($ativos_inativos,$id_cliente,$id_endereco,$tabela) = @_;
    my $tabela_final = ($tabela eq "endereco") ? "crud_enderecos" : "crud_clientes1";
    my $condicao = ($tabela eq "endereco") ? " id = ?" : " codigo = ?";
    my $id = ($tabela eq "endereco") ? $id_endereco : $id_cliente;
    my $sql = "
    UPDATE 
        $tabela_final
    SET
        ativo = ? 
    WHERE 
        $condicao ";
    
    my $sth = $conexao->prepare($sql);

    mysql('close');
    my $retorno = "false";
    if($sth->execute($ativos_inativos,$id)){
        $retorno = "true";
    }
    return $retorno;
}

sub alterar_cliente {
    mysql('open');

    my ($id_cliente,$nome,$email,$cpf,$rg,$data_nascimento,$telefone1,$telefone2) = @_;
    my $sql = "
    UPDATE  
        crud_clientes1
    SET
        nome = ?,
        cpf = ?,
        rg = ?,
        email = ?,
        telefone1 = ?,
        telefone2 = ?,
        data_nascimento = ?
    WHERE
        codigo = ?
    ";
        my $sth = $conexao->prepare($sql);

        mysql('close');
        my $retorno = "false";
        if($sth->execute($nome,$cpf,$rg,$email,$telefone1,$telefone2,$data_nascimento,$id_cliente)){
            $retorno = "true";
        }
        return $retorno;   
}

sub salvar_cliente {
    mysql('open');
    my ($nome,$email,$cpf,$rg,$data_nascimento,$telefone1,$telefone2,$id_usuario,$habilita_cadastro_endereco) = @_;
    my $ativo =  0 ;
    if($habilita_cadastro_endereco eq 't'){
        $ativo = 1;
    }

    my $sql = "
    INSERT INTO 
        crud_clientes1(
        nome,
        cpf,
        rg,
        email,
        telefone1,
        telefone2,
        data_nascimento,
        ativo,
        id_login
    )
    VALUES(
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    )
    ";

    my $sth = $conexao->prepare($sql);
    mysql('close');
    
    $sth->execute($nome,$cpf,$rg,$email,$telefone1,$telefone2,$data_nascimento,$ativo,$id_usuario);
    return $sth->{mysql_insertid};  
}

#-- END FUNÇÕES CLIENTES --

#FUNÇÕES ENDEREÇOS
sub listarEnderecosCliente {
    mysqlr('open');
    my ($id_cliente,$possuiId,$id_endereco) = @_;
    my $condicao = ($possuiId eq "t" ) ? " id = ?" : " codigo_cliente = ?"; 
    my $id = ($possuiId eq "t") ? $id_endereco : $id_cliente;
    
    my $sql = "
    SELECT
        id,
        logradouro,
        numero,
        bairro,
        cep,
        cidade,
        estado,
        codigo_cliente,
        ativo
    FROM
        crud_enderecos
    WHERE
        $condicao
    ";
    
    my $sth = $conexaor->prepare($sql);
    mysqlr('close');
    $sth->execute($id);
    
    return $sth->fetchall_arrayref({});
}

sub inserir_endereco {
    mysql('open');
    my ($logradouro,$numero,$bairro,$cep,$estado,$cidade,$id_cliente) = @_;
    my $sql="
    INSERT INTO crud_enderecos(
        logradouro,
        numero,
        bairro,
        cep,
        estado,
        cidade,
        codigo_cliente,
        ativo)
    VALUES(
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?)
    ";
    my $sth = $conexao->prepare($sql);
    my $ativo = 1;
    mysql('close');
    return $sth->execute($logradouro,$numero,$bairro,$cep,$estado,$cidade,$id_cliente,$ativo);
}

sub excluir_endereco {
    mysql('open');
    my ($codigo_endereco) = @_;
    my $sql="
    DELETE FROM
        crud_enderecos
    WHERE
        id = ?
    ";
    my $sth = $conexao->prepare($sql);
    mysql('close');
    my $retorno = "false";
    if($sth->execute($codigo_endereco)){
        $retorno = "true";
    }
    return $retorno;
}

sub alterarEndereco {
    mysql('open');
    my ($logradouro,$numero,$bairro,$cep,$estado,$cidade,$id_endereco) = @_;
    my $sql="
    UPDATE
        crud_enderecos
    SET
        logradouro = ?,
        numero = ?,
        bairro = ?,
        cep = ?,
        cidade = ?,
        estado = ?
    WHERE
        id = ?";
    my $sth = $conexao->prepare($sql);
    mysql('close');
    my $retorno = "false";
    if($sth->execute($logradouro,$numero,$bairro,$cep,$cidade,$estado,$id_endereco)){
       $retorno = "true";
    }
    return $retorno;
}

#LOGIN

sub validarUsuarioExistente {
    mysqlr('open');
    my($login) = @_;
    my $sql = "
    SELECT
        id,
        login,
        permissoes,
        senha
    FROM
        crud_login
    WHERE
        login = ?";
    my $sth = $conexaor->prepare($sql);
    $sth->execute($login);
    mysqlr('close');
    return $sth->fetchall_arrayref({});
}

sub cadastrarUsuario {
    mysql('open');
    my($login,$senha) = @_;
    my $sql="
    INSERT INTO
        crud_login(
        login,
        senha,
        permissoes)
    VALUES(
        ?,
        ?,
        ?)";
    my $sth = $conexao->prepare($sql);
    my $permissoes = 0;
    mysql('close');

    return $sth->execute($login,$senha,$permissoes);
}

sub logarUsuario {
    mysqlr('open');
    my ($usuario,$senha) = @_;
    my $sql = "
    SELECT 
        login,
        senha,
        permissoes
    FROM
        crud_login
    WHERE
        login = ?
    AND
        senha = ?";
    my $sth = $conexaor->prepare($sql);
    $sth->execute($usuario,$senha);
    mysqlr('close');
    return $sth->rows;
}

sub listarUsuarios {
    mysqlr('open');
    my $sql = "
    SELECT
        id,
        login,
        permissoes
    FROM 
        crud_login
    ORDER BY login";
    my $sth = $conexaor->prepare($sql);
    mysqlr('close');
    $sth->execute();
    return $sth->fetchall_arrayref({});
}

sub editarUsuario {
    mysql('open');
    my ($id_usuario,$tipo_usuario) = @_;
    my $sql = "
    UPDATE
        crud_login
    SET
        permissoes = ?
    WHERE id = ?";
    my $sth = $conexao->prepare($sql);
    mysql('close');
    return $sth->execute($tipo_usuario,$id_usuario);
}

sub excluir_perfil {
    mysql('open');
    my ($codigo_perfil) = @_;
    my $sql="
    DELETE FROM
        crud_login
    WHERE
        id = ?
    ";
    my $sth = $conexao->prepare($sql);
    mysql('close');
    my $retorno = "false";
    if($sth->execute($codigo_perfil)){
       $retorno = "true";
    }
    return $retorno;
}

sub validarEndereco {
    mysqlr('open');
    my ($id_cliente) = @_;
    my $sql = "
    SELECT
        *
    FROM
        crud_enderecos
    WHERE
        codigo_cliente = ?
    AND ativo = 1";
    my $sth = $conexaor->prepare($sql);
    mysqlr('close');
    $sth->execute($id_cliente);
    return $sth->rows;
}

given ($acao) {
    when ('salvarCadastro') {      
        my $nome = SimpleEncoding::encodeToIso(form('nome'));
        my $email = form('email');
        my $cpf = form('cpf');
        my $rg = form('rg');
        my $tel1 = form('tel1');
        my $tel2 = form('tel2');
        my $data_nasc = form('data_nasc');

        my @dados_cliente = salvaDadosCliente($nome,$email,$cpf,$rg,$tel1,$tel2,$data_nasc);

        print $json->encode({
            "status" => "Sucesso",
            "mensagem"=> $msg
        });
    }

    when ('listarClientes') {
        my $campo = form('campo');
        my $valor = SimpleEncoding::encodeToIso(form('valor'));
        my $permissoes = form('permissoes');
        my $id_usuario = form('id_usuario');
        my $possuiId = form('possuiId');
        my $id_cliente = form('id_cliente');
        my $todos_clientes = listarClientes($campo,$valor,$permissoes,$id_usuario,$possuiId,$id_cliente);

        print $json->encode({
            "status"   => "sucesso",
            "retorno" => $todos_clientes
        });
    }

    when ('desativar_ativar') {
        my $ativo_inativo = form('ativo_inativo');
        my $id_cliente = form('id_cliente');
        my $id_endereco = form('id_endereco');
        my $tabela = form('tabela');

        my $retorno = desativar_ativar($ativo_inativo,$id_cliente,$id_endereco,$tabela);
        my $status;
        my $msg = "";
        $msg = "Ocorreu um erro ao realizar a operação!";
        $status = "false"; 
        my $campo = ($tabela eq 'endereco') ? "Endereço" : "Cliente";
        if($retorno == "true"){
            $msg = "$campo Desativado com Sucesso! ";
            if($ativo_inativo == 1){
                $msg = "$campo Ativado com Sucesso! ";
            }
            $status = "true";   
        }

        print $json->encode({
            "status"   => "$status",
            "msg" => "$msg",
        });
    }

    when ('alterar_cliente'){
        my $id_cliente = form('id_cliente');
        my $nome = SimpleEncoding::encodeToIso(form('nome_editar'));
        my $email = form('email_editar');
        my $cpf = form('cpf_editar');
        my $rg = form('rg_editar');
        my $data_nascimento = form('data_nasc');
        my $telefone1 = form('tel1_editar');
        my $telefone2 = form('tel2_editar');

        my $retorno = alterar_cliente($id_cliente,$nome,$email,$cpf,$rg,$data_nascimento,$telefone1,$telefone2);

        my $status = "Sucesso";
        my $msg = "Cliente alterado com sucesso!";

        if($retorno eq "false"){
            $status = "Erro";
            $msg = "Ocorreu um erro ao alterar o cliente!";
        }

        print $json->encode({
            "status" => "$status",
            "msg"   => "$msg",
        });
    }

    when ('salvar_cliente'){
        my $nome = SimpleEncoding::encodeToIso(form('nome'));
        my $email = form('email');
        my $cpf = form('cpf');
        my $rg = form('rg');
        my $data_nascimento = form('data_nasc_mascara');
        my $telefone1 = form('tel1');
        my $telefone2 = form('tel2');
        my $id_usuario = form('id_usuario');
        my $logradouro_cadastro = form('logradouro_cadastro');
        my $numero_cadastro = form('numero_cadastro');
        my $cep_cadastro = form('cep_cadastro');
        my $bairro_cadastro = form('bairro_cadastro');
        my $estado_cadastro = form('estado_cadastro');
        my $cidade_cadastro = SimpleEncoding::encodeToIso(form('cidade_cadastro'));
        my $habilita_cadastro_endereco = form('habilita_cadastro_endereco');

        my $retorno = salvar_cliente($nome,$email,$cpf,$rg,$data_nascimento,$telefone1,$telefone2,$id_usuario,$habilita_cadastro_endereco);

        if($habilita_cadastro_endereco eq 't'){
           inserir_endereco($logradouro_cadastro,$numero_cadastro,$bairro_cadastro,$cep_cadastro,$estado_cadastro,$cidade_cadastro,$retorno);
        }
        my $status = "Sucesso";
        my $msg = "Cliente inserido com sucesso!";

        if(!$retorno){
            $status = "Erro";
            $msg = "Ocorreu um erro ao inserir o cliente!";
        }

        print $json->encode({
            "status" => "$status",
            "msg"   => "$msg",
        });
    }
    
    when ('listarEnderecosCliente') {
        my $id_cliente = form('id_cliente');
        my $possuiId = form('possuiId');
        my $id_endereco = form('id_endereco');
        my @retornoEndereco = listarEnderecosCliente($id_cliente,$possuiId,$id_endereco);

        my $status = "Sucesso";
        print $json->encode({
            "status"   => "$status",
            "retorno" => @retornoEndereco,
        });
    }

    when ('inserir_endereco') {
        my $logradouro = SimpleEncoding::encodeToIso(form('logradouro'));
        my $numero = form('numero');
        my $bairro = SimpleEncoding::encodeToIso(form('bairro'));
        my $cep = form('cep');
        my $estado = SimpleEncoding::encodeToIso(form('estado'));
        my $cidade = SimpleEncoding::encodeToIso(form('cidade'));
        my $id_cliente = form('id_cliente');

        my $retorno = inserir_endereco($logradouro,$numero,$bairro,$cep,$estado,$cidade,$id_cliente);
        my $status = "Sucesso";
        my $msg = "Endereço inserido com sucesso!";

        if(!$retorno){
            $status = "Erro";
            $msg = "Ocorreu um erro ao inserir o endereço!";
        }

        print $json->encode({
            "status" => "$status",
            "msg" => "$msg",
        });
    }
    when ('excluir_endereco') {
        my $codigo_endereco = form('codigo_endereco');

        my $retorno = excluir_endereco($codigo_endereco);

        my $status = "Sucesso";
        my $msg = "Endereço excluído com sucesso!";

        if($retorno eq "false"){
            $status = "Erro";
            $msg = "Ocorreu um erro ao excluir o endereço!";
        }
    
        print $json->encode({
            "status" => "$status",
            "msg" => "$msg",
        });

    }

    when('alterar_endereco') {
        my $logradouro = SimpleEncoding::encodeToIso(form('logradouro_editar'));
        my $numero = form('numero_editar');
        my $bairro = SimpleEncoding::encodeToIso(form('bairro_editar'));
        my $cep = form('cep_editar');
        my $estado = SimpleEncoding::encodeToIso(form('estado_editar'));
        my $cidade = SimpleEncoding::encodeToIso(form('cidade_editar'));
        my $id_endereco = form('id_endereco');

        my $retorno = alterarEndereco($logradouro,$numero,$bairro,$cep,$estado,$cidade,$id_endereco);
        
        my $status = "Sucesso";
        my $msg = "Endereço alterado com sucesso!";

        if($retorno eq "false"){
            $status = "Erro";
            $msg = "Ocorreu um erro ao alterar o endereço!";
        }
        print $json->encode({
            "status" => "$status",
            "msg" => "$msg",
        });
    }

    when('validarEndereco') {
        my $id_cliente = form('id_cliente');

        my $retorno = validarEndereco($id_cliente);
  
        print $json->encode({
            "status" => "Sucesso",
            "retorno" => $retorno,
        })
    }

    when('validarUsuarioExistente') {
        my $login = form('login');

        my $retorno = validarUsuarioExistente($login);
  
        print $json->encode({
            "status" => "Sucesso",
            "retorno" => $retorno,
        })
    }

    when('cadastrarUsuario') {
        my $login = form('login');
        my $senha = form('senha');

        my $retorno = cadastrarUsuario($login,$senha);

        my $status = "Sucesso";
        my $msg = "Usuário cadastrado com sucesso!";

        if(!$retorno ){
            $status = "Erro";
            $msg = "Ocorreu um erro ao cadastrar o usuário!";
        }
        print $json->encode({
            "status" => "$status",
            "msg" => "$msg",
        });
    }

    when('logarUsuario'){
        my $usuario = form('login');
        my $senha = form('senha');

        my $retorno = logarUsuario($usuario,$senha);

        print $json->encode({
            "status" => "Sucesso",
            "retorno" => $retorno,
        })
    }

    when('listarUsuarios'){
        my $retorno = listarUsuarios();

        print $json->encode({
            "status" => "Sucesso",
            "retorno" => $retorno,
        })
    }

    when('editarUsuario'){
        my $tipo_usuario = form('tipo_usuario');
        my $id_usuario = form('id_usuario');
        my $retorno = editarUsuario($id_usuario,$tipo_usuario);

        my $status   = "Sucesso";
        my $msg = "Usuário alterado com sucesso";

        if(!$retorno){
            $status   = "Erro";
            $msg = "Ocorreu algum erro ao alterar o usuário!";
        }

         print $json->encode({
            "status" => "$status",
            "msg" => "$msg",
        });
    }

    when ('excluir_perfil') {
        my $codigo_perfil = form('codigo_perfil');

        my $retorno = excluir_perfil($codigo_perfil);

        my $status = "Sucesso";
        my $msg = "Endereço excluído com sucesso!";

        if($retorno eq "false"){
            $status = "Erro";
            $msg = "Ocorreu um erro ao excluir o endereço!";
        }
    
        print $json->encode({
            "status" => "$status",
            "msg" => "$msg",
        });
    }
    default {
        print $json->encode({
            "status" => "Sucesso",
            "mensagem" => "Nenhuma opção",
        });
    }
}
