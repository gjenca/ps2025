
WIDTH=1.5


class PositionedNumber:

    def __init__(self,value,index):

        self.value=value
        top=index+1
        vmid=index+0.5
        hmid=WIDTH/2
        right=WIDTH-0.05
        self.box=f'(0.05,{index})({right},{top})'
        self.center=f'({hmid},{vmid})'

class NumberStack:

    def __init__(self,l,capacity=None):
    
        self.stack=l
        if capacity is None:
            capacity=len(l)
        self.capacity=capacity
        topframe_top=self.capacity+0.5
        self.polylinetop=f'(0,{topframe_top})(0,0)({WIDTH},0)({WIDTH},{topframe_top})'

    def __iter__(self):

        for i,value in enumerate(self.stack):
            yield PositionedNumber(value,i)

        
