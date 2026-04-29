import io
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .forms import QRCodeForm, UserRegistrationForm
from .models import QRCode

ERROR_CORRECTION_MAP = {
    'Низкий': ERROR_CORRECT_L,
    'Средний': ERROR_CORRECT_M,
    'Квартиль': ERROR_CORRECT_Q,
    'Высокий': ERROR_CORRECT_H,
}

def generate_qr_image(text, size, error_correction, fg_color, bg_color, logo_file=None):
    ec = ERROR_CORRECTION_MAP.get(error_correction, ERROR_CORRECT_M)
    qr = qrcode.QRCode(version=None, error_correction=ec, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGB')
    img = img.resize((size, size), Image.LANCZOS)
    if logo_file:
        logo = Image.open(logo_file).convert('RGBA')
        logo_size = int(size * 0.2)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((size - logo_size) // 2, (size - logo_size) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    return img

def generate(request):
    generated_qr = None
    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            img = generate_qr_image(
                data['text'], data['size'], data['error_correction'],
                data['fg_color'], data['bg_color'], data.get('logo')
            )
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            user = request.user if request.user.is_authenticated else None
            qr = QRCode(
                user=user, text=data['text'], size=data['size'],
                error_correction=data['error_correction'],
                fg_color=data['fg_color'], bg_color=data['bg_color']
            )
            qr.save()
            qr.image.save(f'qr_{qr.pk}.png', ContentFile(buf.read()))
            generated_qr = qr
            form = QRCodeForm()
    else:
        form = QRCodeForm()
    return render(request, 'qr_generator/generate.html', {'form': form, 'generated_qr': generated_qr})

def download_qr(request, qr_id):
    qr = get_object_or_404(QRCode, pk=qr_id)
    response = FileResponse(qr.image.open(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="qr_{qr.pk}.png"'
    return response

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('generate')
    else:
        form = UserRegistrationForm()
    return render(request, 'qr_generator/register.html', {'form': form})

@login_required
def history(request):
    return render(request, 'qr_generator/history.html', {
        'qr_codes': QRCode.objects.filter(user=request.user).order_by('-created_at')
    })