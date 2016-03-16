function SIR(S, I ,R, gamma, beta, T){
    
    /* Arrays to hold rhe results */
    var susceptible = [], infected = [], removed = [], time = [], n, S_i, I_i, 
            R_i, dt, t;
    
    dt = 0.5;
    t = 0;
    n = T / dt;


    for (i=0; i < n; i++){
        
        S_i = S - dt * beta * S * I;
        I_i = I + dt * beta * S * I - dt * gamma * I;
        R_i = R + dt * gamma * I;
        t = t + dt;
        
        susceptible.push(S_i);
        infected.push(I_i);
        removed.push(R_i);
        time.push(t);
          
        S = S_i;
        I = I_i;
        R = R_i;
    }
    
    return [susceptible, infected, removed, time];
}   

