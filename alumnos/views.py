from django.shortcuts import render
from alumnos.models import alumnos
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView,DetailView, UpdateView, DetailView, FormView
from alumnos.forms import Alumno_Form, Alumno_Chido, Alumno_Eva, Alumno_EvaDiario
from django.urls import reverse_lazy
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from padres.models import Tutor, Profesor
from maestros.models import  grupos, DiarioTrabajo
import string
from datetime import date, timedelta, datetime

def get_week_days(year, week):
    d = date(year,1,1)
    if(d.weekday()>3):
        d = d+timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return d + dlt,  d + dlt + timedelta(days=6)


def Index(request):
    user = request.user
    if user.is_active is True:
        if user.is_staff is False :
            if user.has_perm('padres.is_teacher'):
                yar = datetime.now().year
                today = date.today()
                wk = today.isocalendar()[1]
                inicio, fin = get_week_days(yar ,wk)
                prf = Profesor.objects.get(pro_nombre = user)
                grp = grupos.objects.select_related().filter(gru_maestro = prf)
                almGRUP = []
                for k in grp:
                    almGRUP.append({"Alumnos": k.gru_alumnos.all(), "Grupo": k.id})

                evaluacionesArray = []
                for j in range(len(almGRUP)):
                    kj = []
                    for hj in almGRUP[j]['Alumnos']:
                        kj.append(hj.id)

                    diarios = []
                    amevals = []
                    evalpos = []
                    

                    diar = DiarioTrabajo.objects.select_related().filter(DT_fecha = today).filter(DT_alumno__id__in = kj)
                    idDiar = []
                    aluDiar = []           
                    for ml in diar:
                        idDiar.append(ml.id)
                        aluDiar.append(ml.DT_alumno.id)

                    diarios.append({"Diario": idDiar, "Alumno": aluDiar})
                    evaluacionesArray.append({"Grupo": almGRUP[j]['Grupo'], "Alumnos": amevals, "EvalId": evalpos, "Diario": diarios})
                ctx = {"Perfil": prf, "Grupos": grp, "Evaluados": evaluacionesArray}
                print(ctx)
            if user.has_perm('padres.is_tutorr'):
                tur = Tutor.objects.get(tut_nombre = user)
                alm = alumnos.objects.filter(alu_tutores__in = [tur])
                ctx = {"Alumno":alm}        
            
            return render(request,'alumnos/index.html', ctx)
        else:
            return render(request,'alumnos/index.html')
        
    return render(request,'alumnos/index.html')




def busquedaTutores(request):
    if  request.method == 'GET':
        datos = []
        filtro = request.GET['filtro']
        data =  Tutor.objects.select_related().filter(tut_apellidos__contains = filtro)
        for dt in data:
            datos.append({"Usuario": str(dt.tut_nombre.username), 'Apellidos': str(dt.tut_apellidos), 'Numero':str(dt.tut_numero), 'Descripcion':str(dt.tut_descripcion)})

        data = serializers.serialize('json',data)
    else:
        data = ""
    return HttpResponse(str(datos))

def busquedaAlumno(request):
    if request.method == 'GET':
        filtro = request.GET['filtro']
        data = serializers.serialize('json', alumnos.objects.filter(alu_nombre__contains = filtro))
    else:
        data = ""
    return HttpResponse(data)

class AlumnoReporte(ListView):
	template_name = "alumnos/reporte.html"
	model = alumnos

class DiarioReporte(ListView):
    template_name="evaluaciones/reporteDiario.html"
    today = date.today()
    model = DiarioTrabajo
    queryset = DiarioTrabajo.objects.all()

    
class Update_Alumno(UpdateView):
    template_name = 'alumnos/updateA.html'
    model = alumnos
    fields = '__all__'
    success_url = reverse_lazy('alumnos_reporte')
    
class Detail_Alumno(DetailView):
    template_name="alumnos/detalleAlumno.html"
    model = alumnos

class CreateAlumno(FormView):
    template_name = "alumnos/crear.html"
    form_class = Alumno_Chido
    success_url = reverse_lazy('alumnos_reporte')
    
    def form_valid(self, form):
        alu = alumnos()
        alu.alu_nombre = form.cleaned_data['alu_nombre']
        alu.alu_genero = form.cleaned_data['alu_genero']
        #alu.alu_tutores = form.cleaned_data['alu_tutores']
        alu.save()
        gen = form.cleaned_data['alu_genero']
        if gen == 'Masculino':
            alu.alu_foto = 'media/fotosAlu/Male-icon.png'
        else:
            alu.alu_foto = 'media/fotosAlu/Female_icon.png'
        alu.alu_tutores.set(form.cleaned_data['alu_tutores'])
        alu.alu_vigente = form.cleaned_data['alu_vigente']
        alu.alu_fechaIngreso = form.cleaned_data['alu_fechaIngreso']
        alu.alu_observaciones = form.cleaned_data['alu_observaciones']
        alu.slug =form.cleaned_data['slug']
        alu.save()
        return super(CreateAlumno,self).form_valid(form)



class EvaDiario(FormView):
    template_name = "alumnos/evaluarDiario.html"
    form_class = Alumno_EvaDiario
    success_url = reverse_lazy('reporteDiario')

    def get_context_data(self, *args, **kwargs):
        ctx = super(EvaDiario, self).get_context_data(*args, **kwargs)
        #ctx['slug'] = self.kwargs['slug'] # or Tag.objects.get(slug=...)
        slug = self.kwargs['slug']
        ctx ['alumno'] = alumnos.objects.get(slug=slug)
        return ctx

    def form_valid(self, form):
        evaD = DiarioTrabajo()
        filtro = form.cleaned_data['DT_maestro']
        maes = Profesor.objects.get(pro_nombre=filtro)
        evaD.DT_maestro = maes
        filtroalum = form.cleaned_data['DT_alumno']
        slug = self.kwargs['slug']
        alu = alumnos.objects.get(slug=slug)
        evaD.DT_alumno = alu
        evaD.DT_fecha = form.cleaned_data['DT_fecha']
        evaD.DT_descripcion = form.cleaned_data['DT_descripcion']
        evaD.DT_actividadApoyo = form.cleaned_data['DT_actividadApoyo']
        evaD.DT_necesidades = form.cleaned_data['DT_necesidades']
        evaD.save()
        return super(EvaDiario,self).form_valid(form)




def reporteDiarioAlumno(request, slug):
    alumn = alumnos.objects.get(slug,slug)
    diarios = DiarioTrabajo.objects.get(DT_alumno = alumn)
    ctx = {"object_list":diarios}
    return render(request, 'evaluaciones/reporteDiario.html', ctx)
