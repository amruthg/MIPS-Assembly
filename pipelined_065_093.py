def b2d(str):
    # x = 0
    # str = str[::-1] 
    # for i in range(len(str)):
    #     if str[i] == '1':
    #         x += 2**i
    # return x
    return int(str,2)

registers=[0]*32
memory = [0]*1000
pc=0
clk=0

#pipeline registers
if_id = {"inst":"nope","control":"nope","pc":0}             #instruction,control
id_ex={"rs":"nope","rt":"nope","imm":"nope","totinst":"nope","ishazard":False,"hazrdmatch":"nope","pc":0}               #rs,rt,imm
ex_mem={"alu_out":0,"rs":"nope","iszero":"nope","opcode":"nope","rd":"nope","pc":0,"hazardyes": False}          #Alu_output,rs,iszero
mem_wb={"alu_out":0,"memout":0,"op":"nope","pc":0}                  #alu_output,memoryoutput
wb_mem2={"alu_out":0,"memout":0,"op":"nope","pc":0} 
#hazard_detection

def hazard():
    if((ex_mem["rd"] == id_ex["rs"]) or (ex_mem["rd"] == id_ex["rt"]) or (mem_wb["op"][16:21] == id_ex["rs"]) or (mem_wb["op"][16:21] == id_ex["rt"]) or (wb_mem2["op"][16:21] == id_ex["rs"]) or (wb_mem2["op"][16:21] == id_ex["rt"])):
        if(ex_mem["opcode"][0:6]=="000100" or mem_wb["op"][0:6]=="000100" or wb_mem2["op"][0:6] == "000100"):
            return False
        return True
    else:
        return False

def hazrd_match():
    if((ex_mem["rd"] == id_ex["rs"]) or (mem_wb["op"][16:21] == id_ex["rs"]) or (wb_mem2["op"][16:21] == id_ex["rs"]) ):
        return id_ex["rs"]
    if((ex_mem["rd"] == id_ex["rt"]) or (mem_wb["op"][16:21] == id_ex["rt"]) or (wb_mem2["op"][16:21] == id_ex["rt"])):
        return id_ex["rt"]

#functions/phases

#IF
def inst_fetch(mem_inst,pc):
    # print(f'op - IF , pc = {pc}, inst = {mem_inst[pc]}')
    if_id["inst"]=mem_inst[pc]
    if_id["pc"]=pc

    # print("s0 = ",registers[16])
#ID
def instdecode():
    global pc
    id_ex["pc"] = if_id["pc"]
    id_ex["rs"] = if_id["inst"][6:11]
    id_ex["rt"] = if_id["inst"][11:16]
    id_ex["imm"] = if_id["inst"][16:32]
    id_ex["totinst"] = if_id["inst"]
    id_ex["ishazard"] = hazard()
    id_ex["hazrdmatch"] = hazrd_match()
    
    
    if(not hazard()):
        
        #ex_mem["alu_out"]=0
        if(id_ex["totinst"][0:6]=="000100"):         #beq
            if(registers[b2d(id_ex["totinst"][11:16])] == registers[b2d(id_ex["totinst"][6:11])]):
                # id_ex["pc"]=id_ex["pc"]+(b2d(id_ex["totinst"][16:32]))      #if wrong output
                pc=id_ex["pc"]+(b2d(id_ex["totinst"][16:32]))+1
            else:
                pass
        elif(id_ex["totinst"][0:6]=="000010"):         #jump
            pc=b2d(id_ex["totinst"][6:32])-1048576-1
    if(hazard()):
        #ex_mem["alu_out"]=0
        if(id_ex["totinst"][0:6]=="000100"): #beq
            # print(f"s0 {registers[16]} t1 {registers[9]}")
            if(id_ex["hazrdmatch"] == id_ex["totinst"][6:11]):
                if(registers[b2d(id_ex["totinst"][11:16])] == ex_mem["alu_out"]):
                    # id_ex["pc"]=id_ex["pc"]+(b2d(id_ex["totinst"][16:32]))      #if wrong output
                    pc=id_ex["pc"]+(b2d(id_ex["totinst"][16:32]))+1
                else:
                    pass
            else:
                if(registers[b2d(id_ex["totinst"][6:11])] == ex_mem["alu_out"]):
                    # id_ex["pc"]=id_ex["pc"]+(b2d(id_ex["totinst"][16:32]))      #if wrong output
                    pc=id_ex["pc"]+(b2d(id_ex["totinst"][16:32]))+1
                else:
                    pass
        elif(id_ex["totinst"][0:6]=="000010"):         #jump
            pc=b2d(id_ex["totinst"][6:32])-1048576-1
    
#EX
def alu():
    #global pc
    ex_mem["pc"]=id_ex["pc"]
    ex_mem["opcode"]=id_ex["totinst"]
    #registers[b2d(id_ex["totinst"][16:21])] rewrite cheyyi with ex_mem["alu_out"]
    ex_mem["hazardyes"] = id_ex["ishazard"]

    if(not id_ex["ishazard"]):
        if(id_ex["totinst"][0:6]=="000000"):       
            if(id_ex["totinst"][26:]=="100000"):       #add
                ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])] +  registers[b2d(id_ex["totinst"][11:16])]
            elif(id_ex["totinst"][26:]=="100010"):     #sub
                ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])] - registers[b2d(id_ex["totinst"][11:16])]       
            elif(id_ex["totinst"][26:]=="000010"):     #mul
                ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])] * registers[b2d(id_ex["totinst"][11:16])]
            elif(id_ex["totinst"][26:]=="101010"):     #slt
                if( registers[b2d(id_ex["totinst"][6:11])] < registers[b2d(id_ex["totinst"][11:16])]):
                    registers[b2d(id_ex["totinst"][16:21])] = 1
                else:
                    registers[b2d(id_ex["totinst"][16:21])] = 0
        elif(id_ex["totinst"][0:6]=="001000"):         #addi
            ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])] + b2d(id_ex["totinst"][16:32])
        
        elif(id_ex["totinst"][0:6]=="000101"):         #bne
            if(registers[b2d(id_ex["totinst"][11:16])] != registers[b2d(id_ex["totinst"][6:11])]):
                ex_mem["pc"]=ex_mem["pc"]+(b2d(id_ex["totinst"][16:32]))      #if wrong output
            else:
                pass
    
        elif(id_ex["totinst"][0:6]=="100011"):         #lw
            ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])]+b2d(id_ex["totinst"][16:32])
        elif(id_ex["totinst"][0:6]=="101011"):         #sw
            ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])]+b2d(id_ex["totinst"][16:32])
    
    if(id_ex["ishazard"]):               #forwarding
        if(id_ex["totinst"][0:6]=="000000"):       
            if(id_ex["totinst"][26:]=="100000"):       #add
                if(id_ex[hazrd_match] == id_ex["totinst"][6:11]):
                    ex_mem["alu_out"] = ex_mem["alu_out"] +  registers[b2d(id_ex["totinst"][11:16])]
                else:
                    ex_mem["alu_out"] = ex_mem["alu_out"] +  registers[b2d(id_ex["totinst"][6:11])]
            
            elif(id_ex["totinst"][26:]=="100010"):     #sub
                if(id_ex[hazrd_match] == id_ex["totinst"][6:11]):
                    ex_mem["alu_out"] = ex_mem["alu_out"] - registers[b2d(id_ex["totinst"][11:16])]
                else:
                    ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])] - ex_mem["alu_out"]     
            
            # elif(id_ex["totinst"][26:]=="000010"):     #mul
            #     ex_mem["alu_out"] = registers[b2d(id_ex["totinst"][6:11])] * registers[b2d(id_ex["totinst"][11:16])]
            
            elif(id_ex["totinst"][26:]=="101010"):     #slt
                if(id_ex[hazrd_match] == id_ex["totinst"][6:11]):
                    if( ex_mem["alu_out"] < registers[b2d(id_ex["totinst"][11:16])]):
                        registers[b2d(id_ex["totinst"][16:21])] = 1
                    else:
                        registers[b2d(id_ex["totinst"][16:21])] = 0
                else:
                    if( registers[b2d(id_ex["totinst"][6:11])] < ex_mem["alu_out"]):
                        registers[b2d(id_ex["totinst"][16:21])] = 1
                    else:
                        registers[b2d(id_ex["totinst"][16:21])] = 0
        
        elif(id_ex["totinst"][0:6]=="001000"):         #addi
            if(id_ex["hazrdmatch"] == id_ex["totinst"][6:11]):
                ex_mem["alu_out"] = ex_mem["alu_out"] + b2d(id_ex["totinst"][16:32])

        
        
        
        elif(id_ex["totinst"][0:6]=="000101"):         #bne
            if(id_ex[hazrd_match] == id_ex["totinst"][6:11]):
                if(registers[b2d(id_ex["totinst"][11:16])] != ex_mem["alu_out"]):
                    ex_mem["pc"]=ex_mem["pc"]+(b2d(id_ex["totinst"][16:32]))      #if wrong output
                else:
                    pass
            else:
                if(registers[b2d(id_ex["totinst"][6:11])] != ex_mem["alu_out"]):
                    ex_mem["pc"]=ex_mem["pc"]+(b2d(id_ex["totinst"][16:32]))      #if wrong output
                else:
                    pass
        
      
        
        elif(id_ex["totinst"][0:6]=="100011"):         #lw
            ex_mem["alu_out"] = ex_mem["alu_out"]+b2d(id_ex["totinst"][16:32])
        
        elif(id_ex["totinst"][0:6]=="101011"):         #sw
            ex_mem["alu_out"] = ex_mem["alu_out"]+b2d(id_ex["totinst"][16:32])
    
    ex_mem["rs"] = id_ex["totinst"][11:16]
    ex_mem["rd"] = id_ex["totinst"][16:21]
  
def mem():
    mem_wb["pc"] = ex_mem["pc"]
    mem_wb["alu_out"] = ex_mem["alu_out"]
    mem_wb["op"] = ex_mem["opcode"]
    if(ex_mem["hazardyes"]):
        pass
    
    if(ex_mem["opcode"][0:6]=="100011"):
        mem_wb["memout"] = memory[ex_mem["alu_out"]]
        # print(f'op - mem , pc = {mem_wb["pc"]}, lw , loading_value {mem_wb["memout"]}')
    
    elif(ex_mem["opcode"][0:6]=="101011"):
        memory[ex_mem["alu_out"]] = registers[b2d(ex_mem["rs"])]
       
    else:
        pass    

def writeback():
    wb_mem2=mem_wb
    
    
    if(mem_wb["op"][0:6]=="000000"):       
        if(mem_wb["op"][26:]=="100000"):       #add
            
            registers[b2d(mem_wb["op"][16:21])] = mem_wb["alu_out"]
        elif(mem_wb["op"][26:]=="100010"):     #sub
          
            registers[b2d(mem_wb["op"][16:21])] = mem_wb["alu_out"]
    elif(mem_wb["op"][0:6]=="001000"):         #addi
     
        registers[b2d(mem_wb["op"][11:16])] = mem_wb["alu_out"]
    elif(mem_wb["op"][0:6]=="100011"):         #lw
     
        registers[b2d(mem_wb["op"][11:16])] = mem_wb["memout"]


my_list=[1,-9,8,17,78,86]
for i in range(len(my_list)):
    memory[i*4]=my_list[i]
registers[10]=0
registers[9] =len(my_list)
registers[11]=4*len(my_list)

mem_ins=[]
with open("ca_inp.txt", 'r') as file:
    for line in file:
        values = line.strip()
        mem_ins.append(values)


while(pc<114):
    if(mem_wb["op"]!="nope"):
        writeback()
    if(ex_mem["opcode"]!="nope"):
        mem()
    if(id_ex["totinst"]!="nope"):
        alu()
    if(if_id["inst"]!="nope"):
        instdecode()
    inst_fetch(mem_ins,pc)

    pc=pc+1
    clk=clk+1

print("total no of clock cycles in pipelined = ",clk)
for i in range(len(my_list)):
    print(memory[4*len(my_list)+i*4])