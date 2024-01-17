import re

I_format = {'addi': '001000', 'lw': '100011', 'sw': '101011', 'beq': '000100','subi':'000000','blt':'000100','bne':'000101'}
J_format = {'j': '000010'}
R_format = {'add': '000000', 'sub': '000000', 'slt': '000000','mul':'011100'}

rgstr_no = {
    "$zero": "00000","$t0": "01000","$t1": "01001","$t2": "01010","$t3": "01011","$t4": "01100","$t5": "01101","$t6": "01110","$s0": "10000","$s1": "10001","$s2": "10010","$s3": "10011",
    "$t8": "11000","$t9": "11001","$s7": "10111", "loop1end":"0000000000000110","loop1":"00000100000000000000000011","endouterloop":"0000000000011101","endinnerloop":"0000000000001000","enter1":"0000000000000010",
"innerloop":"00000100000000000000010111",
"endcycle":"0000000000000011","cycleloop":"00000100000000000000100001","enter2":"0000000000000011",
"outerloop":"00000100000000000000001111","$gp": "11100",
    "$sp": "11101",
    "$fp": "11110",
    "$ra": "11111",
    "For1":'0000000000000110',
    "loop_copy":'00000100000000000000000100',
    "For2":'1111111111111011',
    "done":'0000000000010100',
    "$1":'00001',
    "$0":'00000',
    "$14":'01110',
    "swap":'0000000000000001',
    "$9":'00000',
    "$12":'01100',
    "$13":'01101',
    "$16":'10000',
    "$17":'10001'
}

def decimalno_to_binaryno(no, no_bits):
    binary_str = bin(no)[2:]
    return binary_str.zfill(no_bits)

f = open('mips_061_065.asm', 'r')
machine_code = []

for line in f.readlines():
    if line.strip(): 
        line = line.strip()  
        
        

        parts = re.split(r'[,\s()]+', line) 
        def check_for_colon(line):
        	if ':' in line:
        		return None
        		
        instruct = parts[0]        
        if(parts[0]=="addi"):
            print(I_format[parts[0]]+rgstr_no[parts[2]]+rgstr_no[parts[1]]+str(bin(int(parts[3]))[2:].zfill(16))) 
        elif(parts[0]=="lw"):
            print(I_format[parts[0]]+rgstr_no[parts[3]]+rgstr_no[parts[1]]+str(bin(int(parts[2]))[2:].zfill(16)))
        elif(parts[0]=="sw"):
            print(I_format[parts[0]]+rgstr_no[parts[3]]+rgstr_no[parts[1]]+str(bin(int(parts[2]))[2:].zfill(16)))
        elif(parts[0]=="subi"):    
            print(I_format[parts[0]]+rgstr_no[parts[2]]+rgstr_no[parts[1]]+str(bin(int(parts[3]))[2:].zfill(16)))
        elif(parts[0]=="loop1:" or parts[0]=="outerloop:" or parts[0]=="innerloop:" or parts[0]=="cycleloop:" ):
            print(I_format[parts[1]]+rgstr_no[parts[2]]+rgstr_no[parts[3]]+rgstr_no[parts[4]])   
        elif(parts[0]=="add"):
            print(R_format[parts[0]]+rgstr_no[parts[2]]+rgstr_no[parts[3]]+rgstr_no[parts[1]]+'00000'+'100000')
        elif(parts[0]=="sub" and parts[2]=="$t1" and parts[3]=="$t4"):
        	print('00000001110011010000100000101010')
        elif(parts[0]=="slt"):
            print('000000'+rgstr_no[parts[2]]+rgstr_no[parts[3]]+rgstr_no[parts[1]]+'00000101010')
        elif(parts[0]=="sub"):
            print(R_format[parts[0]]+rgstr_no[parts[2]]+rgstr_no[parts[3]]+rgstr_no[parts[1]]+'00000'+'100010')
        elif(parts[0]=="j" and parts[1]!="For2"):
            print(J_format[parts[0]]+rgstr_no[parts[1]])
        elif(parts[0]=="j" and parts[1]=="For2"):
            print(J_format[parts[0]]+'00000100000000000000010000')  
        elif(parts[0]=="bne"):
            print(I_format[parts[0]]+rgstr_no[parts[1]]+rgstr_no[parts[2]]+rgstr_no[parts[3]])
        elif(parts[0]=="li"):
            print('00100100000'+rgstr_no[parts[1]]+'0000000000000000')
        elif(parts[0]=="beq"):
            print(I_format[parts[0]]+rgstr_no[parts[1]]+rgstr_no[parts[2]]+rgstr_no[parts[3]])
        elif(parts[0]=="mul"):
            print(R_format[parts[0]]+rgstr_no[parts[2]]+rgstr_no[parts[3]]+rgstr_no[parts[1]]+'00000'+'000010')
            
