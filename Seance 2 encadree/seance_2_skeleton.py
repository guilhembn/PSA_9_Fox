#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
squelette de code pour la deuxième séance du projet de synthèse
'''
import math, numpy as np, scipy.integrate
import matplotlib.pyplot as plt
import pdb

import dynamic as dyn
import utils as ut
np.set_printoptions(precision=3, suppress=True, linewidth=200)


def get_trim(aircraft, h, Ma, sm, km):
    '''
    Calcul du trim pour un point de vol
    '''
    aircraft.set_mass_and_static_margin(km, sm)
    va = dyn.va_of_mach(Ma, h)
    Xe, Ue = dyn.trim(aircraft, {'va':va, 'h':h, 'gamma':0})
    return Xe, Ue

def get_all_trims(aircraft, hs, Mas, sms, kms):
    '''
    Calcul de trims pour une serie de points de vol
    TODO
    '''
    pass





def tons_of_newton(N): return N/9.81/1000.
def plot_trims(aircraft, gamma=0., saturate=True):
    '''
    Affichage de trims sous forme de surfaces colorées
    '''
    vs = np.linspace(60, 350, 21, endpoint=True)
    hs = np.linspace(1000, 14000, 21, endpoint=True)
    trims = np.zeros((len(hs), len(vs), 2))
    for i,v in enumerate(vs):
        for j,h in enumerate(hs):
            Xe, Ue = dyn.trim(aircraft, args = {'va': v, 'h': h, 'gamma': gamma})
            trims[j, i] = Xe[dyn.s_a], tons_of_newton(dyn.propulsion_model([0, h, v, 0, 0, 0], [0, Ue[dyn.i_dth], 0, 0], aircraft))
            
            if saturate:
                alpha_c, T_c = trims[j,i][0], trims[j,i,1]
                alpha_max = ut.rad_of_deg(15)
                if alpha_c > alpha_max: 
                    trims[j,i][0] = 1e16
                    trims[j,i][1] = 1e16
                Tmax = tons_of_newton(dyn.propulsion_model([0, h, v, 0, 0, 0], [0, 1, 0, 0], aircraft))
                if T_c > Tmax: 
                    trims[j,i, 0] = 1e16
                    trims[j,i, 1] = 1e16

    fig = plt.figure(figsize=(0.75*20.48, 0.5*10.24))

    ax = plt.subplot(1,2,1)
    thetas_deg = ut.deg_of_rad(trims[:, :, 0])
    v = np.linspace(0, 15, 16, endpoint=True)
    plt.contour(vs, hs, thetas_deg, v, linewidths=0.5, colors='k')
    plt.contourf(vs, hs, thetas_deg, v, cmap=plt.cm.jet)
    ax.set_title(u'$\\alpha$ (degrés)')
    ax.xaxis.set_label_text('vitesse (m/s)')
    ax.yaxis.set_label_text('altitude (m)')
    plt.colorbar(ticks=v)

    ax = plt.subplot(1,2,2)
    T_tons = trims[:, :, 1] #/9.81/1000.
    v = np.linspace(2, 10, 17, endpoint=True)
    plt.contour(vs, hs, T_tons, v, linewidths=0.5, colors='k')
    plt.contourf(vs, hs, T_tons, v, cmap=plt.cm.jet)
    ax.set_title('thrust (tons)')   
    ax.xaxis.set_label_text('vitesse (m/s)')
    ax.yaxis.set_label_text('altitude (m)')
    plt.colorbar(ticks=v)


def plot_traj_trim(aircraft, h, Ma, sm, km):
    '''
    Affichage d'une trajectoire avec un point de trim comme condition initiale
    '''
    aircraft.set_mass_and_static_margin(km, sm)
    va = dyn.va_of_mach(Ma, h)
    Xe, Ue = dyn.trim(aircraft, {'va':va, 'h':h, 'gamma':0})
    time = np.arange(0., 100, 0.5)
    X = scipy.integrate.odeint(dyn.dyn, Xe, time, args=(Ue, aircraft))
    dyn.plot(time, X)


def get_CL_Fmax_trim(aircraft, h, Ma):
    p, rho, T = ut.isa(h)
    va = dyn.va_of_mach(Ma, h)
    pdyn = 0.5*rho*va**2
    return P.m*P.g/(pdyn*P.S), propulsion_model([0, h, va, 0, 0, 0], [0, 1, 0, 0], aircraft)


def get_linearized_model(aicraft, h, Ma, sm, km):    
    aircraft.set_mass_and_static_margin(km, sm)
    va = dyn.va_of_mach(Ma, h)
    Xe, Ue = dyn.trim(aircraft, {'va':va, 'h':h, 'gamma':0})
    A, B = ut.num_jacobian(Xe, Ue, aicraft, dyn.dyn)
    poles, vect_p = np.linalg.eig(A[dyn.s_va:, dyn.s_va:])
    return A, B, poles, vect_p

def plot_poles(aicraft, hs, Mas, sms, kms):
    '''
    TODO
    '''
    # poles.real, poles.imag <- parties réelles et imaginaires d'un complexe 
    pass


aircraft = dyn.Param_A320()

hs, Mas = [3000, 11000], [0.5, 0.8]
sms, kms = [0.2, 1.], [0.1, 0.9]

trims = get_all_trims(aircraft, hs, Mas, sms, kms)

plot_trims(aircraft)

plot_traj_trim(aircraft, 5000, 0.5, 0.2, 0.5)

plot_poles(aircraft, hs, Mas, sms, kms)

plt.show()