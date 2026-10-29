import copy

class FEQ:
    # A future events queue object to hold future events (lists)
    # in a simulation that allows simultaneous events

    def __init__(self, events):
        self.FEQ = events

    # Defines how elements should be added to the FEQ
    def add(self, event):

        if isinstance(event, list) and len(event) == 2:
            init_FEQ = self.FEQ

            for i in range(len(init_FEQ)):
                # If event i will happen at the same time or after our new 
                # event we put the new event before event i in our list. This
                # ensures our FEQ remains in chronological order
                if event[1] <= init_FEQ[i][1]:
                    new_FEQ = init_FEQ[:i] + [event] + init_FEQ[i:]
                    self = FEQ(new_FEQ)
                    return self

                # Catches the case where an added event occurs after all 
                # events in our FEQ
                elif (i + 1) == len(init_FEQ):
                    new_FEQ = init_FEQ[:(i + 1)] + [event]
                    self = FEQ(new_FEQ)
                    return self

        else:
            raise TypeError("The added element must be a list [a, b]")
               
    def add_list(self, queue):

        # Make sure it's the right syntax
        if isinstance(queue, list):

            # Avoids issue where adding an FEQ to itself would break GoToNext
            queue = copy.deepcopy(queue)

            for event in queue:
                self = self.add(event)
        
            return self
        
        else:
            raise TypeError("The added list must be of form"
                            "[[a, b], [c, d],...]")

    # Defines behaviour for moving through the future events queue
    def GoToNext(self):
        # Record the "time taken" before next event
        time_taken = self.FEQ[0][1]

        # Define a new queue
        new_q = self.FEQ[1:]

        # Take away the time taken from every item in the new queue this is so
        # events still happen at the right time
        for event in new_q:
            event[1] = event[1] - time_taken

        self = FEQ(new_q)
        return self, time_taken



if __name__ == '__main__':
    # Ignore for time being I haven't yet written proper tests
    a = FEQ([[-1, 2], [3, 4], [5, 6]])
    a = a.add([-2, 4])
    a = a.add([-7, 3])
    a = a.add([9, 10])
    print(a.FEQ)
    
    a = a.add_list(a.FEQ)

    print(a.FEQ)

    for event in a.FEQ:
        a, time = a.GoToNext()
        print(a.FEQ, time)
