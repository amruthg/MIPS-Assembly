	addi $t9,$t2,0		#here we are storing the memory address of the array in t9
	add $s2,$zero,$zero	#making the value of s2 as 0
	addi $s3,$t3,0		#storing the address of t3 in s3
	add $t4,$zero,$zero

loop_copy:
	beq $s2,$t1 For1	#if copying of the loop is done go to sorting loops
	lw $t8,0($t9)		#copying the element of t2 into a temp variable t8		
	sw $t8,0($s3)		#storing the value in s3=t3+s2*4s
	addi $s3,$s3,4		#s3=s3+4,for memory address
	addi $t9,$t9,4		#t9=t9+4 , to go the next element.
	addi $s2,$s2,1		#s2+=1,iterator increment
	j loop_copy 		#jumping back to the loop


For1:
	blt $t1,$t4, end	#if step==size, then exit the loop.
	addi $t4,$t4,1		#incrementor for the outer loop, step++
	li $t5,0		#reseting the value of the inner loop to 0,i=0.
	j For2			#jump statement to the 2nd for loop.

For2:
	sub $t6,$t1,$t4		#the max value of the inner loop iterator should be size-step-1.
	subi $t6,$t6,1		#since bubble sort happens only till j=n-1=size-step-1
	bgt $t5,$t6,For1	#if j=size-step, exit the inner for loop for next  iteration.
	
	addi $t9,$0,4		#t9=4
	mul $t9,$t9,$t5		#t9=4*j
	add $t9,$t9,$t3		#t9=t2+4*j
	
	lw $s0,0($t9)		#s0=memory[t9+0]=memory[t2+4*j+0]
	lw $s1,4($t9)		#s1=memory[t9+4]=memory[4+t2+4*j]
	addi $t5,$t5,1		#the incrementor for the inner loop, i++
	bgt $s0,$s1,Swap	#if s0>s1 then swap
	
	j For2			#going through the inner for loop again.

	
Swap:
	sw $s1,0($t9)		#memory[0+t9]=memory[t2+4*j]=s1
	sw $s0,4($t9)		#memory[4+t9]=memory[4+4*j+t2]=s0
	j For2			#going through the inner for loop again.
	
							
#endfunction

