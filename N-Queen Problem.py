
import numpy as np
import random
import copy

def fitness_check(array):
    n=len(array)
    count = [0] * len(array)
    fit_count=0
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] == array[j]:        # to chcek similarity in array
                count[i] += 1  ##it checks the number of queens attacked 

    for i in range(len(array)):
        x=array[i]
        for k in range(1,x):        # to check diagonally downward , k start from i+! and keep on going till reaches 8 diagonally , if start from 3 it should not go beyond 8
            if (i+k<n):
                if (array[i]) == (array[i+k]+k):
                    count[i] += 1

    for i in range(len(array)):
        x=(n-array[i])
        for k in range(1,x):        # to check diagonally upward
            if (i+k<n):
                if (array[i]) == (array[i+k]-k):
                    count[i] += 1

    # as have to keep track of the non attcaking queens that come as 8-(i+1)-attacked ..i-1 as have to minus previous ones too
    for i in range(0,n):
        count[i]=n-count[i]-i-1
        fit_count+=count[i] 
    # print(count)    #fitness array
    return fit_count

def roulette_wheel(fitness):
    n= [len(item[0]) for item in fitness]
    n=n[0]
    # print("fitness n " , n)
    sorted_fitness = sorted(fitness, key=lambda x: x[1])
    random_row = random.choice(sorted_fitness)  # select a random row
    index1 = None
    for i, row in enumerate(sorted_fitness):
        if np.array_equal(row[0], random_row[0]) and row[1] == random_row[1]:
            index1 = i
            break
        
    parent1=random_row[0]
    wheel1=random_row[1]

    print(" Fitness array \n " ,fitness)

    ##selecting parent2
    temp=index1+2
    index2=temp%4
    array=sorted_fitness[index2]
    parent2=array[0]
    wheel2=array[1]

    ##selecting parent3
    temp=index1+1
    index3=temp%4
    array=sorted_fitness[index3]
    parent3=array[0]
    wheel3=array[1]
    
    ##selecting parent4
    temp=index3+2
    index4=temp%4
    array=sorted_fitness[index4]
    parent4=array[0]
    wheel4=array[1]

    print("------------------------------------------------------------------------------------------\n")
    return parent1,parent2 ,parent3, parent4

def crossover(parent1 , parent2, parent3, parent4):
    n=len(parent1)
    point=random.randint(1,n-1)
    print("random number generated for cross over is : " , point)
    ## making cross 1 using p1 , p2 at  point
    #cross1_1 = np.empty(n)
    cross1_1 = np.empty_like(parent1)
    for i in range (0,point):
        cross1_1[i]=parent1[i]
    for i in range(point,n):
        cross1_1[i]=parent2[i]
    
        ## making cross 2
    cross1_2 = np.empty_like(parent1)
    for i in range(0,point):
        cross1_2[i]=parent2[i]
    for i in range (point,n):
        cross1_2[i]=parent1[i]
    print("Parent 1 and 2 are :  " , parent1 , parent2)
    print("Cross 1 and 2 using paren1 1 and 2 are :  " , cross1_1, cross1_2)
    ## making cross 2 using p3 ,p4 at  point
    cross2_1 = np.empty_like(parent1)
    for i in range (0,point):
        cross2_1[i]=parent3[i]
    for i in range(point,n):
        cross2_1[i]=parent4[i]
    ## making cross 2
    cross2_2 = np.empty_like(parent1)
    for i in range(0,point):
        cross2_2[i]=parent4[i]
    for i in range (point,n):
        cross2_2[i]=parent3[i]
    
    print("Parent 3 and 4 are :  " , parent3 , parent4)
    print("Cross 1 and 2 using parent 3 and 4 are :  " , cross2_1, cross2_2)

def mutation(array1):
    print("\nFinding the best mutation child of " , array1)
    n=len(array1)
    fitness=0
    fit_Child=[]
    temp=[]
    for i in range (0,50):
        temp = copy.deepcopy(array1)    # deep copy of array1 as lists are mutable having same memory , so to make sure that each child is of array1
        col_x=random.randint(0,n-1)       # for selection of col
        num_x=random.randint(1,n)       # for selection of number after mutation 
        temp[col_x]=num_x
        f_x=fitness_check(temp)
        if(f_x>fitness):
            fitness=f_x
            fit_Child=temp
        
    print("the best fitness child is : " , fit_Child , " with fitness score : " , fitness)

def main():
    print("WELCOME TO 8 QUEEN PROBLEM ")
    n=input("Enter the value of n :  ")
    n=int(n)
    array1 = np.random.randint(1, n+1, size=n)
    array2 = np.random.randint(1, n+1, size=n)
    array3 = np.random.randint(1, n+1, size=n)
    array4 = np.random.randint(1, n+1, size=n)      # 1D  array , np is for numpy library to handle dimensions

    print("1st individual: ", array1)
    print("2nd individual: ", array2)
    print("3rd individual: ", array3)
    print("4th individual: ", array4)

    fitness=[]
    fit1 = fitness_check(array1)
    fit2 = fitness_check(array2)
    fit3 = fitness_check(array3)
    fit4 = fitness_check(array4)
    ## calculate percentages
    fit_total=fit1+fit2+fit3+fit4
    print("fitness score are " , fit1 , fit2 , fit3 , fit4)
    fit1=round((fit1/fit_total)*100)
    fit2=round((fit2/fit_total)*100)
    fit3=round((fit3/fit_total)*100)
    fit4=round((fit4/fit_total)*100)
    print("fitness level % " , fit1 , fit2 , fit3 , fit4)

    fitness.append([array1, fit1])
    fitness.append([array2, fit2])
    fitness.append([array3, fit3])
    fitness.append([array4, fit4])

    p1,p2,p3,p4=roulette_wheel(fitness)
    crossover(p1,p2 , p3 ,p4)
    print("creating 50 random childs to find the one with the best fitness score")
    mutation(array1)
    mutation(array2)
    mutation(array3)
    mutation(array4)
if __name__ == "__main__":
    main()
