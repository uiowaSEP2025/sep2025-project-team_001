import 'package:mobile_app/home/restaurant/models/order.dart';
import 'package:mobile_app/home/restaurant/models/restaurant.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';

Future<void> generateAndPrintReceipt(Order order, String? customerName, Restaurant? restaurant) async {
  final pdf = pw.Document();
  final font = await PdfGoogleFonts.robotoRegular();


  pdf.addPage(
    pw.Page(
      build: (context) => pw.Column(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.Text("Order Receipt", style: pw.TextStyle(font: font,fontSize: 24, fontWeight: pw.FontWeight.bold)),
          pw.SizedBox(height: 10),
          if (restaurant != null)
            pw.Text("Restaurant: ${restaurant.name}"),
          pw.Text("Customer: ${customerName ?? 'N/A'}"),
          pw.Text("Order: #${order.id}"),
          pw.SizedBox(height: 10),
          pw.Text("Items:"),
          pw.Column(
            children: order.items.map((item) {
              final quantity = item['quantity'] ?? '?';
              final name = item['item_name'] ?? 'Unnamed item';
              return pw.Row(
                children: [
                  pw.Text("$quantity x "),
                  pw.Text(name),
                ],
              );
            }).toList(),
          ),
          pw.SizedBox(height: 20),
          pw.Row(
            mainAxisAlignment: pw.MainAxisAlignment.end,
            children: [
              pw.Text("Total: \$${order.totalPrice}", style: pw.TextStyle(font: font,fontSize: 16)),
            ],
          ),
        ],
      ),
    ),
  );

  await Printing.layoutPdf(onLayout: (format) async => pdf.save());
}
