from django.shortcuts import render

# import pytesseract to convert text in image to string
import pytesseract

# import summarize to summarize the ocred text
from gensim.summarization.summarizer import summarize

from .forms import ImageUpload
import os

# import Image from PIL to read image
from PIL import Image

from django.conf import settings


# Create your views here.
def index(request):
    text = ""
    summarized_text = ""
    message = ""
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                image = request.FILES['image']
                image = image.name
                path = settings.MEDIA_ROOT
                pathz = path + "/images/" + image

                # supports both english and polish
                custom_config = r'-l eng+pol --psm 6'
                
                text = pytesseract.image_to_string(Image.open(pathz), config=custom_config)
                text = text.encode("ascii", "ignore")
                text = text.decode()

                # Summary (0.1% of the original content).
                summarized_text = summarize(text, ratio=0.1)
                os.remove(pathz)
            except:
                message = "check your filename and ensure it doesn't have any space or check if it has any text"

    context = {
        'text': text,
        'summarized_text': summarized_text,
        'message': message
    }
    return render(request, 'formpage.html', context)
