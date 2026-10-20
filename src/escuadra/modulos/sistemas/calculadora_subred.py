import ipaddress


class ErrorCIDR(Exception):
    pass


def calcular_subred(ip: str, prefijo_cidr: str) -> dict:
    """
    Calcula información de subred a partir de una IP y un prefijo CIDR.

    Retorna:
        dict con:
        - red
        - broadcast
        - mascara
        - primer_host
        - ultimo_host
        - total_hosts
    """

    # ===== VALIDACIÓN =====
    try:
        prefijo = int(prefijo_cidr)
    except ValueError:
        raise ErrorCIDR("El prefijo CIDR debe ser un número entero")

    if prefijo < 0 or prefijo > 32:
        raise ErrorCIDR("El prefijo CIDR debe estar entre 0 y 32")

    try:
        red = ipaddress.ip_network(f"{ip}/{prefijo}", strict=False)
    except ValueError:
        raise ErrorCIDR("IP inválida o formato incorrecto")

    # ===== CÁLCULOS =====
    network_address = red.network_address
    broadcast_address = red.broadcast_address
    netmask = red.netmask

    # Para prefijos 31 y 32 no hay hosts asignables según los criterios del issue
    if red.prefixlen >= 31:
        primer_host = "N/A"
        ultimo_host = "N/A"
        total_hosts = 0
    else:
        # Sumamos/restamos enteros sobre las direcciones de red y broadcast
        primer_host = str(network_address + 1)
        ultimo_host = str(broadcast_address - 1)
        total_hosts = red.num_addresses - 2

    return {
        "red": str(network_address),
        "broadcast": str(broadcast_address),
        "mascara": str(netmask),
        "primer_host": primer_host,
        "ultimo_host": ultimo_host,
        "total_hosts": total_hosts,
    }
    