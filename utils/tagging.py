import re


def get_phone_number(text):
    return re.findall(r'[\+\d][-()\s\d]+?(?=\s*[+<])', text)


def get_email_address(text):
    return re.findall('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+', text)




if __name__ == "__main__":
    Source = ("<p><strong>Kuala Lumpur</strong><strong>:</strong> 9940-546-789</p>\n"
              "        <p><strong>Mutiara Damansara:</strong> 98-546-86-984</p>\n"
              "        <p><strong>Penang:</strong> + 60 (0)4 255 9000</p>\n"
              "        <h2>Where we are </h2>\n"
              "        <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8686\n"
              "        </p></div><div class=\"sys_two\">\n"
              "    <h3 class=\"parentSchool\">General enquiries</h3><p style=\"FONT-SIZE: 11px\">\n"
              "     <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8000\n"
              "+ 60 (7) 268-6200 <br />\n"
              " Fax:<br /> \n"
              " +60 (7) 228-6202<br /> \n"
              "Phone:</strong><strong style=\"color: #f00\">+601-4228-8055</strong> 99-556-88-987"
              "Hi my name is John and email address is john.doe@somecompany.co.uk.fml and my friend's email is "
              "jane_doe124@gmail.com")
    Source = Source.encode().decode()
    print(get_phone_number(Source))
    print(get_email_address(Source))
