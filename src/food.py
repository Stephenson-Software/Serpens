from entity import Entity


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Food(Entity):
    def __init__(self):
        Entity.__init__(self, "Food")