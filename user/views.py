from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db import transaction
from user.models import User, Registro

class ListPostgres(TemplateView):
    template_name = 'user/user_list_postgres.html'
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'list_postgres':
                data = []
                usuarios_pg = User.objects.using('default').filter(is_active = True)
                for u in usuarios_pg:
                    data.append({
                        'id': u.id,
                        'first_name': u.first_name,
                        'last_name': u.last_name,
                        'username': u.username,
                        'email': u.email,
                        'middle_name': u.middle_name,
                        'dpi': u.dpi,
                        'second_last_name': u.second_last_name,
                        'address': u.address,
                        'phone_home': u.phone_home,
                        'phone_mobile': u.phone_mobile,
                        'salary': format(u.salary),
                        'bonus': format(u.bonus),
                        'nombre_completo' : f"{u.first_name} {u.middle_name}",
                        'apellido_completo' : f"{u.last_name} {u.second_last_name}"
                    })
            elif action == 'add':
                with transaction.atomic():
                    user = User(
                        username=request.POST['username'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                        middle_name=request.POST['middle_name'],
                        dpi=request.POST['dpi'],
                        second_last_name=request.POST['second_last_name'],
                        address=request.POST['address'],
                        phone_home=request.POST['phone_home'],
                        phone_mobile=request.POST['phone_mobile'],
                        salary=request.POST['salary'],
                        bonus=request.POST['bonus'],
                    )
                    user.set_password(request.POST['password'])
                    user.save()
            elif action == 'edit':
                with transaction.atomic(): 
                    user = User.objects.get(pk=request.POST['id'])
                    # username
                    nuevo_username = request.POST['username']
                    if user.username != nuevo_username:
                        if User.objects.exclude(pk=user.pk).filter(username=nuevo_username).exists():
                            raise Exception('El nombre de usuario ya existe.')
                        user.username = nuevo_username  # solo actualiza si cambió y no hay conflicto

                    # email
                    nuevo_email = request.POST['email']
                    if user.email != nuevo_email:
                        if User.objects.exclude(pk=user.pk).filter(email=nuevo_email).exists():
                            raise Exception('El correo ya existe.')
                        user.email = nuevo_email  # solo actualiza si cambió y no hay conflicto
                     
                    nuevo_dpi=request.POST['dpi']   
                    if user.dpi != nuevo_dpi:
                        if User.objects.exclude(pk=user.pk).filter(email=nuevo_dpi).exists():
                            raise Exception('El DPI ya existe.')
                        user.dpi = nuevo_dpi  # solo actualiza si cambió y no hay conflicto

                    # otros campos siempre se pueden actualizar
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.middle_name=request.POST['middle_name']
                    user.second_last_name=request.POST['second_last_name']
                    user.address=request.POST['address']
                    user.phone_home=int(request.POST['phone_home'])
                    user.phone_mobile=int(request.POST['phone_mobile'])
                    user.salary=float(request.POST['salary'])
                    user.bonus=float(request.POST['bonus'])
                    # password si se cambio
                    if request.POST.get('password'):
                        user.set_password(request.POST['password'])

                    # guardar en ambas bases
                    user.save()

            elif action == 'delete':
                with transaction.atomic():
                    user = User.objects.get(pk=request.POST['id'])
                    if user:
                        user.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyecto Replica BD PostreSQL - MySQL'
        context['home'] = reverse_lazy('home')
        return context
    
class ListMysql(TemplateView):
    template_name = 'user/user_list_mysql.html'
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'list_mysql':
                data = []
                usuarios_my = User.objects.using('mysql_replica').filter(is_active = True)
                for u in usuarios_my:
                    data.append({
                        'id': u.id,
                        'first_name': u.first_name,
                        'last_name': u.last_name,
                        'username': u.username,
                        'email': u.email,
                        'middle_name': u.middle_name,
                        'dpi': u.dpi,
                        'second_last_name': u.second_last_name,
                        'address': u.address,
                        'phone_home': u.phone_home,
                        'phone_mobile': u.phone_mobile,
                        'salary': format(u.salary),
                        'bonus': format(u.bonus),
                        'nombre_completo' : f"{u.first_name} {u.middle_name}",
                        'apellido_completo' : f"{u.last_name} {u.second_last_name}" 
                    })
            elif action == 'add':
                with transaction.atomic():
                    user = User(
                        username=request.POST['username'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                        middle_name=request.POST['middle_name'],
                        dpi=request.POST['dpi'],
                        second_last_name=request.POST['second_last_name'],
                        address=request.POST['address'],
                        phone_home=request.POST['phone_home'],
                        phone_mobile=request.POST['phone_mobile'],
                        salary=request.POST['salary'],
                        bonus=request.POST['bonus'],
                    )
                    user.set_password(request.POST['password'])
                    user.save()
            elif action == 'edit':
                with transaction.atomic(): 
                    user = User.objects.get(pk=request.POST['id'])
                    # username
                    nuevo_username = request.POST['username']
                    if user.username != nuevo_username:
                        if User.objects.exclude(pk=user.pk).filter(username=nuevo_username).exists():
                            raise Exception('El nombre de usuario ya existe.')
                        user.username = nuevo_username  # solo actualiza si cambió y no hay conflicto

                    # email
                    nuevo_email = request.POST['email']
                    if user.email != nuevo_email:
                        if User.objects.exclude(pk=user.pk).filter(email=nuevo_email).exists():
                            raise Exception('El correo ya existe.')
                        user.email = nuevo_email  # solo actualiza si cambió y no hay conflicto

                    nuevo_dpi=request.POST['dpi']   
                    if user.dpi != nuevo_dpi:
                        if User.objects.exclude(pk=user.pk).filter(email=nuevo_dpi).exists():
                            raise Exception('El DPI ya existe.')
                        user.dpi = nuevo_dpi  # solo actualiza si cambió y no hay conflicto

                    # otros campos siempre se pueden actualizar
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.middle_name=request.POST['middle_name']
                    user.second_last_name=request.POST['second_last_name']
                    user.address=request.POST['address']
                    user.phone_home=int(request.POST['phone_home'])
                    user.phone_mobile=int(request.POST['phone_mobile'])
                    user.salary=float(request.POST['salary'])
                    user.bonus=float(request.POST['bonus'])
                    # password si se cambio
                    if request.POST.get('password'):
                        user.set_password(request.POST['password'])

                    # guardar en ambas bases
                    user.save()

            elif action == 'delete':
                with transaction.atomic():
                    user = User.objects.get(pk=request.POST['id'])
                    if user:
                        # user.is_active = False
                        # user.save()
                        user.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyecto Replica BD PostreSQL - MySQL'
        context['home'] = reverse_lazy('home')
        return context


class Selecion(TemplateView):
    template_name = 'user/selecion.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyecto Replica BD PostreSQL - MySQL'
        return context
    
    
class ListBitacora(TemplateView):
    template_name = 'user/bitacora.html'
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list_bitacora':
                data = []
                registro = Registro.objects.all()
                for r in registro:
                    data.append({
                        'accion' : r.accion,
                        'modelo' : r.modelo,
                        'descripccion' : r.descripcion,
                        'fecha' : r.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    })
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyecto Replica BD PostreSQL - MySQL'
        context['home'] = reverse_lazy('home')
        return context