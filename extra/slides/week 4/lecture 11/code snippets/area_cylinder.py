def area_cylinder(radius=1, height=1):
    pi = 3.14
    bottom_area = pi * radius ** 2
    side_area = 2 * pi * height * radius
    return side_area + bottom_area * 2


print("No parameters: ", area_cylinder(), '\n')

print("One parameter: ", area_cylinder(2))
print("Check: ", area_cylinder(2, 1), '\n')

print("Two parameters: ", area_cylinder(2, 3), '\n')

print("Specific parameters: ", area_cylinder(height=2))
print("Check: ", area_cylinder(1, 2), '\n')
