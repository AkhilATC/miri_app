from datetime import datetime
from xhtml2pdf import pisa


def set_header(invoiceNumber):
    html_ = f"""<p>GSTIN:32FERPB9239A1ZM</p>\
    <p align='right'>Original for Recepiant<br>Duplicate for transporter<br>Tripicate for Supplier</p>\
    <H1 align='center' style="color:blue;">CASCADE TRADERS</H1>\
    <h2 align=\"center\">Nedumpana,Nedumpana P.O,Kollam,Ph:8139812715</h2>\
    <h3 align=\"center\">BILL OF SUPPLAY</h2> \
    <p align=\"center\">Composltion Taxable person. Not eligible to collect tax on supplies</p>\
    <p align=\"left\"> Invoice No:CACA/2021/{invoiceNumber}</p><hr>"""

    return html_

def set_user_data(html_,user_data):
    username = user_data.get('name')
    address = user_data.get('address')
    html_ += f"""<div style=\"width: 100%;background-color: #DCDCDC;color:black;padding: 14px 20px;margin: 8px 0;\
            border: none; border-radius: 4px;cursor: pointer; display: table;\">\
            <span style="display: table-cell; vertical-align: middle;"><p>Suppliers Ref:</p></span>\
            <span style="display: table-cell; vertical-align: middle;">\
            <p>Date of issue:{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}</p></span>\
            <span style="display: table-cell; vertical-align: middle;"><p>Vehicle No:</p></span></div><hr>\
            <div style="width: 100%;background-color: #E6FFFB;color:black;padding: 14px 20px;margin: 8px 0;\
            border: none; border-radius: 4px;cursor: pointer; display: table;">\
            <span style="display: table-cell; vertical-align: middle;border-style: groove;">\
            <p>Customer details :</p><br><p> {username}\n {address} </p></span>\
            <span style="display: table-cell; vertical-align: middle;border-style: groove;">\
            <p>Retailer details :</p><br><p> {None} </p></span><div><hr>"""
    return html_

def table_render(html_,data):
    html_ += """<table style="font-family: arial, sans-serif ;border-collapse: collapse; width: 100%;">
    <tr>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">SL No</th>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">Description of Goods</th>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">HSN/SAC</th>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">Qty</th>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">UOM</th>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">Unit rate</th>
     <th style="border: 1px solid #dddddd;text-align: left;padding: 8px;">Amount</th>
     </tr>
    """
    #{'name': 'wash baism /3/12333/3', 'cost': '1200', 'count': '2'}
    gross_ = []
    for each in data:
        product_info = each['name'].split('/')
        net_ = int(each['cost'])*int(each['count'])
        gross_.append(net_)
        html_ += f"""<tr><td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{data.index(each)+1}</td>\
        <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{product_info[0]}</td>\
        <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{product_info[2]}</td>\
        <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{each['count']}</td>\
        <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{" "}</td>\
        <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{each['cost']}</td>\
        <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{net_}</td>\
        </tr>"""
    html_+= f"""<tr><td>{ " " }</td>\
    <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{" "}</td>\
    <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{" "}</td>\
    <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{" "}</td>\
    <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{" "}</td>\
    <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{" "}</td>\
    <td style="border: 1px solid #dddddd;text-align: left;padding: 8px;">{sum(gross_)}</td>\
    </tr style="border: 1px solid #dddddd;text-align: left;padding: 8px;"></table>"""
    return html_

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

if __name__ == "__main__":

    # pdf_object = pdfGenerator()
    # pdf_object._save()
    # pdf_object.add_page()
    html = set_header(123)
    html = set_user_data(html,{'name':"akhil t cheriyan",'address':"thenguvilla veedu, allumoodu po,kollam"})
    html = table_render(html,[1,2,3])
    # pdf_object.write_html(html)
    file_name = f"miRi_bill_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.pdf"
    # pdf_object.output(file_name, 'F')
    convert_html_to_pdf(html,file_name)


