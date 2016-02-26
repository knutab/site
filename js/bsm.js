/* The cummulative Normal distribution function copied from 
http://www.espenhaug.com/black_scholes.html */

function CND(x){

var a1, a2, a3, a4 ,a5, k ;

a1 = 0.31938153, a2 =-0.356563782, a3 = 1.781477937, a4= -1.821255978 , a5= 1.330274429;

if(x<0.0)
return 1-CND(-x);
else
k = 1.0 / (1.0 + 0.2316419 * x);
return 1.0 - Math.exp(-x * x / 2.0)/ Math.sqrt(2*Math.PI) * k
* (a1 + k * (-0.356563782 + k * (1.781477937 + k * (-1.821255978 + k * 1.330274429)))) ;
}

/* Formula for calculating d1 */
function d1(S, X, v, r, T){
	var d1;
	d1 = (Math.log(S / X) + (r + v * v / 2.0) * T) / (v * Math.sqrt(T));
    return d1;

}

/* Formula for calculating d2 */
function d2(S, X, v, r, T){
	var d2;
	d2 = d1(S, X, v, r, T) - v * Math.sqrt(T);
    return d2;
}

/*Formula for calculating the Black Scholes Option value */
function BSM(Flag, S, X, v, r, T){

if (Flag==="c")
    
    return S * CND(d1(S, X, v, r, T)) - X * Math.exp(-r * T) * CND(d2(S, X, v, r, T));

if (Flag==="p")
    
    return X * Math.exp(-r * T) * CND(-d2(S, X, v, r, T)) - S * CND(-d1(S, X, v, r, T));
}

/* Formula's for calculating N'(d1) and N'(d2) to simplify some of the
calculations later */
function dNd1(S, X, v, r, T){

    return (1.0/Math.sqrt(2.0*Math.PI))*Math.exp(-(d1(S,X,v,r,T)*d1(S,X,v,r,T))/2.0);
}

function dNd2(S, X, v, r, T){

    return (1.0/Math.sqrt(2.0*Math.PI))*Math.exp(-(d2(S,X,v,r,T)*d2(S,X,v,r,T))/2.0);
}

/*Formula for calculation the Intrensic Value of the option*/
function IV(Flag, S, X){
    
    if (Flag==='c'){
        
        if(S - X > 0){
            return S - X;
        }
        else{
            return 0;
        }
    }
    
    if (Flag==='p'){ 
        
        if(X - S > 0){
            return X - S;
        }
        else{
            return 0;
        }
    }
}

/*Formula for calculation the Time Value of the option*/
function TV(Flag, S, X, v, r, T){
    
    if(Flag==='c'){
        return BSM('c', S, X, v, r, T) - IV('c', S, X);
    }
    else{
        return BSM('p', S, X, v, r, T) - IV('p', S, X);
    }
}

/*Formulas for calculating the greeks */
function delta(Flag, S, X, v, r, T){
    
    if(Flag==='c'){
        return CND(d1(S, X, v, r, T));
    }
    else{
        return CND(d1(S, X, v, r, T)) - 1;
    }
}

function vega(S, X, v, r, T){
 
    return (S * Math.sqrt(T) * (Math.exp((-0.5 * d1(S, X, v, r, T)*d1(S, X, v, r, T))) / 
        Math.sqrt(2.0 * Math.PI))) / 100.0;
}

function gamma(S, X, v, r, T){
    
    return ((X * Math.exp(-r * T) * dNd2(S, X, v, r, T)) / (S * S * v * Math.sqrt(T)));
}

function theta(Flag, S, X, v, r, T){
    
    if(Flag==='c'){
        return (-X * Math.exp(-r * T) * (r * CND(d2(S, X, v, r, T)) + ((v * dNd2(S, X, v, r, T) ) / 
            (2.0 * Math.sqrt(T))))) / 365.0;
    }
    else{
        return (X * Math.exp(-r * T) * (r * CND(-d2(S, X, v, r, T)) - ((v * dNd2(S, X, v, r, T) ) / 
            (2.0 * Math.sqrt(T))))) / 365.0;
    }
}

function rho(Flag, S, X, v, r, T){
    
    if(Flag==='c'){
        return (T * X * Math.exp(-r * T) * CND(d2(S, X, v, r, T))) / 100.0;
    }
    else{
        return (T * X * Math.exp(-r * T) * CND(-d2(S, X, v, r, T))) / 100.0;
    }
}

function NewtonBSM(Flag, S, X, r, T, MV){
    
    var vol, v_i, diff, tol;
    tol = 1.0e-9;

    if (Flag ==='c'){
        vol = Math.sqrt(2.0*Math.PI /T) * MV / S;
    }
    else{
        vol = Math.sqrt(2.0*Math.PI /T) * ((S - X * Math.exp(-r * T) + MV) / S);
    }
    
    for (i = 0; i < 100; i++){

        v_i = vol - (BSM(Flag, S, X, vol, r, T) - MV) / (vega(S, X, vol, r, T) * 100);
        diff = Math.abs(v_i - vol);

        if(diff < tol){
            return v_i;
        }
        vol = v_i;
    }
}