from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import OrderHistory


def generate_invoice(order_id):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    order = OrderHistory.objects.get(id=order_id)

    pdf.setTitle(f"Invoice_{order.id}.pdf")
    pdf.drawString(100, 800, f"Invoice for Order #{order.id}")
    pdf.drawString(100, 780, f"Buyer: {order.buyer.username}")
    pdf.drawString(100, 760, f"Product: {order.product.name}")
    pdf.drawString(100, 740, f"Quantity: {order.quantity}")
    pdf.drawString(100, 720, f"Total Price: ${order.total_price}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
