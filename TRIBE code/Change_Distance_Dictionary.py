def change_distance_dictionary(distance_dictionary):
    if distance_dictionary==None:
        return distance_dictionary
    else:
        values=[]
        for x in range(0,len(distance_dictionary)):
            values.append(distance_dictionary["FID"+str(x+1)])
        sorted_values=sorted(values)
        highest_value=int(sorted_values.pop(len(sorted_values)-1))
        for y in range(0,len(distance_dictionary)):
            item=int(distance_dictionary["FID"+str(y+1)])
            new_value = highest_value - item
            distance_dictionary["FID"+str(y+1)]=new_value
        return distance_dictionary


