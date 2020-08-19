

class Package:

    def __init__(self, ID, address, city, state, zip, delivery_deadline, weight, special_instructions):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.actual_delivery_time = "00:00:00"
        self.weight = weight
        self.special_instructions = special_instructions
        self.delivery_status = "At the hub"

    # Big O Notation -> Constant O(1)
    # set the delivery status of packages hub->in transit -> delivered
    def set_delivery_status(self, delivery_code):
        if delivery_code == 1:
            self.delivery_status = "At the hub"
        elif delivery_code == 2:
            self.delivery_status = "In transit"
        elif delivery_code == 3:
            self.delivery_status = "Delivered"
        else:
            print("invalid delivery code")

