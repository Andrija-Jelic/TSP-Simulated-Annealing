###############################################################
###########Solving the TSP with Simulated Annealing testversion############
###############################################################

#####Required packages#####

import random
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from matplotlib import pyplot as plt


#Read in, filter and prepare data
df=pd.read_csv("Traffic_data_berlin.csv")
#For this test version the name and the geographical data is enough
df=df[["name","lat","lon"]]
# Number as names for the requests, this is more convenient
df.name=[i for i in range(len(df.name))]
#Salesman is able to serve not more than 20 requests per day
df=df[:20]
#Combine all to a list with one request [name,lat,lon] as one element, the sequence in this list presents a first guess of a tour
first_tour=list(map(lambda h,i,j:[h,i,j],df.name,df.lat,df.lon))
#Per definition the salesman starts and finishes his tour in the same place
first_tour.append(first_tour[0])

class Simulated_Annealing():

    def __init__(self,tour):
        self.tour=tour

    def neigbour_solution(self,tour):
        '''Create a neighbour solution of the current solution'''
        neighbour=tour[:]
        if(len(neighbour)>3):
            continue_search = True
            while (continue_search):
                index_1 = random.randint(1, len(neighbour) - 2)
                index_2 = random.randint(1, len(neighbour) - 2)
                if (index_1 != index_2):
                    continue_search = False
                    neighbour[index_1],neighbour[index_2]=neighbour[index_2],neighbour[index_1]
        return neighbour

    def distance(self,tour):
        '''Calulate the distances between the requests'''
        distance = sum(list(map(lambda request,request_2: geodesic((request[1],request[2]),(request_2[1],request_2[2])).meters, tour[:-1],tour[1:])))
        return distance

#Tasks: customize the cooling schedule
    def optimize(self):
        '''Optimize according to acceptance probability'''
        current_best=self.tour[:]
        print("The overall distance of the first tour is: "+str(self.distance(current_best))+" meters")
        for temperature in np.logspace(0, 3, num=10000)[::-1]:
            neighbour = self.neigbour_solution(current_best)
            if (self.distance(current_best) > self.distance(neighbour)):
                current_best = neighbour
            else:
                delta= self.distance(neighbour) - self.distance(current_best)
                r = random.random()
                if (r < np.exp(-(delta / temperature))):
                    current_best = neighbour
        print("The best route found so far has the distance: " + str(self.distance(current_best))+ " meters and the requests are served in following order: ")
        tour_requests=[current_best[i][0] for i in range(len(current_best))]
        return tour_requests

#create instance
one_instance=Simulated_Annealing(first_tour)
print(one_instance.optimize())
