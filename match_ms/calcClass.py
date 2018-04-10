class CalcClass(object):

    def __init__(self,name,description,user_id,subcategory_id, *args, **kw):
        # Initialize any variables you need from the input you get
        self.name=name
        self.description=description
        self.user_id=user_id
        self.subcategory_id=subcategory_id

    def subcategory(self):
        # Do some calculations here
        # returns a tuple ((1,2,3, ), (4,5,6,))
        result = self.subcategory_id# final result
        return result
