from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import CheckFileForm
from .models import FileStatus
from django.conf import settings
from .background_task import ocrPdf
import os
# Create your views here.

def index(request):
    ctx = {
        'message': None,
    }

    if request.method == "POST":
        ctx['message'] = False
        fs = FileSystemStorage(location = settings.INPUT_FILES)
        form = CheckFileForm(request.POST, request.FILES)
        if form.is_valid():
            ctx['message'] = True
            file = request.FILES['pdf']
            email = request.POST['email']
            
            query = FileStatus(file = file.name, email=email, status = False)
            query.save()
            filename = str(query.id) + ".pdf"
            fs.save(filename, file)
            ocrPdf(filename, query.id)
            ctx['job'] = query.id

    return render(request, 'index/index.html', ctx)


def status(request):
    ctx = {
        'resp': ''
    }

    job_id = request.GET.get('job-id', None)
    if job_id and job_id.isdigit():
        job_id = int(job_id)
        ctx['resp'] = 'w'
        ctx['message'] = 'Job Id not assigned'

        q = FileStatus.objects.filter(pk = job_id)
        if len(q) > 0:
            ctx['message'] = 'PDF waiting for OCR'
            if q[0].status:
                ctx['message'] = "Success!"
                ctx['resp'] = 's'
                ctx['link'] = '/download/' + str(job_id)

    return render(request, 'index/status.html', ctx)

def download(request, job):
    q = FileStatus.objects.filter(pk = job)
    p = os.path.join(settings.OUTPUT_FILES, str(job) + ".txt")
    if not os.path.exists(p) or len(q) == 0 or not q[0].status:
        return HttpResponse('Something went wrong')
    
    out = open(p, 'rb')
    response = HttpResponse(out,content_type="text/plain")

    response['Content-Disposition'] = "attachment; filename=" + q[0].file.replace('.pdf', '.txt').replace('.PDF', 'txt')
    return response