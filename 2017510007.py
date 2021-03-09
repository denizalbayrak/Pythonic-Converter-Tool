# encoding: utf-8
import xml.dom.minidom
import csv
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import sys
import json
from lxml import etree as denizet
from io import StringIO
import json as j

#XSD1 düzenleme yaptığım fakat tg mismatch hatası aldığım fakat taglarımın doğru olduğu
#XSD2 düzenleme yapmadığım true döndüren
#CSV TO XML
if (sys.argv[3] == "1"):
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  with open(input_file, 'r', encoding="utf-8") as f:
    #reading according to delimiter
    csv_reader = csv.reader(f, delimiter=';')
    #assigning root from xml tree
    root=etree.Element("departments")
    tree=etree.ElementTree(root)
    #pass first line command
    next(csv_reader)
    for line in csv_reader:
      #assign child elements of an xml tree by reading row by row
      subelement1=etree.SubElement(root, "university")
      subelement1.set("name", line[1])
      subelement1.set("utype", line[0])
      subelement2=etree.SubElement(subelement1, "item")
      subelement2.set("id", line[3])
      subelement2.set("faculty", line[2])
      etree.SubElement(subelement2, "name", lang=line[5], second= line[6]).text=line[4]
      etree.SubElement(subelement2, "period").text = line[8]  
      etree.SubElement(subelement2, "quota", spec = line[11]).text = line[10]
      etree.SubElement(subelement2, "field").text = line[9]
      etree.SubElement(subelement2, "last_min_score", order = line[12]). text = line[13]
      etree.SubElement(subelement2, "grant").text = line[7]
  #correction process to appear correctly in xml file
  data = etree.tostring(root)
  deniz = xml.dom.minidom.parseString(data)
  deniz2 = deniz.toprettyxml()
  #writing to xml output file
  file = open(output_file, "w",encoding="utf-8")
  file.write(deniz2)
  file.close()
#XML TO CSV
elif(sys.argv[3] == "2"):
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  #read the input file and create an xml tree
  tree = etree.parse(input_file)
  root = tree.getroot()
  with open(output_file, 'w', newline='', encoding="utf-8") as file:
      file.write("ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n" )
      #navigating the tree with loops and assigning names
      for item in root.findall('university'):
        uni_name = item.attrib.get('name') 
        uni_utype = item.attrib.get('utype')
        
        for subitem in item.iter('item'):
          item_id = subitem.attrib.get('id')
          item_faculty = subitem.attrib.get('faculty')
          for name in subitem.iter('name'):
            lang = name.get('lang')
            second = name.get('second')
            program = subitem.find('name').text
            period =subitem.find('period').text
            
            if subitem.find('grant').text == None:
              grant = ""
            else:
              grant = subitem.find('grant').text

            for quota in subitem.iter('quota'):
              spec = quota.get('spec')
              cont = subitem.find('quota').text
              field = subitem.find('field').text             
              for last in subitem.iter('last_min_score'):
                order=last.get('order')
                if subitem.find('last_min_score').text == None:
                  last_min_score = ""
                else:
                  last_min_score = subitem.find('last_min_score').text
                #writing these values to the csv file
                file.write(uni_utype +";"+ uni_name + ";" + item_faculty  +";" + item_id + ";" + program + ";"+  lang + ";" + second + ";" + grant + ";" + period + ";" + field +";" + cont + ";" + spec + ";" + order +";"+ last_min_score + "\n")
#XML TO JSON
elif(sys.argv[3] == "3"):
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  tree = etree.parse(input_file)
  root = tree.getroot()
  with open(output_file, 'w', newline='', encoding="utf-8") as file:
    #integer values for each university to print the first line once
    ideu=0
    iege = 0
    iyasar=0   
    iieu=0 
    iiyte=0
    iibu=0 
    iidu=0 
    iikcu=0
    #navigating the tree with loops and assigning names
    for item in root.findall('university'):
          uni_name = item.attrib.get('name') 
          uni_utype = item.attrib.get('utype')
          #checking for all univesity name for the process of throwing values into the JSON file
          if(uni_name == "DOKUZ EYLÜL ÜNİVERSİTESİ"):
            ideu += 1
            #if it is one, we can understans that this university will reading for the first time
            if(ideu==1):
              file.write("[" + "\n" + " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
            #navigating the tree with loops and assigning names
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(ideu==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
                        if(ideu == 13):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          #repeating same things for every university
          if(uni_name == "EGE ÜNİVERSİTESİ"):
            
            iege += 1
            if(iege==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iege==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n")
                        if(iege == 9):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          if(uni_name == "YAŞAR ÜNİVERSİTESİ"):
            iyasar += 1
            if(iyasar==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n" )
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iyasar==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" +"\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
                        if(iyasar == 28):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          if(uni_name == "İZMİR EKONOMİ ÜNİVERSİTESİ"):
            iieu += 1
            if(iieu==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n" )
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iieu==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" +"\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n")
                        if(iieu == 28):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          if(uni_name == "İZMİR YÜKSEK TEKNOLOJİ ENSTİTÜSÜ"):
            iiyte += 1
            if(iiyte==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n" )
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iiyte==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" +"\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" +"\n")
                        if(iiyte == 10):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          if(uni_name == "İZMİR BAKIRÇAY ÜNİVERSİTESİ"):
            iibu += 1
            if(iibu==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n" )
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iibu==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" +"\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" +"\n")
                        if(iibu == 4):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          if(uni_name == "İZMİR DEMOKRASİ ÜNİVERSİTESİ"):
            iidu += 1
            if(iidu==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n" )
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iidu==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" +"\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n")
                        if(iidu == 5):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
          if(uni_name == "İZMİR KATİP ÇELEBİ ÜNİVERSİTESİ"):
            iikcu += 1
            if(iikcu==1):
              file.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n" )
              file.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
        
            for subitem in item.iter('item'):
                  item_id = subitem.attrib.get('id')
                  item_faculty = subitem.attrib.get('faculty')
                  if(iikcu==1):
                    file.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" +"\n")
                  for name in subitem.iter('name'):
                    lang = name.get('lang')
                    second = name.get('second')
                    program = subitem.find('name').text
                    period =subitem.find('period').text
            
                    if subitem.find('grant').text == None:
                      grant = "null"
                    else:
                      grant = subitem.find('grant').text

                    for quota in subitem.iter('quota'):
                      spec = quota.get('spec')
                      cont = subitem.find('quota').text
                      field = subitem.find('field').text             
                      for last in subitem.iter('last_min_score'):
                        order=last.get('order')
                        if subitem.find('last_min_score').text == None:
                          last_min_score = ""
                        else:
                          last_min_score = subitem.find('last_min_score').text
                        file.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
                        if(iikcu == 8):
                          file.write("                            }\n")
                        else:
                          file.write("                            },\n")
    file.write("                     ]\n" +"          }\n"+ "     ]\n" + " }\n")
    file.write("]\n")
#JSON TO XML
elif(sys.argv[3] == "4"):  
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  with open(input_file, encoding="utf-8") as file:
    data = json.load(file)
    root=etree.Element("departments")
    #navigating the tree with loops and assigning names
    for temp in data:
      subelement1=etree.SubElement(root, "university")
      university_name = temp['university name']
      subelement1.set("name", university_name)
      uType = temp['uType']
      subelement1.set("uType",uType)
      items=temp['items']
      for item in items:
        department=item['department']
        for content in department:
          subelement2=etree.SubElement(subelement1, "item")
          faculty=item['faculty']
          subelement2.set("faculty", faculty)
          id=content['id']
          subelement2.set("id", id)
          name=content['name']
          language=content['lang']
          second=content['second']
          etree.SubElement(subelement2, "name" , lang = language , second = second).text = name
          period=content['period']
          etree.SubElement(subelement2, "period").text =period
          spec=content['spec']
          quota=content['quota']
          etree.SubElement(subelement2, "quota", spec=spec).text = quota
          field=content['field']
          etree.SubElement(subelement2, "field").text = field
          last_min_order=content['last_min_order']          
          last_min_score=content['last_min_score']
          etree.SubElement(subelement2, "last_min_score", order = last_min_order).text = last_min_score
          grant=content['grant']
          etree.SubElement(subelement2, "grant").text = grant
  data = etree.tostring(root)
  deniz = xml.dom.minidom.parseString(data)
  deniz2 = deniz.toprettyxml()
  file = open(output_file, "w",encoding="utf-8")
  file.write(deniz2)
  file.close()
#CSV TO JSON
elif(sys.argv[3] == "5"):
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  with open(input_file, 'r', encoding="utf-8") as file:
    #reading according to delimiter
    csv_reader = csv.reader(file, delimiter=';')
    #integer values for each university to print the first line once
    ideu=0
    iege = 0
    iyasar=0   
    iieu=0 
    iiyte=0
    iibu=0 
    iidu=0 
    iikcu=0
    next(csv_reader)
    with open(output_file, 'w', newline='', encoding="utf-8") as f:
      f.write("[" + "\n" )
      for line in csv_reader:
        uni_name = line[1]
        uni_utype = line[0]
        
        if(uni_name == "DOKUZ EYLÜL ÜNİVERSİTESİ"):
          ideu += 1
          if(ideu==1):
            f.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(ideu==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(ideu == 13):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "EGE ÜNİVERSİTESİ"):
          iege += 1
          if(iege==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write(" {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iege==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iege == 9):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "YAŞAR ÜNİVERSİTESİ"):
          iyasar += 1
          if(iyasar==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write( " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iyasar==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iyasar == 28):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "İZMİR EKONOMİ ÜNİVERSİTESİ"):
          iieu += 1
          if(iieu==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write( " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iieu==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iieu == 28):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "İZMİR BAKIRÇAY ÜNİVERSİTESİ"):
          iibu += 1
          if(iibu==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write( " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iibu==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iibu == 4):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "İZMİR YÜKSEK TEKNOLOJİ ENSTİTÜSÜ"):
          iiyte += 1
          if(iiyte==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write( " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iiyte==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iiyte == 10):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "İZMİR DEMOKRASİ ÜNİVERSİTESİ"):
          iidu += 1
          if(iidu==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write( " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iidu==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iidu == 5):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
        if(uni_name == "İZMİR KATİP ÇELEBİ ÜNİVERSİTESİ"):
          iikcu += 1
          if(iikcu==1):
            f.write("                     ]\n" +"          }\n"+ "     ]\n" + " },\n")
            f.write( " {" + "\n" + "   \"university name\": " +  " \"" + uni_name + "\" " + ","+ "\n" + "     \"uType\": \"" + uni_utype + "\"" + ","+"\n" +  "     \"items\": " +"\n" )
          item_id = line[3]
          item_faculty = line[2]
          if(iikcu==1):
            f.write("     [" + "\n" + "          {" + "\n"+ "                    \"faculty\": "+ "\""+ item_faculty + "\","+  "\n" + "                    \"department\": " + "\n                     [" + "\n")
          lang = line[5]
          second = line[6]
          program = line[4]
          period = line[8]
          grant = line[7]
          if (grant == ""):
            grant = "null"
          spec = line[11]
          cont = line[10]
          field = line[9]             
          order=line[12]
          last_min_score = line[13]
          f.write("                            {" +"\n" + "                                 \"id\": " + "\"" + item_id +"\","+ "\n" + "                                 \"name\":\""+program+ "\"," + "\n" +"                                 \"lang\":\""+lang+ "\"," + "\n" +"                                 \"second\":\""+second+ "\"," + "\n" + "                                 \"period\":\""+period+ "\"," + "\n" +"                                 \"spec\":\""+spec+ "\"," + "\n""                                 \"quota\":\""+cont+ "\"," + "\n" + "                                 \"field\":\""+field+ "\"," + "\n" +"                                 \"last_min_score\":\""+last_min_score+ "\"," + "\n" + "                                 \"last_min_order\":\""+order+ "\"," + "\n" +"                                 \"grant\":\""+grant+ "\"" + "\n"+ "\n")
          if(iikcu == 8):
            f.write("                            }\n")
          else:
            f.write("                            },\n")
      f.write("                     ]\n" +"          }\n"+ "     ]\n" + " }\n")
      f.write("]\n")   
#JSON TO CSV
elif(sys.argv[3] == "6"):
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  with open(input_file, encoding="utf-8") as file:
    data = json.load(file)  
    with open(output_file, 'w', newline='', encoding="utf-8") as file:
      file.write("ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n" )
      #navigating the tree with loops and assigning names
      for temp in data:
        university_name = temp['university name']
        uType = temp['uType']       
        items=temp['items']
        for item in items:
          department=item['department']
          for content in department:
            faculty=item['faculty']
            id=content['id']
            name=content['name']
            language=content['lang']
            second=content['second']
            period=content['period']
            spec=content['spec']
            quota=content['quota']
            field=content['field']
            last_min_order=content['last_min_order']          
            last_min_score=content['last_min_score']
            grant=content['grant']
            #writing these values to the csv file
            file.write(uType +";"+ university_name + ";" + faculty  +";" + id + ";" + name + ";"+  language + ";" + second + ";" + grant + ";" + period + ";" + field +";" + quota + ";" + spec + ";" + last_min_order +";"+ last_min_score + "\n")
#XSD VALIDATION
elif(sys.argv[3] == "7"):
  #taking inputs from user
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  doc = denizet.parse(input_file)
  root = doc.getroot()
  #print(denizet.tostring(root))
  xmlschema_doc = denizet.parse(output_file)
  xmlschema = denizet.XMLSchema(xmlschema_doc)
  doc = denizet.XML(denizet.tostring(root))
  validation_result = xmlschema.validate(doc)
  print(validation_result)