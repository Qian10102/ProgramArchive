x_increment = 0
alien_0 = {"color": "yellow", "position_x": 0, "position_y": 10, "speed_x": "fast"}
print(f"The original position of the alien is {alien_0['position_x']}")
if alien_0["speed_x"] == "low":
    x_increment = 1
elif alien_0["speed_x"] == "medium":
    x_increment = 2
elif alien_0["speed_x"] == "fast":
    x_increment = 3
alien_0["position_x"] = alien_0["position_x"] + x_increment
print(f"The new position of the alien is {alien_0['position_x']}")