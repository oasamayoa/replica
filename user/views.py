from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.db import transaction
from user.models import User

class Home(TemplateView):
    template_name = 'user/user_list.html'
    
    def post(self, request, *argas, **kwargs):
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
                    })
            elif action == 'list_mysql':
                data = []
                usuarios_my = User.objects.using('mysql_replica').filter(is_active = True)
                for u in usuarios_my:
                    data.append({
                        'id': u.id,
                        'first_name': u.first_name,
                        'last_name': u.last_name,
                        'username': u.username,
                        'email': u.email, 
                    })
            elif action == 'add':
                with transaction.atomic():
                    user = User(
                        username=request.POST['username'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                    )
                    user.set_password(request.POST['password'])
                    user.save()
                # data = {'success': True}
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

                    # otros campos siempre se pueden actualizar
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']

                    # password si se cambio
                    if request.POST.get('password'):
                        user.set_password(request.POST['password'])

                    # guardar en ambas bases
                    user.save()

            elif action == 'delete':
                with transaction.atomic():
                    user = User.objects.get(pk=request.POST['id'])
                    if user:
                        user.is_active = False
                        user.save()
                        # user.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyecto Replica BD PostreSQL - MySQL'
        return context
