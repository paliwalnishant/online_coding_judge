import commands
x = commands.getstatusoutput('gcc anant1.c')
error=''
for i in x:
    error=error+str(i)+"\n"
print error
