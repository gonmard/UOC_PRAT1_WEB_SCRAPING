#Librerias para web scraping
from requests import get
from bs4 import BeautifulSoup
#Librerías para generación del fichero csv y gráficos
import pandas as pd
import matplotlib.pyplot as plt
#otras libreriías 
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from datetime import datetime
import requests
import locale 
from datetime import timedelta

#Inicialización de las variables
fecha=[]
dia_sorteo=[]
n1=[]
n2=[]
n3=[]
n4=[]
n5=[]
star1=[]
star2=[]
datos=[]
tabla=[]
size=[]
id=[]

#Creamos el  user-agent
ag = UserAgent()
header = {'User-Agent':str(ag.chrome)}
url = 'https://www.combinacionganadora.com/euromillones/'
htmlContent = get(url, headers=header)
#Definimos el perido de captura
fecha_ini = "2019/10/25"
fecha_fin = "2004/05/14"
locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
fecha_sorteo=fecha_ini
date_object = datetime.strptime(fecha_sorteo, "%Y/%m/%d")
dias = timedelta(days=1)
fin=1
sorteo="Si"
i=0
#Definimos el DataFrame para los datos de los sorteos
df= pd.DataFrame(columns=('Fecha', 'dia_sorteo', 'numero1', 'numero2', 'numero3',
                         'numero4', 'numero5', 'estrella1', 'estrella2')) 
#Creamos un bucle para que selecciones la url de cada sorteo
while fin!= 0:
    
    date_object = datetime.strptime(fecha_sorteo, "%Y/%m/%d")
    fecha_sorteo=(datetime.strftime(date_object, "%Y/%m/%d"))
    dweek=datetime.strftime(date_object , "%A")
    #Comprobamos si el día de la semana es viernes o martes y asignamos "SI" a la variable sorteo
    if dweek=="viernes":
        sorteo="SI"
    elif dweek=="martes" and fecha_sorteo>="2011/05/10":
        sorteo="SI"
    #En caso contrario asignamos "NO" a la variable sorteo
    else:
        sorteo="NO"
    #Comprobamos si la fecha está dentro de la fecha final
    if fecha_sorteo<fecha_fin:
        fin=0
    else:
        fin=1
    #Si la variable sorteo es "SI", asignamos la fecha_sorteo ala url
    if sorteo=="SI":
       #definimos la url en cada sorteo
       url_page = 'https://www.combinacionganadora.com/euromillones/'+fecha_sorteo +'/'
       #Verificación que la página existe
       try:
           html = urlopen(url_page)
       except HTTPError as e:
           sys.exit('HTTP error')
       except URLError as e:
       	sys.exit('Server not found!')
        #Realizar petición (target) de la pagina web
       respuesta = get(url_page).text
       req = requests.get(url_page)
       BSoup = BeautifulSoup(req.text, "html.parser")
       #Buscamos en la clase div
       sort = BSoup.find('div',{'class':'off-canvas-wrap'})
       #para los números definicmos la variable resultado 'ul'
       resultado=sort.find('ul')
       #para las estrellas definimos la variavle res_star 'dl'
       res_star=sort.find('dl')
       #añadimos al array la fecha del sorteo
       datos.append(fecha_sorteo)
       #añadimos al array el día del sorteo
       datos.append(dweek)
       #Buscasmos con un for todos los datos de los números 'li' y los añadimos al array datos
       for combinacion in resultado.find_all('li'):
           numero=combinacion.text
           datos.append(numero)
       #Buscasmos con un for todos los datos de las estrellas 'dd' y los añadimos al array datos
       for estrellas in res_star.find_all('dd'):
           num=estrellas.text
           datos.append(num)
       #Asigamos los valores del array datos a cada variables
       fecha=datos[0]
       date_object = datetime.strptime(fecha, "%Y/%m/%d")
       fecha=(datetime.strftime(date_object, "%d/%m/%Y")) 	 
       dia_sorteo=datos[1]
       n1=datos[2]
       n2=datos[3]
       n3=datos[4]
       n4=datos[5]    
       n5=datos[6] 
       star1=datos[7]
       star2=datos[8]
       #Añadimos el sorteo al DataFrame
       df= df.append({'Fecha': fecha, 'dia_sorteo': dia_sorteo,'numero1': n1,
                 'numero2': n2,
                 'numero3': n3,
                 'numero4': n4,
                 'numero5': n5,
                 'estrella1': star1, 'estrella2': star2}, ignore_index=True)
    else:
        pass   
    #restamos un día a la fecha anterior
    date_object=date_object-dias
    #convertimos la fecha en el formato esperado
    fecha_sorteo=(datetime.strftime(date_object, "%Y/%m/%d"))  
    #vaciamos el array de datos
    datos.clear()
    
#Modificamos el formato de la fecha_fin
date_object = datetime.strptime(fecha_fin, "%Y/%m/%d")
#Generamos el fichero EuroMillones.csv con los datos del DataFrame
df.to_csv('EuroMillones.csv')
#Ordenamos el DataFrame por la fecha del sorteo
df= df.sort_values(by='Fecha', ascending=False)

#Definimos las repeticiones de cada número y estrella para imprimir el gráfico
nu1=df['numero1'].astype(int)
nu2=df['numero2'].astype(int)
nu3=df['numero3'].astype(int)
nu4=df['numero4'].astype(int)
nu5=df['numero5'].astype(int)
st1=df['estrella1'].astype(int)
st2=df['estrella2'].astype(int)
count1=[]
count2=[]
count3=[]
count4=[]
count5=[]
ct1=[]
ct2=[]
ct=[]
count=[]
#Definimos el DataFrame para las repeticiones de los números
df1= pd.DataFrame(columns=('numero', 'repeticiones')) 
#Definimos el DataFrame para las repeticiones de las estrellas
df2= pd.DataFrame(columns=('estrella', 'repeticiones')) 
#Generamos un bucle for para comprobar las repeticiones de cada número en cada columna
for i in range(1, 51):
    count1=(nu1[nu1==i].size)
    count2=(nu2[nu2==i].size)
    count3=(nu3[nu3==i].size)
    count4=(nu4[nu4==i].size)
    count5=(nu5[nu5==i].size)
    #Sumamos todas las columnas
    count=count1+count2+count3+count4+count5
    #Añadimos el resultado al DataFrame
    df1=df1.append({'numero': i, 'repeticiones': count}, ignore_index=True)
   
#Generamos un bucle for para comprobar las repeticiones de cada estrella en cada columna
for i in range(1, 13):
    ct1=(st1[st1==i].size)
    ct2=(st2[st2==i].size)
    #Sumamos todas las columnas
    ct=ct1+ct2
    #Añadimos el resultado al DataFrame
    df2=df2.append({'estrella': i, 'repeticiones': ct}, ignore_index=True)

#Gráfico repeticiones de números en sorteos
plt.figure(figsize=(15,6))
ax = plt.gca()
df1.plot(kind='bar', x='numero', y='repeticiones',color='blue',ax=ax)
plt.title('Repeticiones de números en sorteos')
plt.ylabel('Número de repeticiones')
plt.xlabel('Número')

#Se genera la imagen del grafico generado
plt.savefig('Gráfico Repeticiones números.jpg', bbox_inches='tight')
plt.show()


#Gráfico repeticiones de estrellas en sorteos
ax = plt.gca()
df2.plot(kind='bar', x='estrella', y='repeticiones',color='blue',ax=ax)
plt.title('Repeticiones de estrellas en sorteos')
plt.ylabel('Número de repeticiones.jpg')
plt.xlabel('Estrellas')
#Se genera la imagen del grafico generado
plt.savefig('Gráfico Repeticiones estrellas.jpg', bbox_inches='tight') 
plt.show()
  
#ORdenamos las repeticiones descentes y mostramos en consola las 5 más grandes
df1=df1.sort_values(by='repeticiones', ascending=False)
print(df1[:5])
#ORdenamos las repeticiones descentes y mostramos en consola las 2 más grandes
df2=df2.sort_values(by='repeticiones', ascending=False)
print(df2[:2])
