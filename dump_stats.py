import os
import csv
from dateutil import parser

from skyrec.processing import Image

observed_okta = {}
with open('contrib/data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wd = parser.parse(row['timestamp']).strftime('%Y%m%d_%H')
        observed_okta[wd] = row['observed']

basedir = '/lustre/storeB/users/thomasn/webcams/cropped'

txt_file = open('extracted_features.txt', 'w')
txt_file.write("filename,msat,vsat,mbr,vbr,bf,gf,observed\n")

html_file = open('raw_values.html', 'w')
html_file.write("<html><body><table border = \"1\">")
html_file.write("""
<tr>
    <th>Image</th>
    <th>Saturation (mean)</th>
    <th>Saturation (var)</th>
    <th>Brightness (mean)</th>
    <th>Brightness (var)</th>
    <th>Blue Fraction</th>
    <th>Grey Fraction</th>
    <th>Observed okta</th>
</tr>""")


def write_txt_row(iname, oo, sm, sv, bm, bv, bf, gf):
    txt_file.write("%s, %.5f, %.1f, %.5f, %.1f, %.5f, %.5f, %s\n" % (iname, sm, sv, bm, bv, bf, gf, oo))

def write_html_row(ip, oo, sm, sv, bm, bv, bf, gf):
    color = "#FFFFFF"


    if (im.brightness['mean'] < 0.4):
        color = "#FF0000"

    html_file.write("<tr bgcolor=\"%s\">\n" % color)
    html_file.write("<td><img src=\"%s\" style=\"width:400px\"</td>\n" % ip)
    html_file.write("<td>%.5f</td>\n" % sm)
    html_file.write("<td>%.1f</td>\n" % sv)
    html_file.write("<td>%.5f</td>\n" % bm)
    html_file.write("<td>%.1f</td>\n" % bv)
    html_file.write("<td>%.5f</td>\n" % bf)
    html_file.write("<td>%.5f</td>\n" % gf)
    html_file.write("<td>%s</td>\n" % oo)
    html_file.write("</tr>\n")


for image_name in os.listdir(basedir):
    if image_name.endswith(".jpg"):
        try:
            oo = observed_okta[image_name[:11]]
        except:
            oo = ''

        image_path = (basedir + '/' + image_name)
        im = Image(image_path)

        write_html_row(image_path, oo, im.saturation['mean'], im.saturation['var'], im.brightness['mean'], im.brightness['var'], im.blue_fraction, im.grey_fraction)
        write_txt_row(image_name, oo, im.saturation['mean'], im.saturation['var'], im.brightness['mean'], im.brightness['var'], im.blue_fraction, im.grey_fraction)

html_file.write("</table></body></html>\n")
html_file.close()

txt_file.write("\n")
txt_file.close()