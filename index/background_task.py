from background_task import background
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .pdf2text import Pdf2Text
import os
from django.core.mail import send_mail as sm
from .models import FileStatus

@background(queue="tesseract")
def ocrPdf(filename, id):
    # check whether output directory
    if not os.path.exists(settings.OUTPUT_FILES):
        os.mkdir(settings.OUTPUT_FILES)

    # convert to text
    output_filename = str(id) + ".txt"
    converter = Pdf2Text(os.path.join(settings.INPUT_FILES, filename), os.path.join(settings.OUTPUT_FILES, output_filename))
    converter.convert()

    # remove the raw file
    query = FileStatus.objects.filter(pk = id)[0]
    query.status = True
    query.save()
    fs = FileSystemStorage(location = settings.INPUT_FILES)
    fs.delete(filename)

    #send mail to the client
    subject = query.file + " - " + str(id)
    message = "your job id - " + str(id) + "\nyour file - " + query.file + "\nDownload - %s/download/%d/"%(settings.HOST_URL, id) 
    res = sm( subject = subject, message=message, from_email="youremail.com", recipient_list = [query.email], fail_silently = False)