import qrcode
search=input("describe picture or the information you are looking for: ")
google=f"{search}"#converting the input into other format
content_qr=qrcode.make(google)#generating qrcode for going to the google info page
# content_qr.save("info-qr.png")#saving the generated qr
content_qr.show()
# content_qr.save()