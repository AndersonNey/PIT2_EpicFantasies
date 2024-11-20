from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from .models import Perfil,User,Historias,Comentario,Reacao,Categoria,Denuncias,TwoFactorAuth,SystemUtilities
from django.urls import reverse
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractDay
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator


class BuilderStory:
    def __init__(self,historia,comentario,reacao):
        self.id = historia.id
        self.historia = historia
        self.comentario = comentario.order_by('-id')
        self.reacao = reacao
        
        self.reacaoExcelente = 0
        self.reacaoBom = 0
        self.reacaoLegal = 0
        self.reacaoNaoetaolegal = 0
        self.reacaoNaogostei = 0


        for reacao_indivudal in reacao: 
            if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[0][0]:
                self.reacaoExcelente += 1
            if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[1][0]:
                self.reacaoBom += 1
            if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[2][0]:
                self.reacaoLegal += 1
            if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[3][0]:
                self.reacaoNaoetaolegal += 1
            if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[4][0]:
                self.reacaoNaogostei += 1




def home(request):
    if SystemUtilities.objects.all().exists():
        imagem_ads = SystemUtilities.objects.all().first().get_picture_ads_url
    else:
        imagem_ads =  'https://placehold.co/1200x1200'

    return render(request,'epicfantasiesapp/pages/home.html',context={'imagem_ads':imagem_ads,},)


def entrar(request):


    if request.user.is_authenticated:
        if not request.user.perfil.is_verified:
            return redirect('/entrar/codigodeverificacao')        
        if request.user.is_superuser:
            return redirect('/admin')
        if request.user.perfil.is_administrador_sys:
            return redirect('/meuPerfilAdministrador')
        return redirect('/meuPerfil') 
    
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=name,password=password)
        if user is not None:
            messages.info(request, "Login Correto")
            login(request,user) 
            if not request.user.perfil.is_verified:
                return redirect('/entrar/codigodeverificacao/')
            else:
                return redirect('/meuPerfil') 
                
        
                  
                
        else:
            messages.error(request,"Login Incorreto")

        
    

    

    return render(request,'epicfantasiesapp/pages/entrar.html')


def cadastrar(request):
    if request.user.is_authenticated:
        logout(request)


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        passwordconfirm = request.POST['passwordconfirm']
        email = request.POST['email']
        
        if password != passwordconfirm:
            messages.error(request, "As senhas não coincidem")
            return redirect('/cadastrar')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso")
            return redirect('/cadastrar')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já está em uso")
            return redirect('/cadastrar')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        perfil, created = Perfil.objects.get_or_create(user=user)

        login(request,user)
        return render(request,'epicfantasiesapp/pages/meuperfilusuario.html')
    

    return render(request,'epicfantasiesapp/pages/cadastrar.html')


@login_required(login_url='/entrar')
def feed(request):
    
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    historias = Historias.objects.filter(is_published=True)
    categorias_disponiveis = Categoria.objects.all()
    
    lista_view = []
  
    for historia in historias:
        comentario = Comentario.objects.filter(historia=historia)   
        reacao = Reacao.objects.filter(historia=historia)
        b1 = BuilderStory(historia,comentario,reacao)
        lista_view.append(b1)

    paginator = Paginator(lista_view, 10)
    pagina = request.GET.get('page')
    itens_pagina = paginator.get_page(pagina)

    
    return render(request,'epicfantasiesapp/pages/feed.html',context={"user":request.user,
                                                                      "lista_view":itens_pagina,
                                                                      "categorias_disponiveis":categorias_disponiveis,
                                                                      "is_feed":True,
                                                                      "is_detalhes":False,
                                                                      "is_meuperfil":False,
                                                                      })


@login_required(login_url='/entrar')
def perfilUsuario(request):
    if request.user.perfil.is_administrador_sys:
        return redirect('/meuPerfilAdministrador')
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    historias = Historias.objects.filter(user=request.user)
    categorias_disponiveis = Categoria.objects.all()
    
    lista_view_published = []
    lista_view_not_published = []

    for historia in historias:
        comentario = Comentario.objects.filter(historia=historia)   
        reacao = Reacao.objects.filter(historia=historia)
        b1 = BuilderStory(historia,comentario,reacao)
        if historia.is_published:
            lista_view_published.append(b1)
        else:
            lista_view_not_published.append(b1)






    return render(request,'epicfantasiesapp/pages/meuperfilusuario.html',context={"user":request.user,
                                                                                  "lista_view_published":lista_view_published,
                                                                                  "lista_view_not_published":lista_view_not_published,
                                                                                  "categorias_disponiveis":categorias_disponiveis,
                                                                                  "is_feed":False,
                                                                                  "is_detalhes":False,
                                                                                  "is_meuperfil":True,
                                                                                  })


@login_required(login_url='/entrar')
def perfilUsuarioUpdate(request):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    user = request.user
    perfil = user.perfil
    redessociais = user.redessociais
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        foto_perfil = request.FILES.get('foto_perfil')
        instagram = request.POST.get('instagram')
        facebook = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        tiktok = request.POST.get('tiktok')

        if first_name and first_name != user.first_name:
            user.first_name = first_name

        if last_name and last_name != user.last_name:
            user.last_name = last_name

        if foto_perfil:
            perfil.foto_perfil = foto_perfil

        if instagram != redessociais.instagram:
            redessociais.instagram = instagram

        if facebook != redessociais.facebook:
            redessociais.facebook = facebook

        if twitter != redessociais.twitter:
            redessociais.twitter = twitter

        if tiktok != redessociais.tiktok:
            redessociais.tiktok = tiktok

        user.save()
        perfil.save()
        redessociais.save()


    return redirect('/system/redirecionamento/0/')


@login_required(login_url='/entrar')
def meuPerfilStory(request):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        previu = request.POST.get('previu')
        conteudo = request.POST.get('conteudo')
        categoria_id = request.POST.get('categoria')
        is_published = request.POST.get('is_published')
        try:
            categoria_id = int(categoria_id)
        except:
            categoria_id = None
        if not Categoria.objects.filter(id=categoria_id).exists():
            categoria_id = None

        foto = request.FILES.get('foto') if 'foto' in request.FILES else None
        if is_published =="on":
            is_published = True
        else:
            is_published = False
        
        
        historia = Historias(
            user=request.user,  
            titulo=titulo,
            previu=previu,
            conteudo=conteudo,
            categoria=Categoria.objects.filter(id=categoria_id)[0],
            foto=foto,
            is_published=is_published
        )
        historia.save()

    return redirect('/meuPerfil')


def storyDetalhes(request,id):  
    historias = Historias.objects.filter(id=id)
    
    lista_view = []


                    
    for historia in historias:
        comentario = Comentario.objects.filter(historia=historia)   
        reacao = Reacao.objects.filter(historia=historia)
        b1 = BuilderStory(historia,comentario,reacao)
        lista_view.append(b1)

    return render(request,'epicfantasiesapp/pages/detalhes.html',context={"user":request.user,
                                                                          "lista_view":lista_view,
                                                                          "is_feed":False,
                                                                          "is_detalhes":True,
                                                                          "is_meuperfil":False,
                                                                          })


def error404(request,exception):  
    return render(request,'epicfantasiesapp/pages/error404.html',status=404)


@login_required(login_url='/entrar')
def perfilAdministrador(request):
    if not request.user.perfil.is_administrador_sys:
        return redirect('/meuPerfil')
    
    if SystemUtilities.objects.all().exists():
        imagem_ads = SystemUtilities.objects.all().first().get_picture_ads_url
    else:
        imagem_ads =  'https://placehold.co/1200x1200'

    historias_com_denuncias = Historias.objects.annotate(num_denuncias=Count('denuncias')).filter(num_denuncias__gt=1)
    
    # #GRAFICO1
    # historias = Historias.objects.values('categoria__nome').annotate(total=Count('id'))
    # categorias = [h['categoria__nome'] for h in historias]
    # totais = [h['total'] for h in historias]

    # #GRAFICO2
    # historias_2023 = Historias.objects.filter(data_de_criacao=2023).annotate(month=ExtractMonth('data_de_criacao')).values(
    #     'month').annotate(count=Count('id')).order_by('month')

    # historias_2024 = Historias.objects.filter(data_de_criacao__year=2024).annotate(month=ExtractMonth('data_de_criacao')).values(
    #     'month').annotate(count=Count('id')).order_by('month')

    # labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']  # Rótulos para os meses
    # dados_2023 = [historia['count'] for historia in historias_2023]
    # dados_2024 = [historia['count'] for historia in historias_2024]

    # #GRAFICO3
    # mes_atual = timezone.now().month
    # ano_atual = timezone.now().year

    # # Consulta para obter o número de histórias por dia no mês atual
    # historias_por_dia = (Historias.objects.filter(data_de_criacao__month=mes_atual, data_de_criacao__year=ano_atual).annotate(dia=ExtractDay('data_de_criacao'))
    #     .values('dia').annotate(count=Count('id')).order_by('dia')
    # )

    # # Preparar os dados para o gráfico
    # labels1 = [dia['dia'] for dia in historias_por_dia]
    # dados1 = [dia['count'] for dia in historias_por_dia]


    return render(request,'epicfantasiesapp/pages/meuperfiladministrador.html',context={"user":request.user,
                                                                                        # 'categorias': categorias,
                                                                                        # 'totais': totais,
                                                                                        # 'labels': labels,
                                                                                        # 'historias_2023': dados_2023,
                                                                                        # 'historias_2024': dados_2024,
                                                                                        # 'labels_historias_por_dia': labels1,
                                                                                        # 'dados_historias_por_dia': dados1,
                                                                                        'historias_com_denuncias':historias_com_denuncias,
                                                                                        'imagem_ads':imagem_ads,})


@login_required(login_url='/entrar')
def sair(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/')


@login_required(login_url='/entrar')
def editarHistoria(request,id):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    if request.method == 'POST':
        historia = Historias.objects.filter(id=id,user=request.user)
        historia = historia[0]

        titulo = request.POST.get('titulo')
        previu = request.POST.get('previu')
        conteudo = request.POST.get('conteudo')
        foto = request.FILES.get('foto') if 'foto' in request.FILES else None
        is_published = request.POST.get('is_published')

        if is_published =="on":
            is_published = True
        else:
            is_published = False


        if titulo != historia.titulo:
            historia.titulo = titulo

        if previu != historia.previu:
            historia.previu = previu
        
        if conteudo != historia.conteudo:
            historia.conteudo = conteudo

        if foto:
            historia.foto = foto

        if is_published != historia.is_published:
            historia.is_published = is_published

        historia.save()
        return redirect("/system/redirecionamento/0/")


    


    historias = Historias.objects.filter(id=id,user=request.user)
    
    lista_view = []
                    
    for historia in historias:
        comentario = Comentario.objects.filter(historia=historia)   
        reacao = Reacao.objects.filter(historia=historia)
        b1 = BuilderStory(historia,comentario,reacao)
        lista_view.append(b1)

    return render(request, "epicfantasiesapp/pages/editarHistoria.html",context={"user":request.user,"lista_view":lista_view[0],})


@login_required(login_url='/entrar')
def redirecionamento(request,id):
    if id == 1 or id == 0:
        return render(request,"epicfantasiesapp/pages/paginaDeRedirecionamento.html",context={"status":id})
    return redirect("/")


@login_required
def comentario(request, id):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        comentario_texto = data.get('comment')
        usuario = request.user

        user_logado = "true"
        
        if comentario_texto:
            try:
                historia = Historias.objects.get(id=id)
                comentario = Comentario.objects.create(
                    historia=historia,
                    user=usuario,
                    valor_comentario=comentario_texto
                )
                response_data = {
                    'comment': comentario.valor_comentario,
                    'user_logado':user_logado,
                    'user': {
                        'username': usuario.username,
                        'profile_picture': usuario.perfil.get_foto_perfil_url
                    }
                }
                return JsonResponse(response_data, status=201)
            except Historias.DoesNotExist:
                return JsonResponse({'error': 'História não encontrada','user_logado':user_logado,}, status=404)
        else:
            return JsonResponse({'error': 'Dados inválidos','user_logado':user_logado,}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido','user_logado':user_logado,}, status=405)
    

@login_required(login_url='/entrar')
def emocao(request,id):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   

    

    emoji = request.GET.get('emoji')

    
    if emoji == 'Excelente':
        reacao_valor=Reacao.TIPO_REACAO_CHOICES[0][0]
    elif emoji == 'Bom':
        reacao_valor=Reacao.TIPO_REACAO_CHOICES[1][0]
    elif emoji == 'Legal':
        reacao_valor=Reacao.TIPO_REACAO_CHOICES[2][0]
    elif emoji == 'Naoetaolegal':
        reacao_valor=Reacao.TIPO_REACAO_CHOICES[3][0]
    elif emoji == 'Naogostei':
        reacao_valor=Reacao.TIPO_REACAO_CHOICES[4][0]

    historia = Historias.objects.filter(id=id).first()    

    if Reacao.objects.filter(historia=historia,user=request.user).exists():
        reacao = Reacao.objects.filter(historia=historia,user=request.user).first()
        if reacao.tipo_reacao == reacao_valor:
            reacao.delete()
        else:
            reacao.delete()
            reacao = Reacao(historia=historia,user=request.user,tipo_reacao=reacao_valor)
            reacao.save()
    else:
        reacao = Reacao(historia=historia,user=request.user,tipo_reacao=reacao_valor)
        reacao.save()


    reacao = Reacao.objects.filter(historia=historia)

    reacaoExcelente = 0
    reacaoBom =0
    reacaoLegal =0
    reacaoNaoetaolegal=0
    reacaoNaogostei=0
    for reacao_indivudal in reacao: 
        if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[0][0]:
            reacaoExcelente += 1
        if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[1][0]:
            reacaoBom += 1
        if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[2][0]:
            reacaoLegal += 1
        if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[3][0]:
            reacaoNaoetaolegal += 1
        if reacao_indivudal.tipo_reacao == Reacao.TIPO_REACAO_CHOICES[4][0]:
            reacaoNaogostei += 1

    response_data = {
        'excelente': reacaoExcelente,  
        'bom': reacaoBom,
        'legal': reacaoLegal,
        'naoetaolegal': reacaoNaoetaolegal,
        'naogostei': reacaoNaogostei,
    }
    
    return JsonResponse(response_data)
    

@login_required(login_url='/entrar')
def denuncia(request,id):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   

    if request.method == 'POST':

        if Historias.objects.filter(id=id).exists():
            historia = Historias.objects.filter(id=id).first()
            if not Denuncias.objects.filter(historia=historia,user=historia.user,usuario_denunciou=request.user).exists():
                denuncia = Denuncias(historia=historia,user=historia.user,usuario_denunciou=request.user)
                denuncia.save()
        
        return JsonResponse({'message': 'Denúncia recebida com sucesso.'})
    
    return JsonResponse({'error': 'Método não permitido.'}, status=405)
    

@login_required(login_url='/entrar')
def categoria(request,category):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   
    if not Categoria.objects.filter(id=category).exists():
        return redirect("/feed")
    
    categoria = Categoria.objects.filter(id=category)


    historias = Historias.objects.filter(categoria=categoria[0],is_published = True)
    categorias_disponiveis = Categoria.objects.all()
    
    lista_view = []

    for historia in historias:
        comentario = Comentario.objects.filter(historia=historia)   
        reacao = Reacao.objects.filter(historia=historia)
        b1 = BuilderStory(historia,comentario,reacao)
        lista_view.append(b1)

    
    return render(request,'epicfantasiesapp/pages/categoria.html',context={"user":request.user,"lista_view":lista_view,"categorias_disponiveis":categorias_disponiveis,"page_categoria":categoria[0]})
      

@login_required(login_url='/entrar')
def verificacao(request):
    def gerar_codigo_aleatorio():
        digitos = string.digits
        codigo = ''.join(random.choice(digitos) for _ in range(6))
        return codigo
    
    if request.user.perfil.is_verified:
        return redirect('/meuPerfil')

    if TwoFactorAuth.objects.filter(user=request.user).exists():
        verificacao = TwoFactorAuth.objects.filter(user=request.user).first()
        if TwoFactorAuth.code_expired(verificacao.timestamp):
            messages.info(request,'Código Expirado, um e-mail já foi enviado com seu novo código')
            verificacao.delete()
            code_random = gerar_codigo_aleatorio()

            subject = "Código de Verificação"
            html_message = render_to_string("emails/codigo_verificacao.html",{
                'user_name': request.user.username,
                'verification_code': code_random
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]
            send_mail(subject, plain_message, from_email, recipient_list,html_message=html_message)
            
            verificacao = TwoFactorAuth(
                user= request.user,
                verification_code = code_random
            )
            verificacao.save()
    else:
        code_random = gerar_codigo_aleatorio()
        messages.info(request,'Código enviado por e-mail, ele terá validade de 30 minutos')

        subject = "Código de Verificação"
        html_message = render_to_string("epicfantasiesapp/emails/codigo_verificacao.html",{
            'user_name': request.user.username,
            'verification_code': code_random
        })
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        send_mail(subject, plain_message, from_email, recipient_list,html_message=html_message)
        
        
        verificacao = TwoFactorAuth(
            user= request.user,
            verification_code = code_random
        )
        verificacao.save()


    if request.method == 'POST':
        codigo = ''.join([
            request.POST.get('codigo1', ''),
            request.POST.get('codigo2', ''),
            request.POST.get('codigo3', ''),
            request.POST.get('codigo4', ''),
            request.POST.get('codigo5', ''),
            request.POST.get('codigo6', '')
        ])

  
        codigo_esperado = TwoFactorAuth.objects.filter(user=request.user).first().verification_code

        if codigo == codigo_esperado:
            messages.info(request,'Código verificado com sucesso!')
            perfil = Perfil.objects.filter(user=request.user).first()
            perfil.is_verified = True
            perfil.save()
            codigo_usuario = TwoFactorAuth.objects.filter(user=request.user).first()
            codigo_usuario.delete()
            return render(request,'epicfantasiesapp/pages/paginaDeRedirecionamento.html')
        else:
            messages.info(request,'Código inválido. Tente novamente.')
    


    return render(request,'epicfantasiesapp/pages/entrarVerificacao.html')

@login_required(login_url='/entrar')
def thumbnail(request):
    if not request.user.perfil.is_verified:
        return redirect('/entrar/codigodeverificacao')   

    if request.method == 'POST':
        print(request.FILES.get('foto'))
        foto = request.FILES.get('foto') if 'foto' in request.FILES else None
        if not foto:
            return redirect("/system/redirecionamento/1/")
        
        if SystemUtilities.objects.all().exists():
            imagem_ads = SystemUtilities.objects.all().first()
            imagem_ads.picture_ads = foto
            imagem_ads.save()
        else:
            imagem_ads = SystemUtilities(picture_ads=foto)
            imagem_ads.save()
        
        return redirect("/system/redirecionamento/0/")
    
    return redirect('/entrar')
 







