import numpy as np

# Klobuchar parameters
A = 210                                                                 #azimuth
E = 20                                                                  #elevation angle
Phi_u = 40                                                              #geographic lat
Lambda_u = -100                                                         #geographic longitude
Time_GPS = 74700                                                        #GPS time
Alpha = [3.82E-08,  1.49E-08, -1.79E-07, 0]
Beta = [1.43E+05, 0, -3.28E+05, 1.13E+05]

# Earth-centered angle
psi_i = (0.0137/ ((E/180) + 0.11)) - 0.022                              #in semicircles  
print("psi_i =", psi_i, "(semicircles)")

# Subionosphere latitude
phi_i = Phi_u/180 + psi_i*np.cos (A*np.pi/180)/np.pi
if phi_i > 0.416:
    phi_i = 0.416
elif phi_i < -0.416:
    phi_i = -0.416
print("phi_i =", phi_i, "(semicircles)")

# Subionosphere longitude
lambdal = Lambda_u/180 + psi_i*np.sin(A*np.pi/180)/np.cos(phi_i)
print("Lambdal =", lambdal, "(semicircles)")

# Geomagnetic latitude
phi_m = phi_i + 0.064*np.cos((lambdal-1.617)*np.pi)/np.pi
print("phi_m =", phi_m, "(semicircles)")

# Local time
t = 4.32E+04*lambdal + Time_GPS
if t > 86400:
    t = t - 86400
elif t < 0:
    t = t + 86400

print("time =", t, "(seconds)")

# Slant factor
F = 1.0 + 16*((0.53-E/180)**3)
print("F =", F)

# Compute x
Ai = Alpha[0] + Alpha[1] * phi_m + Alpha[2] * phi_m**2 + Alpha[3] * phi_m**3
Bi = Beta[0] + Beta[1] * phi_m + Beta[2] * phi_m**2 + Beta[3] * phi_m**3

x = 2*np.pi*(t-50400)/Bi
print("x =", x)

# Compute Tiono for L1 frequency

Tiono = F*(5E-09+Ai*(1-((x*x)/2)+((x**4)/24)))
print("Tiono in seconds =", Tiono)
print("Tiono in meters =", Tiono*299792458)
