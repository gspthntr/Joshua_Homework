import pandas as pd
import math

PI = math.pi
SPINDLE_SPEED_FACTOR = 4
CUTTING_SPEED_FACTOR = 0.262

# Surface Factor
material_dict = {
    "aluminium": 300,
    "stainless_steel": 150,
    "tungsten": 20,
    "tungsten_carbide": 45
}


def check_input():
    while True:
        chosen_material = input("What is your chosen material?")
        if chosen_material in material_dict:
            print(f"CHOSEN MATERIAL: {chosen_material}\n")
            break
        else:
            print("Enter a valid material.\n")

    while True:
        try:
            num_teeth = int(input("What is the number of teeth on your cutting tool?"))
            is_int = isinstance(num_teeth, int)
            if is_int and num_teeth > 0:
                print(f"NUMBER OF TEETH: {num_teeth} teeth\n")
                break
            if num_teeth <= 0:
                print("Number of teeth cannot be less than or equal to 0. Enter a valid integer\n")
        except ValueError:
            print("Enter a valid integer.\n")

    while True:
        try:
            diameter_cutting_tool = float(input("What is the diameter of your cutting tool"))
            is_int = isinstance(diameter_cutting_tool, float)
            if is_int and diameter_cutting_tool > 0:
                print(f"DIAMETER: {diameter_cutting_tool}mm\n")
                break
            if diameter_cutting_tool <= 0:
                print("Diameter cannot be less than or equal to 0. Enter a valid integer\n")
        except ValueError:
            print("Enter a valid diameter.\n")
    print(f"You material is {chosen_material}, number of teeth is {num_teeth}, diameter is {diameter_cutting_tool}mm")
    return chosen_material, diameter_cutting_tool, num_teeth


def calculate_spindle_speed(diameter, material):
    spindle_speed = material_dict[material] * diameter
    print(f"SPINDLE SPEED:{spindle_speed}RPM")
    return spindle_speed


def calculate_cutting_speed(material):
    cutting_speed = CUTTING_SPEED_FACTOR * material_dict[material]
    print(F"CUTTING SPEED: {cutting_speed}m/min")
    return cutting_speed


def calculate_feed_rate(cutting_speed, teeth, diameter):
    feed_rate = cutting_speed * teeth * diameter
    print(f"FEED RATE: {feed_rate}mm/min")
    return feed_rate


def main():
    material, diameter, teeth = check_input()
    spindle_speed = calculate_spindle_speed(diameter, material)
    cutting_speed = calculate_cutting_speed(material)
    feed_rate = calculate_feed_rate(cutting_speed, teeth, diameter)

    df = pd.DataFrame({
        'Spindle speed(RPM)': [spindle_speed],
        'Cutting speed(m/min)': [cutting_speed],
        'Feed rate(mm/min)': [feed_rate]
    })
    df.index = range(1, len(df) + 1)

    try:
        cnc_data = pd.read_csv("CNC.csv")
        data_index = len(cnc_data) + 1
    except FileNotFoundError:
        print("\nERROR: FileNotFoundError\nCNC data file does not exist. Creating new CNC data file")
        df.to_csv("CNC.csv", mode="w", header=True, index_label="Index")
        data_index = 1
        df.index = [data_index]
    except pd.errors.EmptyDataError:
        print("CNC data file is empty. Initializing with index 1.")
        data_index = 1
        df.index = [data_index]
        df.to_csv("CNC.csv", mode="a", header=False, index_label="Index")
    else:
        df.index = [data_index]
        df.to_csv("CNC.csv", mode="a", header=False, index_label="Index")
    print(df)


still_have_inputs = True
while still_have_inputs:
    main()
    more_inputs = input("\nDo you still have more inputs?[Y/N]").lower()
    while more_inputs != "n" and more_inputs != "y":
        print("Enter Y or N")
        more_inputs = input("\nDo you still have more inputs?[Y/N]\n").lower()
    if more_inputs == "n":
        print("---------------------Program shutting down---------------------")
        still_have_inputs = False
    elif more_inputs == "y":
        continue



