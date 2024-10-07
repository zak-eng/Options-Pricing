from scipy import optimize, stats
from scipy.optimize import  brentq
import  numpy as np

from scipy.stats import norm
from matplotlib import pyplot as plt
from scipy.optimize import root_scalar






def strike_from_spot_delta(tte, fwd, vol, delta, dcf_for, put_call):
    sigma_root_t = vol * np.sqrt(tte)
    inv_norm = norm.ppf(delta * put_call * dcf_for)

    return fwd * np.exp(-sigma_root_t * put_call * inv_norm + 0.5 * sigma_root_t * sigma_root_t)

def strike_from_fwd_delta(tte, fwd, vol, delta, put_call):
    sigma_root_t = vol * np.sqrt(tte)
    inv_norm = norm.ppf(delta * put_call)
    return fwd * np.exp(-sigma_root_t * put_call * inv_norm + 0.5 * sigma_root_t * sigma_root_t)

def volchecker(BF,ATM,RR):

    call25 = ATM+BF[1]  + 0.5*RR[0]
    call10 = ATM+BF[0]  + 0.5*RR[1]
    put25  = ATM+BF[1]  - 0.5*RR[0]
    put10  = ATM+BF[0]  - 0.5*RR[1]

    return np.array([ATM,call25,put25,call10,put10])
def getstrike(vol,forward,rf,deltas,t):
    strike= np.zeros_like(vol)
    n,m=vol.shape
    for j in range(n):
        for i in range(m):
            delta = 0.5 if deltas[i] == "ATM" else int(deltas[i].split(" ")[0].replace("D", "")) / 100.
            put_call = 1 if deltas[i] == "ATM" else -1 if deltas[i].split(" ")[1] == "Put" else 1
            fwd = forward[j]
            for_dcf = np.exp(-rf[j]*t[j])
            if t[j] < 1.:
                strike[j][i] = strike_from_spot_delta(t[j], fwd, vol[j][i], put_call*delta, for_dcf, put_call)
            else:
                strike[j][i] = strike_from_fwd_delta(t[j], fwd, vol[j][i], put_call*delta, put_call)
    return  strike		

