set NODE; 
set COURSE;
set Arcs within (NODE cross NODE) ;

param I {NODE, COURSE} >=0; #INBOUNDING COST
param O {NODE, COURSE} >=0; #OUTBOUNDING COST
param R := 0; # Reefer 1, or Non-reefer 0
param K {NODE, NODE, COURSE} >= 0; 
param N {NODE, NODE, COURSE} >= 0; #availability of the Arcs
param WR {NODE} >= 0; # Warehouse cost for reefer
param WN {NODE} >= 0; # Warehouse cost for non-reefer
param Vt >=0; # total volume
param W {NODE} >=0; # capacity of warehouse in node i
param C {NODE, NODE, COURSE} >=0; # capacity of mode c
param T >= 0; # time
param S {NODE, NODE, COURSE} >=0;  # transportation time

var X {i in NODE, j in NODE, c in COURSE} binary; # the route


minimize Cost:
sum {c in COURSE, (i,j) in Arcs} (I[j,c]+O[i,c]+R * WR[j] + (1-R)*WN[j])*Vt * X[i,j,c] +
sum {c in COURSE, (i,j) in Arcs} N[i,j,c] * K[i,j,c]* Vt  * X[i,j,c]; 
# fixed cost + transportation cost
# assume all the goods will be transitted together

subject to CapacityNode {(i,j) in Arcs}:
sum{c in COURSE} Vt * X[i,j,c] <= W[j];
# capacity of Nodes' warehouse

subject to CapacityTrans {(i,j) in Arcs, c in COURSE} :
Vt * X[i,j,c] <= C[i, j, c];
# capacity of transport modes

subject to  Transit {i in NODE} :
sum {c in COURSE} X[1,i,c] = sum {c in COURSE} X[i,2,c]; 
# supply = demand
   

subject to Time{(i,j) in Arcs, c in COURSE}:
max(S[1,i,c]*X[1,i,c]) + max(S[i,j,c]*X[i,j,c]) + max(S[j,2,c]*X[j,2,c]) <= T;
# time constrain

#subject to supply {(i,j) in Arcs} :
#sum {c in COURSE} X[i,j,c] <= 1;

subject to demand :
sum {i in NODE, c in COURSE} X[i,2,c] >= 1; 
#transport to destination, 2 denotes the destination

subject to supply :
sum {i in NODE, c in COURSE} X[1,i,c] >= 1; 
#transport from origin, 1 denotes the destination







