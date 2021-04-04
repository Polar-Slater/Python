#
# Example file for working with functions
#

# define a basic function
def func1():
    print("I am a function")

# function that takes arguments
def func2(arg1, arg2):
    print(arg1, " ", arg2)

# function that returns a value
def cube(x):
    return x*x*x

# function with default value for an argument
def power(num, x=1):
    result = 1
    for i in range(x):
        result = result * num
    return result

#function with variable number of arguments
def multi_add(*args):   #that is a list
    result = 0
    for x in args:
        result = result + x
    return result


#func1()
#print(func1())
## Output:| I am a function    Explain: the first line from the "print" inside the function, 
##        | None                        but it does not return a value, so the it return the default value of "None"
#print(func1)    #print the value of function defination

#func2(10,20)
#print(func2(10,20)) #func2 has no return value, so after execute "print" in func2, it return the default value "None"
#print(cube(3))
#cube(3)

#print(power(2))
#print(power(2,3))
#print(power(x=4,num=2))     #python will automatically detact the parameter, the sequance does not affected

print(multi_add(2,54,78,4,8))