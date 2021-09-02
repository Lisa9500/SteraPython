import csv

with open('utf8.csv', 'w', newline='', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(['商品名','価格'])
    writer.writerow(['りんご','300'])
    writer.writerow(['みかん','200'])
    writer.writerow(['パイナップル','500'])
with open('utf8.csv', encoding='utf8') as f_in:
    with open('shiftjis.csv', 'w', encoding='shift_jis') as f_out:
        f_out.write(f_in.read())
