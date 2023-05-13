def calculate_displacement(self, accelerations, dt):
    displacement = 0
    velocity = 0
    

    for acceleration in accelerations:
        velocity += acceleration * 3 * dt
        displacement += velocity * 3 * dt

    return displacement

def calculate_group_average(self, group_size):
    averaged_accelerations_x = []
    averaged_accelerations_y = []
    for i in range(0, len(accelerations), group_size):
        group_x = accelerations['x'][i:i+group_size]
	group_y = accelerations['y'][i:i+group_size]
        average_x = sum(group_x) / len(group)
	average_y = sum(group_y) / len(group)
        averaged_accelerations_x.append(average)
	averaged_accelerations_y.append(average)
    return [averaged_accelerations_x, averaged_accelerations_y]


def current_pos(self, displacement_x, displacement_y):
    return [self.x + displacement_x, self.y + displacement_y]