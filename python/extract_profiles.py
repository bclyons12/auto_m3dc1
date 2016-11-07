# -*- coding: utf-8 -*-
"""
extract_profiles

Extract profiles for various tokamaks

Author:       Brendan Carrick Lyons
Date created: Tue Oct 25 
"""

import os
from subprocess import call
from glob import glob
import my_shutil as mysh
import numpy as np

def extract_profiles(machine='DIII-D',profile='all'):
    
    if machine in ['DIII-D','NSTX-U']:
    
        profile = 'all'
        print 'Extracting all profiles from single file'
        
        if len(glob(r'm3dc1_profiles_*.txt')) != 0:
            mysh.cp(r'm3dc1_profiles_*.txt','m3dc1_profiles_0.txt')
            prof = 'm3dc1_profiles_0.txt'
        elif len(glob(r'p*.*')) != 0:
            mysh.cp(r'p*.*','p0.0')
            prof = 'p0.0'
        else:
            print 'Error: EFIT profiles file not found'
            return
        
        # extract profiles using Nate's utility        
        call(['extract_profiles.sh', prof])
        
        if prof == 'p0.0':
            # extact the Carbon toroidal rotation from the p-file
            with open('p0.0','r') as fin:
                iprint = False
                for line in fin:
                    if not iprint:
                        if 'psinorm omeg' in line:
                            iprint = True
                            fout = open('profile_omega.Ctor','w')
                    else:
                        if 'psinorm'  not in line:
                            fout.write(line)
                        else:
                            iprint = False
                            fout.close()
    
        os.remove(prof)
    
    elif machine in ['AUG']:
        
        print 'Extracting profile '+profile
        
        if profile in ['all','ne']:
            if len(glob(r'neprof_*.asc')) != 0:
                mysh.cp(r'neprof_*.asc','neprof_0.asc')
                prof = 'neprof_0.asc'
                ne = np.loadtxt('neprof_0.asc')
                ne[:,0] = ne[:,0]**2
                ne[:,1] = ne[:,1]*1e-20
                np.savetxt('profile_ne',ne[ne[:,0]<=1.0],fmt='%.6e',delimiter='   ')
                os.remove(prof)
        
        if profile in ['all','te','Te']:
            if len(glob(r'Teprof_*.asc')) != 0:
                mysh.cp(r'Teprof_*.asc','Teprof_0.asc')
                prof = 'Teprof_0.asc'
                Te = np.loadtxt('Teprof_0.asc')
                Te[:,0] = Te[:,0]**2
                Te[:,1] = Te[:,1]*1e-3
                np.savetxt('profile_te',Te[Te[:,0]<=1.0],fmt='%.6e',delimiter='   ')
                os.remove(prof)
            
        if profile in ['all','vt','vtor']:
            if len(glob(r'vtprof_*.asc')) != 0:
                mysh.cp(r'vtprof_*.asc','vtprof_0.asc')
                prof = 'vtprof_0.asc'
                vt = np.loadtxt('vtprof_0.asc')
                vt[:,0] = vt[:,0]**2
                vt[:,1] = vt[:,1]*1e-3
                np.savetxt('profile_omega.Btor',vt[vt[:,0]<=1.0],fmt='%.6e',delimiter='   ')
                os.remove(prof)
                mysh.cp(r'profile_omega.Btor','profile_omega')
        
        if profile in ['all','omgeb','ExB']:
            if len(glob(r'omgeb_*.asc')) != 0:
                mysh.cp(r'omgeb_*.asc','omgeb_0.asc')
                prof = 'omgeb_0.asc'
                omgeb = np.loadtxt('omgeb_0.asc')
                omgeb[:,0] = omgeb[:,0]**2
                omgeb[:,1] = omgeb[:,1]*1e-3
                np.savetxt('profile_omega.ExB',omgeb[omgeb[:,0]<=1.0],fmt='%.6e',delimiter='   ')
                os.remove(prof)
                mysh.cp(r'profile_omega.ExB','profile_omega')
        
    return
        
        
        
        
        
        
