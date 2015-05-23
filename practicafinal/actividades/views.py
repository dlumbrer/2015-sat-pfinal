from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from models import Actividades, UltimaActualizacion, Usuarios, Apuntada
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context, Template
from bs4 import BeautifulSoup
import urllib
import datetime
import constructores
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


# Create your views here.
@csrf_exempt
def inicio(request):
    salida = ""
    i = 0
    
    if request.method == "POST" and "rss" in request.POST.keys():
        salida += '<?xml version="1.0" encoding="utf-8"?>\n'
        salida += '<rss version="2.0">\n'
        salida += '<channel>\n'
        salida += '<title>Actividades de la pagina principal</title>\n'
        salida += '<link>http://localhost:' + request.META['SERVER_PORT'] + '</link>'
        salida += '<description>10 actividades mas proximas</description>\n'
        
        #DIEZ MAS PROXIMAS
        for m in range(0,11): #de 1+0 enero hasta 11+1 diciembre
            for d in range(0,30): #del dia 1 al 31
                try:
                    #saco las que coincidan con el dia y el mes
                    actividades = Actividades.objects.filter(mes=(datetime.date.today().month+m), dia=(datetime.date.today().day+d))
                    #si hay mas de una
                    for actividad in actividades:
                        salida += '<item>\n'
                        salida += '<title>' + actividad.titulo + '</title>\n'
                        salida += '<link>http://localhost:' + request.META['SERVER_PORT'] + '/actividad/' + str(actividad.id) + '</link>\n'
                        salida += '<precio>' + actividad.precio + '</precio>\n'
                        salida += '<fecha>' + str(actividad.anno)  + "/" + str(actividad.mes) + "/" + str(actividad.dia) + " " + actividad.hora + '</fecha>\n'
                        salida += '<duracion>' + actividad.duracion + '</duracion>\n'
                        salida += '<latitud>' + actividad.lat + '</latitud>\n'
                        salida += '<longitud>' + actividad.lon + '</longitud>\n'
                        salida += '<lugar>' + actividad.lugar + '</lugar>\n'
                        salida += '<distrito>' + actividad.distrito + '</distrito>\n'
                        salida += '</item>\n'
                        i = i + 1
                        if i == 10:
                            break
                    if i == 10:
                        break
                except Actividades.DoesNotExist:
                    continue
            if i == 10:
                break        
        
        salida += '</channel>\n'    
        salida += '</rss>'
        return HttpResponse(salida, content_type="text/xml")        
    
    
    
    if request.user.is_authenticated():
        logueado = "Hola, eres " + request.user.username + ".<a href='/logout'>LOGOUT</a>"
    else:
        logueado = "No estas logueado, logueate: " + request.user.username + "<a href='/login'>LOGIN</a>"  
    
    #DIEZ MAS PROXIMAS
    for m in range(0,11): #de 1+0 enero hasta 11+1 diciembre
        for d in range(0,30): #del dia 1 al 31
            try:
                #saco las que coincidan con el dia y el mes
                actividades = Actividades.objects.filter(mes=(datetime.date.today().month+m), dia=(datetime.date.today().day+d))
                #si hay mas de una
                for actividad in actividades:
                    fechahora = str(actividad.anno) + "-" + str(actividad.mes) + "-" + str(actividad.dia) + ". Hora: " + actividad.hora
                    url = "actividad/" + str(actividad.id)
                    salida += constructores.actividad_simple(actividad.titulo, actividad.tipo, actividad.precio, fechahora, actividad.duracion, url)
                    salida += "<br><br>" 
                    i = i + 1
                    if i == 10:
                        break
                if i == 10:
                    break
            except Actividades.DoesNotExist:
                continue
        if i == 10:
            break    
    
    
    salida += "<hr><hr><br>"
    
    
    salida += "<header><h2>USUARIOS</h2><br>"
    for usuario in Usuarios.objects.all():
        salida += "<span class='byline'>" + usuario.usuario + " - <a href='/" + usuario.usuario + "'>" + usuario.titulo + "</a>" + " - " + usuario.descripcion + "</span>"
    salida += '<hr><hr><form action="" method="post"><button class="button" name="rss" value="rss">RSS</button>'    
    salida += "</header>" 
            
    plantilla = get_template('inicio.html')
    c = Context({'actividades': salida, 'usuario': logueado})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)

@csrf_exempt    
def todas(request):
    salida = ""
    boton_actualizar = ""
    
    #SI HAY UN POST, HA SELECCIONADO/DESELECCIONADO UNA ACTIVIDAD O SE HA FILTRADO
    if request.method == "POST":
        if "actividad" in request.POST.keys():
            actividad = Actividades.objects.get(id=int(request.POST["actividad"]))
            usuario = Usuarios.objects.get(usuario=request.user.username)
            #SI ESTA EN LA LISTA DE APUNTADAS CON EL USUARIO LA TENGO QUE ELIMINAR
            try:
                apuntada = Apuntada.objects.get(usuario=usuario, actividad=actividad)
                apuntada.delete()
            except Apuntada.DoesNotExist:
                apuntar = Apuntada(usuario=usuario, fecha=str(datetime.datetime.now()), actividad=actividad)
                apuntar.save()
                
            actividades = Actividades.objects.all()
        elif "tipo" in request.POST.keys():
            if request.POST["tipo"] == "fecha":
                actividades = Actividades.objects.filter(anno=int(request.POST["contenido"].split("-")[0]),mes=int(request.POST["contenido"].split("-")[1]),dia=int(request.POST["contenido"].split("-")[2]))
            elif request.POST["tipo"] == "tipo":
                actividades = Actividades.objects.filter(tipo=request.POST["contenido"])
            elif request.POST["tipo"] == "distrito":
                actividades = Actividades.objects.filter(distrito=request.POST["contenido"])
            elif request.POST["tipo"] == "precio":
                if request.POST["contenido"] == "Gratuito":
                    actividades = Actividades.objects.filter(precio="Gratuito")
                else:
                    actividades = Actividades.objects.exclude(precio="Gratuito")
            
    else:
        actividades = Actividades.objects.all()
    
    #BOTON DE ACTUALIZAR SI ESTAS DENTRO + ULTIMA ACTUALIZACION + LOGIN
    if request.user.is_authenticated():
        logueado = "Hola, eres " + request.user.username + ".<a href='/logout'>LOGOUT</a>"
        ult_act = UltimaActualizacion.objects.last().ultima.split(".")[0]
        if not ult_act:
            ult_act = "TODAVIA NO HAY ULTIMA ACTUALIZACION"
        boton_actualizar += '<div><a href="actualizar" class="button">Actualizar</a><span>Ultima actualizacion: ' + ult_act +  " - " + str(len(Actividades.objects.all())) + " actividades " +'<span></div>'
    else:
        logueado = "No estas logueado, logueate: " + request.user.username + "<a href='/login'>LOGIN</a>"    
    
    #PINTO TODAS
    for actividad in actividades:
        fechahora = str(actividad.anno) + "-" + str(actividad.mes) + "-" + str(actividad.dia) + ". Hora: " + actividad.hora
        url = "actividad/" + str(actividad.id)
        salida += constructores.actividad_simple(actividad.titulo, actividad.tipo, actividad.precio, fechahora, actividad.duracion, url)
        
        #SI ESTOY AUTENTICADO PUEDO SELECCIONARLA O DESELECCIONARLA = PINTAR BOTON
        if request.user.is_authenticated():
            try:
                usuario = Usuarios.objects.get(usuario=request.user.username)
                #SI LA TENGO EN LA LISTA DE APUNTADAS, TENGO QUE PONER LA OPCION DE DEJAR DE SEGUIR
                try:
                    Apuntada.objects.get(usuario=usuario, actividad=actividad)
                    accion = "Dejar de seguir"
                except Apuntada.DoesNotExist:
                    accion = "Seguir"
                salida += '<form action="" method="post"><button class="button" name="actividad" value="' + str(actividad.id) + '">' + accion + '</button></form>'
            except Usuarios.DoesNotExist:
                None
            
        salida += "<br><hr><br>"
    
    plantilla = get_template('todas.html')
    c = Context({'actividades': salida, 'boton_actualizar': boton_actualizar, 'usuario': logueado})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
    
def actualizar(request):
    
    #PARSEO
    xml_doc = urllib.urlopen("http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.rdf")
    soup = BeautifulSoup(xml_doc)

    for evento in soup.find_all("c:vevent"):
        
        titulo = evento.find("v:fn").string
        
        if evento.find("rdf:type"):
            tipo = evento.find("rdf:type").get("rdf:resource").split("/")[-1]
        else:
            tipo = "Sin tipo definido"
            
        if evento.find("c:resource").string:
            precio = evento.find("c:resource").string
        else:
            precio = "Gratuito"
         
        anno = int(evento.find("c:dtstart").string.split(" ")[0].split("-")[0])
        mes = int(evento.find("c:dtstart").string.split(" ")[0].split("-")[1])
        dia = int(evento.find("c:dtstart").string.split(" ")[0].split("-")[2])
        hora_entera = evento.find("c:dtstart").string.split(" ")[1]
        hora = hora_entera.split(":")[0] + ":" + hora_entera.split(":")[1]
        
        if evento.find("c:interval"):
            duracion = "Evento de larga duracion. "
            duracion += "Duracion: " + evento.find("c:byday").string
        else:            
            duracion = "Evento de corta duracion."
            
        url = evento.find("c:url").string
        
        try:
            if evento.find("geo:lat").string:
                latitud = evento.find("geo:lat").string
                longitud = evento.find("geo:long").string
            else:
                latitud = ""
                longitud = ""
        except AttributeError:
            latitud = ""
            longitud = ""

        try:
            lugar = evento.find("c:location").string
        except AttributeError:
            lugar = ""
            
        try:
            distrito = evento.find("loc:distrito").get("rdf:resource").split("/")[-1]
        except AttributeError:
            distrito = ""  
             
        #COMPRUEBO Y GUARDO EN BD SI HACE FALTA (MUCHO DELAY)
        try:
            print "COMPRUEBO"
            Actividades.objects.get(titulo=titulo, tipo=tipo, anno=anno, mes=mes, dia=dia, url=url)
        except Actividades.DoesNotExist:
            print "GUARDO EN LA BASE DE DATOS"
            p = Actividades(titulo=titulo, tipo=tipo, precio=precio, anno=anno, mes=mes, dia=dia, hora=hora, duracion=duracion, url=url, lat=latitud, lon=longitud, lugar=lugar, distrito=distrito)
            p.save()
    
    #HORA DE ACTUALIZACION
    ult_act = UltimaActualizacion(ultima=str(datetime.datetime.now()))
    ult_act.save()
    
    
    #REDIRIJO A /TODAS    
    return HttpResponseRedirect("todas")
    
def ayuda(request):
    if request.user.is_authenticated():
        logueado = "Hola, eres " + request.user.username + ".<a href='/logout'>LOGOUT</a>"
    else:
        logueado = "No estas logueado, logueate: " + request.user.username + "<a href='/login'>LOGIN</a>"          
    plantilla = get_template('ayuda.html')
    c = Context({'usuario': logueado})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
    
@csrf_exempt   
def login(request):
    salida = ""
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                auth_login(request, user)
                salida += "Logueado correctamente. <br>"
            else:
                salida += "La clave es correcta, pero la cuenta esta deshabilitada! <br>"
        else:
            # the authentication system was unable to verify the username and password
            salida += "Usuario o clave incorrectas. <br>"

    if request.user.is_authenticated():
        salida += "No hace falta que te identifiques, eres " + request.user.username + " " + "<a href='/logout'>logout</a>"
    else:
        salida += constructores.formulario_login()
        
    plantilla = get_template('login.html')
    c = Context({'contenido': salida})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("login")
    
def actividad(request, recurso):
    salida = ""
    
    if request.user.is_authenticated():
        logueado = "Hola, eres " + request.user.username + ".<a href='/logout'>LOGOUT</a>"
    else:
        logueado = "No estas logueado, logueate: " + request.user.username + "<a href='/login'>LOGIN</a>"  
    
    try:
        actividad = Actividades.objects.get(id=recurso)
        
        fechahora = str(actividad.anno) + "-" + str(actividad.mes) + "-" + str(actividad.dia) + ". Hora: " + actividad.hora
        url = actividad.url
        
        if actividad.lat:
            localizacion = actividad.lat + ", " + actividad.lon
        else:
            localizacion = "No hay una localizacion posicional"
            
        if actividad.lugar:
            lugar = actividad.lugar
        else:
            lugar = "No hay una lugar especificado"
            
        if actividad.distrito:
            distrito = actividad.distrito
        else:
            distrito = "No hay un distrito especificado"
        
        
        if actividad.masinfo:
            print "YA TENIA LA INFO"
            masinfo = actividad.masinfo
        else:
            print "NUEVA INFO"
            url_html = urllib.urlopen(url)
            soup = BeautifulSoup(url_html)
            divs = soup.findAll("div", { "class" : "parrafo" })
            masinfo = ""
            for div in divs:
                for p in div.find_all("p"):
                    masinfo += str(p) + " "
            if not masinfo:
                masinfo = "No hay informacion adicional"
            actividad.masinfo = masinfo
            actividad.save()
        
        
        salida += constructores.actividad_completa(actividad.titulo, actividad.tipo, actividad.precio, fechahora, actividad.duracion, url, localizacion, lugar, distrito, masinfo)
    except Actividades.DoesNotExist:
        salida = "Lo sentimos, la actividad no existe"
    
    plantilla = get_template('actividad.html')
    c = Context({'actividades': salida, 'usuario': logueado})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
    
def rss(request, recurso):
    salida = ""
    try:
        usuario = Usuarios.objects.get(usuario=recurso)
        actividades = Apuntada.objects.filter(usuario=usuario)
        salida += '<?xml version="1.0" encoding="utf-8"?>\n'
        salida += '<rss version="2.0">\n'
        salida += '<channel>\n'
        salida += '<title>Actividades de: ' + usuario.usuario + '</title>\n'
        salida += '<link>http://localhost:' + request.META['SERVER_PORT'] + "/" + usuario.usuario + '</link>'
        salida += '<description>' + usuario.titulo + '</description>\n'

        for apuntada in actividades:
            salida += '<item>\n'
            salida += '<title>' + apuntada.actividad.titulo + '</title>\n'
            salida += '<link>http://localhost:' + request.META['SERVER_PORT'] + '/actividad/' + str(apuntada.actividad.id) + '</link>\n'
            salida += '<precio>' + apuntada.actividad.precio + '</precio>\n'
            salida += '<fecha>' + str(apuntada.actividad.anno)  + "/" + str(apuntada.actividad.mes) + "/" + str(apuntada.actividad.dia) + " " + apuntada.actividad.hora + '</fecha>\n'
            salida += '<duracion>' + apuntada.actividad.duracion + '</duracion>\n'
            salida += '<latitud>' + apuntada.actividad.lat + '</latitud>\n'
            salida += '<longitud>' + apuntada.actividad.lon + '</longitud>\n'
            salida += '<lugar>' + apuntada.actividad.lugar + '</lugar>\n'
            salida += '<distrito>' + apuntada.actividad.distrito + '</distrito>\n'
            salida += '<apuntada>' + apuntada.fecha + '</apuntada>\n'
            salida += '</item>\n'
        
        salida += '</channel>\n'    
        salida += '</rss>'
        return HttpResponse(salida, content_type="text/xml")
    except Usuarios.DoesNotExist:
        salida += "El usuario no existe"
        return HttpResponse(salida)
    
@csrf_exempt    
def usuario(request, recurso):
    salida = ""
    formularios = ""
    i = 0
    
    if request.user.is_authenticated():
        logueado = "Hola, eres " + request.user.username + ".<a href='/logout'>LOGOUT</a>"
    else:
        logueado = "No estas logueado, logueate: " + request.user.username + "<a href='/login'>LOGIN</a>"  
    
    if request.user.username == recurso:
        formularios = constructores.formularios_cambio(recurso)

    #SI RECIBO UN POST PUEDE QUE ME HAYAN PEDIDO LAS 10 SIGUIENTES O LAS 10 ANTERIORES O PARA CAMBIAR TITULO Y DESCRIPCION
    if request.method == "POST":
        if "nextpagina" in request.POST.keys():
            i = int(request.POST['nextpagina'])
        elif "prevpagina" in request.POST.keys():
            i = int(request.POST['prevpagina'])
        elif "titulo" in request.POST.keys():
            usuario = Usuarios.objects.get(usuario=recurso)
            usuario.titulo = request.POST['titulo']
            usuario.save()
        elif "descripcion" in request.POST.keys():
            usuario = Usuarios.objects.get(usuario=recurso)
            usuario.descripcion = request.POST['descripcion']
            usuario.save()
        elif "colorletra" in request.POST.keys():
            if request.POST['colorletra']:
                colorletra = request.POST['colorletra'];
            else:
                colorletra = "white";
                
            if request.POST['imagenfondo']:
                imagenfondo = request.POST['imagenfondo'];
            else:
                imagenfondo = "images/img01.jpg";
            
            if request.POST['colornavbar']:
                colornavbar = request.POST['colornavbar'];
            else:
                colornavbar = "white";
                
            if request.POST['colortitulotop']:
                colortitulotop = request.POST['colortitulotop'];
            else:
                colortitulotop = "rgba(255,175,77,1)";
                
            if request.POST['colortitulobot']:
                colortitulobot = request.POST['colortitulobot'];
            else:
                colortitulobot = "rgba(233,90,58,1)";
            
            if request.POST['colorbordetitulo']:
                colorbordetitulo = request.POST['colorbordetitulo'];
            else:
                colorbordetitulo = "white";
                
            usuario = Usuarios.objects.get(usuario=recurso)
            plantilla = get_template('static/css/style_mod.css')
            c = Context({'colorletra': colorletra, 'imagenfondo': imagenfondo, 'colornavbar': colornavbar, 'colortitulotop': colortitulotop, 'colortitulobot': colortitulobot, 'colorbordetitulo': colorbordetitulo})
            css = plantilla.render(c)
            
            usuario.css = css
            usuario.save()
        elif "reset" in request.POST.keys():
            usuario = Usuarios.objects.get(usuario=recurso)          
            usuario.css = ""
            usuario.save()
            
        
    try:
        usuario = Usuarios.objects.get(usuario=recurso)
        actividades = Apuntada.objects.filter(usuario=usuario)
        titulo = usuario.titulo
        descripcion = usuario.descripcion
        
        for apuntada in actividades[(0 + (i*10)):(10 + (i*10))]:
            fechahora = str(apuntada.actividad.anno) + "-" + str(apuntada.actividad.mes) + "-" + str(apuntada.actividad.dia) + ". Hora: " + apuntada.actividad.hora
            url = "actividad/" + str(apuntada.actividad.id)
            salida += constructores.actividad_simple(apuntada.actividad.titulo, apuntada.actividad.tipo, apuntada.actividad.precio, fechahora, apuntada.actividad.duracion, url)
            salida += "<p>APUNTADA EN: " + apuntada.fecha + "</p>"
            salida += "<br><hr><br>"
        
        #COMPRUEBO SIEMPRE EL 11 O EL -1 PARA SABER SI HAY NOTICIAS ANTES O DESPUES
        try:
            actividades[(-1 + (i*10))]
            salida += '<form action="" method="post"><button class="button" name="prevpagina" value="' + str(i - 1) + '">Anteriores 10 actividades</button>'
        except AssertionError:
            None
        try: 
            actividades[(10 + (i*10))]
            salida += '<form action="" method="post"><button class="button" name="nextpagina" value="' + str(i + 1) + '">Siguientes 10 actividades</button>'             
        except IndexError:
            None
        #########################################CSS MODIFICADO #################################
        if usuario.css:
            f = open("templates/static/css/style_usuario.css", "w")
            f.write(usuario.css)
            f.close()
            css_usuario = "/static/css/style_usuario.css"
        else:
            css_usuario = ""
            
    except Usuarios.DoesNotExist:
        salida = "<h2>Lo sentimos, el usuario " + recurso + " no existe</h2>"
        titulo = "Usuario no existente"
        descripcion = ""
        css_usuario = ""
     
       
    
    plantilla = get_template('otras.html')
    c = Context({'actividades': salida, 'usuario': logueado, 'title': titulo, 'desc': descripcion, 'formularios_cambio': formularios, 'css_usuario': css_usuario})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
    
