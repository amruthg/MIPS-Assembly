def b2d(str):
    return int(str,2)

registers = [0]*32
memory = [0]*1000
CLK_count = 1
pc=0
# print(registers)

reg={
    '$0':'00000',"$at": "00001","$v0": "00010","$v1": "00011","$a0": "00100","$a1": "00101","$a2": "00110",
    "$a3": "00111",'$t0': '01000','$t1': '01001','$t2': '01010','$t3': '01011','$t4': '01100',
    '$t5': '01101','$t6': '01110','$t7': '01111','$t8': '11000','$t9': '11001','$s0': '10000',
    '$s1': '10001','$s2': '10010','$s3': '10011','$s4': '10100','$s5': '10101','$s6': '10110',
    '$s7': '10111',
}

op_code={
        "add":"000000","addi":"001000","beq":"000100","bne":"000101","j":"000010",
        "jal":"000011","lw":"100011","sw":"101011","slt":"000000","mul":"011100"
    }

f_field={"add":"100000","slt":"101010","mul":"000010","sub":"100010"}

def alu(I):
    global CLK_count
    global pc
    # if it is an R-type instruction
    if(I[0:6]=="000000"):       
        if(I[26:]=="100000"):       #add
            registers[b2d(I[16:21])] = registers[b2d(I[6:11])] +  registers[b2d(I[11:16])]
        elif(I[26:]=="100010"):     #sub
            registers[b2d(I[16:21])] = registers[b2d(I[6:11])] - registers[b2d(I[11:16])]       
        elif(I[26:]=="101010"):     #slt
            if( registers[b2d(I[6:11])] < registers[b2d(I[11:16])]):
                registers[b2d(I[16:21])] = 1
            else:
                registers[b2d(I[16:21])] = 0

    elif(I[0:6]=="011100"):     #mul
        registers[b2d(I[16:21])] = registers[b2d(I[6:11])] * registers[b2d(I[11:16])]
    elif(I[0:6]=="001000"):         #addi
        if(I[16]=="1"):
            imm_binary=''.join('1' if bit == '0' else '0' for bit in I[16:])
            imm = -(int(imm_binary,2)+1)
        else:
            imm = int(I[16:],2)
        
        registers[b2d(I[11:16])] = registers[b2d(I[6:11])] + imm
    elif(I[0:6]=="000100"):         #beq

        if(I[16]=="1"):
            imm_binary=''.join('1' if bit == '0' else '0' for bit in I[16:])
            imm = -(int(imm_binary,2)+1)
        else:
            imm = int(I[16:],2)

        if(registers[b2d(I[11:16])] == registers[b2d(I[6:11])]):
            pc=pc+imm     #if wrong output
        else:
            pass
    elif(I[0:6]=="000101"):         #bne

        if(I[16]=="1"):
            imm_binary=''.join('1' if bit == '0' else '0' for bit in I[16:])
            imm = -(int(imm_binary,2)+1)
        else:
            imm = int(I[16:],2)

        if(registers[b2d(I[11:16])] != registers[b2d(I[6:11])]):
            pc=pc+imm      #if wrong output
        else:
            pass
    elif(I[0:6]=="000010"):         #jump
        pc=b2d(I[6:32])-1048576-1
        
    elif(I[0:6]=="100011"):         #lw
        registers[b2d(I[11:16])] = memory[
            registers[b2d(I[6:11])]+b2d(I[16:32])]
    elif(I[0:6]=="101011"):         #sw
        memory[registers[b2d(I[6:11])]+b2d(I[16:32])] = registers[b2d(I[11:16])]

##############################################################################################################################################

            #the input for the SORTING ALGORITHM ( SELECTION SORT ).

# my_list=[11,7,9,-1,0,1,543,4,4,8,91]
# for i in range(len(my_list)):
#     memory[i*4]=my_list[i]
# registers[10]=0
# registers[9] =len(my_list)
# registers[11]=4*len(my_list)

# #             # inst=[list(map(int,input.split())) for i in range(45)]

# inp=[]
# with open("text.txt", 'r') as file:
#     for line in file:
#         values = line.strip()
#         inp.append(values)


# while(pc<45):
#     alu(inp[pc])
#     pc=pc+1
#     CLK_count=CLK_count+1

# print("the clock count is" , CLK_count*5)

# for i in range(len(my_list)):
#     print(memory[(i+len(my_list))*4])

##############################################################################################################################################

#the input for the FACTORIAL

my_list=[1,8,17,7,8]
for i in range(len(my_list)):
    if(my_list[i]==0):
        my_list[i]=1
for i in range(len(my_list)):
    memory[i*4]=my_list[i]

  
registers[10]=0
registers[9] =len(my_list)
registers[11]=4*len(my_list)

inp=[]
with open("factorial_mc.txt", 'r') as file:
    for line in file:
        values = line.strip()
        inp.append(values)

while(pc<18):
    alu(inp[pc])
    pc=pc+1
    CLK_count += 1

print("the clock count is" ,CLK_count*5)



for i in range(len(my_list)):
    print(memory[(i+len(my_list))*4])
    
