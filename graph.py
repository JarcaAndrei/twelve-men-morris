import pygame
import sys
import math
import copy
import pandas as pd
import numpy as np
import time
import statistics
ADANCIME_MAX=2
def distEuclid(p0,p1):
	(x0,y0)=p0
	(x1,y1)=p1
	return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Graph:
	#coordonatele nodurilor ()
	noduri=[
		#(coloana,linie)
		(0,0),
		(2,0),
		(4,0),
		(0.7,0.7),
		(2,0.7),
		(3.4,0.7),
		(1.4,1.4),
		(2,1.4),
		(2.7,1.4),
		(0,2),
		(0.7,2),
		(1.4,2),
		(2.7,2),
		(3.4,2),
		(4,2),
		(1.4,2.7),
		(2,2.7),
		(2.7,2.7),
		(0.7,3.4),
		(2,3.4),
		(3.4,3.4),
		(0,4),
		(2,4),
		(4,4)
	]
	muchii=[(0,1),(0,3),(0,9),(1,4),(1,2),(2,5),(2,14),(3,4),(3,6),(3,10),(4,5)
	,(4,7),(5,8),(5,13),(6,11),(6,7),(7,8),(8,12),(9,21),(9,10),(10,11),(10,18)
	,(11,15),(12,13),(12,17),(13,14),(13,20),(14,23),(15,16),(15,18),(16,17)
	,(16,19),(17,20),(18,21),(18,19),(19,20),(19,22),(20,23),(21,22),(22,23)]
	scalare=100
	translatie=20
	razaPct=10
	razaPiesa=20

class Joc:
	"""
	Clasa care defineste jocul. Se va schimba de la un joc la altul.
	"""
	NR_COLOANE=7
	JMIN=None
	JMAX=None
	GOL='#'

	@classmethod
	def initializeaza(cls, display, NR_COLOANE=3, dim_celula=100):
		cls.display=display
		cls.dim_celula=dim_celula
		cls.x_img = pygame.image.load('ics.png')
		cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, math.floor(dim_celula*cls.x_img.get_height()/cls.x_img.get_width())))
		cls.zero_img = pygame.image.load('zero.png')
		cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula,math.floor(dim_celula*cls.zero_img.get_height()/cls.zero_img.get_width())))
		cls.celuleGrid=[] #este lista cu patratelele din grid
		for linie in range(NR_COLOANE):
			cls.celuleGrid.append([])
			for coloana in range(NR_COLOANE):
				patr = pygame.Rect(coloana*(dim_celula+1), linie*(dim_celula+1), dim_celula, dim_celula)
				cls.celuleGrid[linie].append(patr)



	def deseneaza_grid(self, marcaj=None): # tabla de exemplu este ["#","x","#","0",......]

		for linie in range(Joc.NR_COLOANE):
			for coloana in range(Joc.NR_COLOANE):
				if marcaj==(linie,coloana):
					#daca am o patratica selectata, o desenez cu rosu
					culoare=(255,0,0)
				else:
					#altfel o desenez cu alb
					culoare=(255,255,255)
				pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[linie][coloana]) #alb = (255,255,255)
				if self.matr[linie][coloana]=='x':
					self.__class__.display.blit(self.__class__.x_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)+ (self.__class__.dim_celula-self.__class__.x_img.get_height())//2))
				elif self.matr[linie][coloana]=='0':
					self.__class__.display.blit(self.__class__.zero_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)+(self.__class__.dim_celula-self.__class__.zero_img.get_height())//2))
		#pygame.display.flip() # !!! obligatoriu pentru a actualiza interfata (desenul)
		pygame.display.update()



	def __init__(self, tabla=None,freq=[],rand=0,albCnt=12,negruCnt=12,pieseAlbe=[],pieseNegre=[],millPos=[],idxMill=[],prevAlb=None,prevNegru=None):
		if tabla:
			self.matr=tabla #matricea 
			self.freq=freq #daca e 1, inseamna ca moara respectiva e activa
			self.rand=rand #cate elemente avem de eliminat la ai
			self.albCnt=albCnt  #numar de piese albe ramase de pus
			self.negruCnt=negruCnt #numar de piese negre ramase de pus
			self.pieseAlbe=pieseAlbe #coordonate pentru piese albe puse 
			self.pieseNegre=pieseNegre #coordonate pentru piese negre puse
			self.millPos=millPos #colectie de coordonate pentru toate morile
			self.idxMill=idxMill #colectia de mori formate din indicii pieselor
			self.prevAlb=prevAlb #mutare anterioara alba
			self.prevNegru=prevNegru #mutare anterioara neagra
		else:
			self.prevAlb=prevAlb
			self.prevNegru=prevNegru
			self.matr= [[0,'#','#', 1,'#','#', 2],
						['#',3,'#', 4,'#', 5, '#'],
						['#','#',6, 7,  8, '#','#'],
						[9,  10, 11,'#',12,13, 14],
						['#','#',15,16, 17,'#','#'],
						['#',18,'#',19,'#',20,'#'],
						[21,'#','#',22,'#','#',23]
					]
			self.innate=copy.deepcopy(self.matr)
			self.millPos=[[0,1,2],[0,3,6],[0,9,21],[1,4,7],[2,5,8],[2,14,23],[3,4,5]
						,[3,10,18],[5,13,20],[6,7,8],[6,11,15],[8,12,17],[9,10,11]
						,[12,13,14],[15,16,17],[15,18,21],[16,19,22],[17,20,23],
						[18,19,20],[21,22,23]]
			self.idxMill=copy.deepcopy(self.millPos)
			for i in range(len(self.millPos)):
				temp=[]
				for j in range(len(self.matr)):
					for k in range(len(self.matr[0])):
						if self.matr[j][k]==self.millPos[i][0]:
							temp.append([j,k])
						elif self.matr[j][k]==self.millPos[i][1]:
							temp.append([j,k])
						elif self.matr[j][k]==self.millPos[i][2]:
							temp.append([j,k])
				self.millPos[i]=copy.deepcopy(temp)
			self.freq=[]
			for i in range(len(self.millPos)):
				self.freq.append(0)
			self.pieseAlbe=[]
			self.pieseNegre=[]
			self.albCnt=12
			self.negruCnt=12
			self.rand=0 #sau sterge
		self.innate=[[0,'#','#', 1,'#','#', 2],
						['#',3,'#', 4,'#', 5, '#'],
						['#','#',6, 7,  8, '#','#'],
						[9,  10, 11,'#',12,13, 14],
						['#','#',15,16, 17,'#','#'],
						['#',18,'#',19,'#',20,'#'],
						[21,'#','#',22,'#','#',23]
					]
	@classmethod
	def jucator_opus(cls, jucator):
		return cls.JMAX if jucator==cls.JMIN else cls.JMIN

		#cand un jucator nu mai poate face mutari, verificat daca celalalt
		#are doar o piesa ramasa de pus
	def final(self,prev1=None,prev2=None):
		"""
		:prev1 - de unde pleaca piesa anterioara a playerului real
		:prev2 - unde ajunge piesa anterioara pt player real
		"""
		vec=[]
		for i in range(24):
			vec.append(i)
		ok=0
		#conditia pentru draw este ca am pus toate piesele pe tabla si n avem unde muta
		#asa ca e de ajuns sa nu fie niciun loc gol pe harta
		for i in self.matr:
			for j in i:
				if j in vec:
					ok+=1
		if ok==0:
			return 'draw'

		#n0=coordonateNoduri.index(nod)
		#n1=coordonateNoduri.index(nodPiesaSelectata)
		#if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii):
		ok=0
		#verificam daca alb nu are niciun loc unde ar putea muta
		for i in self.pieseAlbe:
			for j in coordonateNoduri:
				n0=coordonateNoduri.index(i)
				n1=coordonateNoduri.index(j)
				#verificam si cazurile cu piesa anterioara
				if self.prevAlb!=None:
					if i==self.prevAlb[1] and j==self.prevAlb[0]:
						continue
				if Joc.JMIN=='alb':
					if i==prev2 and j==prev1:
						continue
				if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii):
					if j not in self.pieseAlbe+self.pieseNegre:
						ok=1
						break
		if ok==0 and self.albCnt==0:
			return 'negru'
		#pos=[[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
		#ok=0
		albAm=0
		negAm=0
		#verificam daca mai sunt doar 2 piese albe pe harta si nu mai avem alte piese de adaugat albe
		for i in range(len(self.matr)):
			for j in range(len(self.matr[0])):
				if self.matr[i][j]=='A':
					albAm+=1
		if albAm==2 and self.albCnt==0:
			return 'negru'
		ok=0
		#analog pt piese negre
		for i in self.pieseNegre:
			for j in coordonateNoduri:
				n0=coordonateNoduri.index(i)
				n1=coordonateNoduri.index(j)
				if self.prevNegru!=None:
					if i==self.prevNegru[1] and j==self.prevNegru[0]:
						continue
				if Joc.JMIN=='negru':
					if i==prev2 and j==prev1:
						continue
				if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii):
					if j not in self.pieseAlbe+self.pieseNegre:
						ok=1
						break
		if ok==0 and self.negruCnt==0:
			return 'alb'
		for i in range(len(self.matr)):
			for j in range(len(self.matr[0])):
				if self.matr[i][j]=='N':
					negAm+=1
		if negAm==2 and self.negruCnt==0:
			return 'alb'
		return False

	def mutari(self, jucator):#jucator = simbolul jucatorului care muta

		#preluam referinta pentru piesele puse pe harta de la jucatorul care muta acum
		#self.rand ne spune cate elemente avem de eliminat si ne pune in piesele necesare
		l_mutari=[]
		if (jucator=='negru' and self.rand==0) or (jucator=='alb' and self.rand!=0):
			pieseCurente=copy.deepcopy(self.pieseNegre)
		elif (jucator=='alb' and self.rand==0) or (jucator=='negru' and self.rand!=0):
			pieseCurente=copy.deepcopy(self.pieseAlbe)
		'''
		if (jucator=='negru'):
			pieseCurente=copy.deepcopy(self.pieseNegre)
		elif (jucator=='alb'):
			pieseCurente=copy.deepcopy(self.pieseAlbe)
		'''
		#elimina o piesa opusa de la jucatorul celalalt
		if self.rand!=0:
			#caz in care eliminam 2 piese si celalalt jucator are doar o piesa pe tabla
			#atunci elimina doar piesa aia si pierde dreptul de eliminat inca o piesa
			if pieseCurente==[]:
				copieself=copy.deepcopy(self)
				copieself.rand=0
				l_mutari.append(copieself)
				return l_mutari
			#verificam daca e un element care nu e in moara ca sa vedem daca putem elimina piese din mori sau nu
			for k in pieseCurente:
				n=coordonateNoduri.index(k)
				mori=0
				for i,j in enumerate(self.idxMill):
					if (j[0]==n or j[1]==n or j[2]==n) and self.freq[i]==1:
						mori+=1
				if mori==0:
					break
			for k in pieseCurente:
				if mori==0:				
					dont=0
					n1=coordonateNoduri.index(k)
					for i,j in enumerate(self.idxMill):
						if (j[0]==n1 or j[1]==n1 or j[2]==n1) and self.freq[i]==1:
							dont=-5
					if dont==-5:
						#incearca sa elimine o piesa dintr o moara, cand avem piese care nu sunt in mori
						continue
					#bucata unde eliminam la propriu piesa
					pieseNext=copy.deepcopy(pieseCurente)
					pieseNext.remove(k)
					for i in range(7):
						for j in range(7):
							if tabla_curenta.innate[i][j]==n1:
								copie_matr=copy.deepcopy(self.matr)
								copie_matr[i][j]=n1
					#adauga parametrii si in init, verifica sa adaugi in func black/white
					#si daca e la ultima eliminare
					if jucator=='alb':
						l_mutari.append(Joc(copie_matr,self.freq,self.rand-1,self.albCnt,self.negruCnt,self.pieseAlbe,pieseNext,self.millPos,self.idxMill,self.prevAlb,self.prevNegru))
					else:
						l_mutari.append(Joc(copie_matr,self.freq,self.rand-1,self.albCnt,self.negruCnt,pieseNext,self.pieseNegre,self.millPos,self.idxMill,self.prevAlb,self.prevNegru))
				else:
					#aici toate elementele sunt valide de eliminat, pt ca toate se afla in mori
					n1=coordonateNoduri.index(k)
					pieseNext=copy.deepcopy(pieseCurente)
					pieseNext.remove(k)
					for i in range(7):
						for j in range(7):
							if tabla_curenta.innate[i][j]==n1:
								copie_matr=copy.deepcopy(self.matr)
								copie_matr[i][j]=n1
					copie_freq=copy.deepcopy(self.freq)
					#verificam daca am eliminat element din moara ca sa updatam ca nu mai e moara acolo
					for i,j in enumerate(self.idxMill):
						if (j[0]==n1 or j[1]==n1 or j[2]==n1) and copie_freq[i]==1:
							copie_freq[i]=0
					#adauga parametrii si in init, verifica sa adaugi in func black/white
					#si daca e la ultima eliminare
					if jucator=='alb':
						l_mutari.append(Joc(copie_matr,copie_freq,self.rand-1,self.albCnt,self.negruCnt,self.pieseAlbe,pieseNext,self.millPos,self.idxMill,self.prevAlb,self.prevNegru))
					else:
						l_mutari.append(Joc(copie_matr,copie_freq,self.rand-1,self.albCnt,self.negruCnt,pieseNext,self.pieseNegre,self.millPos,self.idxMill,self.prevAlb,self.prevNegru))	
			return l_mutari
					#else faci ac lucru, nu mai trb verificat daca e moara
		#aici adaugam element din cele 12 pe tabla
		if (jucator=='alb' and self.albCnt!=0) or (jucator=='negru' and self.negruCnt!=0):
			for k in coordonateNoduri:
				if k not in self.pieseNegre+self.pieseAlbe:
					#punem pe fiecare loc gol cate o piesa, verificam daca am facut mori, facem o copie
					#etc
					pieseNext=copy.deepcopy(pieseCurente)
					pieseNext.append(k)
					n0=coordonateNoduri.index(k)
					copieself=copy.deepcopy(self)
					for i in range(7):
						for j in range(7):
							if copieself.matr[i][j]==n0:
								if jucator=='alb':
									copieself.matr[i][j]='A'
									copieself.albCnt-=1
									copieself.pieseAlbe=copy.deepcopy(pieseNext)
									tt=copieself.check43s(0)
								else:
									copieself.matr[i][j]='N'
									copieself.negruCnt-=1
									copieself.pieseNegre=copy.deepcopy(pieseNext)
									tt=copieself.check43s(1)
								break
					#resetam piesa anterioara de la punctul 3 din cerinta, pentru ca am facut o mutare
					if jucator=='alb':
						copieself.prevAlb=None
					else:
						copieself.prevNegru=None
					copieself.rand=tt
						#print(n0)
					#print(copieself.sirAfisare())
					l_mutari.append(copieself)
		#mutam o piesa existenta
		if (jucator=='alb' and self.albCnt!=12) or (jucator=='negru' and self.negruCnt!=12):
			for k in pieseCurente:
				for l in coordonateNoduri:
					n0=coordonateNoduri.index(k)
					n1=coordonateNoduri.index(l)
					pieseNext=copy.deepcopy(pieseCurente)
					if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii) and (l not in self.pieseAlbe+self.pieseNegre):
						pieseNext.remove(k)
						pieseNext.append(l)
						copieself=copy.deepcopy(self)
						#punem ultima mutare pentru data viitoare
						if copieself.prevAlb==None and jucator=='alb':
							copieself.prevAlb=[]
							copieself.prevAlb.append(k)
							copieself.prevAlb.append(l)
						elif copieself.prevNegru==None and jucator=='negru':
							copieself.prevNegru=[]
							copieself.prevNegru.append(k)
							copieself.prevNegru.append(l)
						#verificam daca am incercat sa mutam in pozitia anterioara de la pct3
						elif copieself.prevNegru!=None and jucator=='negru':
							if copieself.prevNegru[0]==l and copieself.prevNegru[1]==k:
								continue
						elif copieself.prevAlb!=None and jucator=='alb':
							if copieself.prevAlb[0]==l and copieself.prevAlb[1]==k:
								continue
						#reselectam noua mutare dupa ce am mutat 
						if jucator=='alb':
							copieself.prevAlb=[]
							copieself.prevAlb.append(k)
							copieself.prevAlb.append(l)
						elif jucator=='negru':
							copieself.prevNegru=[]
							copieself.prevNegru.append(k)
							copieself.prevNegru.append(l)
						#updatam daca am mutat dintr o moara
						for i,j in enumerate(self.idxMill):
							if (j[0]==n0 or j[1]==n0 or j[2]==n0) and copieself.freq[i]==1:
								copieself.freq[i]=0
						for i in range(7):
							for j in range(7):
								if self.innate[i][j]==n0:
									copieself.matr[i][j]=n0
						#punem datele noi, dupa ce am mutat o piesa existenta
						for i in range(7):
							for j in range(7):
								if copieself.matr[i][j]==n1:
									if jucator=='alb':
										copieself.matr[i][j]='A'
										copieself.pieseAlbe=pieseNext
										tt=copieself.check43s(0)
									else:
										copieself.matr[i][j]='N'
										copieself.pieseNegre=pieseNext
										tt=copieself.check43s(1)
						copieself.rand=tt
						l_mutari.append(copieself)
		#l_mutari.append(Joc(copie_matr,self.rand-1)) 
		return l_mutari
		#adauga cate o piesa, daca au mai ramas piese de pus din 12
		#append

		#muta fiecare piesa 
		#append

		#dupa fiecare ultim pas, verifica daca s au facut mori, daca da, self.rand=nr mori si 
		#intra in elimina dupa
		'''
		for i in range(self.__class__.NR_COLOANE):
			for j in range(self.__class__.NR_COLOANE):
				if self.matr[i][j]==Joc.GOL:
					copie_matr=copy.deepcopy(self.matr)
					copie_matr[i][j]=jucator
					l_mutari.append(Joc(copie_matr))
		if rand==1:
			pieseCurente=stare_curenta.tabla_curenta.pieseNegre
		else:
			pieseCurente=stare_curenta.tabla_curenta.pieseAlbe
		if nod not in stare_curenta.tabla_curenta.pieseAlbe+stare_curenta.tabla_curenta.pieseNegre:
			if nodPiesaSelectata :
				n0=coordonateNoduri.index(nod)
				n1=coordonateNoduri.index(nodPiesaSelectata)
				if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii):
					pieseCurente.remove(nodPiesaSelectata)
					pieseCurente.append(nod)
					for i,j in enumerate(tabla_curenta.idxMill):
						if (j[0]==n1 or j[1]==n1 or j[2]==n1) and stare_curenta.tabla_curenta.freq[i]==1:
							stare_curenta.tabla_curenta.freq[i]=0
					for i in range(7):
						for j in range(7):
							if tabla_curenta.innate[i][j]==n1:
								stare_curenta.tabla_curenta.matr[i][j]=n1
							elif stare_curenta.tabla_curenta.matr[i][j]==n0:
								if rand==0:
									stare_curenta.tabla_curenta.matr[i][j]='A'
								else:
									stare_curenta.tabla_curenta.matr[i][j]='N'
					tt=stare_curenta.tabla_curenta.check43s(rand)
					if tt:
						print(f"Eliminiati {tt} piesa/e")
						elimin=tt
						rand=1-rand
					else:
						rand=1-rand
						stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
						print("Muta "+ ("negru" if rand else "alb"))
					
					nodPiesaSelectata=False
			else:
				if rand==0 and stare_curenta.tabla_curenta.albCnt==0:
					continue
				if rand==1 and stare_curenta.tabla_curenta.negruCnt==0:
					continue
				pieseCurente.append(nod)
				n0=coordonateNoduri.index(nod)
				for i in range(7):
					for j in range(7):
						if stare_curenta.tabla_curenta.matr[i][j]==n0:
							if rand==0:
								stare_curenta.tabla_curenta.matr[i][j]='A'
								stare_curenta.tabla_curenta.albCnt-=1
							else:
								stare_curenta.tabla_curenta.matr[i][j]='N'
								stare_curenta.tabla_curenta.negruCnt-=1
							break
				tt=stare_curenta.tabla_curenta.check43s(rand)
				if tt:
					print(f"Eliminiati {tt} piesa/e")
					elimin=tt
					rand=1-rand
				else:
					rand=1-rand
					stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
					print("Muta "+ ("negru" if rand else "alb"))
				
		else:
			if nod in pieseCurente and elimin!=0:
				for k in pieseCurente:
					n=coordonateNoduri.index(k)
					mori=0
					for i,j in enumerate(tabla_curenta.idxMill):
						if (j[0]==n or j[1]==n or j[2]==n) and stare_curenta.tabla_curenta.freq[i]==1:
							mori+=1
					if mori==0:
						break
				if mori==0:
					n1=coordonateNoduri.index(nod)
					for i,j in enumerate(tabla_curenta.idxMill):
						if (j[0]==n1 or j[1]==n1 or j[2]==n1) and stare_curenta.tabla_curenta.freq[i]==1:
							mori=-5
				if mori==-5:
					break
				n1=coordonateNoduri.index(nod)
				pieseCurente.remove(nod)
				for i in range(7):
					for j in range(7):
						if tabla_curenta.innate[i][j]==n1:
							stare_curenta.tabla_curenta.matr[i][j]=n1
				for i,j in enumerate(tabla_curenta.idxMill):
					if (j[0]==n1 or j[1]==n1 or j[2]==n1) and stare_curenta.tabla_curenta.freq[i]==1:
						stare_curenta.tabla_curenta.freq[i]=0
				elimin-=1
				if elimin==0:
					print("Muta "+ ("negru" if rand else "alb"))
				else:
					print(f"Elimin {elimin} piese/piesa")
			elif nod in pieseCurente:	
				if nodPiesaSelectata==nod:					
					nodPiesaSelectata=False
				else:
					nodPiesaSelectata= nod
		return l_mutari
	'''

	#linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
	#practic e o linie fara simboluri ale jucatorului opus
	def linie_deschisa(self,lista, jucator):
		jo=self.jucator_opus(jucator)
		#verific daca pe linia data nu am simbolul jucatorului opus
		if not jo in lista:
				return 1
		return 0
			
	def linii_deschise(self, jucator):
		return self.linie_deschisa(self.matr[0],jucator)
		+ self.linie_deschisa(self.matr[1], jucator) 
		+ self.linie_deschisa(self.matr[2],jucator) 
		+ self.linie_deschisa([self.matr[0][0],self.matr[1][0],self.matr[2][0]],jucator)
		+ self.linie_deschisa([self.matr[0][1],self.matr[1][1],self.matr[2][1]], jucator) 
		+ self.linie_deschisa([self.matr[0][2],self.matr[1][2],self.matr[2][2]], jucator) 
		+ self.linie_deschisa([self.matr[0][0],self.matr[1][1],self.matr[2][2]], jucator) 
		+ self.linie_deschisa([self.matr[0][2],self.matr[1][1],self.matr[2][0]], jucator) 
			
		
	def estimeaza_scor(self, adancime,cul):
		"""
		:adancime - adancimea la care am ajuns
		:cul - culoarea la care ne aflam cand mutam
		prima functie de estimat scor, se calculeaza din 
		3 puncte pentru fiecare piesa de culoare pe harta
		1 punct pentru fiecare grup de 2 piese de aceeasi culoare care fac moara cu inca una
		1.5 puncte pt fiecare moara anulata de la inamic din grupuri de gen A N A
		-5 puncte daca avem grupuri de 2 piese de la inamic care vor face moara
		E important sa avem cat mai multe piese pe harta ca sa facem mai multe mutari
		Important sa avem cat mai multe posibilitati sa facem mori, de aceea 2 piese de ac cul adiacente
		o sa fie f importante pt ca o sa se orienteze dupa posibilitati duble de a face moara
		Important sa avem grija sa nu lasam inamicul sa faca mori cand e optim
		Scadem in caz ca celalalt e aproape de a face moara
		De aceea e eficient
		"""
		t_final=self.final()
		#if (adancime==0):
		if cul=='A':
			temp='alb'
		else:
			temp='negru'
		if t_final==self.__class__.JMAX and temp==self.__class__.JMAX:
			return (99+adancime)
		elif t_final==self.__class__.JMIN and temp==self.__class__.JMIN:
			return (-99-adancime)
		elif t_final=='remiza':
			return 0
		else:
			cnt=0
			for i in self.matr:
				for j in i:
					if j==cul:
						cnt+=3
			for i,k in enumerate(self.millPos):
				if self.freq[i]==0:
					a=self.matr[k[0][0]][k[0][1]]
					b=self.matr[k[1][0]][k[1][1]]
					c=self.matr[k[2][0]][k[2][1]]
					if (a=='A' and b=='A') or (a=='A' and c=='A') or (b=='A' and c=='A') and cul=='A':
						cnt+=1
					if (a=='N' and b=='N') or (a=='N' and c=='N') or (b=='N' and c=='N') and cul=='N':
						cnt+=1
			for i,k in enumerate(self.millPos):
				if self.freq[i]==0:
					a=self.matr[k[0][0]][k[0][1]]
					b=self.matr[k[1][0]][k[1][1]]
					c=self.matr[k[2][0]][k[2][1]]
					if (a=='A' and b=='A' and c=='N') or (a=='A' and c=='A' and b=='N') or (b=='A' and c=='A' and a=='N') and cul=='N':
						cnt+=1.5
					if (a=='N' and b=='N' and c=='A') or (a=='N' and c=='N' and b=='A') or (b=='N' and c=='N' and a=='A') and cul=='A':
						cnt+=1.5
			for i,k in enumerate(self.millPos):
				if self.freq[i]==0:
					a=self.matr[k[0][0]][k[0][1]]
					b=self.matr[k[1][0]][k[1][1]]
					c=self.matr[k[2][0]][k[2][1]]
					if (a=='A' and c=='A') or (b=='A' and c=='A') or (a=='A' and b=='A') and cul=='N':
						cnt-=5
					if (a=='N' and c=='N') or (b=='N' and c=='N') or (a=='N' and b=='N') and cul=='A':
						cnt-=5
			#n are rost sa adaugam si spatii goale
			return cnt
	def estimeaza_scor1(self, adancime,cul):
		"""
		argumente analog de la estimeaza_scor()
		3 puncte pt piese pe harta
		1 punct pt fiecare moara existenta
		cate 0.1 puncte pt fiecare mutare posibila de pe harta
		inutil sa verificam cate piese mai putem pune pt ca o sa se anuleze din scadere
		Strategie orientata pe format cat mai multe mori, fata de cea anterioara care se orienteaza
		pe facut cat mai multe posibilitati de mori, ambele se descurca bine, 
		dar aceasta estimare se orienteaza pe a face celalalt jucator sa ramana fara mutari
		"""
		t_final=self.final()
		#if (adancime==0):
		if cul=='A':
			temp='alb'
		else:
			temp='negru'
		if t_final==self.__class__.JMAX and temp==self.__class__.JMAX:
			return (999+adancime)
		elif t_final==self.__class__.JMIN and temp==self.__class__.JMIN:
			return (-999-adancime)
		elif t_final=='remiza':
			return 0
		else:
			cnt=0
			for i in self.matr:
				for j in i:
					if j==cul:
						cnt+=3
			for i,k in enumerate(self.millPos):
				a=self.matr[k[0][0]][k[0][1]]
				b=self.matr[k[1][0]][k[1][1]]
				c=self.matr[k[2][0]][k[2][1]]
				if a=='A' and b=='A' and c=='A' and cul=='A':
					cnt+=1
				if a=='N' and b=='N' and c=='N' and cul=='N':
					cnt+=1
			if temp=='alb':
				pieseCurente=self.pieseAlbe
			else:
				pieseCurente=self.pieseNegre
			for k in pieseCurente:
				for l in coordonateNoduri:
					n0=coordonateNoduri.index(k)
					n1=coordonateNoduri.index(l)
					if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii) and (l not in self.pieseAlbe+self.pieseNegre):
						cnt+=0.1
			return cnt

	def check43s(self,rand):
		"""
		:rand - 0 = alb, 1 = negru
		"""
		cnt=0
		for i,k in enumerate(self.millPos):
			if self.freq[i]==0:
				a=self.matr[k[0][0]][k[0][1]]
				b=self.matr[k[1][0]][k[1][1]]
				c=self.matr[k[2][0]][k[2][1]]
				#updateaza daca am facut o moara noua 
				#returneaza numarul de mori formate
				if a=='A' and b=='A' and c=='A' and rand==0:
					self.freq[i]=1
					cnt+=1
				if a=='N' and b=='N' and c=='N' and rand==1:
					self.freq[i]=1
					cnt+=1
		return cnt
	def deseneazaEcranJoc(self):
		#functie care deseneaza harta generala, din default de pe site
		ecran.fill(culoareEcran)
		for nod in coordonateNoduri:
				pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,width=0) #width=0 face un cerc plin
			
		for muchie in Graph.muchii:
			p0=coordonateNoduri[muchie[0]]
			p1=coordonateNoduri[muchie[1]]
			pygame.draw.line(surface=ecran,color=culoareLinii,start_pos=p0,end_pos=p1,width=5)
		for nod in self.pieseAlbe:
			ecran.blit(piesaAlba ,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
		for nod in self.pieseNegre:
			ecran.blit(piesaNeagra,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
		if nodPiesaSelectata:
			ecran.blit(piesaSelectata,(nodPiesaSelectata[0]-Graph.razaPiesa,nodPiesaSelectata[1]-Graph.razaPiesa))
		out=Buton(display=ecran, top=500, left=30, w=40, h=30, text="exit", culoareFundal=(155,0,55))
		out.deseneaza()
		pygame.display.update()
	def deseneazaFinal(self,winner):
		#coloreaza castigatorul
		ecran.fill(culoareEcran)
		for nod in coordonateNoduri:
				pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,width=0) #width=0 face un cerc plin
			
		for muchie in Graph.muchii:
			p0=coordonateNoduri[muchie[0]]
			p1=coordonateNoduri[muchie[1]]
			pygame.draw.line(surface=ecran,color=culoareLinii,start_pos=p0,end_pos=p1,width=5)
		for nod in self.pieseAlbe:
			ecran.blit(piesaAlba if winner=='negru' else piesaSelectata,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
		for nod in self.pieseNegre:
			ecran.blit(piesaNeagra if winner=='alb' else piesaSelectata,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
		out=Buton(display=ecran, top=500, left=30, w=40, h=30, text="exit", culoareFundal=(155,0,55))
		out.deseneaza()
		pygame.display.update()
	def sirAfisare(self):
		#afisam matricea cu np si pd ca sa fie simetric
		x=np.array(self.matr)
		rlb=[0,1,2,3,4,5,6]
		clb=[0,1,2,3,4,5,6]
		return pd.DataFrame(x,columns=clb,index=rlb)

		sir="  |"
		sir+=" ".join([str(i) for i in range(self.NR_COLOANE)])+"\n"
		sir+="-"*(self.NR_COLOANE+1)*2+"\n"
		for i in range(self.NR_COLOANE): #itereaza prin linii
			sir+= str(i)+" |"+" ".join([str(x) for x in self.matr[i]])+"\n"
		return sir

	def __str__(self):
		return self.sirAfisare()

	def __repr__(self):
		return self.sirAfisare()
pygame.init()
pygame.display.set_caption("Jarca Andrei Twelve men's morris")
culoareEcran=(255,255,255)
culoareLinii=(0,0,0)

ecran=pygame.display.set_mode(size=(700,600))

piesaAlba = pygame.image.load('piesa-alba.png')
diametruPiesa=2*Graph.razaPiesa
piesaAlba = pygame.transform.scale(piesaAlba, (diametruPiesa,diametruPiesa))
piesaNeagra = pygame.image.load('piesa-neagra.png')
piesaNeagra = pygame.transform.scale(piesaNeagra, (diametruPiesa,diametruPiesa))
piesaSelectata = pygame.image.load('piesa-rosie.png')
piesaSelectata = pygame.transform.scale(piesaSelectata, (diametruPiesa,diametruPiesa))
nodPiesaSelectata=False
coordonateNoduri=[[Graph.translatie + Graph.scalare * x for x in nod] for nod in Graph.noduri]
pieseAlbe=[]
nodPiesaSelectata=None
pieseNegre=[]

def deseneazaFinal(winner):
	#varianta initiala, inainte sa o pun in clasa
	ecran.fill(culoareEcran)
	for nod in coordonateNoduri:
			pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,width=0) #width=0 face un cerc plin
		
	for muchie in Graph.muchii:
		p0=coordonateNoduri[muchie[0]]
		p1=coordonateNoduri[muchie[1]]
		pygame.draw.line(surface=ecran,color=culoareLinii,start_pos=p0,end_pos=p1,width=5)
	for nod in pieseAlbe:
		ecran.blit(piesaAlba if winner=='negru' else piesaSelectata,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
	for nod in pieseNegre:
		ecran.blit(piesaNeagra if winner=='alb' else piesaSelectata,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
	out=Buton(display=ecran, top=500, left=30, w=40, h=30, text="exit", culoareFundal=(155,0,55))
	out.deseneaza()
	pygame.display.update()

def deseneazaEcranJoc():
	#varianta initiala inainte sa o pun in clasa
	ecran.fill(culoareEcran)
	for nod in coordonateNoduri:
			pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,width=0) #width=0 face un cerc plin
		
	for muchie in Graph.muchii:
		p0=coordonateNoduri[muchie[0]]
		p1=coordonateNoduri[muchie[1]]
		pygame.draw.line(surface=ecran,color=culoareLinii,start_pos=p0,end_pos=p1,width=5)
	for nod in pieseAlbe:
		ecran.blit(piesaAlba ,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
	for nod in pieseNegre:
		ecran.blit(piesaNeagra,(nod[0]-Graph.razaPiesa,nod[1]-Graph.razaPiesa))
	if nodPiesaSelectata:
		ecran.blit(piesaSelectata,(nodPiesaSelectata[0]-Graph.razaPiesa,nodPiesaSelectata[1]-Graph.razaPiesa))
	out=Buton(display=ecran, top=500, left=30, w=40, h=30, text="exit", culoareFundal=(155,0,55))
	out.deseneaza()
	pygame.display.update()

class Buton:
	def __init__(self, display=None, left=0, top=0, w=0, h=0,culoareFundal=(53,80,115), culoareFundalSel=(89,134,194), text="", font="arial", fontDimensiune=16, culoareText=(255,255,255), valoare=""):
		self.display=display		
		self.culoareFundal=culoareFundal
		self.culoareFundalSel=culoareFundalSel
		self.text=text
		self.font=font
		self.w=w
		self.h=h
		self.selectat=False
		self.fontDimensiune=fontDimensiune
		self.culoareText=culoareText
		#creez obiectul font
		fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
		self.textRandat=fontObj.render(self.text, True , self.culoareText) 
		self.dreptunghi=pygame.Rect(left, top, w, h) 
		#aici centram textul
		self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)
		self.valoare=valoare

	def selecteaza(self,sel):
		self.selectat=sel
		self.deseneaza()
		
	def selecteazaDupacoord(self,coord):
		if self.dreptunghi.collidepoint(coord):
			self.selecteaza(True)
			return True
		return False

	def updateDreptunghi(self):
		self.dreptunghi.left=self.left
		self.dreptunghi.top=self.top
		self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)

	def deseneaza(self):
		culoareF= self.culoareFundalSel if self.selectat else self.culoareFundal
		pygame.draw.rect(self.display, culoareF, self.dreptunghi)	
		self.display.blit(self.textRandat ,self.dreptunghiText) 

class GrupButoane:
	def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10,left=0, top=0):
		self.listaButoane=listaButoane
		self.indiceSelectat=indiceSelectat
		self.listaButoane[self.indiceSelectat].selectat=True
		self.top=top
		self.left=left
		leftCurent=self.left
		for b in self.listaButoane:
			b.top=self.top
			b.left=leftCurent
			b.updateDreptunghi()
			leftCurent+=(spatiuButoane+b.w)

	def selecteazaDupacoord(self,coord):
		for ib,b in enumerate(self.listaButoane):
			if b.selecteazaDupacoord(coord):
				self.listaButoane[self.indiceSelectat].selecteaza(False)
				self.indiceSelectat=ib
				return True
		return False

	def deseneaza(self):
		#atentie, nu face wrap
		for b in self.listaButoane:
			b.deseneaza()

	def getValoare(self):
		return self.listaButoane[self.indiceSelectat].valoare

def deseneaza_alegeri(display):
	#pus butoane initiale
	btn_alg=GrupButoane(
		top=30, 
		left=30,  
		listaButoane=[
			Buton(display=display, w=80, h=30, text="minimax", valoare="1"), 
			Buton(display=display, w=80, h=30, text="alphabeta", valoare="2")
			],
		indiceSelectat=1)
	btn_juc=GrupButoane(
		top=100, 
		left=30, 
		listaButoane=[
			Buton(display=display, w=35, h=30, text="alb", valoare="alb"),
			Buton(display=display, w=50, h=30, text="negru", valoare="negru")
			], 
		indiceSelectat=0)
	btn_dif=GrupButoane(
		top=170, 
		left=30, 
		listaButoane=[
			Buton(display=display, w=80, h=30, text="incepator", valoare="incepator"), 
			Buton(display=display, w=80, h=30, text="mediu", valoare="mediu"), 
			Buton(display=display, w=80, h=30, text="avansat", valoare="avansat")
			], 
		indiceSelectat=0)
	btn_heur=GrupButoane(
		top=240, 
		left=30, 
		listaButoane=[
			Buton(display=display, w=80, h=30, text="calc1", valoare=0), 
			Buton(display=display, w=80, h=30, text="calc2", valoare=1), 
			], 
		indiceSelectat=0)
	ok=Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155,0,55))
	btn_alg.deseneaza()
	btn_juc.deseneaza()
	btn_dif.deseneaza()
	btn_heur.deseneaza()
	ok.deseneaza()
	while True:
		for ev in pygame.event.get(): 
			if ev.type== pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif ev.type == pygame.MOUSEBUTTONDOWN: 
				pos = pygame.mouse.get_pos()
				if not btn_alg.selecteazaDupacoord(pos):
					if not btn_juc.selecteazaDupacoord(pos):
						if not btn_dif.selecteazaDupacoord(pos):
							if not btn_heur.selecteazaDupacoord(pos):
								if ok.selecteazaDupacoord(pos):
									display.fill((0,0,0)) #stergere ecran 
									deseneazaEcranJoc()
									return btn_juc.getValoare(), btn_alg.getValoare(), btn_dif.getValoare(), btn_heur.getValoare()
		pygame.display.update()

class Stare:
	"""
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
	"""
	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
		self.tabla_curenta=tabla_joc
		self.j_curent=j_curent
		
		#adancimea in arborele de stari
		self.adancime=adancime	
		
		#estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
		self.estimare=estimare
		
		#lista de mutari posibile din starea curenta
		self.mutari_posibile=[]
		
		#cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa=None


	def mutari(self):	
		l_mutari=self.tabla_curenta.mutari(self.j_curent)
		l_stari_mutari=[]
		for i in l_mutari:
			if i.rand==0:
				juc_opus=Joc.jucator_opus(self.j_curent)
			else:
				#daca urmeaza sa eliminam piese, nu schimbam jucatorul, ca sa putem elimina piese
				juc_opus=self.j_curent
			l_stari_mutari.append(Stare(i,juc_opus,self.adancime-1,parinte=self))
		'''
		for i in l_mutari:
			juc_opus=Joc.jucator_opus(self.j_curent)
			l_stari_mutari.append(Stare(i,juc_opus,self.adancime-1,parinte=self))
		'''
		#verificat rand in fiecare l_mutari
		return l_stari_mutari
		
	
	def __str__(self):
		sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
		return sir


def min_max(stare,calc):	
	"""
	:calc este ce estimare folosim
	"""
	if stare.adancime==0 or stare.tabla_curenta.final() :
		#scadem scorul jucatorului negru cu cel alb si invers pentru ce caz avem
		if Joc.JMAX=='negru':
			if calc==0:
				stare.estimare=stare.tabla_curenta.estimeaza_scor(stare.adancime,'N')-stare.tabla_curenta.estimeaza_scor(stare.adancime,'A')
			else:
				stare.estimare=stare.tabla_curenta.estimeaza_scor1(stare.adancime,'N')-stare.tabla_curenta.estimeaza_scor1(stare.adancime,'A')
		else:
			if calc==0:
				stare.estimare=stare.tabla_curenta.estimeaza_scor(stare.adancime,'A')-stare.tabla_curenta.estimeaza_scor(stare.adancime,'N')
			else:
				stare.estimare=stare.tabla_curenta.estimeaza_scor1(stare.adancime,'A')-stare.tabla_curenta.estimeaza_scor1(stare.adancime,'N')
		return stare
	#calculez toate mutarile posibile din starea curenta
	stare.mutari_posibile=stare.mutari()
	#aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
	mutariCuEstimare=[min_max(mutare, calc) for mutare in stare.mutari_posibile]
	#adun cate noduri avem in total
	try:
		nod_[nr_calc]+=len(mutariCuEstimare)
	except:
		nod_.append(0)
		nod_[nr_calc]+=len(mutariCuEstimare)
	if stare.j_curent==Joc.JMAX :
		#daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
		stare.stare_aleasa=max(mutariCuEstimare, key=lambda x: x.estimare)
	else:
		#daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
		stare.stare_aleasa=min(mutariCuEstimare, key=lambda x: x.estimare)
	stare.estimare=stare.stare_aleasa.estimare
	return stare
def alpha_beta(alpha, beta, stare, calc):
	#analog cu minmax
	if stare.adancime==0 or stare.tabla_curenta.final() :
		if Joc.JMAX=='negru':
			if calc==0:
				stare.estimare=stare.tabla_curenta.estimeaza_scor(stare.adancime,'N')-stare.tabla_curenta.estimeaza_scor(stare.adancime,'A')
			else:
				stare.estimare=stare.tabla_curenta.estimeaza_scor1(stare.adancime,'N')-stare.tabla_curenta.estimeaza_scor1(stare.adancime,'A')
		else:
			if calc==0:
				stare.estimare=stare.tabla_curenta.estimeaza_scor(stare.adancime,'A')-stare.tabla_curenta.estimeaza_scor(stare.adancime,'N')
			else:
				stare.estimare=stare.tabla_curenta.estimeaza_scor1(stare.adancime,'A')-stare.tabla_curenta.estimeaza_scor1(stare.adancime,'N')
		return stare
	if alpha>beta:
		return stare #este intr-un interval invalid deci nu o mai procesez
	
	stare.mutari_posibile=stare.mutari()
		

	if stare.j_curent==Joc.JMAX :
		estimare_curenta=float('-inf')
		#sortez dupa scor pentru cerinta bonus
		if Joc.JMAX=='negru':
			if calc==0:
				stare.mutari_posibile.sort(key=lambda x:x.tabla_curenta.estimeaza_scor(stare.adancime,'N')-x.tabla_curenta.estimeaza_scor(stare.adancime,'A'),reverse=True)
			else:
				stare.mutari_posibile.sort(key=lambda x:x.tabla_curenta.estimeaza_scor1(stare.adancime,'N')-x.tabla_curenta.estimeaza_scor1(stare.adancime,'A'),reverse=True)
		else:
			if calc==0:
				stare.mutari_posibile.sort(key=lambda x:x.tabla_curenta.estimeaza_scor(stare.adancime,'A')-x.tabla_curenta.estimeaza_scor(stare.adancime,'N'),reverse=True)
			else:
				stare.mutari_posibile.sort(key=lambda x:x.tabla_curenta.estimeaza_scor1(stare.adancime,'A')-x.tabla_curenta.estimeaza_scor1(stare.adancime,'N'),reverse=True)
		for mutare in stare.mutari_posibile:
			#calculeaza estimarea pentru starea noua, realizand subarborele
			stare_noua=alpha_beta(alpha, beta, mutare, calc)
			try:#adun aici si mai jos numarul de noduri
				nod_[nr_calc]+=1
			except:
				nod_.append(0)
				nod_[nr_calc]+=1
			if (estimare_curenta<stare_noua.estimare):
				stare.stare_aleasa=stare_noua
				estimare_curenta=stare_noua.estimare
			if(alpha<stare_noua.estimare):
				alpha=stare_noua.estimare
				if alpha>=beta:
					break

	elif stare.j_curent==Joc.JMIN :
		estimare_curenta=float('inf')
		
		for mutare in stare.mutari_posibile:
			
			stare_noua=alpha_beta(alpha, beta, mutare, calc)
			try:
				nod_[nr_calc]+=1
			except:
				nod_.append(0)
				nod_[nr_calc]+=1
			if (estimare_curenta>stare_noua.estimare):
				stare.stare_aleasa=stare_noua
				estimare_curenta=stare_noua.estimare

			if(beta>stare_noua.estimare):
				beta=stare_noua.estimare
				if alpha>=beta:
					break
	stare.estimare=stare.stare_aleasa.estimare

	return stare
rand, tip_algoritm, dificultate, calc = deseneaza_alegeri(ecran) #ecran initial cu optiuni
if rand=='alb':
	rand=0
	Joc.JMIN='alb'
else:
	rand=1
	Joc.JMIN='negru'
Joc.JMAX= 'alb' if Joc.JMIN == 'negru' else 'negru'
print(Joc.JMAX)
print(tip_algoritm,dificultate)
tabla_curenta=Joc()
print(tabla_curenta.matr)
print(tabla_curenta.millPos)
print("Tabla initiala")
print(tabla_curenta.sirAfisare())
deseneazaEcranJoc()
out=Buton(display=ecran, top=500, left=30, w=40, h=30, text="exit", culoareFundal=(155,0,55))
#albCnt=12
#negruCnt=12
elimin=0
fin=0
print("Muta "+ ("negru" if rand else "alb"))
if dificultate=='incepator':
	ADANCIME_MAX=1
elif dificultate=='mediu':
	ADANCIME_MAX=2
else:
	ADANCIME_MAX=3
if rand==0:
	stare_curenta=Stare(tabla_curenta,'alb',ADANCIME_MAX)
else:
	stare_curenta=Stare(tabla_curenta,'negru',ADANCIME_MAX)
prev_move=None
prev_piece=None
#afisari si comentarii
t_min=99999
t_max=-99999
t_sum=0
t_juc_inainte=int(round(time.time() * 1000))
nr_calc=0
nr_juc=0
med=[]
t_total=int(round(time.time() * 1000))
nod_=[]
while True:
	if (stare_curenta.j_curent==Joc.JMIN):
		#verific daca incerc sa elimin 2 piese si celalalt are doar 1 piesa pe tabla
		if rand==1:
			piesa=piesaNeagra
			pieseCurente=stare_curenta.tabla_curenta.pieseNegre
			if pieseCurente==[] and elimin!=0:
				elimin=0
				stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
				continue
		else:
			piesa=piesaAlba
			pieseCurente=stare_curenta.tabla_curenta.pieseAlbe
			if pieseCurente==[] and elimin!=0:
				elimin=0
				stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
				continue
		for ev in pygame.event.get(): 
			if ev.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if ev.type == pygame.MOUSEBUTTONDOWN: 
				pos = pygame.mouse.get_pos()
				if out.selecteazaDupacoord(pos):
					#cand apas pe exit, pt penultima cerinta
					print(f"Timpul min,max,mediu,median:{t_min},{t_max},{t_sum//nr_calc},{statistics.median(med)}")
					print(f"Timp total este {int(round(time.time() * 1000)) - t_total}")
					print(f"Noduri generate min,max,mediu,median:{min(nod_)},{max(nod_)},{sum(nod_)//nr_calc},{statistics.median(nod_)}")
					print(f"Nr mutari calc, jucator: {nr_calc}, {nr_juc}")
					exit()
				if fin==0:
					for nod in coordonateNoduri:
						if distEuclid(pos,nod)<=Graph.razaPct:
							#selectez nodurile din care o sa fac operatii
							if rand==1:
								piesa=piesaNeagra
								pieseCurente=stare_curenta.tabla_curenta.pieseNegre
								if nod not in pieseCurente and elimin!=0:
									#ce zice in print
									print('Nod selectat nu exista sau e de alta culoare')
									continue
							else:
								piesa=piesaAlba
								pieseCurente=stare_curenta.tabla_curenta.pieseAlbe
								if nod not in pieseCurente and elimin!=0:
									print('Nod selectat nu exista sau e de alta culoare')
									continue
							#aici mut o piesa
							if nod not in stare_curenta.tabla_curenta.pieseAlbe+stare_curenta.tabla_curenta.pieseNegre:
								if nodPiesaSelectata :
									n0=coordonateNoduri.index(nod)
									n1=coordonateNoduri.index(nodPiesaSelectata)
									if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii):
										#caz sa nu pot muta in loc anterior
										if prev_move==None:
											prev_move=nodPiesaSelectata
											prev_piece=nod
										elif prev_move==nod and prev_piece==nodPiesaSelectata:
											print("Nu puteti muta in pozitia imediat anterioara")
											continue
										prev_move=nodPiesaSelectata
										prev_piece=nod
										#trb si sa fie aceeasi piesa inreg
										pieseCurente.remove(nodPiesaSelectata)
										pieseCurente.append(nod)
										#scot moara daca e cazul de la piesa pe care abia am mutat o
										for i,j in enumerate(tabla_curenta.idxMill):
											if (j[0]==n1 or j[1]==n1 or j[2]==n1) and stare_curenta.tabla_curenta.freq[i]==1:
												stare_curenta.tabla_curenta.freq[i]=0
										#update in matrice
										for i in range(7):
											for j in range(7):
												if tabla_curenta.innate[i][j]==n1:
													stare_curenta.tabla_curenta.matr[i][j]=n1
												elif stare_curenta.tabla_curenta.matr[i][j]==n0:
													if rand==0:
														stare_curenta.tabla_curenta.matr[i][j]='A'
													else:
														stare_curenta.tabla_curenta.matr[i][j]='N'
										
										print(stare_curenta.tabla_curenta.sirAfisare())
										q=stare_curenta.tabla_curenta.final(prev_move,prev_piece)
										#verific stare finala
										nr_juc+=1 #numar de mutari
										if q=='draw':
											print("It's a draw")
											stare_curenta.tabla_curenta.deseneazaFinal(q)
											fin=1
										elif q=='alb':
											print("Alb a castigat")
											fin=1
											stare_curenta.tabla_curenta.deseneazaFinal(q)
										elif q=='negru':
											print("Negru a castigat")
											fin=1
											stare_curenta.tabla_curenta.deseneazaFinal(q)
										if fin==0:
											tt=stare_curenta.tabla_curenta.check43s(rand)
											if tt:
												print(f"Eliminiati {tt} piesa/e")
												elimin=tt
												rand=1-rand
											else:
												rand=1-rand
												stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
												print("Muta "+ ("negru" if rand else "alb"))
											
											nodPiesaSelectata=False
								else:
									#adaug o piesa pe tabla daca mai avem piese
									if rand==0 and stare_curenta.tabla_curenta.albCnt==0:
										continue
									if rand==1 and stare_curenta.tabla_curenta.negruCnt==0:
										continue
									prev_move=None
									prev_piece=None
									pieseCurente.append(nod)
									n0=coordonateNoduri.index(nod)
									for i in range(7):
										for j in range(7):
											if stare_curenta.tabla_curenta.matr[i][j]==n0:
												if rand==0:
													stare_curenta.tabla_curenta.matr[i][j]='A'
													stare_curenta.tabla_curenta.albCnt-=1
												else:
													stare_curenta.tabla_curenta.matr[i][j]='N'
													stare_curenta.tabla_curenta.negruCnt-=1
												break
									#adaugat piesa
									print(stare_curenta.tabla_curenta.sirAfisare())
									q=stare_curenta.tabla_curenta.final()
									nr_juc+=1
									if q=='draw':
										print("It's a draw")
										stare_curenta.tabla_curenta.deseneazaFinal(q)
										fin=1
									elif q=='alb':
										print("Alb a castigat")
										fin=1
										stare_curenta.tabla_curenta.deseneazaFinal(q)
									elif q=='negru':
										print("Negru a castigat")
										fin=1
										stare_curenta.tabla_curenta.deseneazaFinal(q)
									if fin==0:
										tt=stare_curenta.tabla_curenta.check43s(rand)
										if tt:
											print(f"Eliminiati {tt} piesa/e")
											elimin=tt
											rand=1-rand
										else:
											rand=1-rand
											stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
											print("Muta "+ ("negru" if rand else "alb"))
									
							else:
								#scot o piesa din totalul elimin
								if nod in pieseCurente and elimin!=0:
									for k in pieseCurente:
										n=coordonateNoduri.index(k)
										mori=0
										for i,j in enumerate(tabla_curenta.idxMill):
											if (j[0]==n or j[1]==n or j[2]==n) and stare_curenta.tabla_curenta.freq[i]==1:
												mori+=1
										if mori==0:
											break
									#verific daca exista piese care nu sunt in mori la inamic
									if mori==0:
										n1=coordonateNoduri.index(nod)
										for i,j in enumerate(tabla_curenta.idxMill):
											if (j[0]==n1 or j[1]==n1 or j[2]==n1) and stare_curenta.tabla_curenta.freq[i]==1:
												mori=-5
									#daca da, nu putem elimina piese din mori
									if mori==-5:
										print('Nu puteti elimina nod dintr-o moara momentan')
										break
									n1=coordonateNoduri.index(nod)
									pieseCurente.remove(nod)
									nr_juc+=1
									for i in range(7):
										for j in range(7):
											if tabla_curenta.innate[i][j]==n1:
												stare_curenta.tabla_curenta.matr[i][j]=n1
									#analog ca mai sus
									for i,j in enumerate(tabla_curenta.idxMill):
										if (j[0]==n1 or j[1]==n1 or j[2]==n1) and stare_curenta.tabla_curenta.freq[i]==1:
											stare_curenta.tabla_curenta.freq[i]=0
									elimin-=1
									print(stare_curenta.tabla_curenta.sirAfisare())
									q=stare_curenta.tabla_curenta.final()
									if q=='draw':
										print("It's a draw")
										stare_curenta.tabla_curenta.deseneazaFinal(q)
										fin=1
									elif q=='alb':
										print("Alb a castigat")
										fin=1
										stare_curenta.tabla_curenta.deseneazaFinal(q)
									elif q=='negru':
										print("Negru a castigat")
										fin=1
										stare_curenta.tabla_curenta.deseneazaFinal(q)
									if fin==0:
										if elimin==0:
											print("Muta "+ ("negru" if rand else "alb"))											
											stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
										else:
											print(f"Elimin {elimin} piese/piesa")
								elif nod in pieseCurente:	
									if nodPiesaSelectata==nod:					
										nodPiesaSelectata=False
									else:
										nodPiesaSelectata= nod
							t_juc_dupa=int(round(time.time() * 1000))
							print("Jucatorul a \"gandit\" timp de "+str(t_juc_dupa-t_juc_inainte)+" milisecunde.")
							if fin==0:
								stare_curenta.tabla_curenta.deseneazaEcranJoc()
								break
				else:
					#la final
					print(f"Timpul min,max,mediu,median:{t_min},{t_max},{t_sum//nr_calc},{statistics.median(med)}")
					print(f"Timp total este {int(round(time.time() * 1000)) - t_total}")
					print(f"Noduri generate min,max,mediu,median:{min(nod_)},{max(nod_)},{sum(nod_)//nr_calc},{statistics.median(nod_)}")
					print(f"Nr mutari calc, jucator: {nr_calc}, {nr_juc}")
	else:
		#actualizez culoarea pt jucator real
		rand=1-rand

		t_inainte=int(round(time.time() * 1000))
		if tip_algoritm=='1':
			stare_actualizata=min_max(stare_curenta,calc)
		else: #tip_algoritm==2
			stare_actualizata=alpha_beta(-500, 500, stare_curenta,calc)
		stare_curenta.tabla_curenta=stare_actualizata.stare_aleasa.tabla_curenta
		print("Tabla dupa mutarea calculatorului")
		print(stare_curenta.tabla_curenta.sirAfisare())
		
		
		stare_curenta.tabla_curenta.deseneazaEcranJoc()
		#preiau timpul in milisecunde de dupa mutare
		t_dupa=int(round(time.time() * 1000))
		print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
		print(f"Estimarea calculatorului a fost {stare_actualizata.estimare}")
		print(f"Calculatorul a generat {nod_[nr_calc]}noduri")
		if t_dupa-t_inainte < t_min:
			t_min=t_dupa-t_inainte
		if t_dupa-t_inainte > t_max:
			t_max=t_dupa-t_inainte
		t_sum+=t_dupa-t_inainte
		#timpii, nodurile, mediana
		nr_calc+=1
		t_juc_inainte=int(round(time.time() * 1000))
		med.append(t_dupa-t_inainte)
		q=stare_curenta.tabla_curenta.final()
		if q=='draw':
			print("It's a draw")
			stare_curenta.tabla_curenta.deseneazaFinal(q)
			fin=1
		elif q=='alb':
			print("Alb a castigat")
			fin=1
			stare_curenta.tabla_curenta.deseneazaFinal(q)
		elif q=='negru':
			print("Negru a castigat")
			fin=1
			stare_curenta.tabla_curenta.deseneazaFinal(q)
			
		#S-a realizat o mutare. Schimb jucatorul cu cel opus
		if stare_curenta.tabla_curenta.rand==0:
			#daca nu fac o eliminare
			stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
			if fin!=1:
				print("Muta "+ ("negru" if rand else "alb"))
		else:
			#elimin stare_curenta.tabla_curenta.rand piese
			rand=1-rand
			print(f"Elimina {stare_curenta.tabla_curenta.rand} piese")
		if fin==1:
			#la final afisez toate chestiile
			print(f"Timpul min,max,mediu,median:{t_min},{t_max},{t_sum//nr_calc},{statistics.median(med)}")
			print(f"Timp total este {int(round(time.time() * 1000)) - t_total}")
			print(f"Noduri generate min,max,mediu,median:{min(nod_)},{max(nod_)},{sum(nod_)//nr_calc},{statistics.median(nod_)}")
			print(f"Nr mutari calc, jucator: {nr_calc}, {nr_juc}")
			while True:
				#astept sa ies din program
				for ev in pygame.event.get(): 
					if ev.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if ev.type == pygame.MOUSEBUTTONDOWN: 
						pos = pygame.mouse.get_pos()
						if out.selecteazaDupacoord(pos):
							exit()



"""
while True:	
	for ev in pygame.event.get(): 
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if ev.type == pygame.MOUSEBUTTONDOWN: 
			pos = pygame.mouse.get_pos()
			if out.selecteazaDupacoord(pos):
				exit()
			if fin==0:
				for nod in coordonateNoduri:
					if distEuclid(pos,nod)<=Graph.razaPct:
						if rand==1:
							piesa=piesaNeagra
							pieseCurente=pieseNegre
							if nod not in pieseCurente and elimin!=0:
								continue
						else:
							piesa=piesaAlba
							pieseCurente=pieseAlbe
							if nod not in pieseCurente and elimin!=0:
								continue
						if nod not in pieseAlbe+pieseNegre:
							if nodPiesaSelectata :
								n0=coordonateNoduri.index(nod)
								n1=coordonateNoduri.index(nodPiesaSelectata)
								if ((n0,n1) in Graph.muchii or (n1,n0) in Graph.muchii):
									pieseCurente.remove(nodPiesaSelectata)
									pieseCurente.append(nod)
									for i,j in enumerate(tabla_curenta.idxMill):
										if (j[0]==n1 or j[1]==n1 or j[2]==n1) and tabla_curenta.freq[i]==1:
											tabla_curenta.freq[i]=0
									for i in range(7):
										for j in range(7):
											if tabla_curenta.innate[i][j]==n1:
												tabla_curenta.matr[i][j]=n1
											elif tabla_curenta.matr[i][j]==n0:
												if rand==0:
													tabla_curenta.matr[i][j]='A'
												else:
													tabla_curenta.matr[i][j]='N'
									
									print(tabla_curenta.sirAfisare())
									q=tabla_curenta.final()
									if q=='draw':
										print("It's a draw")
										exit()
									elif q=='alb':
										print("Alb a castigat")
										fin=1
										deseneazaFinal(q)
									elif q=='negru':
										print("Negru a castigat")
										fin=1
										deseneazaFinal(q)
									if fin==0:
										tt=tabla_curenta.check43s(rand)
										if tt:
											print(f"Eliminiati {tt} piesa/e")
											elimin=tt
											rand=1-rand #aici nu schimb in jmax
										else:
											rand=1-rand
											print("Muta "+ ("negru" if rand else "alb"))
										
										nodPiesaSelectata=False
							else:
								if rand==0 and albCnt==0:
									continue
								if rand==1 and negruCnt==0:
									continue
								pieseCurente.append(nod)
								n0=coordonateNoduri.index(nod)
								for i in range(7):
									for j in range(7):
										if tabla_curenta.matr[i][j]==n0:
											if rand==0:
												tabla_curenta.matr[i][j]='A'
												albCnt-=1
											else:
												tabla_curenta.matr[i][j]='N'
												negruCnt-=1
											break
								
								print(tabla_curenta.sirAfisare())
								q=tabla_curenta.final()
								if q=='draw':
									print("It's a draw")
									exit()
								elif q=='alb':
									print("Alb a castigat")
									fin=1
									deseneazaFinal(q)
								elif q=='negru':
									print("Negru a castigat")
									fin=1
									deseneazaFinal(q)
								if fin==0:
									tt=tabla_curenta.check43s(rand)
									if tt:
										print(f"Eliminiati {tt} piesa/e")
										elimin=tt
										rand=1-rand
									else:
										rand=1-rand
										print("Muta "+ ("negru" if rand else "alb"))
								
						else:
							if nod in pieseCurente and elimin!=0:
								for k in pieseCurente:
									n=coordonateNoduri.index(k)
									mori=0
									for i,j in enumerate(tabla_curenta.idxMill):
										if (j[0]==n or j[1]==n or j[2]==n) and tabla_curenta.freq[i]==1:
											mori+=1
									if mori==0:
										break
								if mori==0:
									n1=coordonateNoduri.index(nod)
									for i,j in enumerate(tabla_curenta.idxMill):
										if (j[0]==n1 or j[1]==n1 or j[2]==n1) and tabla_curenta.freq[i]==1:
											mori=-5
								if mori==-5:
									break
								n1=coordonateNoduri.index(nod)
								pieseCurente.remove(nod)
								for i in range(7):
									for j in range(7):
										if tabla_curenta.innate[i][j]==n1:
											tabla_curenta.matr[i][j]=n1
								for i,j in enumerate(tabla_curenta.idxMill):
									if (j[0]==n1 or j[1]==n1 or j[2]==n1) and tabla_curenta.freq[i]==1:
										tabla_curenta.freq[i]=0
								elimin-=1
								print(tabla_curenta.sirAfisare())
								q=tabla_curenta.final()
								if q=='draw':
									print("It's a draw")
									exit()
								elif q=='alb':
									print("Alb a castigat")
									fin=1
									deseneazaFinal(q)
								elif q=='negru':
									print("Negru a castigat")
									fin=1
									deseneazaFinal(q)
								if fin==0:
									if elimin==0:
										print("Muta "+ ("negru" if rand else "alb"))
									else:
										print(f"Elimin {elimin} piese/piesa")
							elif nod in pieseCurente:	
								if nodPiesaSelectata==nod:					
									nodPiesaSelectata=False
								else:
									nodPiesaSelectata= nod
						if fin==0:
							deseneazaEcranJoc()
							break
"""