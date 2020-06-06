from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

from django.utils import timezone

#Probando, va a quedar un choclo gigante con todos los objetos aca
#Orden Author-> Gender-> Editorial-> CreditCards-> Account-> Profile->  
# Publication (y sus hijos)-> StateOfBook-> Comment -> Like -> LikeComment -->>
# -> ExpirationDates -> UpDates-> UserSolicitud-> CounterStates

#Author
class Author(models.Model):
    name= models.CharField("Nombre", max_length=50)
    last_name = models.CharField("apellido", max_length=50) 
    image= models.ImageField("imagen", upload_to='bookflix/static/autores', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    description = models.TextField("descripcion",blank=True, null=True)
    created_date = models.DateTimeField("fecha de creacion", default=timezone.now)


    def publish(self):
        self.save()

    def ret(self):
        return self.name 
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

#Gender
class Gender(models.Model):
    name= models.CharField("Nombre", max_length=50, unique=True)
    description = models.TextField("descripcion", blank=True, null=True)
    created_date = models.DateTimeField("fecha de creacion",default=timezone.now)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Genero"
        verbose_name_plural = "Generos"

#Editorial
class Editorial(models.Model):
    name= models.CharField("Nombre", max_length=50, primary_key=True)
    description = models.TextField("descripcion",blank=True, null=True)
    mail = models.EmailField( max_length=254, blank=True, null=True)
    created_date = models.DateTimeField("",default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.confirmo=True
        user.save(using=self.db)
        return user

    """ def get_by_natural_key(self, username):
       return self.get(username=username)"""

#ConfirmationMail
class ConfirmationMail(models.Model):
    mail= models.EmailField( max_length=254, unique=True)
    codigo = models.CharField( max_length=10)
    tipo = models.IntegerField()
    #tipo de mails de confirmacion: 1 para confirmar cuenta, 2 confirmar cambio de contraseña 

    def publish(self):
        self.save()

#Account
class Account(AbstractBaseUser):

    #Valores para los diferentes tipos de cuenta
    free='free'
    normal='normal'
    premium='premium'
    admin = 'admin'
    AC_CHOICES= (
        (free, 'free'),
        (normal, 'normal'),
        (premium, 'premium'),
        (admin, 'admin')
    )

    email = models.EmailField(verbose_name='mail',max_length=60, unique=True)
    username = models.CharField("nombre de usuario", max_length=50, unique=True)
    
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    confirmo= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    plan = models.CharField( max_length=8, choices=AC_CHOICES, default=free)
    date_start_plan = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    time_pay = models.IntegerField(default=0)
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def nombre(self):
        return self.username

    def has_perm (self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    
#CreditCards
class CreditCards(models.Model):
    number = models.CharField(('numero'),max_length=16, primary_key=True)
    cod = models.IntegerField()
    card_name = models.CharField("nombre de tarjeta",max_length=50)
    date_expiration = models.DateField("fecha de vencimiento",auto_now=False, auto_now_add=False)
    bank = models.CharField(('banco'),max_length=50)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return self.card_name

    class Meta:
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"

#Profile

class Profile(models.Model):
    name= models.CharField( max_length=50)
    account= models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active_now= models.BooleanField(default=False)
    hour_activation= models.DateTimeField( auto_now=False, auto_now_add=False, blank=True, null=True)
    pleasures_gender = models.ManyToManyField(Gender, blank=True, null=True)
    pleasures_author = models.ManyToManyField(Author, blank=True, null=True)
    pleasures_editorial = models.ManyToManyField(Editorial,blank=True, null=True, verbose_name="Editoriales Favoritas")

    date_of_creation = models.DateTimeField(default=timezone.now)
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.name  
    
    class Meta:
        unique_together = ('name', 'account',)
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

"-------Book-------"
class Book(models.Model):
    title = models.CharField(('titulo'), max_length=50)
    description = models.TextField(('descripcion'))
    image= models.ImageField( upload_to='portadas_libros', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    isbn = models.IntegerField(primary_key=True)
    author= models.ForeignKey(Author, on_delete=models.CASCADE)
    genders = models.ManyToManyField(Gender)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    mostrar_en_home= models.BooleanField(default=False)
    on_normal = models.BooleanField(default=False)
    on_premium = models.BooleanField(default=False)
    url = models.URLField( max_length=200, blank=True, null=True)


    def publish(self):
        self.save()

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return self.title

 
"-------BookByChapter-------"
class BookByChapter(models.Model):
    book= models.OneToOneField(Book, on_delete=models.CASCADE)
    cant_chapter = models.IntegerField(default = 1)
    
    def publish(self):
        self.save()
    
    class Meta:
        verbose_name = "Libro por capítulo"
        verbose_name_plural = "Libro por capítulos"


"-------Billboard-------"
class Billboard(models.Model):
    title = models.CharField("titulo", max_length=50, )
    description = models.TextField(blank=True, null=True)
    mostrar_en_home= models.BooleanField(default=False)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    video=  models.URLField(  max_length=255, blank=True, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"


"-------Chapter-------"
class Chapter(models.Model):
    number = models.IntegerField("numero",default=0)
    book= models.ForeignKey(BookByChapter, on_delete=models.CASCADE)
    url = models.URLField( max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('number', 'book',)
        verbose_name = "Capítulo"
        verbose_name_plural = "Capítulos"

    def publish(self):
        self.save()

#StateOfBook

class StateOfBook(models.Model):

    reading='reading'
    future_reading='future_reading'
    finished='finished'
    AC_CHOICES= (
        (reading, 'reading'),
        (future_reading, 'future_reading'),
        (finished, 'finished')
    )

    date= models.DateField("fecha",default=timezone.now)
    state = models.CharField("estado", max_length=16, choices=AC_CHOICES, default=finished)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together= ('book', 'profile') 
        verbose_name = "Estado del libro"
        verbose_name_plural = "Estados del libro"
         
    def publish(self):
        self.save()

    def __str__(self):
        return self.state        

#Comment
class Comment(models.Model):

    is_a_spoiler = models.BooleanField("es espoiler",default=False)
    description = models.TextField("descripcion",)
    profile= models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication = models.ForeignKey(Book, on_delete=models.CASCADE)    


    def publish(self):
        self.save()

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

#Like
class Like(models.Model):
    
    is_like = models.BooleanField("me gusta",default = False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('author', 'book')

    def publish(self):
        self.save()

    class Meta:
        verbose_name = "Me gusta"
        verbose_name_plural = "Me gusta/s"



#LikeComment
class LikeComment(models.Model):
    
    is_like = models.BooleanField("me gusta",default = False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'comment')
        verbose_name = "Me gusta de comentario"
        verbose_name_plural = "Me gustas/s de comentarios"

    def publish(self):
        self.save()

#ExpirationDates
class ExpirationDates(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    expiration_normal= models.DateField("expiracion normal",blank=True, null=True)
    expiration_premium= models.DateField("expiracion premium",blank=True, null=True)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = "DarDeBajaLibro"
        verbose_name_plural = "DarDeBajaLibros"

#UpDates
class   UpDates(models.Model):
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    up_normal= models.DateField("pasar a normal",blank=True, null=True)
    up_premium= models.DateField("pasar a premium",blank=True, null=True)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = "DarDeAltaLibro"
        verbose_name_plural = "DarDeAltaLibros"


#ExpirationDates
class ExpirationDatesBillboard(models.Model):

    publication = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    expiration_date= models.DateField("fecha de vencimiento",blank=True, null=True)


    def publish(self):
        self.save()

    class Meta:
        verbose_name = "DarDeBajaNovdedad"
        verbose_name_plural = "DarDeBajaNovedades"

#UpDates
class   UpDatesBillboard(models.Model):
    
    publication = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    up_date= models.DateField("actualizar",blank=True, null=True)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = "DarDeAltaNovedades"
        verbose_name_plural = "DarDeAltaNovedades"
#UserSolicitud

class UserSolicitud(models.Model):
    pass
    "Valores para los diferentes tipos de cuenta"
    alta='1'
    cambio='2'
    baja='4'
    AC_CHOICES= (
        (alta, 'alta'),
        (cambio, 'cambio'),
        (baja, 'baja')
    )
    free = 'f'
    normal = 'n'
    premium = 'p'
    TY_CHOICES= (
        (free, 'free'),
        (normal, 'normal'),
        (premium, 'premium')
    )
    "Valores del modelo"    
    """Si se pide una baja, se debe llenar con la fecha en que termina el plan.
        Si se pude el cambio, apenas empieza el dia de que termine el tiempo pagado del usuario,
        se debería cambiar el usuario al plan nuevo """

    """en caso de que el usuario quiera pagar tiempo hay que revisar que no tenga una solicitud de
      cambio de plan, en ese caso se debe generar una solicitud de alta con el plan nuevo y el tiempo"""  

    "tipo de solicitud que se hace"
    type_of_solicitud = models.CharField( max_length=2, choices=AC_CHOICES, default=alta)
    "tipo de plan al que se quiere cambiar, en caso de que sea baja, por defecto es free"
    type_of_plan = models.CharField( max_length=2, choices=TY_CHOICES, default=free)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_of_solicitud = models.DateTimeField(default=timezone.now)
    "fecha limite para atender la solicitud, si es un alta es un dia despues de la fecha de creacion"
    "si es un cambio o baja es cuando se termina el tiempo comprado por el usuario"
    date_limit_to_attend = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.type_of_solicitud

    class Meta:
        verbose_name = "Solicitud de usuario"
        verbose_name_plural = "Solicitudes de Usuarios"

#CounterStates

class CounterStates(models.Model):

    publication = models.ForeignKey(Book, on_delete=models.CASCADE,related_name="publicacion")  #acá tuve que cambbiar el orden y usar la variable "nombre relacionado"
    date_start = models.DateField("fecha de inicio")                                                            # por errores con este modelo chuzmear acá.
    cant_reading = models.IntegerField("leyendo",default=0)
    cant_future_read = models.IntegerField("en futuras lecturas",default=0)
    cant_finished = models.IntegerField("terminados",default=0)

    
    def publish(self):
        self.save()
    
    class Meta:
        verbose_name = "Estadística de libro"
        verbose_name_plural = "Estadísticas de libros"

    

