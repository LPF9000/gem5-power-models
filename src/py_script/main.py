import re
import matplotlib.pyplot as plt

def extract_power_values(file_path, pattern):
    power_values = []

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                power_values.append(float(match.group(1)))

    return power_values

def plot_graph(power_values, title, filename):
    plt.figure()
    plt.plot(power_values, label=title)
    plt.xlabel('Samples')
    plt.ylabel('Power (Watts)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{filename}.png")
    plt.show()

def main():
    file_path = "stats.txt"  # Path to your stats.txt file
    clusters = ["system.bigCluster", "system.littleCluster"]
    power_types = ["dynamicPower", "staticPower"]
    pm_states = ["", "pm0."]

    for cluster in clusters:
        for power_type in power_types:
            for pm_state in pm_states:
                # Adjusted pattern to be more flexible in matching power values
                pattern = rf"{cluster}\.cpus\.power_model\.{pm_state}{power_type}\s+([\d.]+)"
                power_values = extract_power_values(file_path, pattern)
                title = f"{cluster} {pm_state}{power_type} vs. Samples"
                filename = f"{cluster}_{pm_state}{power_type}_graph"
                plot_graph(power_values, title, filename)

if __name__ == "__main__":
    main()
