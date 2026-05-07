from scapy.all import sniff, get_if_list


def detect_interface():
    interfaces = get_if_list()

    print("\nAvailable interfaces:\n")

    for index, interface in enumerate(interfaces):
        print(f"{index}: {interface}")

    selected = input("\nSelect interface number: ")

    chosen_interface = interfaces[int(selected)]

    print(f"\nUsing interface: {chosen_interface}")

    return chosen_interface


if __name__ == "__main__":
    detect_interface()