#!/usr/bin/env python

# This code is part of Amoco
# Copyright (C) 2014 Axel Tillequin (bdcht3@gmail.com) 
# published under GPLv2 license

# spec_xxx files are providers for instruction objects.

from .utils import *

#------------------------------------------------------
# amoco SSE instruction specs:
#------------------------------------------------------

ISPECS = []

@ispec_ia32("*>[ {0f}{10} /r ]", mnemonic="MOV")
@ispec_ia32("*>[ {0f}{51} /r ]", mnemonic="SQRT")
@ispec_ia32("*>[ {0f}{58} /r ]", mnemonic="ADD")
@ispec_ia32("*>[ {0f}{59} /r ]", mnemonic="MUL")
@ispec_ia32("*>[ {0f}{5c} /r ]", mnemonic="SUB")
@ispec_ia32("*>[ {0f}{5d} /r ]", mnemonic="MIN")
@ispec_ia32("*>[ {0f}{5e} /r ]", mnemonic="DIV")
@ispec_ia32("*>[ {0f}{5f} /r ]", mnemonic="MAX")
@ispec_ia32("*>[ {0f}{c2} /r ]", mnemonic="CMP")
def ia32_sse2(obj,Mod,REG,RM,data):
    obj.mnemonic += "PS"
    # order is important here (see tests/test_x86.asm)
    if obj.misc['opdsz']==16: obj.mnemonic+="PD"       #66 pfx
    if obj.misc['pfx'][0]=='repne': obj.mnemonic+="SD" #f2 pfx
    if obj.misc['pfx'][0]=='rep': obj.mnemonic+="SS"   #f3 pfx
    obj.misc['opdsz']=128
    op2,data = getModRM(obj,Mod,RM,data)
    op1 = env.getreg(REG,op2.size)
    obj.operands = [op1,op2]
    obj.type = type_data_processing

@ispec_ia32("*>[ {0f}{d0} /r ]", mnemonic="ADDSUBP")
@ispec_ia32("*>[ {0f}{7c} /r ]", mnemonic="HADDP")
@ispec_ia32("*>[ {0f}{7d} /r ]", mnemonic="HSUBP")
def ia32_sse2(obj,Mod,REG,RM,data):
    # order is important here (see tests/test_x86.asm)
    if obj.misc['opdsz']==16: obj.mnemonic+="D"
    elif obj.misc['repne']: obj.mnemonic+="S"
    else: raise InstructionError(obj)
    obj.misc['opdsz']=128
    op2,data = getModRM(obj,Mod,RM,data)
    op1 = env.getreg(REG,op2.size)
    obj.operands = [op1,op2]
    obj.type = type_data_processing

@ispec_ia32("*>[ {0f}{54} /r ]", mnemonic="ANDP",   _opdsz=128, _inv=False) #xmm1 / xmm2/m128
@ispec_ia32("*>[ {0f}{56} /r ]", mnemonic="ORP",    _opdsz=128, _inv=False)
@ispec_ia32("*>[ {0f}{57} /r ]", mnemonic="XORP",   _opdsz=128, _inv=False)
@ispec_ia32("*>[ {0f}{2e} /r ]", mnemonic="UCOMIS", _opdsz=64,  _inv=False)
@ispec_ia32("*>[ {0f}{2f} /r ]", mnemonic="COMIS",  _opdsz=64,  _inv=False)
@ispec_ia32("*>[ {0f}{28} /r ]", mnemonic="MOVAP",  _opdsz=128, _inv=False)
@ispec_ia32("*>[ {0f}{29} /r ]", mnemonic="MOVAP",  _opdsz=128, _inv=True)
@ispec_ia32("*>[ {0f}{12} /r ]", mnemonic="MOVLP",  _opdsz=64,  _inv=False)
@ispec_ia32("*>[ {0f}{13} /r ]", mnemonic="MOVLP",  _opdsz=64,  _inv=True)
@ispec_ia32("*>[ {0f}{14} /r ]", mnemonic="UNPCKLP",_opdsz=128, _inv=False)
@ispec_ia32("*>[ {0f}{15} /r ]", mnemonic="UNPCKHP",_opdsz=128, _inv=False)
def ia32_sse2(obj,Mod,REG,RM,data,_opdsz,_inv):
    obj.mnemonic += 'D' if obj.misc['opdsz']==16 else 'S'
    obj.misc['opdsz']=_opdsz
    op2,data = getModRM(obj,Mod,RM,data)
    op1 = env.getreg(REG,op2.size)
    obj.operands = [op1,op2] if not _inv else [op2,op1]
    obj.type = type_data_processing


# DPPD,DPPS
# EXTRACTPS
# INSERTPS


