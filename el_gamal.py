import array
import math
import time
import sys
from random import randint

class point:
    def __init__(self,x,y):
        self.x_intercept = x
        self.y_intercept = y

class elliptic_curve:
    def __init__(self,param_a,param_b,f):
        self.a = param_a
        self.b = param_b
        self.field = f
        
def print_elliptic_curve(t):
    print "y^2 = x^3 +" , t.a , "x + " , t.b

def print_point(a):
    print "(" , a.x_intercept , " , " , a.y_intercept , ")"

def sec_sq(base,exp,mod):

	Q = base
	R = 1
	
	while exp > 0:
		if exp % 2 == 1:
			R = (Q*R) % mod
			exp = exp - 1
			
		Q = (Q*Q) % mod
		exp = exp/2
	
	return R
        
def find_inverse(number,mod):

    mult = []
    rem = []

    num = number
    m = mod
    if number % mod == 0:
    		if number > mod:
			return -mod
		else:
			return - number
    elif number == 1:
		return 1
		
    else:
		if number < mod:
	    		c = mod
	    		mod = number
	    		number = c
	
	
		q = int(math.floor(number/mod))
		r = number%mod
		rem.append(number)
		rem.append(mod)
		c = r

		while r != 0:
		    mult.append(q)
		    rem.append(r)

		    c = r
		    number = mod
		    mod = r
		       
		    r = number%mod
		    q = int(math.floor(number/mod))

		if c != 1 and c != -1:
			return -c
		else:
			if len(mult) == 1:
				s = -mult[0]
				t = -mult[0]
			else:
				s = (-mult[len(mult)-1])*(-mult[len(mult)-2])+1
				t = -mult[len(mult)-1]

			for i in range(len(mult)-2,0,-1):
				temp = t
				t = s
				s = temp + s * - mult[i-1]
	
			if num > m:
				if t < 0:
					return t + m
				else:
					return t
			else:
				if s < 0:
					return s + m
				else:
					return s
					
def add_points(a,b,c):
    
    if a.x_intercept == 0 and a.y_intercept == 0:
    		return b
    elif b.x_intercept == 0 and b.y_intercept == 0:
    		return a
    else:
		if a == b:
			numer = 3*a.x_intercept*a.x_intercept + c.a
			denom = 2*a.y_intercept
				
			if denom < 0:
				denom = c.field + denom
			if numer < 0:
				numer = c.field + numer
		
		  	m = ((numer)*(find_inverse(denom,c.field))) % c.field
		   	
			tempx = (m*m - a.x_intercept - b.x_intercept) % c.field
			tempy = (m*(a.x_intercept - tempx) - a.y_intercept) % c.field
			
			if tempx < 0:
					tempx = c.field + tempx
					
			if tempy < 0:
					tempy = c.field + tempy
			
			temp = point(tempx,tempy)
			return temp

		elif a.x_intercept == b.x_intercept:
				temp = point(0,0)
				return temp
		else:
			numer = b.y_intercept - a.y_intercept
			denom = b.x_intercept - a.x_intercept
				
			if denom < 0:
				denom = c.field + denom
			if numer < 0:
				numer = c.field + numer

			m = ((numer)*(find_inverse(denom,c.field))) % c.field
		
			tempx = (m*m - a.x_intercept - b.x_intercept) % c.field
			tempy = (m*(a.x_intercept - tempx) - a.y_intercept) % c.field 	
			
			if tempx < 0:
					tempx = c.field + tempx
					
			if tempy < 0:
					tempy = c.field + tempy
			
			temp = point(tempx,tempy)
	  		return temp
		  		
def gcd(number, mod):
	if number == 0 or mod == 0:
		return 0
	elif number % mod == 0:
		if number > mod:
	   		return mod
   		else:
   			return number 
	elif number == 1:
		return 1
	else:
		if number < mod:
	    		c = mod
	    		mod = number
	    		number = c
	
		r = number%mod

		while r != 0:
		    c = r
		    number = mod
		    mod = r
		       
		    r = number%mod
	    
		return c

def jacobi(top,bottem):
	ans = 0
	sign = 1
	while ans != 1 or ans != -1:
		if gcd(top,bottem) != 1:
			return 0
		elif gcd(top,bottem) == 1 and top > bottem:
			top = top % bottem
		elif top == -1:
			return sign*int(pow(-1,(bottem-1)/2))
		elif top == 2:
			if bottem%8 == 1 or bottem%8 == 7:
				return sign*1
			elif bottem%8 == 3 or bottem%8 == 5:
				return sign*-1
		elif top%2 == 1 and gcd(bottem,top) == 1:
			if bottem%4 == 3 and top%4 == 3:
				temp = bottem
				bottem = top
				top = temp
				sign = -1*sign
			else:
				temp = bottem
				bottem = top
				top = temp
				sign = 1*sign
		elif top%2 == 0 and gcd(top,bottem) == 1:
			while top%2 == 0:
				if top == 2:
					if bottem%8 == 1 or bottem%8 == 7:
						return sign*1
					elif bottem%8 == 3 or bottem%8 == 5:
						return sign*-1
				if bottem%8 == 1 or bottem%8 == 7:
					sign = sign*1
					top = top/2
				elif bottem%8 == 3 or bottem%8 == 5:
					sign = sign*-1
					top = top/2

def subtract_points(a,b,c):
	tem = -b.y_intercept 
	temp = point(b.x_intercept, tem)
	ans = add_points(a,temp,c)
	return ans;

def double_add(a, n, t): 
	Q = a
	R = point(0,0)
	
	while n > 0:
		if n % 2 == 1:
			R = add_points(R,Q,t)
			n = n - 1
		Q = add_points(Q,Q,t)
		n = n/2

	return R

def generate_curve(p,a,field):
	
	b = ((p.y_intercept*p.y_intercept) - (p.x_intercept*p.x_intercept*p.x_intercept) - a*p.x_intercept)%field
	
	t = elliptic_curve(a,b,field)
	
	return t
	
def el_gamal_encrypt(E,n,P,Q,K,m):

	n = str(n)
	if len(m) > (len(n)/2)-1:
		print "message is to long!"
		exit(-1)
	
	n = int(n)
	
	let = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ",".",",","!","?",":",";","0","1","2","3","4","5","6","7","8","9","10"]
	num = ["01","02","03","04","05","06","07","08","09", "10", "11", "12","13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66","67", "68", "69", "70"]


	for t in range(0,len(let)):
		if m[0] == let[t]:
			enc = num[t]
			
	for i in range(1, len(m)):
		for j in range(0,len(let)):
			if let[j] == m[i]:
				enc = enc + num[j]
			
	enc = int(enc)
	enc = enc%E.field
	
	if enc*K + K > (n-1):
			print "out of bounds"
			exit(-1)
	
	for j in range (0, K):
		tempx = enc*K + j
		y_temp = int(tempx*tempx*tempx + (E.a*tempx) + E.b)
		y_temp = y_temp % n
		if jacobi(y_temp,n) == 1:
			break

	if n%4 == 3:
		a = (n+1)/4
		y_temp = sec_sq(y_temp,a,n)
	else:
		print "need 3 (mod 4) prime"
		exit(-1)
	
	tem = point(tempx,y_temp)
	
	print "message point"
	print_point(tem)
	
	r = 331
	
	temp_P = double_add(P,r,E)
	
	temp_R = double_add(Q,r,E)
	
	print "Q 'double' by random r"
	print_point(temp_R)
	
	temp_Q = add_points(temp_R,tem,E)
	
	print "generated points"
	print "rP"
	print_point(temp_P)
	print "rQ + m"
	print_point(temp_Q)
	
	points = []

	points.append(temp_P)
	
	points.append(temp_Q)	
	
	return points


def el_gamal_decrypt(E,n,Pe,Qe,K):

	let = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ",".",",","!","?",":",";","0","1","2","3","4","5","6","7","8","9","10"]
	num = ["01","02","03","04","05","06","07","08","09", "10", "11", "12","13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66","67", "68", "69", "70"]

	print "recieved points"
	print_point(Pe)
	print_point(Qe)

	tempP = double_add(Pe,n,E)
	
	print "nrP"
	print_point(tempP)
	
	mes = subtract_points(Qe,tempP,E)
	
	print "Recieved message point"
	print_point(mes)

	message = mes.x_intercept/K
	message = str(message)
	
	c = message[0]
	c = int(c)
	
	if len(message)%2 == 1:
		message = "0" + message
	
	for t in range(0,len(num)):
		if num[t] == (message[0] + message[1]):
			ans = let[t]
	
	for i in range(2,len(message)-1,2):
		temp = message[i] + message[i+1]
		for j in range(0,len(num)):
			if num[j] == temp:
				ans = ans + let[j]
				
	print "decrypted message: " , ans
		
	
		
pr = 2367495770217142995264827948666809233066409497699870112003149352380375124855230068487109373226251983
P = point(31,51)
E = generate_curve(P,113,pr)
secret_n = 1266
Q = double_add(P,secret_n,E)
K = 100
print "****public info****"
print "Elliptic curve E: " 
print_elliptic_curve(E)
print "point P: " 
print_point(P)
print "point Q: " 
print_point(Q)
print "prime r: " 
print pr
m = raw_input("enter message:	 ")
pon = el_gamal_encrypt(E,pr,P,Q,K,m)

Pons = pon[0]
Pont = pon[1]

el_gamal_decrypt(E,secret_n,Pons,Pont,K)




