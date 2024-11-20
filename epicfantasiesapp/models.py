from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils import timezone

def user_directory_path(instance, filename):
    user_username = instance.user.username
    now = timezone.now()
    return f'historias/{user_username}/{now.year}/{now.month}/{now.day}/{now.hour}/{now.minute}/{filename}'

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    data_criacao = models.DateTimeField(auto_now_add=True)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    quantidade_seguidores = models.IntegerField(default=0)
    is_administrador_sys = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    @property
    def get_foto_perfil_url(self):
        if self.foto_perfil:
            print(type(self.foto_perfil))
            print(self.foto_perfil)
            if self.foto_perfil is None or self.foto_perfil == "None":
                return "https://via.placeholder.com/60"
            return settings.MEDIA_URL + str(self.foto_perfil)
        else:
            return "https://via.placeholder.com/60"
class RedesSociais(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    tiktok = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Redes Sociais de {self.user.username}"

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome



class Historias(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historias')
    titulo = models.CharField(max_length=255)
    previu = models.TextField()
    conteudo = models.TextField(default='')  
    data_de_criacao = models.DateTimeField(default=timezone.now)  
    foto = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    @property
    def get_foto_story_url(self):
        if self.foto:
            return settings.MEDIA_URL + str(self.foto)
        return None

class Comentario(models.Model):
    historia = models.ForeignKey(Historias, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    data_hora = models.DateTimeField(auto_now_add=True)
    foi_alterado = models.BooleanField(default=False)
    valor_comentario = models.TextField()

    def __str__(self):
        return f"{self.user.username} comentou na história de {self.historia.user.username}"
    


class Reacao(models.Model):
    historia = models.ForeignKey(Historias, on_delete=models.CASCADE, related_name='reacoes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reacoes')
    TIPO_REACAO_CHOICES = [
        ('EXC', 'Excelente'),
        ('BOM', 'Bom'),
        ('LEG', 'Legal'),
        ('NTL', 'Não é tão legal'),
        ('NGO', 'Não gostei'),
    ]
    tipo_reacao = models.CharField(max_length=3, choices=TIPO_REACAO_CHOICES)

    def __str__(self):
        return f"{self.user.username} reagiu a história {self.historia} com: {self.tipo_reacao}"
    


class Denuncias(models.Model):
    historia = models.ForeignKey(Historias, on_delete=models.CASCADE, related_name='denuncias')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='denuncias')
    data_hora = models.DateTimeField(auto_now_add=True)
    usuario_denunciou = models.ForeignKey(User, on_delete=models.CASCADE, related_name='denuncias_feitas')

    def __str__(self):
        return f"{self.usuario_denunciou.username} denunciou a história de '{self.historia}' feita por {self.user.username}"

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(default=timezone.now)

    @classmethod
    def code_expired(cls,timestamp):
        now = timezone.now()
        time_difference = now - timestamp
        minutes_passed = time_difference.total_seconds() / 60
        return minutes_passed >= 30
    
    def __str__(self):
        return f"Código do usuário {self.user.username}: {self.verification_code}"
    

class SystemUtilities(models.Model):
    picture_ads = models.ImageField(upload_to='propaganda/', null=True, blank=True)

    @property
    def get_picture_ads_url(self):
        if self.picture_ads:
            return settings.MEDIA_URL + str(self.picture_ads)
        return None
    
    def __str__(self):
        return f"{self.get_picture_ads_url}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
        RedesSociais.objects.create(user=instance)


@receiver(post_save, sender=User)
@receiver(post_save, sender=Perfil)
@receiver(post_save, sender=RedesSociais)
def save_user_related(sender, instance, **kwargs):
    if sender == User:
        instance.perfil.save()
        instance.redessociais.save()



