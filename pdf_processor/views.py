from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadedPDF
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize
def upload_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['pdf_file']
        pdf_obj = UploadedPDF(pdf_file=uploaded_file)
        pdf_obj.save()

        # Process the uploaded PDF
        pdf_text = extract_text_from_pdf(pdf_obj.pdf_file.path)
        summary = generate_summary(pdf_text)

        return render(request, 'summary.html', {'summary': summary})

    return render(request, 'upload.html')


def extract_text_from_pdf(pdf_path):
    pdf_text = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page_text = pdf_reader.pages[page_num].extract_text()
            if page_text:
                pdf_text += page_text
    return pdf_text

def generate_summary(text):
    sentences = sent_tokenize(text)
    num_sentences = len(sentences)
    summary = ' '.join(sentences[:5])  # Generate a summary of the first 5 sentences
    return summary
