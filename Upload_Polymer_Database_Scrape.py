#second layer will iterate through the class of polymers and call the 'data_scrape.py'
# function to print individual polymer data
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "new_polymer_data.csv"
f = open(filename, "w", errors = "ignore")
f.write("Polymer_Name" + "," + "Smiles" + "," + "Molar_Volume" + "," + "Density"+ "," + "Solubility_Parameter" + "\n")
count = 1
#change link to a BeautifulSoup readable file
home_URL = 'http://polymerdatabase.com/home.html'
the_page = uReq(home_URL)
home_page = the_page.read()
the_page.close()

#the for loop is generating the outmost links to click on
#includes all polymers from A-V
home_parse = soup(home_page, "html.parser")
menu_links = home_parse.findAll("ul",{"class":"auto-style19"})[0]
pages = []
for menus in menu_links.find_all('a'):
    page = menus.get('href')
    pages = pages + ['http://polymerdatabase.com/' + page]
#indexing removes links with in the menu bar that donot contain polymer data
pages = pages[1:7]

#nested for loop is generating all the links to materials pages by mateials class
material_class = []
count = 0
for my_URL in pages:
    #print(my_URL)
    #my_URL corresponds to unique materials set range, A-B, C-D, E-F... ect. 
    count = count + 1
    my_page = uReq(my_URL)
    page = my_page.read()
    my_page.close() 
    parse_page = soup(page, "html.parser")
    a = parse_page.table.tr
    
    for links in a.find_all('a'):
        mat = links.get('href')
        #mat specific material link with in each range, for example A-B...
        #has 17 specific polymer classes
        #print(mat)
        if count == 1:
            #first page (aka home page, A-B polymers) has a different href format than all remaining pages
            #omits material classes outside of data set scope because difficult structure to model
            if mat != 'polymer index/polyamides.html' and mat != 'polymer index/polyanhydrides.html'\
            and mat != 'polymer index/polyesters.html' and mat != 'polymer index/polyesters.html'\
            and mat != 'polymer index/polyketones.html' and mat != 'polymer index/polysulfides.html':
                mat = 'http://polymerdatabase.com/' + mat
                material_class = material_class + [mat]
        else:
            #omitting material classes outside of data set scope because difficult structure to model
            if mat != 'polycarbonates.html' and mat != 'Cellulose.html' and mat != 'epoxyresins.html' \
            and mat != 'polyesters.html' and mat != 'polykentones.html' and mat != 'polyethersulfones.html'\
            and mat != 'polyhydroxymethacrylates.html' and mat != 'polyurethanes.html' and \
            mat != 'polyterephthalates.html' and mat != 'poly(bisphenol).html' and \
            mat != 'polyamides.html' and mat != 'Polysuccinates.html' and mat != 'polyvinylalcohols.html'\
            and mat != 'polysebascates.html':
                material_class = material_class + ['http://polymerdatabase.com/polymer index/' + mat]

material_class.pop(10)      
material_class = material_class[:-1]
#removes repeat entries
material_class = list(set(material_class))
# print(material_class))       

#takes each materials catagory such as  polhyacrylamides and access individual 
#materials with in specific materials class, stores results in links
links = []
for material in material_class:
    #print(material)
    my_new_page = uReq(material)
    new_page = my_new_page.read()
    my_new_page.close() 
    
    parse_page_new = soup(new_page, "html.parser")
    data_grids = parse_page_new.findAll("ul",{"class":"auto-style13"})[0]
      
    for link in data_grids.find_all('a'):
        actual_link = link.get("href")
        if actual_link != '../polymers/polyvinylbutyral.html' and actual_link != '../polymers/polyvinylformal.html'\
        and actual_link != 'polymers/polyvinylbutyrate.html' and actual_link != '../polymers/polyvinylpyrrolidone.html':
            actual_link = 'http://polymerdatabase.com/' + actual_link[3:]
            links = links + [actual_link]        
    
#iterates through every link and finds all of the tables needs         
for n in links:
    uClient = uReq(n)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    #finds polymer name and prints to a .csv file
    #_.replace(',','')- names containing ',' replaced with '' to aviod creating 
    #new next data frame when printing to .csv file 
    #print(n)
    polymer_name = page_soup.title.string.replace(',','')
    #print(polymer_name)
    f.write(polymer_name + ",")
    #data grids contains 4 seperate table, the last three are relavent
    data_grids = page_soup.findAll("div",{"class":"datagrid"})
    
    for i in [1,2,3]:
        table = data_grids[i]
        #second table, accessed in first loop, contains SMILES string 
        if i == 1:
             smiles = table.findAll("tr")[2].findAll("td")[1].string
             #removes any " " or \n that would result in a next line .csv file
             smiles = smiles.lstrip()
             #print(smiles)
             f.write(smiles + ",")
        
        #third table, accessed in second loop, contains experimental data
        #experimental data is prioritized of computational data
        #two columns of interest, 'value/value range' and 'preferred'
        #'preferred' is prioritized over 'value/value range'
        elif i == 2:
            #if preffered value of molar volume exists store value, other wise 
            #take the value/value range. Note it is still possible value/value range
            #contains a blank
            #_.strip() removes all leading and trailing white spaces
              if table.findAll("tr")[1].findAll("td")[3].text != "":
                  molar_volume = table.findAll("tr")[1].findAll("td")[3].text.strip()
                  molar_volume = molar_volume.strip("*")
              else:
                  molar_volume = table.findAll("tr")[1].findAll("td")[2].text.strip()
                  molar_volume = molar_volume.strip("*")
          		
              if table.findAll("tr")[2].findAll("td")[3].text != "":
                  density 	  = table.findAll("tr")[2].findAll("td")[3].text.strip()
                  denstiy      = density.strip("*")
              else:
                  density 	  = table.findAll("tr")[2].findAll("td")[2].text.strip()
                  denstiy      = density.strip("*")
        		
              if table.findAll("tr")[3].findAll("td")[3].text != "":
                  solubility_p = table.findAll("tr")[3].findAll("td")[3].text.strip()
                  
              else:
                  solubility_p = table.findAll("tr")[3].findAll("td")[2].text	.strip()
        #forth table, accessed in third loop, contains computed data. if statements
        #check to see whether or not a value has been stored. If an empty string 
        #is stored, computed data is used with the same prioritization of exp. data
        elif i == 3:
              if molar_volume == "":
                      if table.findAll("tr")[3].findAll("td")[3].text != "":
                          molar_volume = table.findAll("tr")[3].findAll("td")[3].text
                          f.write(molar_volume + ",")
                      else:
                          molar_volume = table.findAll("tr")[3].findAll("td")[2].text
                          f.write(molar_volume + ",")
              else:
                      f.write(molar_volume + ",")        
        
              if density == "":
                  if table.findAll("tr")[4].findAll("td")[3].text != "":
                            density = table.findAll("tr")[4].findAll("td")[3].text
                            f.write(density + ",")
                  else: 
                            density = table.findAll("tr")[4].findAll("td")[2].text 
                            f.write(density + ",")
              else:
                      f.write(density + ",")                         
              f.write(solubility_p + "\n")    
# =============================================================================
#               if solubility_p == "" or solubility_p == "&nbsp;":
#                   if table.findAll("tr")[5].findAll("td")[3].text != "":
#                           solubility_p = table.findAll("tr")[5].findAll("td")[3].text
#                           f.write(solubility_p + "\n")
#       
#                   else:
#                           solubility_p = table.findAll("tr")[5].findAll("td")[2].text
#                           f.write(solubility_p + "\n")
#               else:
#                       f.write(solubility_p + "\n")
# =============================================================================

