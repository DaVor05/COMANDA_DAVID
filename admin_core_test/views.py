# admin_core_test/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Categoria, Producto, Pedido, PedidoItem
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# ---------- VISTAS BÁSICAS ----------
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


# ---------- CARRITO EN SESIÓN ----------
def _get_cart(request):
    """
    Carrito guardado en sesión con estructura:
    {
      'producto_id': {'nombre': ..., 'precio': ..., 'cantidad': ...},
      ...
    }
    """
    cart = request.session.get('cart', {})
    return cart

def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ---------- MENÚ (CATÁLOGO) ----------
def menu(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    cart = _get_cart(request)

    contexto = {
        'categorias': categorias,
        'cart': cart,
    }
    return render(request, 'menu.html', contexto)


def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = _get_cart(request)

    item = cart.get(str(producto.id), {
        'nombre': producto.nombre,
        'precio': float(producto.precio),  # para poder serializar en sesión
        'cantidad': 0,
    })
    item['cantidad'] += 1
    cart[str(producto.id)] = item

    _save_cart(request, cart)
    return redirect('comandas')  # después de agregar, ver comanda


def clear_cart(request):
    _save_cart(request, {})
    return redirect('comandas')


# ---------- PANTALLA DE COMANDA ----------
def comandas(request):
    cart = _get_cart(request)

    items = []
    total = 0
    for pid, data in cart.items():
        subtotal = data['precio'] * data['cantidad']
        total += subtotal
        items.append({
            'id': pid,
            'nombre': data['nombre'],
            'precio': data['precio'],
            'cantidad': data['cantidad'],
            'subtotal': subtotal,
        })

    contexto = {
        'items': items,
        'total': total,
    }
    return render(request, 'comandas.html', contexto)


# ---------- CONFIRMAR PEDIDO Y GUARDAR EN BD ----------
def confirmar_pedido(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('comandas')

    # en versión simple, mesa y mesero fijos o tomados de un formulario
    mesa = request.POST.get('mesa', '5A')
    mesero = request.POST.get('mesero', 'Mesero Demo')

    pedido = Pedido.objects.create(mesa=mesa, mesero=mesero)

    for pid, data in cart.items():
        producto = Producto.objects.get(id=int(pid))
        PedidoItem.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=data['cantidad'],
            precio_unitario=data['precio'],
        )

    # limpiamos carrito
    _save_cart(request, {})

    # redirigimos directo al PDF
    return redirect('pedido_pdf', pedido_id=pedido.id)


# ---------- GENERAR PDF ----------
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def pedido_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # respuesta HTTP con PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"pedido_{pedido.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, y, f"Comanda - NextOrder")
    y -= 20
    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Pedido #{pedido.id} | Mesa: {pedido.mesa} | Mesero: {pedido.mesero}")
    y -= 20
    p.drawString(40, y, f"Fecha: {pedido.fecha.strftime('%d/%m/%Y %H:%M')}")
    y -= 30

    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, y, "Cant.")
    p.drawString(90, y, "Producto")
    p.drawString(320, y, "P. Unit.")
    p.drawString(400, y, "Subtotal")
    y -= 15
    p.line(40, y, 500, y)
    y -= 20

    p.setFont("Helvetica", 11)
    for item in pedido.items.all():
        if y < 80:  # salto de página simple
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 11)

        p.drawString(40, y, str(item.cantidad))
        p.drawString(90, y, item.producto.nombre[:30])
        p.drawRightString(380, y, f"{item.precio_unitario:.2f}")
        p.drawRightString(480, y, f"{item.subtotal:.2f}")
        y -= 18

    y -= 10
    p.line(300, y, 500, y)
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(480, y, f"TOTAL: {pedido.total:.2f}")

    p.showPage()
    p.save()
    return response
