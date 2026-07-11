class Cell:

    def __init__(self, value=0, fixed=False):

        self.value = value
        self.fixed = fixed

        self.notes = set()

        self.selected = False

        self.invalid = False

        self.highlighted = False

        self.same_number = False

        self.anim_scale = 1.0
